#!/usr/bin/env python
# coding: utf-8
"""Check Probe/Primer's sensitivity to SARS-COV-2"""
import argparse
import logging
import os
import sys
import time
# from collections import Counter
# import subprocess
import pandas as pd
import urllib
from Bio import Entrez
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from tqdm import tqdm

from .utils import disambiguate_seq, get_logger, UNAMBIG_LIMIT

logger = get_logger(__name__)

NCOVID = "2697049"
DISAMBSEQFILE = "all_disamb_seqs.fa"
BLASTRESULTFILE = "disamb_seqs_blast.csv"
KRONAINFOFILE = "krona_info.txt"
KRONAPLOTFILE = "false_positive_taxonomy_distribution.html"
# MUMRECORDS = list(SeqIO.parse("data/MUMs.fa", "fasta"))
# NCOVRECORDS = list(SeqIO.parse("data/filtered_genomes.fasta", "fasta"))


def get_ncbi_record():
    """ Generate a nCoV Accession List"""
    handle = Entrez.esearch(
        db="nuccore",
        retmax=200,
        term="txid" + NCOVID +
        " AND (complete genome[title] or partial genome[title])",
        idtype="acc")
    record = Entrez.read(handle)
    return record


def get_ncov_list(record):
    """Get nCov list from ncbi search record"""
    ncov_acc_list = []
    for ncovaccid in record["IdList"]:
        ncov_acc_list.append(ncovaccid.split(".")[0])
    return ncov_acc_list


def read_input_csv(filename, intermediatedir):
    """ Read CSV input"""
    dis_amb_seq_file_path = os.path.join(intermediatedir, DISAMBSEQFILE)
    seq_dict = {}
    origin_seq_dict = {}
    input_csv = pd.read_csv(filename).drop("Lab", axis=1)
    for oligo in input_csv.values:
        seqname = oligo[0] + "_" + oligo[1].replace(' ', '')
        if oligo[1] == "Probe":
            origin_seq_dict.update({seqname: [None, "Probe", oligo[2]]})
        else:
            origin_seq_dict.update(
                {seqname: [oligo[1].split(".")[0], "Primer", oligo[2]]})
        disamb = disambiguate_seq(oligo[2])
        for k, disambseq in enumerate(disamb):
            seq_dict.update({f"{seqname}_D{k}": disambseq})

    with open(dis_amb_seq_file_path, "w") as dis_amb_seq:
        for oligoseqs in seq_dict:
            dis_amb_seq.writelines(">" + oligoseqs + "\n")
            dis_amb_seq.writelines(seq_dict[oligoseqs] + "\n")
    return seq_dict


def read_input_fasta(filename, intermediatedir):
    """ Read fasta input, fasta input does not contain orientation """
    dis_amb_seq_file_path = os.path.join(intermediatedir, DISAMBSEQFILE)
    seq_dict = {}
    oligolist = (SeqIO.parse(filename, format="fasta"))
    for oligo in oligolist:
        seqname = str(oligo.id).replace(' ', '')
        if "probe" in seqname.lower():
            origin_seq_dict.update({seqname: [None, "Probe", str(oligo.seq)]})
        else:
            origin_seq_dict.update({seqname: [None, "Primer", str(oligo.seq)]})
        seq_dict.update({f"{seqname}":oligo.seq})
        disamb = disambiguate_seq(str(oligo.seq))
        for k, disambseq in enumerate(disamb):
            seq_dict.update({f"{seqname}_D{k}": disambseq})

    with open(dis_amb_seq_file_path, "w") as dis_amb_seq_file:
        for oligoseqs in seq_dict:
            dis_amb_seq_file.writelines(">" + oligoseqs + "\n")
            dis_amb_seq_file.writelines(seq_dict[oligoseqs] + "\n")
    return seq_dict


