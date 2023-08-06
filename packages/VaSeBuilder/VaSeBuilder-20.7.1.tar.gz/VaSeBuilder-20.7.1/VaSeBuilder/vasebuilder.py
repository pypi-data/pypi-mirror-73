#!/usr/bin/env python
"""Main VaSeBuilder module."""
import sys
import io
import time
import random
import logging
import gzip
import os
from datetime import datetime
from collections import OrderedDict

import numpy as np
import pysam

# Import VaSe specific classes.
from VaSeBuilder.sample_mapper import SampleMapper
from VaSeBuilder.variant_context_file import VariantContextFile
from VaSeBuilder.variant_context import VariantContext
from VaSeBuilder.overlap_context import OverlapContext


class VaSeBuilder:
    """Method object with all main functionality.

    The init also saves the identifier, date, and time of the current run.

    Attributes
    ----------
    creation_id : str
        Unique (uuid) identifier to identify VaSeBuilder runs
    creation_time : str
        The date and time of creation to identify VaSeBuilder runs
    vaselogger : Logger
        VaSeBuilder logger to log VaSeBuilder activity
    """

    def __init__(self, vaseid):
        self.vaselogger = logging.getLogger("VaSe_Logger")
        self.creation_id = str(vaseid)
        self.creation_time = datetime.now()
        self.vaselogger.info(f"VaSeBuilder: {self.creation_id} ; {self.creation_time}")

        # VariantContextFile that saves the acceptor, donor, and variant contexts
        # with their associated data.
        self.contexts = VariantContextFile()

        # Dictionary used for debug messages.
        self.debug_dict = {"vw": "Establishing search window",
                           "dr": "Gathering donor variant reads",
                           "dc": "Determining donor context",
                           "ar": "Gathering acceptor variant reads",
                           "ac": "Determining acceptor context",
                           "cc": "Determining combined context",
                           "cdr": "Gathering combined context donor reads",
                           "car": "Gathering combined context acceptor reads",
                           "done": "Variant complete. Processing"}

    # Method to print debug messages.
    def debug_msg(self, step, variant_id, starting_time=None):
        """Print preformed debug message for a given step.

        If a starting_time parameter is set, the massage output will include
        the elapsed time from starting_time to the the time the
        message is printed.

        Parameters
        ----------
        step : str
            DESCRIPTION.
        variant_id : str
            DESCRIPTION.
        starting_time : float, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        process = self.debug_dict[step]
        for_var = f"for variant {variant_id}"
        if starting_time:
            took = f" took {time.time() - starting_time} seconds."
        else:
            took = "."
        self.vaselogger.debug(f"{process} {for_var}{took}")

    # ===METHODS TO PRODUCE VARIANT CONTEXTS===================================
    def get_sample_vcf_variants_2(self, variant_fileloc, filterlist=None):
        """Read and return read variants from a variant file.

        Parameters
        ----------
        variant_fileloc : str
            Path to variant file to read
        filterlist : list of tuple
            Variants to include

        Returns
        -------
        sample_variant_list : list of pysam.VariantRecord
            Read variants fro the variant file
        """
        sample_variant_list = []
        try:
            variant_file = pysam.VariantFile(variant_fileloc, "r")
            vcfvars = list(variant_file.fetch())
        except IOError:
            self.vaselogger.warning(f"Could not open variant file {variant_fileloc}")
            return sample_variant_list
        if filterlist is None:
            sample_variant_list = [(var, None) for var in vcfvars]
            return sample_variant_list
        for var in vcfvars:
            variant_to_add = self.filter_vcf_variant(var, filterlist)
            if variant_to_add is not None:
                sample_variant_list.append(variant_to_add)
        return sample_variant_list

    def refetch_donor_variants(self, samples, varconfile):
        """Refetch VCF variants from sample VCFs using variant context as a filter.

        Used in BuildSpikeIns tool while running with a pre-made variant
        context file. Variant context files only store alignment read IDs and
        basic variant info, so the original full records must be retrieved
        from their original files before constructing spike-ins. Only variants
        matching those in the variant context file will be retrieved from each
        sample. Variants retrieved will overwrite the placeholder filter
        variants located in the variant contexts read from file.

        Parameters
        ----------
        samples : list of sample_mapper.Sample objects.
        varconfile : VariantContextFile
        """
        all_varcons = varconfile.get_variant_contexts_by_sampleid()
        for sample in samples:
            sample_varcons = all_varcons[sample.hash_id]
            for sample_varcon in sample_varcons:
                varcon_variants = self.get_sample_vcf_variants_2(sample.vcf, sample_varcon.variants)
                sample_varcon.variants = [var[0] for var in varcon_variants]

    def rebuild(self, samples, varconfile, reference):
        """Refetch reads and variants for variant contexts."""
        all_varcons = varconfile.get_variant_contexts_by_sampleid()
        viables = [sample for sample in samples
                   if sample.hash_id in all_varcons]
        self.refetch_donor_reads(viables, varconfile, reference)
        self.refetch_donor_variants(viables, varconfile)

    @staticmethod
    def filter_vcf_variant(vcfvariant, filtervariantlist):
        """Check if a sample variant is in the filter list and set prioritization.

        Compares variant sample, chromosome, position, and alleles. Alleles
        are only checked for at least one matching allele in both ref and alt,
        not exact matches for all alleles. Prioritization settings are added if
        present in the filter. If multiple matching variants are found, the
        highest prioritization settings are used if present.

        Parameters
        ----------
        vcfvariant : pysam.VariantRecord
            Sample variant to check
        filtervariantlist : list of InclusionVariant objects
            List of variants to include and their prioritizations

        Returns
        -------
        (vcfvariant, [Filter...])
            vcfvariant and its prioritization Filter objects, or None if none found
        """
        # Check if chrom and pos match with an inclusion variant.
        matches = [filtervar for filtervar in filtervariantlist
                   if filtervar.chrom == vcfvariant.chrom
                   and filtervar.pos == vcfvariant.pos]
        # Check if alleles match with matched position variants.
        matches = [filtervar for filtervar in matches
                   if set(vcfvariant.ref.split(",")) & set(filtervar.ref.split(","))
                   and set(vcfvariant.alts) & set(filtervar.alts)]
        # Return None if no matches found.
        if not matches:
            return None
        # Get existing prioritization filters for all matches.
        match_priorities = [x.priorities for x in matches
                            if x.priorities is not None]
        # Set highest prioritization filter, or None if None.
        if not match_priorities:
            return (vcfvariant, None)
        return (vcfvariant, max(match_priorities))

    @staticmethod
    def determine_variant_type(vcfvariantstart, vcfvariantstop):
        """Determine and return the variant type.

        Determination of the variant type is based on the distance between
        the right and left most genomic position of the variant reference
        and alternative allele(s).

        Parameters
        ----------
        vcfvariantstart : int
            Leftmost genomic position of the variant
        vcfvariantstop : int
            Rightmost genomic position of the variant

        Returns
        -------
        str
            Type of variant (snp/indel)
        """
        if (vcfvariantstop - vcfvariantstart) <= 1:
            return "snp"
        return "indel"

    def determine_read_search_window(self, varianttype, vcfvariant):
        """Determine and return the search window for fetching reads.

        The determined search window depends on the provided variant type.
        SNPs return a search window of SNP position -1 and +1. Indels return
        a search window based indel leftmost position and length. If the
        variant type is neither SNP or indel, the search window returned
        will be [-1, -1].

        Parameters
        ----------
        varianttype : str
            Variant type to determine search window for
        vcfvariant : VcfVariant
            Variant to determine search window with

        Returns
        -------
        list of int
            Search window start and stop, -1 and -1 if variant type is invalid
        """
        if varianttype == "snp":
            return [vcfvariant.get_variant_pos() - 1, vcfvariant.get_variant_pos() + 1]
        if varianttype == "indel":
            return self.determine_indel_read_range(vcfvariant.get_variant_pos(),
                                                   vcfvariant.get_variant_ref_allele(),
                                                   vcfvariant.get_variant_alt_alleles())
        return [-1, -1]

    # Returns the search start and stop to use for searching BAM reads
    # overlapping with the range of the indel.
    @staticmethod
    def determine_indel_read_range(variantpos, variantref, variantalts):
        """Determine and return the search start and stop to use for an indel.

        Parameters
        ----------
        variantpos : int
            Leftmost genomic position of the variant
        variantref : str
            Variant reference allele(s)
        variantalts : tuple
            Variant alternative allele(s)

        Returns
        -------
        list of int
            Search window start and stop
        """
        searchstart = variantpos
        searchstop = variantpos + max(
            max([len(x) for x in variantref.split(",")]),
            max([len(x) for x in variantalts])
        )
        return [searchstart, searchstop]

    def get_variant_reads(self, variantchrom, variantstart, variantend, bamfile):
        """Fetch and return reads overlapping with a specified variant.

        First reads overlapping directly with the variant position are
        fetched. Then the read mates are fetched using the RNEXT and PNEXT
        values of each read. Lastly, it is ensured that each read only
        occurs once.

        Parameters
        ----------
        contextid : str
            Identifier of the context to fetch reads for
        variantchrom : str
            Chromosome name to fetch reads from
        variantstart : int
            Leftmost genomic position to use for fetching
        variantend : int
            Rightmost genomic position to use for fetching
        bamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile
        umatelist : list of str
            Identifiers of reads with an unmapped mate

        Returns
        -------
        variantreads : list of pysam.AlignedSegment
            Fetched reads and their read mates
        """
        hardclipped_read_num = 0
        duplicate_read_num = 0
        secondary_read_num = 0

        read_objects = []
        variantreads = []
        clipped_reads = []
        list_r1 = []
        list_r2 = []

        for vread in bamfile.fetch(variantchrom, variantstart-1, variantend+1):
            if vread.is_duplicate:
                duplicate_read_num += 1
            if vread.is_secondary:
                secondary_read_num += 1
            if self.read_is_hard_clipped(vread):
                hardclipped_read_num += 1
                clipped_reads.append(vread)
                continue
            read_objects.append(vread)

        self.vaselogger.debug(f"Fetched {hardclipped_read_num} reads with hardclipped bases")
        for clipped in clipped_reads:
            read_objects.append(self.fetch_primary_from_secondary(clipped, bamfile))

        for vread in read_objects:
            if vread.is_read1:
                list_r1.append(vread)
            elif vread.is_read2:
                list_r2.append(vread)

        list_r1_ids = [x.query_name for x in list_r1]
        list_r2_ids = [x.query_name for x in list_r2]

        for r1 in list_r1:
            if r1.query_name not in list_r2_ids:
                list_r2.append(self.fetch_mate_read(r1.query_name, r1.next_reference_name,
                                                    r1.next_reference_start,
                                                    self.get_read_pair_num(r1), bamfile))
        for r2 in list_r2:
            if r2.query_name not in list_r1_ids:
                list_r1.append(self.fetch_mate_read(r2.query_name, r2.next_reference_name,
                                                    r2.next_reference_start,
                                                    self.get_read_pair_num(r2), bamfile))

        variantreads = list_r1 + list_r2
        variantreads = self.uniqify_variant_reads(variantreads)
        return variantreads

    @staticmethod
    def fetch_primary_from_secondary(secondary_read, bamfile):
        """Fetch the primary alignment of a read based on the position recorded in its SA tag.

        The SA tag is read from a provided Pysam read object. Then, reads
        at the recorded alignment position are fetched. The first
        non-secondary alignment with a matching read ID and pair number is
        returned.

        Parameters
        ----------
        secondary_read : pysam.AlignedSegment
            Secondary alignment whose primary alignment will be located
        bamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile

        Returns
        -------
        primary_read : pysam.AlignedSegment
            Primary alignment with the same read ID and pair number
            as the input secondary alignment.
        """
        primary_locus = secondary_read.get_tag("SA").split(",")[0:2]
        for fetched in bamfile.fetch(primary_locus[0],
                                     int(primary_locus[1]) - 1,
                                     int(primary_locus[1])):
            if ((fetched.query_name == secondary_read.query_name)
                    and (fetched.is_read1 == secondary_read.is_read1)
                    and not fetched.is_secondary):
                primary_read = fetched
                break
        return primary_read

    @staticmethod
    def uniqify_variant_reads(variantreads):
        """Ensure each read only occurs once and return the updated set.

        Parameters
        ----------
        variantreads : list of pysam.AlignedSegment
            Sets of reads to process

        Returns
        -------
        unique_variantreads : list of pysam.AlignedSegment
            Set of reads with each read occurring only once
        """
        unique_variantreads = []
        checklist = []
        for fetched in variantreads:
            readpn = "2"
            if fetched.is_read1:
                readpn = "1"
            id_pair = (fetched.query_name, readpn)
            if id_pair not in checklist:
                unique_variantreads.append(fetched)
                checklist.append(id_pair)
        return unique_variantreads

    def fetch_mate_read(self, readid, rnext, pnext, pair_num, bamfile):
        """Fetch and return the mate read of a specified read.

        The mate read is fetched from an opened alignment file using the
        RNEXT and PNEXT value of the read. Of the fetched reads, only the
        read with the same identifier is returned.

        Parameters
        ----------
        rnext : str
            Chromosome name the mate read is located on
        pnext : int
            Leftmost genomic position of the mate read
        readid : str
            Identifier of the read to search the mate for
        bamfile : pysam.AlignmentFile
            Already opened pysam alignment file

        Returns
        -------
        pysam.AlignedSegment or None
            The mate read if found, None if not
        """
        for bamread in bamfile.fetch(rnext, pnext, pnext + 1):
            if (bamread.query_name == readid
                    and bamread.reference_start == pnext
                    and self.get_read_pair_num(bamread) != pair_num):
                return bamread
        return None

    def determine_context(self, contextreads, contextorigin, contextchr):
        """Determine and return an acceptor/donor context.

        The acceptor/donor context is determined from a set of reads
        overlapping with the variant including their read mates. The leftmost
        and rightmost genomic positions of all reads are collected and
        filtered for outliers. The context start (leftmost genomic) position
        is then determined by taking minimum and maximum leftmost and
        rightmost position respectively.

        Parameters
        ----------
        contextreads : list of pysam.AlignedSegment
            Reads that form the context
        contextorigin : int
            Variant genomic position the context will be based on
        contextchr : str
            Chromosome name the context is located on

        Returns
        -------
        list of str and int
            Essential context data (chromosome, variant pos, start, end)
        """
        # Check whether there are reads to determine the context for.
        if not contextreads:
            return []

        # Get read start and stop position, while filtering out read mates
        # that map to different chr.
        starts = [conread.reference_start
                  for conread in contextreads
                  if conread.reference_name == contextchr]

        stops = [conread.reference_end
                 for conread in contextreads
                 if conread.reference_name == contextchr and conread.reference_end is not None]

        # Number of mates filtered for mapping to different chr.
        num_diff_chr = len(contextreads) - len(starts)

        # Filter outlier read start/stops.
        filtered_starts = self.filter_outliers(starts)
        filtered_stops = self.filter_outliers(stops)

        # Number of filtered outlier positions.
        num_filtered = (len(starts)
                        + len(stops)
                        - len(filtered_starts)
                        - len(filtered_stops))

        self.vaselogger.debug(f"{num_diff_chr} read mate(s) filtered due to "
                              "alignment to different reference sequence.")
        self.vaselogger.debug(f"{num_filtered} outlier read position(s) filtered.")

        # Set variant context as chr, min start, max end.
        contextstart = min(filtered_starts)
        contextend = max(filtered_stops)
        return [contextchr, contextorigin, contextstart, contextend]

    @staticmethod
    def filter_outliers(pos_list, k=3):
        """Filter outliers from a list of start or stop positions and return the filtered list.

        Outlier start/stop positions are filtered from the list using Tukey's
        Fences method. For more info please see:
            https://en.wikipedia.org/wiki/Outlier#Tukey's_fences

        Parameters
        ----------
        pos_list : list of int
            Start/stop positions
        k : int
            Factor to determine outlier
        Returns
        -------
        filtered : list of str
            List of read positions without outliers
        """
        # First and third quartile values of the positions.
        quartile_1 = np.percentile(pos_list, 25)
        quartile_3 = np.percentile(pos_list, 75)
        # Interquartile range.
        iq_range = quartile_3 - quartile_1
        # Only include positions that fall within the range of
        # (quartile_1 to quartile_3) +/- k*iq_range.
        filtered = [x for x in pos_list
                    if (quartile_1 - (k * iq_range)) <= x <= (quartile_3 + (k * iq_range))]
        return filtered

    @staticmethod
    def determine_largest_context(contextorigin, acceptor_context,
                                  donor_context):
        """Determine the size of the variant context based on both the acceptor and donor reads.

        Parameters
        ----------
        contextorigin : int
            Variant position that the context is based on
        acceptor_context : list of str and int
            Essential acceptor context data
        donor_context : list of str and int
            Essential donor context data

        Returns
        -------
        list of str and int
            Context (chromosome, variant pos, start, end)
        """
        largest_context = [donor_context[0]]
        largest_context.append(contextorigin)
        # Determine and save the smallest context start.
        largest_context.append(min(acceptor_context[2], donor_context[2]))
        # Determine and save the largest context end.
        largest_context.append(max(acceptor_context[3], donor_context[3]))
        return largest_context

    # ===METHODS TO PRODUCE THE VALIDATION FASTQ FILES=========================
    @staticmethod
    def build_donor_fq(donorbamreaddata, fr, fastq_outpath):
        """Build and write a fastq file containing only donor reads.

        Parameters
        ----------
        donorbamreaddata : list of tuple
            Donor reads to write to fastq file
        fr : str
            Write forward ('1') or reverse ('2') fastq file
        fastq_outpath : str
            Path and name to write donor fastq file to
        """
        # Write the new VaSe FastQ file.
        # vasefq_outname = self.set_fastq_out_path(fastq_outpath, fr, 1)
        fqgz_outfile = io.BufferedWriter(open(fastq_outpath, "wb"))

        donorbamreaddata.sort(key=lambda dbr: dbr[0], reverse=False)
        for bamread in donorbamreaddata:
            # Check if the BAM read is R1 or R2.
            if bamread[1] == fr:
                fqlines = ("@" + str(bamread[0]) + "\n"
                           + str(bamread[2]) + "\n"
                           + "+\n"
                           + str(bamread[3]) + "\n")
                fqgz_outfile.write(fqlines.encode("utf-8"))
        fqgz_outfile.flush()
        fqgz_outfile.close()

    @staticmethod
    def is_required_read(bamread, fr):
        """Check and return whether the current read is the one that is required.

        When writing the validation fastq files only R1, or forward (F),
        reads should go to the R1 validation fastq file. Similarly, the R2
        reads should only go into the R2 validation fastq file.

        Parameters
        ----------
        bamread : DonorBamRead
            Read to check
        fr : str
            Whether the read is required for R1 or R2

        Returns
        -------
        bool
            True if the read is required, False if not
        """
        if fr == "F":
            return bamread.is_read1
        return bamread.is_read2

    @staticmethod
    def set_fastq_out_path(outpath, fr, lnum):
        """Set and return the fastq output path and filename.

        Parameters
        ----------
        outpath : str
            Path and suffix to write fastq file to
        fr: str
            Will the fastq file be R1 ('1') or R2 ('2')
        lnum: int
            Lane number (i.e.: 1, 2, 3 or 4)

        Returns
        -------
        str
            Full path to write fastq file to
        """
        if fr == "1":
            return f"{outpath}_{datetime.now().date()}_L{lnum}_R1.fastq"
        return f"{outpath}_{datetime.now().date()}_L{lnum}_R2.fastq"

    # ===METHODS TO OBTAIN SOME DATA OF THE VASEBUILDER OBJECT=================
    def get_creation_id(self):
        """Return the identifier of the current VaSeBuilder object.

        Returns
        -------
        self.creation_id : str
            VaSeBuilder creation identifier
        """
        return self.creation_id

    def get_creation_time(self):
        """Return the date and time the current VaSeBuilder object has been made.

        Returns
        -------
        str
            VaSeBuilder creation date and time
        """
        return self.creation_time

    @staticmethod
    def get_vcf_variant_id(vcfvariant):
        """Return an identifier for a variant as CHROM_POS.

        Parameters
        ----------
        vcfvariant : pysam.VariantRecord
            Variant for which to construct an identifier
        Returns
        -------
        str
            Variant identifier as CHROM_POS
        """
        return f"{vcfvariant.chrom}_{vcfvariant.pos}"

    @staticmethod
    def get_read_pair_num(pysam_bamread):
        """Return the read pair number of a provided read.

        Parameters
        ----------
        pysam_bamread : pysam.AlignedSegment
            Read to determine the read pair number of

        Returns
        -------
        str
            Read pair number ('1' or '2')
        """
        if pysam_bamread.is_read1:
            return "1"
        return "2"

    # ===METHODS TO WRITE OUTPUT FILES=========================================
    def write_used_donor_files(self, outfileloc, samples,
                               used_donor_files, vbuuid, file_type):
        """Write a list of donor alignment or variant files used in constructing variant contexts.

        Parameters
        ----------
        outfileloc : str
            Path to write the output file to
        filesamplemap : dict
            Donor files per sample
        used_donor_files : list
            Donor alignment or variant files used to construct variant contexts
        vbuuid : str
            Unique identifier of the current VaSeBuilder
        """
        try:
            with open(outfileloc, "w") as outfile:
                outfile.write(f"#VBUUID: {vbuuid}\n")
                outfile.write("#SampleId\tDonorFile\n")
                for sample in samples:
                    if file_type == "a":
                        if sample.bam in used_donor_files:
                            # XXX: Need to figure out what to do about sample name in the filenames.
                            outfile.write(f"{sample.hash_id}\t{sample.bam}\n")
                    elif file_type == "v":
                        if sample.vcf in used_donor_files:
                            outfile.write(f"{sample.hash_id}\t{sample.vcf}\n")
        except IOError:
            self.vaselogger.critical("Could not write used donor files to "
                                     f"{outfileloc}")

    def write_optional_output_files(self, outpath, contextfile):
        """Write optional output files to a specified output location.

        The optional output files contain data about acceptor and donor
        contexts as well as output files containing the reads with unmapped
        mates per variant context. The optional output files are only
        produced when VaSeBuilder is run with with debug set to True.

        Parameters
        ----------
        outpath: str
            Path to write the optional output file to
        contextfile: VariantContextFile
            Variant context data
        """
        # Write the optional acceptor context files; acceptor contexts,
        # read ids with unmapped mate and left/right positions.
        self.vaselogger.debug("Writing acceptor contexts to "
                              f"{outpath}acceptorcontexts.txt")
        contextfile.write_acceptor_context_file(f"{outpath}acceptorcontexts.txt",
                                                self.creation_id)

        self.vaselogger.debug("Writing acceptor context statistics to "
                              f"{outpath}acceptorcontextstats.txt")
        contextfile.write_acceptor_context_stats(f"{outpath}acceptorcontextstats.txt",
                                                 self.creation_id)

        self.vaselogger.debug("Writing acceptor context read identifiers with "
                              "unmapped mates to"
                              f"mates to {outpath}acceptor_unmapped.txt")
        contextfile.write_acceptor_unmapped_mates(f"{outpath}acceptor_unmapped.txt",
                                                  self.creation_id)

        self.vaselogger.debug("Writing left and right most read positions of "
                              "each acceptor context to "
                              f"{outpath}acceptor_positions.txt")
        contextfile.write_acceptor_left_right_positions(f"{outpath}acceptor_positions.txt",
                                                        self.creation_id)

        # Write the optional donor context files; donor contexts,
        # read ids with unmapped mate and left/right positions.
        self.vaselogger.debug("Writing donor contexts to "
                              f"{outpath}donorcontexts.txt")
        contextfile.write_donor_context_file(f"{outpath}donorcontexts.txt",
                                             self.creation_id)

        self.vaselogger.debug("Writing donor context statistics to "
                              f"{outpath}donorcontextstats.txt")
        contextfile.write_donor_context_stats(f"{outpath}donorcontextstats.txt",
                                              self.creation_id)

        self.vaselogger.debug("Writing donor context read identifiers "
                              f"with unmapped mates to {outpath}donor_unmapped.txt")
        contextfile.write_donor_unmapped_mates(f"{outpath}donor_unmapped.txt",
                                               self.creation_id)

        self.vaselogger.debug("Writing left and right most read positions "
                              f"of each donor context to {outpath}donor_positions.txt")
        contextfile.write_donor_left_right_positions(f"{outpath}donor_positions.txt",
                                                     self.creation_id)

        # Write the optional variant context files; acceptor & donor
        # unmapped mates and left/right positions.
        self.vaselogger.debug("Writing variant context acceptor read identifiers with unmapped "
                              f"mates to {outpath}varcon_unmapped_acceptor.txt")
        contextfile.write_reads_with_unmapped_mate("acceptor",
                                                   f"{outpath}varcon_unmapped_acceptor.txt",
                                                   self.creation_id)

        self.vaselogger.debug("Writing variant context donor read identifiers "
                              f"with unmapped mates to {outpath}varcon_unmapped_donor.txt")
        contextfile.write_reads_with_unmapped_mate("donor", f"{outpath}varcon_unmapped_donor.txt",
                                                   self.creation_id)

        self.vaselogger.debug("Writing variant context left- and right-most read positions of "
                              f"acceptor reads to {outpath}varcon_positions_acceptor.txt")
        contextfile.write_left_right_positions(
            "acceptor",
            f"{outpath}varcon_positions_acceptor.txt",
            self.creation_id
        )

        self.vaselogger.debug("Writing variant context left and right most "
                              "read positions of donor reads to "
                              f"{outpath}varcon_positions_donor.txt")
        contextfile.write_left_right_positions(
            "donor",
            f"{outpath}varcon_positions_donor.txt",
            self.creation_id
        )

    def write_bed_file(self, variantcontextdata, bedoutloc, vbuuid):
        """Write variant contexts as a BED file.

        Parameters
        ----------
        variantcontextdata : list of VariantContext
            Variants contexts to write to BED file
        bedoutloc : str
            Path to write the BED file to
        """
        try:
            with open(bedoutloc, "w") as bedoutfile:
                bedoutfile.write(f"#VBUUID: {vbuuid}\n")
                for varcon in variantcontextdata:
                    bedoutfile.write(f"{varcon.get_variant_context_chrom()}\t"
                                     f"{varcon.get_variant_context_start()}\t"
                                     f"{varcon.get_variant_context_end()}\t"
                                     f"{varcon.get_variant_context_id()}\n")
        except IOError:
            self.vaselogger.warning("Could not write variant context data to BED file: "
                                    f"{bedoutloc}")

    def check_sequence_names(self, referencefile, alignmentfile):
        """Check if the chromosome names in the genome reference and alignment file are the same.

        Parameters
        ----------
        referencefile : str
            Path to genome reference fasta file
        alignmentfile : pysam.AlignmentFile

        Returns
        -------
        None
        """
        reference_seqnames = self.get_reference_sequence_names(referencefile)
        alignment_seqnames = SampleMapper.get_alignment_sequence_names(alignmentfile)
        shared_seqnames = reference_seqnames & alignment_seqnames
        if (len(shared_seqnames) < len(reference_seqnames)
                or len(shared_seqnames) < len(alignment_seqnames)):
            self.vaselogger.warning("Reference file and alignment file do not "
                                    "contain the same sequence names")

    def get_reference_sequence_names(self, reference_fileloc):
        """Return the sequence names from the reference genome fasta file.

        Parameters
        ----------
        reference_fileloc: str
            Path to genomic reference fasta file

        Returns
        -------
        reference_seqnames : list of str
            Extracted chromosome names
        """
        reference_seqnames = set()
        try:
            with open(reference_fileloc, "r") as reference_file:
                for fileline in reference_file:
                    if fileline.startswith(">"):
                        filelinedata = fileline.strip().split(" ")
                        reference_seqnames.add(filelinedata[0][1:])
        except IOError:
            self.vaselogger.critical(f"Could not read genome reference file {reference_fileloc}")
            sys.exit()
        return reference_seqnames

    @staticmethod
    def divide_donorfastqs_over_acceptors(list_of_donorfqs, num_of_acceptors):
        """Divide a list of donor fastq files over a number of acceptor fastq files.

        Donor fastq files are divided equally into a specified number of
        groups. The number of groups is specified by the number of acceptor
        fastq files to use as template.

        Parameters
        ----------
        list_of_donorfqs: list of str
            Paths to donor fastq files
        num_of_acceptors: int
            Number of template fastq files
        """
        cycler = 0
        split_donors = [[] for x in range(num_of_acceptors)]
        copy_list_donorfqs = list(list_of_donorfqs)
        while copy_list_donorfqs:
            cycle = cycler % num_of_acceptors
            split_donors[cycle].append(copy_list_donorfqs.pop())
            cycler += 1
        return split_donors

    # BUILDS A SET OF R1/R2 VALIDATION FASTQS WITH ALREADY EXISTING DONOR FASTQS
    @classmethod
    def make_bam_headers(cls, samples, variant_context_file):
        """Construct simple BAM headers for all samples.

        Retrieves original BAM header information from the first read from the
        first variant context (arbitrary selection) constructed for each
        sample. If no variant context was created for a sample, it is skipped.
        Headers are reduced to only necessary information, and sample IDs are
        replaced with the hashed ID for each sample (if a hash was created).
        Returns a dictionary of sample_ID: header pairs.

        Parameters
        ----------
        samples : list of sample_mapper.Sample objects
        variant_context_file : VariantContextFile

        Returns
        -------
        used_headers : list of OrderedDict objects
        """
        # Get all varcons per sample and all used donor BAM filenames.
        varcons_per_sample = variant_context_file.get_variant_contexts_by_sampleid()
        # used_bams = variant_context_file.get_donor_alignment_files()
        # Empty dict to store results.
        used_headers = {}
        for sample in samples:
            # Skip unused samples.
            if sample.hash_id not in varcons_per_sample:
                continue
            # if sample.bam not in used_bams:
                # continue
            # Retrieve header from arbitrary read from this sample.
            head = varcons_per_sample[sample.hash_id][0].variant_context_dreads[0].header.as_dict()
            # Replace header sample and library fields with hash (if hashed).
            if "RG" in head:
                for i in range(len(head["RG"])):
                    head["RG"][i]["SM"] = sample.hash_id
                    head["RG"][i]["LB"] = sample.hash_id
            # Keep only basic header information.
            head = cls.select_bam_header_fields(head, ["HD", "SQ", "RG"])
            used_headers[sample.hash_id] = head
        return used_headers

    def run_a_mode_v3(self, samples, variant_context_file, out_path, prefix="VaSe"):
        """Write all spike-ins to a single BAM and single VCF.

        All donor reads from all created variant contexts are written to a
        single BAM file, which has a merged header constructed from all used
        sample BAMs with only minimal necessary header lines retained. If
        hashing was enabled when creating sample objects (default), sample IDs
        in the BAM headers will be replaced with their hashes. All donor
        variants from all created variant contexts are written to one
        single-sample VCF file with an arbitrary sample name.

        Parameters
        ----------
        samples : list of sample_mapper.Sample objects
        variant_context_file : VariantContextFile
        out_path : str
            Path to output directory.
        prefix : str
            Prefix for output BAM and VCF filenames
        """
        self.vaselogger.debug("Running VaSeBuilder A-mode")

        # Get all used headers and replace IDs if necessary, then merge them.
        headers = self.make_bam_headers(samples, variant_context_file)
        merged_header = list(headers.values())[0]
        for header in list(headers.values())[1:]:
            merged_header = self.merge_donor_alignment_headers(merged_header, header)

        # Get all donor reads from all variant contexts and write to BAM.
        donor_reads_to_add = variant_context_file.get_all_variant_context_donor_reads_2()
        outpathbam = f"{out_path}{prefix}.bam"
        self.vaselogger.debug(f"Start writing A-mode donor BAM output file to {outpathbam}")
        self.write_spike_in_bam(merged_header, donor_reads_to_add, outpathbam)
        # Get all variants from all variant contexts and write to VCF.
        donor_variants_to_add = variant_context_file.get_all_variant_context_variant_records()
        outpathvcf = f"{out_path}{prefix}.vcf"
        self.vaselogger.debug(f"Start writing A-mode donor VCF output file to {outpathvcf}")
        self.write_vcf_slice("VaSeBuilder", donor_variants_to_add, outpathvcf)

    @staticmethod
    def merge_donor_alignment_headers(base_header, header_to_add):
        """Merge a new header into a provided header.

        Parameters
        ----------
        base_header : OrderedDict
            Header to add another header to
        header_to_add : OrderedDict
            AlignmentFile header to merge into larger header

        Returns
        -------
        base_header : OrderedDict
        """
        merged_header = OrderedDict(base_header)
        present_read_groups = {x["ID"] for x in base_header["RG"]
                               if x is not None}
        if "RG" in header_to_add:
            for rg_entry in header_to_add["RG"]:
                if rg_entry["ID"] not in present_read_groups:
                    merged_header["RG"].append(rg_entry)
        return merged_header

    def run_f_mode(self, variantcontextfile, fq1_in, fq2_in, fq_out, random_seed):
        """Run VaSeBuilder F-mode.

        This run mode creates a full set of validation fastq files from
        established variant contexts and a set of acceptor fastq files to
        use as template to create the validation fastq files.

        Parameters
        ----------
        variantcontextfile : VariantContextFile
            Variant contexts to use
        fq1_in : list of str
            R1 fastq files to use as template
        fq2_in : list of str
            R2 fastq files to use as template
        fq_out : str
            Path and suffix to write validation fastq files to
        """
        self.vaselogger.info("Running VaSeBuilder F-mode")

        # Combine all donor reads from all variant contexts
        add_list = variantcontextfile.get_all_variant_context_donor_reads()
        self.vaselogger.info("Writing FastQ files.")
        skip_list = set(variantcontextfile.get_all_variant_context_acceptor_read_ids())

        donor_read_add_data = {}
        for i, fq_i in zip(["1", "2"], [fq1_in, fq2_in]):
            # Write the fastq files.
            self.vaselogger.info(f"Start writing the R{i} FastQ files.")
            fq_starttime = time.time()
            self.build_fastq_v2(fq_i, skip_list, add_list, i, fq_out,
                                random_seed, donor_read_add_data)
            self.vaselogger.info(f"Wrote all R{i} FastQ files.")
            self.vaselogger.debug(f"Writing R{i} FastQ file(s) took "
                                  f"{time.time() - fq_starttime} seconds.")
        self.vaselogger.info("Finished writing FastQ files.")
        self.write_donor_insert_positions_v2(donor_read_add_data,
                                             f"{fq_out}_donor_read_insert_positions.txt")

    def run_p_mode_v3(self, samples, variantcontextfile, outpath, prefix="VaSe"):
        """Run VaSeBuilder in P-mode.

        Parameters
        ----------
        samples : list of Sample objects
            Sample objects containing relevant file paths and attributes.
        variantcontextfile : VariantContextFile object
            Object containing the constructed variant contexts to use.
        outpath : str
            Path to output dir.
        prefix : str, optional
            Prefix for created BAM and VCF file names. The default is "VaSe".

        Returns
        -------
        None.

        """
        context_bam_link = {}
        self.vaselogger.info("Running VaSeBuilder P-mode")
        self.vaselogger.info("Begin writing BAM files")

        headers = self.make_bam_headers(samples, variantcontextfile)

        for varcon in variantcontextfile.get_variant_contexts():
            outpathbam = f"{outpath}{prefix}_{varcon.get_variant_context_id()}.bam"
            outpathvcf = f"{outpath}{prefix}_{varcon.get_variant_context_id()}.vcf"
            self.write_spike_in_bam(headers[varcon.sample_id], varcon.get_donor_reads(), outpathbam)
            self.write_vcf_slice(varcon.sample_id, varcon.variants, outpathvcf)
            context_bam_link[varcon.get_variant_context_id()] = outpathbam
        self.write_pmode_bamlinkfile(context_bam_link,
                                     f"{outpath}pmode_bamlink_{self.creation_id}.txt")

    @staticmethod
    def get_sample_filter(sample, filterdict):
        """Retrieve sample's filter variants."""
        if sample.id not in filterdict:
            return None
        return filterdict[sample.id]

    # =====SPLITTING THE BUILD_VARCON_SET() INTO MULTIPLE SMALLER METHODS=====
    def bvcs(self, samples, acceptorbamloc, outpath, reference_loc, varcon_outpath,
             variantlist, merge=True):
        """Build, write, and return a variant context file.

        The variant context file is built from the provided variants and
        acceptor and donors alignment files.

        Parameters
        ----------
        samples : list of sample_mapper.Sample objects
        acceptorbamloc : str
            Path to alignment file to use as acceptor
        outpath : str
            Path to folder to write output files to
        reference_loc : str
            Path to the genomic reference fasta file
        varcon_outpath : str
            Path and name to write variant context file to
        variantlist : dict
            Variants to use per sample
        merge : bool
            Whether to merge overlapping contexts from the same sample

        Returns
        -------
        variantcontexts : VariantContextFile
            Established variant contexts
        """
        donor_vcfs_used = []
        donor_bams_used = []
        variantcontexts = VariantContextFile()

        try:
            acceptorbamfile = pysam.AlignmentFile(acceptorbamloc, reference_filename=reference_loc)
        except IOError:
            self.vaselogger.critical("Could not open Acceptor BAM/CRAM")
            sys.exit()

        # Start iterating over the samples
        for sample in samples:
            self.vaselogger.debug(f"Start processing sample {sample.hash_id}")

            # Establish variant filter for this sample, if present.
            sample_var_filter = None
            if variantlist is not None:
                sample_var_filter = self.get_sample_filter(sample, variantlist)
                if sample_var_filter is None:
                    continue
            samplevariants = self.get_sample_vcf_variants_2(sample.vcf, sample_var_filter)

            if not samplevariants:
                self.vaselogger.warning(f"No variants obtained for sample {sample.hash_id}. "
                                        "Skipping sample")
                continue

            # Call the method that will process the sample
            self.bvcs_process_sample(sample.hash_id, variantcontexts, acceptorbamfile,
                                     sample.bam, reference_loc, samplevariants, merge)

            # Add the used donor VCF and BAM to the lists of used VCF and BAM files
            donor_bams_used.append(sample.bam)
            donor_vcfs_used.append(sample.vcf)

        # Check if there are no variant contexts.
        if variantcontexts.get_number_of_contexts() <= 0:
            self.vaselogger.info("No variant contexts were created. "
                                 "No output files will be written.")
            return None

        # Write the output variant context output data
        self.bvcs_write_output_files(outpath, varcon_outpath, variantcontexts, samples,
                                     donor_vcfs_used, donor_bams_used)

        # Checks whether the program is running on debug and, if so, write some extra output files.
        if self.vaselogger.getEffectiveLevel() == 10:
            self.write_optional_output_files(outpath, variantcontexts)

        # Set the used acceptor and donor files
        variantcontexts.set_template_alignment_file(acceptorbamloc)
        variantcontexts.set_donor_alignment_files(donor_bams_used)
        variantcontexts.set_donor_variant_files(donor_vcfs_used)
        return variantcontexts

    def bvcs_process_sample(self, sampleid, variantcontextfile, abamfile, dbamfileloc,
                            referenceloc, samplevariants, merge=True):
        """Process a sample and add variant contexts to a variant context file.

        Parameters
        ----------
        sampleid : str
            Sample name/identifier
        variantcontextfile : VariantContextFile
            Variant context file that saves variant contexts
        abamfile: pysam.AlignmentFile
            Already opened pysam AlignmentFile to use as acceptor
        dbamfileloc: str
            Path to the alignment file to use as donor
        referenceloc: str
            Path to the genomic reference fasta file
        samplevariants : list of VcfVariants
            Variants to process for the specified sample
        merge : bool
            Whether to merge overlapping contexts from the same sample
        """
        try:
            donorbamfile = pysam.AlignmentFile(dbamfileloc, reference_filename=referenceloc)
        except IOError:
            self.vaselogger.warning(f"Could not open {dbamfileloc} ; Skipping {sampleid}")
            return

        # Iterate over the sample variants
        for samplevariant in samplevariants:
            variantcontext = self.bvcs_process_variant(sampleid, samplevariant[0],
                                                       abamfile, donorbamfile)
            if not variantcontext:
                self.vaselogger.info("Could not establish variant context; Skipping.")
                continue

            # Set the priority label and priority level for the variant context
            variantcontext.priorities = samplevariant[1]

            varcon_collided = variantcontextfile.context_collision_v2(variantcontext.get_context())
            if varcon_collided is None:
                variantcontextfile.add_existing_variant_context(
                    variantcontext.get_variant_context_id(),
                    variantcontext
                    )
                continue
            self.vaselogger.debug(f"Variant context {variantcontext.get_variant_context_id()} "
                                  "overlaps with variant context"
                                  f"{varcon_collided.get_variant_context_id()}")
            is_same_sample = (varcon_collided.get_variant_context_sample() ==
                              variantcontext.get_variant_context_sample())
            if merge and is_same_sample:
                self.vaselogger.debug("Merging contexts from same sample.")
                variantcontext = self.merge_variant_contexts(varcon_collided, variantcontext)
                variantcontextfile.add_existing_variant_context(
                    variantcontext.get_variant_context_id(),
                    variantcontext
                    )
                continue
            self.vaselogger.debug("Colliding contexts from different sample.")
            # Start selecting which variant context to keep
            if variantcontext.priorities <= varcon_collided.priorities:
                self.vaselogger.debug("Keeping original variant context with same or higher "
                                      "priority.")
                continue
            self.vaselogger.debug("Removing original variant context with lower priority.")
            variantcontextfile.remove_variant_context(varcon_collided.get_variant_context_id())
            variantcontextfile.add_existing_variant_context(variantcontext.get_variant_context_id(),
                                                            variantcontext)

    def bvcs_process_variant(self, sampleid, samplevariant, abamfile, dbamfile):
        """Process a variant and return the established variant context.

        Parameters
        ----------
        sampleid : str
            Sample name/identifier
        samplevariant : pysam.VariantRecord
            Variant to process and for which to establish an acceptor, donor and variant context
        abamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile to use as acceptor
        dbamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile to use as donor

        Returns
        -------
        vcontext : VariantContext or None
            The established variant context, None if context could not be established
        """
        # Establish the donor context
        variantid = self.get_vcf_variant_id(samplevariant)
        varianttype = self.determine_variant_type(samplevariant.start, samplevariant.stop)

        self.vaselogger.debug(f"Processing variant {variantid}.")
        self.debug_msg("vw", variantid)
        self.vaselogger.debug(f"Variant {variantid} determined to be {varianttype}")
        searchwindow = [samplevariant.pos, samplevariant.stop]
        self.vaselogger.debug(f"Search window determined to be {samplevariant.chrom}:"
                              f"{searchwindow[0]}-{searchwindow[1]}")

        # Determine the donor context.
        self.debug_msg("dc", variantid)
        start_time = time.time()
        dcontext = self.bvcs_establish_context(sampleid, variantid, samplevariant.chrom,
                                               samplevariant.pos, searchwindow, dbamfile)
        if not dcontext:
            self.vaselogger.info("Could not establish donor context. "
                                 f"Skipping variant {variantid}")
            return None
        self.debug_msg("dc", variantid, start_time)
        self.vaselogger.debug(f"Donor context determined to be {dcontext.get_context_chrom()}:"
                              f"{dcontext.get_context_start()}-{dcontext.get_context_end()}")

        # Determine the acceptor context.
        self.debug_msg("ac", variantid)
        start_time = time.time()
        acontext = self.bvcs_establish_context(sampleid, variantid, samplevariant.chrom,
                                               samplevariant.pos, searchwindow, abamfile,
                                               dcontext.get_context())
        self.debug_msg("ac", variantid, start_time)
        self.vaselogger.debug(f"Acceptor context determined to be {acontext.get_context_chrom()}:"
                              f"{acontext.get_context_start()}-{acontext.get_context_end()}")

        # Determine the variant context.
        self.debug_msg("cc", variantid)
        start_time = time.time()
        vcontext = self.bvcs_establish_variant_context(sampleid, variantid, samplevariant,
                                                       samplevariant.pos, acontext, dcontext,
                                                       abamfile, dbamfile)
        self.debug_msg("cc", variantid, start_time)
        if vcontext is not None:
            self.vaselogger.debug(f"Combined context determined to be "
                                  f"{vcontext.get_variant_context_chrom()}:"
                                  f"{vcontext.get_variant_context_start()}-"
                                  f"{vcontext.get_variant_context_end()}")
        return vcontext

    def bvcs_establish_variant_context(self, sampleid, variantid, variant, variantpos,
                                       acontext, dcontext, abamfile, dbamfile):
        """Establish and return a variant context.

        The variant context window is established based on the acceptor and
        donor contexts. Reads and mates overlapping  with the variant context
        are also fetched and added to the variant context.

        Parameters
        ----------
        sampleid : str
            Sample name/identifier
        variantid : str
            Variant identifier
        variantpos: int
            Leftmost genomic position of the variant
        acontext : OverlapContext
            Established acceptor context
        dcontext : OverlapContext
            Established donor context
        abamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile used as acceptor
        dbamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile used as donor

        Returns
        -------
        variant_context : VariantContext
            Established variant context with all associated data
        """
        unmapped_alist = []
        unmapped_dlist = []

        # Determine the variant context from the acceptor and donor context
        vcontext_window = self.determine_largest_context(variantpos, acontext.get_context(),
                                                         dcontext.get_context())

        # Gather variant context donor reads.
        self.debug_msg("cdr", variantid)
        start_time = time.time()
        vcontext_dreads = self.get_variant_reads(vcontext_window[0], vcontext_window[2],
                                                 vcontext_window[3], dbamfile)
        self.debug_msg("cdr", variantid, start_time)

        # Gather variant context acceptor reads.
        self.debug_msg("car", variantid)
        start_time = time.time()
        vcontext_areads = self.get_variant_reads(vcontext_window[0], vcontext_window[2],
                                                 vcontext_window[3], abamfile)
        self.debug_msg("car", variantid, start_time)

        variant_context = VariantContext(variantid, sampleid, *vcontext_window, vcontext_areads,
                                         vcontext_dreads, acontext, dcontext, [variant])

        # Set the variant context unmapped read ids
        variant_context.set_unmapped_acceptor_mate_ids(unmapped_alist)
        variant_context.set_unmapped_donor_mate_ids(unmapped_dlist)
        return variant_context

    # Establishes an acceptor/donor context by fetching reads (and their mates)
    # overlapping directly with the variant.
    def bvcs_establish_context(self, sampleid, variantid, variantchrom, variantpos, searchwindow,
                               bamfile, fallback_window=None):
        # pylint: disable=E1120
        """Establish and return an acceptor/donor context.

        The context window is established from fetched reads and their mates
        overlapping with the variant.

        Parameters
        ----------
        sampleid : str
            Sample name/identifier
        variantid : str
            Variant identifier
        variantchrom : str
            Chromosome name the variant is located on
        variantpos : int
            Leftmost genomic position of the variant
        searchwindow: list of int
            Search window to use for fetching reads
        bamfile : pysam.AlignmentFile
            Already opened pysam AlignmentFile
        fallback_window : list
            Window to set if no window could be set/determined

        Returns
        -------
        OverlapContext or None
            Acceptor/donor context if context is established, None if not
        """
        unmappedlist = []

        # Fetch context reads and establish the context window
        self.vaselogger.debug("Fetching reads.")
        start_time = time.time()
        context_reads = self.get_variant_reads(variantchrom, *searchwindow, bamfile)
        self.vaselogger.debug(f"Fetching reads took {time.time() - start_time} seconds")

        if not context_reads:
            self.vaselogger.debug("No reads were found.")
        context_window = self.determine_context(context_reads, variantpos, variantchrom)

        # Check whether the context_window is valid and, if not, whether a
        # fallback window has been set
        if not context_window:
            self.vaselogger.debug("Context window could not be determined.")
            if fallback_window:
                context_window = fallback_window
                self.vaselogger.debug("Context window is set to the fall back window.")
            else:
                return None

        # Create the context object containing all context data
        adcontext = OverlapContext(variantid, sampleid, *context_window, context_reads)
        adcontext.set_unmapped_mate_ids(unmappedlist)
        return adcontext

    def bvcs_write_output_files(self, outpath, varcon_outpath, variantcontextfile, samples,
                                used_donor_vcfs, used_donor_bams):
        """Write VaSeBuilder output files.

        These output files are the standard output files when building a
        variant context file. Output files include the variant context file,
        variant context statistics file, variant context BED file, used donor
        variant files and used donor alignment files.

        Parameters
        ----------
        outpath: str
            Path to folder to write the output files to
        varcon_outpath : str
            Path to write variant context file to
        variantcontextfile : VariantContextFile
            Variant contexts to write to file
        vcfsamplemap : dict
            Variant files per sample
        bamsamplemap : dict
            Alignment files per sample
        used_donor_vcfs : list of str
            Donor variant files used to create the variant contexts
        used_donor_bams : list of str
            Donor alignment files used to create the variant contexts
        """
        # Write the variant context file itself
        self.vaselogger.info(f"Writing variant contexts to {varcon_outpath}")
        variantcontextfile.write_variant_context_file(varcon_outpath, self.creation_id)

        # Write the variant context statistics file
        self.vaselogger.info(f"Writing variant context statistics to {outpath}varconstats.txt")
        variantcontextfile.write_variant_context_stats(f"{outpath}varconstats.txt",
                                                       self.creation_id)

        # Write the variant contexts as a BED file
        self.vaselogger.info("Writing the variant contexts to a BED file")
        self.write_bed_file(variantcontextfile.get_variant_contexts(),
                            f"{outpath}variantcontexts.bed",
                            self.creation_id)

        # Write a listfile of the used variant (VCF/BCF) files
        self.vaselogger.info("Writing the used donor variant files per sample to "
                             f"{outpath}donor_variant_files.txt")
        self.write_used_donor_files(f"{outpath}donor_variant_files.txt", samples, used_donor_vcfs,
                                    self.creation_id, "v")

        # Write a listfile of the used alignment (BAM/CRAM) files
        self.vaselogger.info("Writing the used donor alignment files per sample to "
                             f"{outpath}donor_alignment_files.txt")
        self.write_used_donor_files(f"{outpath}donor_alignment_files.txt", samples, used_donor_bams,
                                    self.creation_id, "a")

        # Write a hashtable for hashed sampleIDs if necessary.
        if samples[0].id == samples[0].hash_id:
            return
        self.vaselogger.info(f"Writing sampleID hashtable to {outpath}donor_sampleID_hashtable.txt")
        self.write_hashtable(f"{outpath}donor_sampleID_hashtable.txt", samples, self.creation_id)

    def write_hashtable(self, outfileloc, samples, vbuuid):
        """Write a file containing sample IDs and corresponding sample ID hashes.

        Contains VBUUID and field name header lines. Hashes are written as
        full Argon2 encoded hashes, which include Argon2 parameters used to
        create the hashes, for reproducibility and hash checking.

        Parameters
        ----------
        outfileloc : str
            Path to write the file to.
        samples : list of sample_mapper.Sample objects
            Sample objects containing relevant file paths and attributes.
        vbuuid : str
            ID of this VaSeBuilder run.

        Returns
        -------
        None.
        """
        try:
            with open(outfileloc, "w") as outfile:
                outfile.write(f"#VBUUID: {vbuuid}\n")
                outfile.write("#SampleID\tArgon2Encoding\n")
                for sample in samples:
                    outfile.write(f"{sample.id}\t{sample.hash}\n")
        except IOError:
            self.vaselogger.critical(f"Could not write hashtable to {outfileloc}")

    def write_pmode_linkfile(self, outpath, context_fqs_links):
        """Write the link from variant context identifier to fastq output files for P-mode.

        This output file is meant to link a VaSeBuilder run with fastq output files.

        Parameters
        ----------
        outpath : str
            Path to output folder to write the link file to.
        context_fqs_links : dict of str: list
            Fastq files per variant context identifier
        """
        plinkloc = f"{outpath}plink_{self.creation_id}.txt"
        try:
            with open(plinkloc, "w") as plinkfile:
                plinkfile.write(f"#VBUUID: {self.creation_id}\n")
                for contextid, fqfiles in context_fqs_links.items():
                    plinkfile.write(f"{contextid}\t{fqfiles[0]}\t{fqfiles[1]}\n")
        except IOError:
            self.vaselogger.warning(f"Could not write P-mode link file {plinkloc} "
                                    f"for run {self.creation_id}")

    @staticmethod
    def shuffle_donor_read_identifiers(donorreads, seed=2):
        """Shuffle and return a list of donor read identifiers.

        Prior to shuffling the donor read identifiers, the provided donor
        read list is copied to preserve the original. The new list is then
        sorted and a seed is set to ensure that the shuffling can be
        reproduced if the same data is used.

        Parameters
        ----------
        donorreads :
            Donor read identifiers to shuffle
        s: int
            Seed to set for shuffling (default = 2)

        Returns
        -------
        shuffled_donor_reads : list of str
            Shuffled donor read identifiers
        """
        shuffled_donor_reads = donorreads.copy()
        shuffled_donor_reads.sort()

        random.seed(seed)
        random.shuffle(shuffled_donor_reads)
        return shuffled_donor_reads

    def shuffle_donor_add_positions(self, num_of_template_reads, num_of_donor_reads, seed=2):
        """Shuffle FASTQ donor read add positions.

        Parameters
        ----------
        num_of_template_reads : int
            Number of template reads in the acceptor
        num_of_donor_reads : int
            Number of donor reads to be added
        s : int
            Seed to set for shuffling (default = 2)

        Returns
        -------
        add_positions : list of int
            Shuffled positions in fastq file to add donor reads to
        """
        random.seed(seed)
        self.vaselogger.debug(f"Semi random donor add positions seed set to {seed}")
        add_positions = []

        # Check whether the number of donor reads to add exceeds the number
        # of acceptor reads in the template.
        if num_of_donor_reads > num_of_template_reads:
            self.vaselogger.debug("Found more donor reads to add than")
            random_sample_size = num_of_donor_reads
            while random_sample_size > 0:
                pos_to_add = []
                if random_sample_size >= num_of_template_reads:
                    pos_to_add = random.sample(range(0, num_of_template_reads),
                                               num_of_template_reads)
                else:
                    pos_to_add = random.sample(range(0, num_of_template_reads),
                                               random_sample_size)
                add_positions.extend(pos_to_add)
                random_sample_size = random_sample_size - num_of_template_reads
            return add_positions
        add_positions = random.sample(range(0, num_of_template_reads), num_of_donor_reads)
        return add_positions

    @staticmethod
    def read_is_hard_clipped(fetchedread):
        """Return whether the provided read is hard-clipped.

        Parameters
        ----------
        fetchedread : pysam.AlignedSegment
            Read fetched from alignment file with pysam

        Returns
        -------
        bool
            True if read is hardclipped, False if not or read has no cigar string
        """
        if fetchedread.cigarstring is not None:
            return "H" in fetchedread.cigarstring
        return False

    @staticmethod
    def check_template_size(templatefqloc):
        """Return the number of reads in the template fastq file.

        The returned number is divided by 4 as each read entry consists of four lines.

        Parameters
        ----------
        templatefqloc : str
            Path to acceptor fastq file to check

        Returns
        -------
        int
            Number of read entries in the template fastq file
        """
        line_count = 0
        with gzip.open(templatefqloc, "r") as templatefq:
            for _ in templatefq:
                line_count += 1
        return int(line_count/4)

    def build_fastq_v2(self, acceptorfq_filepaths, acceptorreads_toskip, donor_context_reads,
                       forward_or_reverse, vasefq_outpath, random_seed, donor_read_insert_data):
        """Build and write a set of validation fastq files.

        A set of validation fastq files is build using a set of
        template/acceptor fastq files. Acceptor reads will be filtered from
        these file via read identifier and donor reads will be added. Donor
        reads reads will be added at semi-random positions. The random.seed()
        method is used to ensure reproducibility as using the same data (in
        the same order) and the same seed results in the same shuffle.

        Parameters
        ----------
        acceptorfq_filepaths : list of str
            Paths to template fastq files to use
        acceptorreads_toskip : list of str
            Identifiers of acceptor reads to skip
        donor_context_reads : list of tuple
            Donor reads to add to the validation fastq files
        forward_or_reverse : str
            Write forward ('1') or reverse ('2')
        vasefq_outpath :
            Path to write VaSeBuilder validation fastq files to
        """
        # Split all donor reads to add over the template fastq files
        donor_read_ids = [x[0] for x in donor_context_reads]
        donor_read_ids.sort()
        donor_read_ids = list(set(donor_read_ids))
        # self.vaselogger.debug(f"Donor read ids: {donor_read_ids}")
        distributed_read_ids = self.divide_donorfastqs_over_acceptors(donor_read_ids,
                                                                      len(acceptorfq_filepaths))
        # self.vaselogger.debug(f"Distributed read ids: {distributed_read_ids}")

        # Iterate over the R1/R2 fastq in files to use as templates for the
        for i in range(0, len(acceptorfq_filepaths)):
            # Collect the donor reads to write.
            add_donor_ids = distributed_read_ids[i]
            self.vaselogger.debug(f"Distributed read ids: {add_donor_ids}")
            add_donor_reads = [x for x in donor_context_reads if x[0] in add_donor_ids]
            self.vaselogger.debug(f"Will add {len(add_donor_ids)} donor reads")

            # Write the new VaSe FastQ file.
            vasefq_outname = self.set_fastq_out_path(vasefq_outpath, forward_or_reverse, i + 1)
            self.vaselogger.debug(f"Set FastQ output path to: {vasefq_outname}")

            # Check whether to add the fastq file name into the donor read insert position map
            if vasefq_outname.split(".")[0][:-3] not in donor_read_insert_data:
                donor_read_insert_data[vasefq_outname.split(".")[0][:-3]] = {}

            self.write_vase_fastq_v2(acceptorfq_filepaths[i], vasefq_outname,
                                     acceptorreads_toskip, add_donor_reads, add_donor_ids,
                                     forward_or_reverse, random_seed, donor_read_insert_data)

    def write_vase_fastq_v2(self, acceptor_infq, fastq_outpath,
                            acceptorreads_toskip, donorbamreaddata,
                            donor_readids, fr, random_seed, donor_read_insert_data):
        """Create and write a single VaSeBuilder validation fastq file.

        Parameters
        ----------
        acceptor_infq : str
            Path to
        fastq_outpath : str
            Path to write VaSeBuilder validation fastq file to
        acceptorreads_toskip : list of str
            Acceptor read identifiers to exclude from the validation fastq file
        donorbamreaddata : list of tuple
            Donor reads to writes
        fr : str
            Forward('1') or reverse ('2') fastq file
        """
        fastq_prefix = fastq_outpath.split(".")[0][:-3]
        try:
            fqgz_outfile = io.BufferedWriter(open(fastq_outpath, "wb"))
            self.vaselogger.debug(f"Writing data to validation fastq {fastq_outpath}")

            cur_line_index = -1    # Current read position in the template fastq
            cur_add_index = 0    # Current read position in the validation fastq

            # Determine where to semi randomly add the donor reads in the fastq
            num_of_template_reads = self.check_template_size(acceptor_infq)
            self.vaselogger.debug(f"Template has {num_of_template_reads} reads")
            donor_add_positions = self.shuffle_donor_add_positions(num_of_template_reads,
                                                                   len(donor_readids),
                                                                   random_seed)
            # self.vaselogger.debug(f"Add positions for {fastq_outpath} = {donor_add_positions}")
            donor_reads_to_addpos = self.link_donor_addpos_reads_v2(donor_add_positions,
                                                                    donor_readids,
                                                                    donorbamreaddata)
            # self.vaselogger.debug(f"Read to add pos for {fastq_outpath} = "
            #                       f"{donor_reads_to_addpos}")

            # Open the template fastq and write filtered data to a new fastq.gz file.
            fqgz_infile = io.BufferedReader(gzip.open(acceptor_infq, "rb"))
            self.vaselogger.debug(f"Opened template FastQ: {acceptor_infq}")
            for fileline in fqgz_infile:
                cur_line_index += 1
                # Check if we are located at a read identifier.
                if not fileline.startswith(b"@"):
                    continue
                if fileline.decode("utf-8").split()[0][1:] not in acceptorreads_toskip:
                    fqgz_outfile.write(fileline)
                    fqgz_outfile.write(next(fqgz_infile))
                    fqgz_outfile.write(next(fqgz_infile))
                    fqgz_outfile.write(next(fqgz_infile))
                    cur_add_index += 1
                else:
                    self.vaselogger.debug(f"Skipping acceptor read {fileline}")

                # Check if we need to add a donor read at the current position
                if cur_line_index not in donor_reads_to_addpos:
                    continue
                # self.vaselogger.debug(f"{cur_line_index} is in list of positions to add donor")
                for donorread in donor_reads_to_addpos[cur_line_index]:
                    if donorread[1] == fr:
                        fqlines = ("@" + str(donorread[0]) + "\n"
                                   + str(donorread[2]) + "\n"
                                   + "+\n"
                                   + str(donorread[3]) + "\n")
                        fqgz_outfile.write(fqlines.encode("utf-8"))
                        cur_add_index += 1
                        # self.vaselogger.debug(f"Added donor read {donorread[0]}/{donorread[1]} "
                        #                       f"at {cur_add_index}")
                        self.add_donor_insert_data(fastq_prefix, donorread[0], fr,
                                                   cur_add_index, donor_read_insert_data)
            fqgz_infile.close()

            fqgz_outfile.flush()
            fqgz_outfile.close()

        except IOError as ioe:
            if ioe.filename == acceptor_infq:
                self.vaselogger.critical("The supplied template FastQ file "
                                         "could not be found.")
            if ioe.filename == fastq_outpath:
                self.vaselogger.critical("A FastQ file could not be written "
                                         "to the provided output location.")
            sys.exit()

    @staticmethod
    def link_donor_addpos_reads_v2(donor_addpos, donor_read_ids, donor_reads):
        """Link and return donor add positions and donor reads.

        Parameters
        ----------
        donor_addpos : list of int
            Positions in validation fastq to add donor reads at
        donor_read_ids : list of str

        donor_reads : list of tuple
            Donor reads to add to validation fastq

        Returns
        -------
        add_posread_link : dict of list
            Donor reads to add per add position
        """
        add_posread_link = {}
        for addpos, dread_id in zip(donor_addpos, donor_read_ids):
            if addpos not in add_posread_link:
                add_posread_link[addpos] = []
            add_posread_link[addpos].extend([x for x in donor_reads if x[0] == dread_id])
        return add_posread_link

    def read_donor_fastq(self, donor_fastq, forward_reverse, donor_read_data):
        """Read and save the donor fastq reads.

        Parameters
        ----------
        donor_fastq : str
            Path to the donor fastq file to read
        forward_reverse : str
            Reading forward (R1) or reverse (R2) donor read data
        donor_read_data : dict
            Dictionary saving the donor read data

        Returns
        -------
        donor_read_data : dict
            Updated dictionary containing donor read data
        """
        try:
            with gzip.open(donor_fastq, "rt") as dfqfile:
                for dfqfileline in dfqfile:
                    if dfqfileline.startswith("@"):
                        dfq_readid = dfqfileline[1:].strip()
                        dfq_readseq = next(dfqfile).strip()
                        # dfq_optline = next(dfqfile).strip()
                        dfq_readqual = next(dfqfile).strip()
                        if dfq_readid not in donor_read_data:
                            donor_read_data[dfq_readid] = []
                        donor_read_data[dfq_readid].append((dfq_readid, forward_reverse,
                                                            dfq_readseq, dfq_readqual))
        except IOError:
            self.vaselogger.debug(f"Could not read donor fastq file {donor_fastq}")
        return donor_read_data

    def run_ac_mode_v2(self, afq1_in, afq2_in, dfqs, varconfile, random_seed, outpath):
        """Run VaSeBuilder AC-mode.

        This run mode builds a set of validation fastq files by adding already
        existing fastq files to acceptor fastq files used as template. The
        variant context file used to construct the variant contexts of the
        donor fastq files is required to filter out the acceptor reads to be
        replaced with the donor data.

        Parameters
        ----------
        afq1_in : list of str
            R1 acceptor fastq files to use as template
        afq2_in : list of str
            R2 acceptor fastq files to use as template
        dfqs : list of list of str
            R1 and R2 donor fastq files to add
        varconfile: VariantContextFile
            Variant context to use for filtering out acceptor reads
        outpath: str
            Path to folder to write the output to
        """
        self.vaselogger.info("Running VaSeBuilder AC-mode")
        # Split the donor fastqs into an R1 and R2 group
        r1_dfqs = [dfq[0] for dfq in dfqs]
        r2_dfqs = [dfq[1] for dfq in dfqs]

        # Get the list of acceptor reads to exclude
        skip_list = varconfile.get_all_variant_context_acceptor_read_ids()
        skip_list.sort()

        # Read all the donor read fastq data
        donor_reads = {}
        for fr_i, dfq_i in zip(["1", "2"], [r1_dfqs, r2_dfqs]):
            for j in range(len(dfq_i)):
                donor_reads = self.read_donor_fastq(dfq_i[j], fr_i, donor_reads)

        # Divide the donor reads equally over the template fastq files
        donor_read_ids = list(donor_reads.keys())
        donor_read_ids.sort()

        # Distribute the read identifiers over the fastq files
        distributed_donor_read_ids = self.divide_donorfastqs_over_acceptors(donor_read_ids,
                                                                            len(afq1_in))

        # Iterate over the acceptor fastq files
        donor_read_add_data = {}
        for fr_i, afq_i in zip(["1", "2"], [afq1_in, afq2_in]):
            self.build_fastqs_from_donors_v2(afq_i, skip_list, distributed_donor_read_ids,
                                             donor_reads, fr_i, random_seed, outpath,
                                             donor_read_add_data)
        self.write_donor_insert_positions_v2(donor_read_add_data,
                                             f"{outpath}_donor_read_insert_positions.txt")

    def run_ac_mode_v25(self, afq1_in, afq2_in, donor_bams, variant_context_file,
                        random_seed, outpath):
        """Run VaSeBuilder AB-mode.

        Parameters
        ----------
        afq1_in : list of str
            List of R1 template fastq files
        afq2_in : list of str
            List of R2 template fastq files
        donor_bams : list of str
            List of BAM donor files to add
        variant_context_file : VariantContextFile
            Variant context file containing variant contexts
        random_seed : int
            Seed value to use for random read insertion
        outpath : str
            Folder to write output files to
        """
        # Get all acceptor read identifiers
        acceptor_skip_list = variant_context_file.get_all_variant_context_acceptor_read_ids()
        acceptor_skip_list.sort()

        # Read all the donor BAM files
        donor_reads = {}
        for dbamfile in donor_bams:
            donor_reads = self.read_donor_bam_v3(dbamfile, donor_reads)
        donor_read_ids = list(donor_reads.keys())
        donor_read_ids.sort()

        distributed_donor_read_ids = self.divide_donorfastqs_over_acceptors(donor_read_ids,
                                                                            len(afq1_in))

        donor_read_add_data = {}
        for fr_i, afq_i in zip(["1", "2"], [afq1_in, afq2_in]):
            self.build_fastqs_from_donors_v2(afq_i, acceptor_skip_list, distributed_donor_read_ids,
                                             donor_reads, fr_i, random_seed, outpath,
                                             donor_read_add_data)
        self.write_donor_insert_positions_v2(donor_read_add_data,
                                             f"{outpath}_donor_read_insert_positions.txt")

    def read_donor_bam_v3(self, path_to_donorbam, donorreaddata):
        """Read a provided BAM file and add the reads from the file.

        Parameters
        ----------
        path_to_donorbam : str
            Path to BAM donor file to read
        donorreaddata : dict
            Already saved donor data to add reads to

        Returns
        -------
        donorreaddata : dict
            Updated donor read data with added reads from BAM file
        """
        rep_dict = {"a": "t", "c": "g", "g": "c", "t": "a", "n": "n",
                    "A": "T", "C": "G", "G": "C", "T": "A", "N": "N"}
        readnum = 0
        try:
            dbamfile = pysam.AlignmentFile(path_to_donorbam, "rb")
            for donorread in dbamfile.fetch():

                donor_read_qualities = "".join([chr(x+33) for x in donorread.query_qualities])

                # Check if the read is read 1 or 2
                donor_read_fr = "2"
                if donorread.is_read1:
                    donor_read_fr = "1"

                # Check alignment direction.
                if donorread.is_reverse:
                    donor_seq = ""
                    for nt in donorread.query_sequence[::-1]:
                        donor_seq += rep_dict[nt]
                    donor_read_qualities = donor_read_qualities[::-1]
                else:
                    donor_seq = donorread.query_sequence

                # Check where to add the read to
                if donorread.query_name not in donorreaddata:
                    donorreaddata[donorread.query_name] = []
                if donor_read_fr == "1":
                    donorreaddata[donorread.query_name].insert(0, tuple([donorread.query_name,
                                                                         donor_read_fr,
                                                                         donor_seq,
                                                                         donor_read_qualities]))
                else:
                    donorreaddata[donorread.query_name].append(tuple([donorread.query_name,
                                                                      donor_read_fr,
                                                                      donor_seq,
                                                                      donor_read_qualities]))
                readnum += 1
            dbamfile.close()
        except IOError:
            self.vaselogger.warning(f"Could not read donor BAM file {path_to_donorbam}")
        self.vaselogger.debug(f"Read {readnum} donor reads from {path_to_donorbam}")
        return donorreaddata

    def build_fastqs_from_donors_v2(self, acceptor_fqsin, acceptor_reads_to_exclude,
                                    distributed_donor_reads, donor_reads, forward_reverse,
                                    random_seed, outpath, donor_read_insert_data):
        """Build a set of R1/R2 validation fastq files using existing donor fastq files.

        Parameters
        ----------
        acceptor_fqsin: list of str
            Template/Acceptor fastq files to use
        acceptor_reads_to_exclude: list of str
        distributed_donor_reads : list of list of str
        donor_reads: dict
        forward_reverse: str
            Whether to construct an R1 or R2 fastq file
        random_seed: int
            Random seed to use for shuffling donor add positions
        outpath: str
            Path top write produced fastq file to
        donor_read_insert_data:
        """
        for i in range(len(acceptor_fqsin)):
            fqoutname = self.set_fastq_out_path(outpath, forward_reverse, i + 1)

            # Add the fastq file entry to the insert positions map
            if fqoutname.split(".")[0][:-3] not in donor_read_insert_data:
                donor_read_insert_data[fqoutname.split(".")[0][:-3]] = {}

            # Filter the donor reads specific to the template file
            selected_donor_reads = [donor_reads[y] for y in distributed_donor_reads[i]]
            donor_reads_to_add = []
            for j in selected_donor_reads:
                donor_reads_to_add.extend(j)
            self.write_vase_fastq_v2(acceptor_fqsin[i], fqoutname, acceptor_reads_to_exclude,
                                     donor_reads_to_add, distributed_donor_reads[i],
                                     forward_reverse, random_seed, donor_read_insert_data)

    def write_donor_insert_positions_v2(self, inserted_position_data, outpath):
        """Write the insert positions for each set of reads.

        Insert positions are written per read identifier.

        Parameters
        ----------
        inserted_position_data : dict
            Position data
        outpath : str
            Path and name to write the donor read insert position data to
        """
        try:
            with open(outpath, "w") as ipd_outfile:
                ipd_outfile.write(f"#VBUUID: {self.creation_id}\n")
                ipd_outfile.write("ReadId\tR1_InsertPos\tFastqR1Out\tR2_InsertPos\tFastqR2Out\n")

                # Iterate over the donor read insert position data and write to file
                for fastqout in inserted_position_data:
                    readid_list = sorted(inserted_position_data[fastqout])

                    # Iterate over each read identifier for the specified
                    # output R1 and R2 fastq set.
                    for readid in readid_list:
                        r1_insertpos = self.get_saved_insert_position(
                            "1",
                            inserted_position_data[fastqout][readid]
                            )
                        r2_insertpos = self.get_saved_insert_position(
                            "2",
                            inserted_position_data[fastqout][readid]
                            )

                        ipd_outfile.write(f"{readid}\t{r1_insertpos}\t{fastqout}_R1.fastq\t"
                                          f"{r2_insertpos}\t{fastqout}_R2.fastq\n")
        except IOError:
            self.vaselogger.warning(f"Could not write donor insert position data to {outpath}")

    @staticmethod
    def get_saved_insert_position(readpn, read_insert_data):
        """Return the insert position of a read, or 'NA' if not available.

        Parameters
        ----------
        readpn : str
            The readpair number ('1' or '2')
        read_insert_data : tuple of str and int
            The read insert data

        Returns
        -------
        int or str
            The insert position, 'NA' if not available
        """
        if readpn in read_insert_data:
            readpn_index = read_insert_data.index(readpn)
            if readpn_index < len(read_insert_data)-1:
                return read_insert_data[read_insert_data.index(readpn)+1]
        return "NA"

    @staticmethod
    def add_donor_insert_data(fqoutname, readid, forward_reverse, insertpos, donor_insert_data):
        """Add the insert position and read id to the insertion data map.

        The insertion data map saves the position at which a read for each set
        of validation fastq output files was inserted.

        Parameters
        ----------
        fqoutname : str
            Name of fastq file
        readid : str
            Read identifier for which to save the insert position
        forward_reverse : str
            Indicator whether the read is R1 or R2
        insertpos : int
            Position the donor read was inserted at in the validation fastq
        donor_insert_data: dict
            Saved donor read insertions into validation fastq
        """
        if fqoutname in donor_insert_data:
            if readid in donor_insert_data[fqoutname]:
                if forward_reverse not in donor_insert_data[fqoutname][readid]:
                    donor_insert_data[fqoutname][readid] = donor_insert_data[fqoutname][readid] + \
                                                           (forward_reverse, insertpos)
            else:
                donor_insert_data[fqoutname][readid] = (forward_reverse, insertpos)

    def refetch_donor_reads(self, samples, variant_context_file, genome_reference):
        """Refetch the donor reads from a set of donor BAM files.

        Parameters
        ----------
        variant_context_file : VariantContextFile
            Collection of variant contexts
        donor_alignment_files : dict
            List of paths to donor alignment files
        genome_reference : str
            Path to genome reference file
        """
        varcon_per_sample_id = variant_context_file.get_variant_contexts_by_sampleid()

        # Start iterating over the samples
        for sample in samples:
            try:
                dalnfile = pysam.AlignmentFile(sample.bam, reference_filename=genome_reference)

                # Iterate over the variant contexts for the current sample
                for varcon in varcon_per_sample_id[sample.hash_id]:
                    donor_read_ids = set(varcon.get_donor_read_ids())
                    fetched_reads = self.get_variant_reads(
                        varcon.get_variant_context_chrom(),
                        varcon.get_variant_context_start(),
                        varcon.get_variant_context_end(), dalnfile
                        )

                    # Filter out fetched reads not satisfying the donor read identifiers
                    donor_reads = [fdread for fdread in fetched_reads
                                   if fdread.query_name in donor_read_ids]
                    varcon.variant_context_dreads = donor_reads
                dalnfile.close()
            except IOError:
                self.vaselogger.warning("Could not open donor alignment file "
                                        f"{sample.bam}")

    def merge_variant_contexts(self, varcon1, varcon2):
        """Merge two variant contexts and return the merged context.

        First the associated acceptor and donor contexts are merged. Then the
        maximum window from both variant contexts is determined and reads are
        merged. The newly combined variant context will retain the context
        identifier of the first variant context.

        Parameters
        ----------
        varcon1 : VariantContext
            First variant context to be merged
        varcon2 : VariantContext
            Second variant context to be merged

        Returns
        -------
        combined_varcon : VariantContext
            New merged variant context
        """
        # Combine the acceptor and donor contexts
        combined_acceptor_context = self.merge_overlap_contexts(varcon1.get_acceptor_context(),
                                                                varcon2.get_acceptor_context())
        combined_donor_context = self.merge_overlap_contexts(varcon1.get_donor_context(),
                                                             varcon2.get_donor_context())

        # Obtain a list of acceptor and donor reads from both variant contexts
        vareads = varcon1.get_acceptor_reads() + varcon2.get_acceptor_reads()
        vdreads = varcon1.get_donor_reads() + varcon2.get_donor_reads()

        # Combine the two variant contexts by determining the new context
        # window and acceptor and donor reads
        combined_window = self.determine_largest_context(varcon1.get_variant_context_origin(),
                                                         varcon1.get_context(),
                                                         varcon2.get_context())
        combined_vareads = self.uniqify_variant_reads(vareads)
        combined_vdreads = self.uniqify_variant_reads(vdreads)

        # Set the new combined variant context
        combined_varcon = VariantContext(varcon1.get_variant_context_id(),
                                         varcon1.get_variant_context_sample(),
                                         *combined_window, combined_vareads, combined_vdreads,
                                         combined_acceptor_context, combined_donor_context,
                                         varcon1.variants + varcon2.variants)

        # Determine new prioritization levels.
        if varcon1.priorities is None or varcon2.priorities is None:
            combined_varcon.priorities = None
            return combined_varcon

        # Set each priority filter as the highest from either original context.
        for p1, p2 in zip(varcon1.priorities, varcon2.priorities):
            combined_varcon.priorities.append(max(p1, p2))
        return combined_varcon

    def merge_overlap_contexts(self, context1, context2):
        # pylint: disable=E1120
        """Merge two acceptor or donor contexts and return the new merged context.

        Acceptor/Donor contexts are merged by constructing the maximum size of
        both contexts. Reads in both contexts are also merged and uniqified.

        Parameters
        ----------
        context1 : OverlapContext
            First acceptor/donor context to be merged
        context2 : OverlapContext
            Second acceptor/donor context to be merged

        Returns
        -------
        combined_accdon_context : OverlapContext
            Combined acceptor/donor context
        """
        adreads = context1.get_context_bam_reads() + context2.get_context_bam_reads()
        combined_window = self.determine_largest_context(
            context1.get_context_origin(),
            context1.get_context(),
            context2.get_context()
            )
        combined_adreads = self.uniqify_variant_reads(adreads)
        combined_accdon_context = OverlapContext(
            context1.get_context_id(),
            context1.get_sample_id(),
            *combined_window,
            combined_adreads
            )
        return combined_accdon_context

    def write_vcf_slice(self, sample_id, variants, outpath):
        """Write a VCF file with a minimal combined header from variants.

        All variants are written to the same VCF file. Header fields are merged
        from all variant objects, with minimal header information. INFO field
        descriptions and non-essential fields are removed. Variants are all
        recorded as belonging to a single sample.

        Parameters
        ----------
        sample_id : str
            Sample field for the VCF column header.
        variants : list of pysam.VariantRecord objects
            Variant to write to VCF.
        outpath : str
            Path to write output VCF file to.
        """
        fields = ["fileformat", "filter", "alt", "format", "contig", "reference", "info"]
        header_records = [str(x) for x in variants[0].header.records
                          if str(x).lstrip("#").split("=")[0].lower() in fields]
        for i, j in enumerate(header_records):
            if j.startswith("##INFO"):
                new_info_field = j.split(",Description")[0]
                if not new_info_field.endswith(">\n"):
                    new_info_field += ">\n"
                header_records[i] = new_info_field
        header_records.append(
            f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{sample_id}\n"
            )
        try:
            with open(outpath, "w") as outfile:
                outfile.writelines(header_records)
                for variant in variants:
                    outfile.write(variant.__str__())
        except IOError:
            self.vaselogger.warning(f"Could not write VCF slice for sample {sample_id}.")

    @staticmethod
    def write_spike_in_bam(out_header, reads, out_path, sort=True):
        """Write a BAM file with the provided header and reads.

        Header must be pre-made and should reflect all reads provided. If
        sort=True, a temporary unsorted BAM file will be written, then removed
        after sorting. Sorted BAM file will be indexed.

        Parameters
        ----------
        out_header : OrderedDict()
            Header with required fields.
        reads : list of pysam.AlignedSegment objects
        out_path : str
            Path to write output BAM file to.
        sort : bool, optional
            Option to coordinate sort and index output BAM. The default is True.
        """
        out_bam = pysam.AlignmentFile(out_path, "wb", header=out_header)
        for read in reads:
            out_bam.write(read)
        out_bam.close()

        if sort:
            sort_out_name = f"{out_path[:-4]}.sorted.bam"
            pysam.sort("-o", sort_out_name, out_path, catch_stdout=False)
            os.remove(out_path)
            pysam.index(sort_out_name, catch_stdout=False)

    @classmethod
    def select_bam_header_fields(cls, bam_header, elements_to_keep, change_sample_name=None):
        """Keep only a selected set of BAM header lines.

        Optionally, samples names in the SM tags of @RG lines can also be changed if required.

        Parameters
        ----------
        bam_header : OrderedDict
            BAM header data to select specific fields from
        elements_to_keep : list of str
            Names of lines to keep (e.g. :SN, RG)
        change_sample_names : str or None
            Str with which to replace sample fields in header (Default: None)

        Returns
        -------
        filtered_header : OrderedDict
            Header with only the required data fields
        """
        filtered_header = OrderedDict()
        for head in bam_header:
            if head in elements_to_keep:
                filtered_header[head] = bam_header[head]

            if change_sample_name is not None:
                cls.change_bam_header_sample_names(filtered_header, change_sample_name)
        return filtered_header

    @staticmethod
    def change_bam_header_sample_names(template_header, replacement_name):
        """Change the sample names with the set replacement label.

        Sample names in the SM tags of each @RG line is replaced in the header.

        Parameters
        ----------
        template_header : OrderedDict
            Header data from the AlignmentHeader
        replacement_name : str
            Label to replace sample names with
        """
        if "RG" in template_header:
            for i in range(len(template_header["RG"])):
                template_header["RG"][i]["SM"] = replacement_name

    @staticmethod
    def change_bam_header_field(template_header, header_line, header_field, replacement_value):
        """Change a specified field in a specified BAM header line (e.g 'RG').

        Parameters
        ----------
        template_header: OrderedDict
        header_line : str
            The type of header line to modify ('RG', SQ, etc)
        header_field : str
            The specific field of the header line to change ('SM', LB, etc)
        replacement_value: str
            Value to use as replacement for the value of the specified field
        """
        if header_line in template_header:
            for i in range(len(template_header[header_line])):
                template_header[header_line][i][header_field] = replacement_value
        return template_header

    def write_pmode_bamlinkfile(self, varcon_bam_link, outpath):
        """Write the P-mode BAM link file.

        Parameters
        ----------
        varcon_bam_link : dict
            BAM output file linked per variant context
        outpath : str
            Path to write output file to
        """
        try:
            with open(outpath, "w") as bamlinkfile:
                bamlinkfile.write("Variant context\tBAM file\n")
                for varcon in varcon_bam_link:
                    bamlinkfile.write(f"{varcon}\t{varcon_bam_link[varcon]}\n")
        except IOError:
            self.vaselogger.warning("Could not write P-mode link file")

    def get_donor_insert_positions(self, acceptor_fq, donorreadids, donorreaddata, randomseed):
        """Create random FastQ insertion positions for donor reads.

        Parameters
        ----------
        acceptor_fq : str
            Path to acceptor fastq file
        donorreadids : list of str
            List of donor read identifiers
        donorreaddata : dict
            Donor read
        randomseed : int
            Seed to set for semi random shuffling

        Returns
        -------
        donor_read_to_addpos : dict
            Read ids linked to insert position
        """
        num_of_template_reads = self.check_template_size(acceptor_fq)
        self.vaselogger.debug(f"Template has {num_of_template_reads} reads")
        donor_add_positions = self.shuffle_donor_add_positions(
            num_of_template_reads,
            len(donorreadids),
            randomseed
            )
        donor_reads_to_addpos = self.link_donor_addpos_reads_v2(
            donor_add_positions,
            donorreadids,
            donorreaddata
            )
        return donor_reads_to_addpos

    # XXX: This will break if it find an incorrect read pair. You can't delete
    # a dictionary entry while looping over it:
    # RuntimeError: dictionary changed size during iteration
    def remove_incorrect_bam_donor_readpairs(self, donorreaddata):
        """Remove BAM donor reads without an R1 or R2 read and return the modified dictionary.

        This method will only be used in AB-mode to check that all BAM donor
        reads from the supplied BAM donor files have a forward and reverse
        read. Reads that are missing either the R1 or R2 read are removed from
        the dictionary.

        Parameters
        ----------
        donorreaddata : dict
            BAM donor read data

        Returns
        -------
        donorreaddata : dict
            Modified BAM donor read data with incorrect read pairs removed
        """
        read_removal_count = 0
        for read_id in donorreaddata:
            if len(donorreaddata[read_id]) != 2:
                del donorreaddata[read_id]
                read_removal_count += 1
        self.vaselogger.debug(f"Removed {read_removal_count} incorrect read pairs.")
        return donorreaddata

    def run_ab_mode_v2(self, variant_context_file, afq1_in, afq2_in,
                       donor_bams, random_seed, fqoutpath):
        """Run the alternative version of the AB-mode.

        This method differs that the insert positions are only determined once per fastq R1/R2 set.

        Parameters
        ----------
        variant_context_file : VariantContextFile
        afq1_in: list of str
            List of R1 template fastq files
        afq2_in: list of str
            List of R2 template fastq files
        donor_bams : list of str
            List of BAM donor files to add
        random_seed:
            Seed number to use for semi random reed distribution
        fqoutpath : str
            Path and name/prefix for the validation fastq files
        """
        # Set the list of acceptor reads to skip when making the
        acceptor_reads_skiplist = set(
            variant_context_file.get_all_variant_context_acceptor_read_ids()
            )

        # Read the read from all donor BAM files.
        donor_read_data = {}
        for dbamfile in donor_bams:
            self.vaselogger.debug(f"Start reading BAM donor file {dbamfile}")
            donor_read_data = self.read_donor_bam_v3(dbamfile, donor_read_data)
        donor_read_data = self.remove_incorrect_bam_donor_readpairs(donor_read_data)

        r1_donor_read_data = {x: y[0] for x, y in donor_read_data.items()}
        r2_donor_read_data = {x: y[1] for x, y in donor_read_data.items()}

        # Set a list of donor read identifiers and divide them over the template R1/R2 fastq sets.
        donor_read_ids = list(set(donor_read_data.keys()))
        donor_read_ids.sort()
        distributed_donor_read_ids = self.divide_donorfastqs_over_acceptors(donor_read_ids,
                                                                            len(afq1_in))

        # Start iterating over the template fastq files and semi-randomly
        # distribute the donor reads.
        donor_read_inserted_positions = {}
        distribution_index = 0
        for r1, r2 in zip(afq1_in, afq2_in):
            r1_outname = self.set_fastq_out_path(fqoutpath, "1", distribution_index + 1)
            r2_outname = self.set_fastq_out_path(fqoutpath, "2", distribution_index + 1)

            # Add the fastq file entry to the insert positions map
            # XXX: Splitting the filename on '.' will fail if the path includes './'
            if r1_outname.split(".")[0][:-3] not in donor_read_inserted_positions:
                donor_read_inserted_positions[r1_outname.split(".")[0][:-3]] = {}

            # Determine the required data
            self.vaselogger.info(f"Counting sequences in {r1}...")
            num_of_template_reads = self.check_template_size(r1)
            donor_add_positions = self.shuffle_donor_add_positions(
                num_of_template_reads,
                len(distributed_donor_read_ids[distribution_index]),
                random_seed
                )
            donor_reads_to_addpos = self.link_donor_addpos_reads_v3(
                donor_add_positions,
                distributed_donor_read_ids[distribution_index]
                )

            # Start writing the R1 and R2 fastq files
            self.write_validation_fastq_file(
                r1, "1", acceptor_reads_skiplist, donor_reads_to_addpos,
                r1_donor_read_data, r1_outname, donor_read_inserted_positions
                )
            self.write_validation_fastq_file(
                r2, "2", acceptor_reads_skiplist, donor_reads_to_addpos,
                r2_donor_read_data, r2_outname, donor_read_inserted_positions
                )
            distribution_index += 1

        # Write the donor read insert position data to a text file.
        self.write_donor_insert_positions_v2(donor_read_inserted_positions,
                                             f"{fqoutpath}_donor_read_insert_positions.txt")

    def write_validation_fastq_file(self, template_fq, fr, acceptorreads_toskip, donoraddpositions,
                                    donorreaddata, fastq_outpath, donorinsertpositions):
        """Write a single R1 or R2 validation set fastq file.

        Parameters
        ----------
        template_fq : str
            Template fastq gz file to use
        fr : str
            Whether to write R1 or R2
        acceptorreads_toskip : list of str
            Acceptor reads to exclude from the validation fastq file
        donoraddpositions : dict
            Positions where to insert donor reads
        donorreaddata : dict
            Donor reads to add to the fastq file
        fastq_outpath : str
            Path and name to write the fastq file to
        donorinsertpositions : dict

        """
        fastq_prefix = fastq_outpath.split(".")[0][:-3]
        try:
            fqgz_outfile = io.BufferedWriter(open(fastq_outpath, "wb"))
            self.vaselogger.debug(f"Writing data to validation fastq {fastq_outpath}")

            cur_line_index = -1  # Current read position in the template fastq
            cur_add_index = 0  # Current read position in the validation fastq=

            # Open the template fastq and write filtered data to a new fastq.gz file.
            fqgz_infile = io.BufferedReader(gzip.open(template_fq, "rb"))
            self.vaselogger.debug(f"Opened template FastQ: {template_fq}")
            for fileline in fqgz_infile:
                cur_line_index += 1

                # Check if we are located at a read identifier.
                if not fileline.startswith(b"@"):
                    continue
                if fileline.decode("utf-8").split()[0][1:] not in acceptorreads_toskip:
                    fqgz_outfile.write(fileline)
                    fqgz_outfile.write(next(fqgz_infile))
                    fqgz_outfile.write(next(fqgz_infile))
                    fqgz_outfile.write(next(fqgz_infile))
                    cur_add_index += 1

                # Check if we need to add a donor read at the current position
                if cur_line_index not in donoraddpositions:
                    continue
                for donorreadid in donoraddpositions[cur_line_index]:
                    donorread = donorreaddata[donorreadid]
                    if not donorread[1] == fr:
                        self.vaselogger.warning(f"{donorread[0]} is not the correct orientation "
                                                "for this template.")
                    fqlines = ("@" + str(donorread[0]) + "\n"
                               + str(donorread[2]) + "\n"
                               + "+\n"
                               + str(donorread[3]) + "\n")
                    fqgz_outfile.write(fqlines.encode("utf-8"))
                    cur_add_index += 1
                    # self.vaselogger.debug(f"Added donor read {donorread[0]}/{donorread[1]} at "
                    #                       f"{cur_add_index}")
                    self.add_donor_insert_data(fastq_prefix, donorread[0], fr, cur_add_index,
                                               donorinsertpositions)
            fqgz_infile.close()

            fqgz_outfile.flush()
            fqgz_outfile.close()

        except IOError as ioe:
            if ioe.filename == template_fq:
                self.vaselogger.critical("The supplied template FastQ file "
                                         "could not be found.")
            if ioe.filename == fastq_outpath:
                self.vaselogger.critical("A FastQ file could not be written "
                                         "to the provided output location.")
            else:
                self.vaselogger.critical(f"{ioe}")
            sys.exit()

    @staticmethod
    def link_donor_addpos_reads_v3(donor_addpos, donor_read_ids):
        """Link and return donor add positions and donor reads.

        Parameters
        ----------
        donor_addpos : list of int
            Positions in validation fastq to add donor reads at
        donor_read_ids : list of str
            List of donor read identifiers

        Returns
        -------
        add_posread_link : dict of list
            Donor reads to add per add position
        """
        add_posread_link = {}
        for addpos, dread_id in zip(donor_addpos, donor_read_ids):
            if addpos not in add_posread_link:
                add_posread_link[addpos] = []
            add_posread_link[addpos].append(dread_id)
        return add_posread_link

    # TODO:
# =============================================================================
#     def select_variant_contexts(self, variant_context_file):
#         """Select contexts and solve overlaps.
#
#         Parameters
#         ----------
#         variant_context_file : VariantContextFile
#             VariantContextFile with variant contexts
#         :return:
#         """
#         print("test")
# =============================================================================
