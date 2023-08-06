#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Built-in modules #
import re

# Internal modules #
from plumbing.common import GenWithLength
from plumbing.color  import Color

# Third party modules #
import Bio
from Bio.Seq import Seq

# Constants #
iupac = {'A':'A',    'G':'G',   'T':'T',   'C':'C',
         'M':'AC',   'R':'AG',  'W':'AT',  'S':'CG',   'Y':'CT',   'K':'GT',
         'V':'ACG',  'H':'ACT', 'D':'AGT', 'B':'CGT',
         'X':'ACGT', 'N':'ACGT'}

# Function to create a regex pattern from a sequence #
iupac_pattern = lambda seq: ''.join(['[' + iupac[char] + ']' for char in seq])

###############################################################################
class TwoPrimers:
    """A container for the two primers of a sample."""

    def __len__(self): return 2

    def __init__(self, fwd_str, rev_str):
        # Original strings #
        self.fwd_str = fwd_str
        self.rev_str = rev_str
        # Lengths in base pairs #
        self.fwd_len = len(self.fwd_str)
        self.rev_len = len(self.rev_str)
        # Sequences as biopython objects #
        self.fwd_seq = Bio.Seq.Seq(self.fwd_str)
        self.rev_seq = Bio.Seq.Seq(self.rev_str)
        # Create search patterns in regex syntax #
        self.fwd_pat = iupac_pattern(self.fwd_seq)
        # Don't add reverse complement here, use the provided option instead #
        self.rev_pat = iupac_pattern(self.rev_seq)
        # Reverse complemented sequences #
        self.fwd_revcomp = self.fwd_seq.reverse_complement()
        self.rev_revcomp = self.rev_seq.reverse_complement()
        # Search patterns when reverse complemented #
        self.fwd_pat_revcomp = iupac_pattern(self.fwd_revcomp)
        self.rev_pat_revcomp = iupac_pattern(self.rev_revcomp)
        # Simple search expression (without mismatches authorized yet) #
        self.fwd_regex = re.compile(self.fwd_pat)
        self.rev_regex = re.compile(self.rev_pat)
        # Uracil instead of thymine #
        self.fwd_regex_uracil = re.compile(self.fwd_pat.replace('T', 'U'))
        self.rev_regex_uracil = re.compile(self.rev_pat.replace('T', 'U'))

###############################################################################
class ReadWithPrimers:
    def __init__(self, read, fwd_regex, rev_regex):
        self.read          = read
        self.fwd_match     = fwd_regex.search(str(read.seq))
        self.rev_match     = rev_regex.search(str(read.seq))
        self.fwd_start_pos = self.fwd_match.start() if self.fwd_match else None
        self.rev_start_pos = self.rev_match.start() if self.rev_match else None
        self.fwd_end_pos   = self.fwd_match.end()   if self.fwd_match else None
        self.rev_end_pos   = self.rev_match.end()   if self.rev_match else None

    @property
    def pretty(self):
        # The string #
        seq  = self.read.seq._data
        fwds = self.fwd_start_pos
        fwde = self.fwd_end_pos
        revs = self.rev_start_pos
        reve = self.rev_end_pos
        # No matches #
        if not self.fwd_match and not self.rev_match:
            return seq + '\n'
        # One matches #
        if self.fwd_match and not self.rev_match:
            return seq[0:fwds]    + Color.red + \
                   seq[fwds:fwde] + Color.end + \
                   seq[fwde:]     + '\n'
        # One matches #
        if not self.fwd_match and self.rev_match:
            return seq[0:revs]    + Color.red + \
                   seq[revs:reve] + Color.end + \
                   seq[reve:]     + '\n'
        # Two matches #
        if self.fwd_match and self.rev_match:
            return seq[0:fwds]    + Color.red + \
                   seq[fwds:fwde] + Color.end + \
                   seq[fwde:revs] + Color.red + \
                   seq[revs:reve] + Color.end + \
                   seq[reve:]     + '\n'

###############################################################################
class ReadWithPrimersRevCompl:
    """Here the reverse primer start and end values will be negative."""

    def __init__(self, read, fwd_regex, rev_regex):
        self.read          = read
        self.fwd_match     = fwd_regex.search(str(read.seq))
        self.rev_match     = rev_regex.search(str(read.seq))
        self.fwd_start_pos = self.fwd_match.start()             if self.fwd_match else None
        self.rev_start_pos = self.rev_match.end() - len(read)   if self.rev_match else None
        self.fwd_end_pos   = self.fwd_match.end()               if self.fwd_match else None
        self.rev_end_pos   = self.rev_match.start() - len(read) if self.rev_match else None

################################################################################
def parse_primers(fasta, primers=None, mismatches=0, revcompl=False):
    """
    This functions takes a FASTA instance as first parameter,
    in a similar fashion to methods of the FASTA object itself.
    The primers will be loaded from that FASTA if not specified.
    """
    # Pass the primers, or we take them from the FASTA instance #
    if primers is None: primers = fasta.primers
    # Special module #
    import regex
    # Case straight #
    if not revcompl:
        fwd_regex = "(%s){s<=%i}" % (primers.fwd_pat, mismatches)
        rev_regex = "(%s){s<=%i}" % (primers.rev_pat, mismatches)
        fwd_regex = regex.compile(fwd_regex)
        rev_regex = regex.compile(rev_regex)
        # Generate a new object for every read #
        read_with_primers = lambda r: ReadWithPrimers(r, fwd_regex, rev_regex)
        generator = (read_with_primers(r) for r in fasta.parse())
    # Case revcompl #
    if revcompl:
        fwd_regex = "(%s){s<=%i}" % (primers.fwd_pat, mismatches)
        rev_regex = "(%s){s<=%i}" % (primers.rev_pat, mismatches)
        fwd_regex = regex.compile("(%s){s<=%i}" % (primers.fwd_pattern,          mismatches))
        rev_regex = regex.compile("(%s){s<=%i}" % (primers.rev_pattern_revcompl, mismatches))
        generator = (ReadWithPrimersRevCompl(r, fwd_regex, rev_regex) for r in fasta.parse())
    # Return #
    return GenWithLength(generator, len(fasta))
