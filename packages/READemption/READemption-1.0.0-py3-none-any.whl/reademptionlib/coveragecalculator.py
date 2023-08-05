import numpy as np
import pysam


class CoverageCalculator(object):
    def __init__(
        self,
        read_count_splitting=True,
        uniquely_aligned_only=False,
        coverage_style="global",
        clip_length=11,
        non_strand_specific=False,
    ):
        self._read_count_splitting = read_count_splitting
        self._uniquely_aligned_only = uniquely_aligned_only
        self._coverage_style = coverage_style
        self._clip_length = clip_length
        self._coverage_add_function = self._select_coverage_add_function()
        self._coverages = {}
        self._non_strand_specific = non_strand_specific

    def ref_seq_and_coverages(self, bam_path):
        bam = self._open_bam_file(bam_path)
        for ref_seq, length in zip(bam.references, bam.lengths):
            self._init_coverage_list(length)
            self._calc_coverage(ref_seq, bam)
            if self._non_strand_specific:
                self._sum_strand_coverages()
            yield (ref_seq, self._coverages)

    def _sum_strand_coverages(self):
        self._coverages["forward_and_reverse"] = [
            cov_for + abs(cov_rev)
            for cov_for, cov_rev in zip(
                self._coverages["forward"], self._coverages["reverse"]
            )
        ]
        self._coverages.pop("forward")
        self._coverages.pop("reverse")

    def _init_coverage_list(self, length):
        for strand in ["forward", "reverse"]:
            self._coverages[strand] = np.array([0.0] * length)

    def _calc_coverage(self, ref_seq, bam):
        for entry in bam.fetch(ref_seq):
            number_of_hits = dict(entry.tags)["NH"]
            if self._uniquely_aligned_only is True and number_of_hits != 1:
                continue
            # Note: No translation from SAMParsers coordinates to python
            # list coorindates is needed.
            start = entry.pos
            end = entry.aend
            # Normalize coverage increment by number of read alignments
            # per read
            if self._read_count_splitting is True:
                increment = 1.0 / float(number_of_hits)
            else:
                increment = 1.0
            self._coverage_add_function(entry, increment, start, end)

    def _select_coverage_add_function(self):
        if self._coverage_style == "first_base_only":
            return self._add_first_base_coverage
        elif self._coverage_style == "last_base_only":
            return self._add_last_base_coverage
        elif self._coverage_style == "centered":
            return self._add_centered_coverage
        else:
            return self._add_whole_alignment_coverage

    def _open_bam_file(self, bam_file):
        return pysam.Samfile(bam_file)

    def _add_whole_alignment_coverage(self, entry, increment, start, end):
        if (entry.is_reverse is False and entry.is_read2 is False) or (
            entry.is_reverse is True and entry.is_read2 is True
        ):
            self._coverages["forward"][start:end] += increment
        else:
            self._coverages["reverse"][start:end] -= increment

    def _add_first_base_coverage(self, entry, increment, start, end):
        if (entry.is_reverse is False and entry.is_read2 is False) or (
            entry.is_reverse is True and entry.is_read2 is True
        ):
            self._coverages["forward"][start] += increment
        else:
            self._coverages["reverse"][end - 1] -= increment

    def _add_last_base_coverage(self, entry, increment, start, end):
        if (entry.is_reverse is False and entry.is_read2 is False) or (
            entry.is_reverse is True and entry.is_read2 is True
        ):
            self._coverages["forward"][end - 1] += increment
        else:
            self._coverages["reverse"][start] -= increment

    def _add_centered_coverage(self, entry, increment, start, end):
        center_start = start + self._clip_length
        center_end = end - self._clip_length
        center_length = float(center_end - center_start)
        if center_length < 1.0:
            # print(entry)
            return
        if (entry.is_reverse is False and entry.is_read2 is False) or (
            entry.is_reverse is True and entry.is_read2 is True
        ):
            self._coverages["forward"][center_start:center_end] += (
                increment / center_length
            )
        else:
            self._coverages["reverse"][center_start:center_end] -= (
                increment / center_length
            )
