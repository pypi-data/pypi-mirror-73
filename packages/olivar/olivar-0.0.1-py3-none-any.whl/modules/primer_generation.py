#!/usr/bin/python
import argparse
import logging
import os
from collections import defaultdict
import subprocess
from subprocess import PIPE
from Bio import SeqIO
from Bio.Seq import Seq
import copy
from tqdm import tqdm
# Local imports
import modules.parameter_checks as prc
from modules.utils import get_logger

eps = 0.0001

logger = get_logger(__name__)

def standardize_sequences(msa):
    for seq in msa:
        seq.seq = seq.seq.upper()
    return msa

def check_identity(bpairs):
    return not bpairs or bpairs.count(bpairs[0]) == len(bpairs)

def get_identity_stretches(msa, orientation, probe):
    stretches = []
    stretch = ""
    for base_pairs in zip(*[seq.seq for seq in msa]):
        if base_pairs[0] != "-" and base_pairs[0] != "N": 
            if check_identity(base_pairs):
                stretch += base_pairs[0]
            else:
                if stretch != "":
                    if orientation == "R":
                        stretch = str(Seq(stretch).reverse_complement())
                    stretches.append((stretch, orientation, probe))
                    stretch = ""
    if orientation == "R":
        stretch = str(Seq(stretch).reverse_complement())
    stretches.append((stretch, orientation, probe))
    return stretches

def get_flanking_stretches(msa, probes):
    stretches = []
    reference_seq = msa[0].seq
    for probe in probes:
        index = reference_seq.find(probe.seq)
        if index == -1:
            logger.error("Probe not found in reference.")
            return []
        # Pre-probe primers (Forward)
        pre_msa = []
        for seq in msa:
            pre_seq = copy.deepcopy(seq)
            pre_seq.seq = seq.seq[index - 150:index]
            pre_msa.append(pre_seq)
        pre_stretches = get_identity_stretches(pre_msa, "F", probe.id)
        # Post-probe primers (Reverse)
        post_msa = []
        for seq in msa:
            post_seq = copy.deepcopy(seq)
            post_seq.seq = seq.seq[index + len(probe):index + len(probe) + 150]
            post_msa.append(post_seq)
        post_stretches = get_identity_stretches(post_msa, "R", probe.id)
        stretches += pre_stretches
        stretches += post_stretches
    return stretches

def filter_length(stretches, min_length):
    filtered = []
    for stretch, ori, pr in stretches:
        if min_length <= len(stretch):
            filtered.append((stretch, ori, pr))
    return filtered

def get_primers_from_stretches(stretches, min_length, max_length):
    primers = []
    for stretch, ori, probe in stretches:
        slen = len(stretch)
        for plen in range(min_length, max_length + 1):
            primers += [(stretch[i:(i + plen)], ori, probe) for i in range(slen - plen + 1)]
    return primers

def filter_to_unique(seqs):
    return list(set(seqs))

def filter_low_complexity(seqs, mono_min_len):
    filtered = []
    for seq, ori, pr in seqs:
        if prc.evaluate_mono_homomers(seq, mono_min_len)[1] < mono_min_len:
            filtered.append((seq, ori, pr))
    return filtered

def filter_oligotm(seqs, tm_high, tm_low, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):
    filtered = []
    logger.info("Filtering Tm...")
    for seq, ori, pr in seqs:
        seq_tm = prc.evaluate_tm(seq, dna_conc, single_ion_conc, double_ion_conc, dntps_conc)
        if tm_high - seq_tm > eps and seq_tm - tm_low > eps:
            filtered.append((seq, ori, pr))
    return filtered

# TODO threads
def generate_primers(
        input_oligos: str,
        output_dir: str,
        msa_input: str,
        primer_min: int,
        primer_max: int,
        config,
        num_threads: int):
    msa = list(SeqIO.parse(msa_input, "fasta"))
    msa = standardize_sequences(msa)
    seqs = list(SeqIO.parse(input_oligos, "fasta"))
    seqs = standardize_sequences(seqs)
    flanking_stretches = get_flanking_stretches(msa, seqs)
    logger.info(f"Total flanking stretches found: {len(flanking_stretches)}")
    filtered_stretches = filter_length(flanking_stretches, primer_min)
    logger.info(f"Flanking stretches >= {primer_min}: {len(filtered_stretches)}")
    primers = get_primers_from_stretches(filtered_stretches, primer_min, primer_max)
    logger.info(f"Total primers generated: {len(primers)}")
    filtered_primers = filter_to_unique(primers)
    logger.info(f"Unique primers: {len(filtered_primers)}")
    # mono_min_len = config.getint("Other", "homomonomer_min_count")
    # filtered_primers = filter_low_complexity(filtered_primers, mono_min_len)
    # logger.info(f"Primers without monohomomers: {len(filtered_primers)}")
    # tm_high = config.getfloat("Primer", "Tm_max")
    # tm_low = config.getfloat("Primer", "Tm_min")
    # filtered_primers = filter_oligotm(filtered_primers, tm_high, tm_low, 
                                      # config.getfloat("Chemistry", "DNA_conc_nano"), 
                                      # config.getfloat("Chemistry", "Single_ion_con_milli"),
                                      # config.getfloat("Chemistry", "Double_ion_con_milli"), 
                                      # config.getfloat("Chemistry", "dNTPs_con_milli"))
    # logger.info(f"Primers with {tm_low} <= Tm <= {tm_high}: {len(filtered_primers)}")
    primers_fasta = os.path.join(output_dir, "primers.fasta")
    with open(primers_fasta, "w") as fout:
        for i, value in enumerate(filtered_primers):
            primer, orientation, probe = value
            probe = probe.split("_")[0]
            fout.write(f">{probe}:Primer{i}_Primer_{orientation}\n{primer}\n")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--msa", help="path to the MSA FASTA file", type=str)
    parser.add_argument("--min-length", help="Minimum length of primers to generate", type=int)
    parser.add_argument("--max-length", help="Maximum length of primers to generate", type=int)
    parser.add_argument("-s", "--seqs", help="path to the probes FASTA file", type=str)
    parser.add_argument("-c", "--config", help="Path to config file", type=str, default=0)
    parser.add_argument("-o", "--output", help="path to the output file", type=str)
    parser.add_argument("--num-threads", help="Number of threads to use", type=int)
    args = parser.parse_args()
    generate_primers(
        args.seqs,
        args.output,
        args.msa,
        args.min_length,
        args.max_length,
        args.config,
        args.num_threads)

if __name__ == "__main__":
    main()