def read_dis_amb_csv(filename, intermediatedir, run_all: bool=False):
    """ Read dis_amb_csv input"""
    dis_amb_seq_file_path = os.path.join(intermediatedir, DISAMBSEQFILE)
    seq_dict = {}
    origin_seq_dict = {}
    input_csv = pd.read_csv(filename)
    for idx, oligo in input_csv.iterrows():
        if oligo["Filters"] == "FAIL" and not run_all:
            continue
        seqname = oligo["ID"]
        seq_dict.update({f"{seqname}": oligo["Disambiguated Sequence"]})

    with open(dis_amb_seq_file_path, "w") as dis_amb_seq:
        for oligoseqs in seq_dict:
            dis_amb_seq.writelines(">" + oligoseqs + "\n")
            dis_amb_seq.writelines(seq_dict[oligoseqs] + "\n")
    return seq_dict

def blast_seqs(intermediatedir, blast_db_dir, number_of_threads):
    """ Blast Sequences, and store sequences to Padnas Dataframes """

    blast_reslut_path = os.path.join(intermediatedir, BLASTRESULTFILE)
    dis_amb_seq_file_path = os.path.join(intermediatedir, DISAMBSEQFILE)
    if blast_db_dir:
        os.system(f"blastn -task blastn-short -db {blast_db_dir}  -query \
                {dis_amb_seq_file_path} -max_target_seqs 5000 -qcov_hsp_perc 85 -dust no -evalue 100 \
            -outfmt \"10 qseqid sseqid pident length mismatch gapopen qstart qend \
            sstart send evalue bitscore qcovhsp qcov\" \
            -out  {blast_reslut_path}  -num_threads {number_of_threads}")
    else:
        os.system(f"blastn -task blastn-short -db nt -remote -query \
                {dis_amb_seq_file_path} -max_target_seqs 5000 -qcov_hsp_perc 85 -dust no -evalue 100 \
            -outfmt \"10 qseqid sseqid pident length mismatch gapopen qstart qend \
            sstart send evalue bitscore qcovhsp qcov\" \
            -out  {blast_reslut_path}")

def process_blast_results(filename):
    """Preprocess Blast result"""
    hittable = pd.read_csv(filename, header=None)
    clusters = list(set(list(hittable[0])))
    dfdic = {}
    for oligo in clusters:
        dfdic.update({oligo: hittable.loc[hittable[0] == oligo]})
    return dfdic, clusters


def blast_result_parsing(dfdic, seq_dict, clusters, ncov_acc_list, ncov_path):
    """Parse Blast Results"""
    ncov_records = list(SeqIO.parse(ncov_path, "fasta"))
    infodic = {}
    for oligo in clusters:
        ncov = []
        not_ncov = []
        temp = []
        mismatch_min = None
        mismatchlist = []
        for oligoinfo in list(dfdic[oligo].values):
            mismatch = len(seq_dict[oligo]) - oligoinfo[3] + oligoinfo[4]
            if mismatch == 0:
                locname = oligoinfo[1].split("|")[3].split(".")[0]
                if locname in ncov_acc_list:
                    ncov.append(locname)
                else:
                    temp.append(locname)
            elif mismatch > 0:
                mismatchlist.append(mismatch)
        if len(mismatchlist) > 0:
            mismatch_min = min(mismatchlist)
        if temp != []:
            for _ in range(20):
                try:
                    time.sleep(0.5)
                    handle1 = Entrez.esummary(db="nuccore", id=",".join(temp))
                except urllib.error.HTTPError:
                    # print("Network!")
                    continue
                break
            try:
                record1 = Entrez.read(handle1)
            except:
                logger.error("Error reading {} results from NCBI".format(oligo))
                logger.debug("{} is invalid nuccore request".format(temp))
                not_ncov = ["make this look like a bad sequence since we know nothing about it"]*1000
                break
                

            time.sleep(0.4)
            if len(temp) > len(record1):
                for k, rec in enumerate(record1):
                    if int(rec['TaxId']) == int(NCOVID):
                        ncov.append(temp[k])
                    else:
                        not_ncov.append((temp[k], int(rec['TaxId'])))
            else:
                for k, taxid in enumerate(temp):
                    if int(record1[k]['TaxId']) == int(NCOVID):
                        ncov.append(taxid)
                        if taxid not in ncov_acc_list:
                            ncov_acc_list.append(taxid)
                    else:
                        not_ncov.append((taxid, int(record1[k]['TaxId'])))

        infolist = [
            len(ncov) + len(not_ncov),
            len(ncov),
            len(not_ncov), not_ncov, mismatch_min
        ]
        infodic.update({oligo: infolist})

    for info in infodic:  #Add False Negative Judgement

        false_negative_cnt = 0
        for cov_seq in ncov_records:
            o_seq = seq_dict[info].upper()
            nc_seq = str(cov_seq.seq).upper()
            if (o_seq not in nc_seq) and (str(
                    Seq(o_seq).reverse_complement()) not in nc_seq):
                false_negative_cnt += 1
        false_negative_percent = (
            '%.3f%%' % (((false_negative_cnt / len(ncov_records))) * 100))
        sensitivity = ('%.3f%%' %
                       ((1 - (false_negative_cnt / len(ncov_records))) * 100))

        infodic[info] += [
            false_negative_cnt, false_negative_percent, sensitivity
        ]

    return infodic


