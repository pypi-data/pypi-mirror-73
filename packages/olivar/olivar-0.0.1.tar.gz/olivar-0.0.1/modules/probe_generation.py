#!/usr/bin/env python
# coding: utf-8
"""Run Parsnp for getting MUMs with consideration of Negatives"""
import argparse
import logging
import pathlib
import os, random
import sys
import re
import subprocess
import shutil
from Bio import SeqIO

from modules.utils import get_logger, run_command

MINIMUM_MUM_LEN = 15

logger = get_logger(__name__)

def generate_read_list(reads, mum_length):
    """
    Generate A list of MUMs form xmfa of Parsnp
    """
    name_list = []
    read_list = []
    tempstr = ""
    for i, read_seqs in enumerate(reads):
        if "#SequenceCount" in read_seqs:
            seq_counter = int(read_seqs.split()[1])
        if read_seqs[0] == "#" or read_seqs[0] == "=":
            continue
        if read_seqs[0] == ">":
            name_list.append(read_seqs[:-1])
            # print(read_seqs)
        elif i == len(reads) - 2:
            tempstr = tempstr + read_seqs[:-1]
            read_list.append([i for i in re.split("A|C|T|G|-", tempstr) if i])
            tempstr = ""
        elif reads[i + 1][0] == ">":
            tempstr = tempstr + read_seqs[:-1]
            read_list.append([i for i in re.split("A|C|T|G|-", tempstr) if i])
            tempstr = ""
        elif reads[i + 1][0] == "=":
            tempstr = tempstr + read_seqs[:-1]
            read_list.append([i for i in re.split("A|C|T|G|-", tempstr) if i])
            tempstr = ""
        else:
            tempstr = tempstr + read_seqs[:-1]
    final_reads = []
    for i, reads_seqs in enumerate(read_list):
        if i % seq_counter == 0:
            final_reads += reads_seqs
    clusters = {}
    for i, reads_seqs in enumerate(final_reads):
        if len(reads_seqs) > mum_length:
            clusters.update({f"cluster{str(i)}": reads_seqs})
    return clusters



def run_parsnp(input_dir, negative_control, work_dir, threads):
    """run parsnp"""
    # TODO obviously fix this
    work_dir = os.path.join(work_dir, "parsnp")
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    positive_gneome = os.path.join(input_dir, random.choice(os.listdir(input_dir)))
    # genome_files = [str(f) for f  in pathlib.Path(input_dir).glob("*")]
    run_command(" ".join([
        "parsnp",
        "-c", 
        "-b", 
        "-r", positive_gneome, 
        "-d", os.path.join(input_dir, "*"), negative_control, 
        "-o", work_dir,
        "-p", str(threads)]), logger)


def parse_xmfa(work_dir):
    """parse parsnp xmfa file"""
    xmfa_path = os.path.join(work_dir, "parsnp", "parsnp.xmfa")
    with open(xmfa_path, "r") as xmfa_file:
        readlist = xmfa_file.readlines()
    clusters = generate_read_list(readlist, MINIMUM_MUM_LEN)
    return clusters


def output_mums(work_dir, clusters):
    """output all mums"""
    outpath = os.path.join(work_dir, "probes")
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    with open(os.path.join(outpath, "parsnp_mums.fasta"), "w") as parsnp_mums:
        for seqs in clusters:
            parsnp_mums.write(">" + seqs + "\n")
            parsnp_mums.write(clusters[seqs] + "\n")


def generate_k_mers(kmer_length_min, kmer_length_max, work_dir):
    """generate k mers from mum files"""
    mums_dir = os.path.join(work_dir, "probes", "parsnp_mums.fasta")
    kmer_dir = os.path.join(work_dir, "probes", "final_kmers.fasta")
    with open(kmer_dir, "w") as final_kmers:
        for mum_seq in list(SeqIO.parse(mums_dir, format="fasta")):
            seq_id = mum_seq.id.replace("_", "-")
            if len(mum_seq.seq) >= kmer_length_min:
                for kmer_length in range(kmer_length_min, kmer_length_max + 1):
                    for j in range(len(mum_seq.seq) - kmer_length):
                        final_kmers.writelines(f">{seq_id}-{kmer_length}-{j}_Probe_F\n")
                        final_kmers.writelines(f"{mum_seq.seq[j:j+kmer_length]}\n")
            else:
                final_kmers.writelines(f">{seq_id}-{len(mum_seq.seq)}-{0}_Probe_F\n")
                final_kmers.writelines(f"{mum_seq.seq}\n")

def run(parsnp_input_dir: str, negative_control: str, output_dir: str, kmer_min: int, kmer_max: int, num_threads: int):
    run_parsnp(
        parsnp_input_dir,
        negative_control,
        output_dir,
        num_threads)
    clusters = parse_xmfa(output_dir)
    output_mums(output_dir, clusters)
    generate_k_mers(kmer_min, kmer_max, output_dir)

def parse_args():
    """Parse all args"""
    parser = argparse.ArgumentParser(
        prog="parsnp_result_parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required_args = parser.add_argument_group("Required named args")
    required_args.add_argument("-f",
                               "--fasta",
                               help="path to the folder of Parsnp Input",
                               type=str)
    required_args.add_argument("--neg",
                               help="path to the negative control file",
                               type=str)
    required_args.add_argument("-w",
                               "--workdir",
                               help="Folder of results, the final kmer \
                                would be stored at [WORKDIR]/out/final_k_mers.fasta",
                               default="work",
                               type=str)

    optional_parameter_args = parser.add_argument_group("Optional parameters")
    optional_parameter_args.add_argument(
        "--kmer-min",
        type=int, 
        default=21, \
        help="Minimum length of desired k-mer probes")
    optional_parameter_args.add_argument(
        "--kmer-max",
        type=int, 
        default=21, \
        help="Maximum length of desired k-mer probes")
    optional_parameter_args.add_argument(
        "-t",
        "--threads",
        default=32,
        help="Number of threads, mainly for parsnp",
        type=int)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    run(args.fasta, args.neg, args.workdir, args.kmer_min, args.kmer_max, args.threads)



if __name__ == "__main__":
    main()
    