def generate_report(infodic, seq_dict):
    """generate report as a pandas dataframe"""
    false_positive_report = pd.DataFrame(columns=[
        "ID", "Disambiguated Sequence",  "Length", "Total Match Number from blast",
        "nCoV Match Number from blast(Irrelevant)",
        "Not-nCov Match Number from blast(FP)", "Not-NCov Match List",
        "False Negative", "False Negative/Total nCoVSeqs",
        "Sensitivity(TP/FN+TP)"
    ])
    for info in infodic:
        false_positive_report = false_positive_report.append(
            pd.DataFrame({
                "ID": [info],
                "Disambiguated Sequence": [seq_dict[info]],
                "Length": [len(seq_dict[info])],
                "Total Match Number from blast": [infodic[info][0]],
                "nCoV Match Number from blast(Irrelevant)": [infodic[info][1]],
                "Not-nCov Match Number from blast(FP)": [infodic[info][2]],
                "Not-NCov Match List": [infodic[info][3]],
                "False Negative": [infodic[info][5]],
                "False Negative/Total nCoVSeqs": [infodic[info][6]],
                "Sensitivity(TP/FN+TP)": [infodic[info][7]]
            }))
    false_positive_report = false_positive_report.sort_values("ID")
    return false_positive_report


def generate_csv_report(false_positive_report, workdir):
    """Generate a CSV report"""
    false_positive_report.to_csv(os.path.join(workdir,
                                              "sensitivity-report.csv"))

# TODO add cutoffs
def generate_fasta_report(false_positive_report, config, run_all, workdir):
    """Generate a CSV report"""
    records_to_write = []
    fp_cutoff = config.getint("Sensitivity", "fp_cutoff")
    fn_cutoff = config.getint("Sensitivity", "fn_cutoff")
    for idx, oligo in false_positive_report.iterrows():
        if run_all or \
            (int(oligo["Not-nCov Match Number from blast(FP)"]) <= fp_cutoff and int(oligo["False Negative"]) <= fn_cutoff):
            records_to_write.append(SeqRecord(
                Seq(oligo["Disambiguated Sequence"]),
                description = oligo["ID"],
                name = oligo["ID"],
                id = oligo["ID"]))
    SeqIO.write(
        records_to_write, 
        os.path.join(workdir, "sensitivity-passed.fasta"), 
        "fasta")

def run(
        input_oligos: str, 
        output_dir: str, 
        ref_sequences: str,
        blastdb_path: str, 
        num_threads: int, 
        is_validated: bool,
        config,
        run_all: bool=False,
        email: str=None,
        api_key: str=None):
    if email:
        Entrez.email = email
    if api_key:
        Entrez.api_key = api_key
    if not email and not api_key:
        logger.critical("NCBI needs an email or API key")
        raise
    if is_validated:
        seq_dict = read_dis_amb_csv(input_oligos, output_dir, run_all)
    else:
        seq_dict = read_input_fasta(input_oligos, output_dir)
    if len(seq_dict) == 0:
        logger.critical("No sequences to run through blast!")
        return -1
    ncov_acc_list = get_ncov_list(get_ncbi_record())
    blast_seqs(output_dir, blastdb_path, num_threads)
    logger.info("Blast run has finished")
    dfdic, clusters = process_blast_results(
        os.path.join(output_dir, BLASTRESULTFILE))
    infodic = blast_result_parsing(
        dfdic, 
        seq_dict, 
        clusters, 
        ncov_acc_list,
        ref_sequences)
    false_positive_report = generate_report(infodic, seq_dict)
    generate_csv_report(false_positive_report, output_dir)
    false_positive_report = pd.read_csv(os.path.join(output_dir, "sensitivity-report.csv"))
    generate_fasta_report(false_positive_report, config, run_all, output_dir)
    return 0

def parse_args():
    """Parse all args"""
    parser = argparse.ArgumentParser(
        prog="OligoSensSpecCheck",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required_args = parser.add_argument_group("Required named args")

    required_args.add_argument("-s",
        "--oligos",
        help="path to the oligos file",
        type=str)
    required_args.add_argument(
        "-a",
        "--sequences",
        help="Path to all SARS-COV-2 sequence, in one file")
    required_args.add_argument(
        "-w",
        "--workdir",
        help="Folder of intermediate files, output csv will be at\
             [WORKDIR]/out/sensitivityreport.csv and Krona Plot\
             will be at [WORKDIR]/out/false_positive_taxonomy_distribution.html",
        default="work",
        type=str)
    ncbi_access = required_args.add_mutually_exclusive_group(required = True)
    ncbi_access.add_argument("-e",
                               "--email",
                               help="email for using Entrez",
                               type=str)
    ncbi_access.add_argument("-i",
                               "--api",
                               help="api key for using Entrez",
                               type=str)  
    optional_parameter_args = parser.add_argument_group("Optional parameters")
    optional_parameter_args.add_argument("-b",
                                         "--blast",
                                         help="path to blast result",
                                         type=str)
    optional_parameter_args.add_argument(
        "-d",
        "--blastdb",
        help="Directory of blast database, otherwise will use blast remote, \
            which have limitation of input sequence number",
        type=str)
    optional_parameter_args.add_argument("-f",
                            "--fasta",
                            help="Input file is fasta format",
                            action='store_false')
    optional_parameter_args.add_argument(
        "-v",
        "--validator",
        help="Take validator output as input, should ba a csv file",
        action='store_true')

    optional_parameter_args.add_argument(
        "-t",
        "--threads",
        default=32,
        help="Number of threads, mainly for blast",
        type=int)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    intermediatedir = args.workdir
    if not os.path.exists(intermediatedir):
        os.mkdir(intermediatedir)
    outdir = os.path.join(args.workdir, "out")

    if args.email:
        Entrez.email = args.email
    elif args.api:
        Entrez.api_key = args.api
    ncov_acc_list = get_ncov_list(get_ncbi_record())
    if args.validator:
        seq_dict = read_dis_amb_csv(args.oligos, intermediatedir)
    else:
        seq_dict = read_input_fasta(args.oligos, intermediatedir)
    # TODO when is this ever the input?
    # else:
        # seq_dict = read_input_csv(args.oligos, intermediatedir)
    if args.blast:
        dfdic, clusters = process_blast_results(args.blast)
    else:
        if args.blastdb:
            dfdic, clusters = blast_seqs(intermediatedir, args.blastdb,
                                         args.threads)
        else:
            dfdic, clusters = blast_seqs(intermediatedir, None, args.threads)

    infodic = blast_result_parsing(dfdic, seq_dict, clusters, ncov_acc_list,
                                   args.sequences)
    false_positive_report = generate_report(infodic, seq_dict)
    generate_csv_report(false_positive_report, outdir)
    # taxon_counter = false_positive_stat(intermediatedir, false_positive_report)
    # false_positive_stat(intermediatedir, false_positive_report)
    # generate_krona_html(intermediatedir, outdir)


if __name__ == "__main__":
    main()

