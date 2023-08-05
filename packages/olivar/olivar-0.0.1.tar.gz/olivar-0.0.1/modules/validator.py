# Standard library imports
import argparse
import logging
import os
import subprocess
import random
import configparser
from collections import defaultdict
import json
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support
# Biopython imports
from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
# Other 3rd party imports
import pandas as pd
from tqdm import tqdm
# Local imports
import modules.parameter_checks as prc
from modules.utils import disambiguate_seq, get_logger, UNAMBIG_LIMIT

logger = get_logger(__name__)

def fill_in_seqeunces(seqs, report):
    """ Returns a Pandas DataFrame with oligos added."""
    logger.info("Filling in sequences...")
    rows = []
    for idx, seq in enumerate(seqs):
        if seq.id.count("_") != 2:
            logger.error(f"Improperly formatted sequence {seq.id}")
            continue
        name, seq_type, orientation = seq.id.split("_")
        unambig_seqs = disambiguate_seq(str(seq.seq))
        for i, unambig_seq in enumerate(random.sample(unambig_seqs,
                                                      min(len(unambig_seqs), UNAMBIG_LIMIT))):
            unambig_id = f"{seq.id}_D{i}"
            d = dict.fromkeys(list(report.columns))
            d.update({"ID": unambig_id, "Group": name.split(":")[0],
                                    "Disambiguated Sequence": unambig_seq,
                                    "Original Sequence": str(seq.seq), "Type": seq_type,
                                    "Orientation": orientation, "Length": len(seq.seq),
                                    "Tm": 0.0, "Failed Tests": ""})

            rows.append(d)
    report = pd.DataFrame(rows)
    logger.info("Validating {} sequences...".format(len(report.index)))
    return report.set_index("ID")

def evaluate_mono_homomers(report, min_count=3, num_threads=1):
    """ Adds annotated sequences with monohomomer stretches marked."""
    with Pool(num_threads) as pool:
        mono_ret = pool.map(
            partial(prc.evaluate_mono_homomers, min_count=min_count),
            [entry[1]["Disambiguated Sequence"] for entry in report.iterrows()])
    for idx, (subseqs, max_subseq_length) in enumerate(mono_ret):
        report.iloc[idx, report.columns.get_loc("Monohomomers")] = "".join(subseqs)
        report.iloc[idx, report.columns.get_loc("Max_Mono_Length")] = max_subseq_length
        if max_subseq_length >= min_count:
            report.iloc[idx, report.columns.get_loc("Failed Tests")] += "Monohomomers|"
    return report

def evaluate_tm(report, dna_conc, single_ion_conc, double_ion_conc, dntps_conc, num_threads=1):
    """ Evaluates melting temperatures using oligotm from Primer 3."""
    with Pool(num_threads) as pool:
        tm_ret = pool.map(partial(prc.evaluate_tm, 
                dna_conc=dna_conc,
                single_ion_conc=single_ion_conc,
                double_ion_conc=double_ion_conc,
                dntps_conc=dntps_conc),
            [entry[1]["Disambiguated Sequence"] for entry in report.iterrows()])
    report["Tm"] = tm_ret
    return report

def evaluate_self_dimers_ANY(report, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):
    """ Determines self-dimer potential for the oligos."""
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        completed_process = prc.evaluate_self_ntthal(seq, dna_conc, single_ion_conc, 
                                                     double_ion_conc, dntps_conc, "ANY")
        report.loc[entry[0], "Self_dimers_ANY"] = completed_process
        info = completed_process.split('\n')[0]
        dG = info.split('\t')[3]
        dGvalue = float(dG.split('=')[1].rstrip())
        report.loc[entry[0], "dG_ANY"] = dGvalue
    return report

def evaluate_self_dimers_END(report, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):
    """ Determines self-dimer potential for the oligos."""
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        completed_process = prc.evaluate_self_ntthal(seq, dna_conc, single_ion_conc, 
                                                     double_ion_conc, dntps_conc, "END1")
        report.loc[entry[0], "Self_dimers_END1"] = completed_process
    return report

def evaluate_hairpins(report, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):
    """ Determines hairpin potential for the oligos."""
    logger.info("Checking for hairpins...")
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        completed_process = prc.evaluate_self_ntthal(seq, dna_conc, single_ion_conc, 
                                                     double_ion_conc, dntps_conc, "HAIRPIN")
        report.loc[entry[0], "Hairpins"] = completed_process
        if completed_process == "No secondary structure could be calculated\n":
            dGvalue = 1000000
        else:
            info = completed_process.split('\n')[0]
            dG = info.split('\t')[4]
            dGvalue = float(dG.split('=')[1].rstrip())
        report.loc[entry[0], "dG_HAIRPIN"] = dGvalue
    return report

def evaluate_gc_content(report):
    '''validate the gc content for the given seq'''
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        report.loc[entry[0], "GC"] = round(GC(seq), 2)
    return report

def evaluate_5_end_probe(report):
    '''validate if the probes violate the rule that avoid G at 5' end'''
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        if entry[0].split("_")[1] == "Probe" and seq[0] != "G":
            report.loc[entry[0], "Avoid_G_at_5\'"] = "TRUE"
        elif entry[0].split("_")[1] == "Probe":
            report.loc[entry[0], "Avoid_G_at_5\'"] = "FALSE"
    return report

def evaluate_primer_gc_clamp(report):
    '''validate the number of G or C at 3' end of the primers'''
    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        if entry[0].split("_")[1] == "Primer":
            report.loc[entry[0], "#GC_at_3\'"] = seq[-5:].count("G") + \
                                                    seq[-5:].count("C")
    return report

def evaluate_dinucleotide_repeats(report):
    '''evaluate the dinucleotide repeats within the sequence'''
    def dinucleotide_repeats(seq, index_shift):
        '''check dinucleotide repeats at even position'''
        dinucleotide_copies = ""
        start_pos = 0
        count = 1
        dinucleotide = ""
        for i in range(0, int(len(seq)/2)-1, 2):
            if seq[i:i+2] == seq[i+2:i+4] and count == 1:
                start_pos = i
                dinucleotide = seq[i:i+2]
                count += 1
            elif seq[i:i+2] == seq[i+2:i+4]:
                count += 1
            elif count > 1 and dinucleotide[0] != dinucleotide[1]:
                dinucleotide_copies += f"{start_pos+index_shift},{count},{dinucleotide}|"
                count = 1
                dinucleotide = ""
            else:
                count = 1
                dinucleotide = ""
        return dinucleotide_copies

    for entry in report.iterrows():
        seq = entry[1]["Disambiguated Sequence"]
        report.loc[entry[0], "Dinucleotide Repeats"] = dinucleotide_repeats(seq, 0) + \
                                                          dinucleotide_repeats(seq[1:], 1)
    return report

def in_range(val, min, max):
    '''reture ture if value is in range between min and max'''
    if val <= max and val >= min:
        return True
    else:
        return False

def gc_test(report, primer_min, primer_max, probe_min, probe_max):
    '''Filter probes/primers by gc content, probes/primers failed the test would be marked'''

    for index, entry in report.iterrows():
        if entry["Type"] == "Primer" and not in_range(entry["GC"], primer_min, primer_max):
            report.loc[index, "Failed Tests"] += "GC|"
        if entry["Type"] == "Probe" and not in_range(entry["GC"], probe_min, probe_max):
            report.loc[index, "Failed Tests"] += "GC|"
    return report

def tm_test(report, primer_min, primer_max, probe_min, probe_max):
    '''Filter probes/primers by Tm, probes/primers failed the test would be marked'''
    for index, entry in report.iterrows():
        if entry["Type"] == "Primer" and not in_range(entry["Tm"], primer_min, primer_max):
            report.loc[index, "Failed Tests"] += "Tm|"
        if entry["Type"] == "Probe" and not in_range(entry["Tm"], probe_min, probe_max):
            report.loc[index, "Failed Tests"] += "Tm|"
    return report

def length_test(report, primer_min, primer_max, probe_min, probe_max):
    '''Filter probes/primers by length, probes/primers failed the test would be marked'''
    for index, entry in report.iterrows():
        if entry["Type"] == "Primer" and not in_range(entry["Length"], primer_min, primer_max):
            report.loc[index, "Failed Tests"] += "Length|"
        if entry["Type"] == "Probe" and not in_range(entry["Length"], probe_min, probe_max):
            report.loc[index, "Failed Tests"] += "Length|"
    return report

def sequence_ends_tests(report, check_5_end, min_GC_3_end, max_GC_3_end):
    for index, entry in report.iterrows():
        if entry["Type"] == "Probe" and entry["Avoid_G_at_5\'"] == "FALSE" and check_5_end:
            report.loc[index, "Failed Tests"] += "G_at_5'|"
        if entry["Type"] == "Primer" and not in_range(entry["#GC_at_3'"], min_GC_3_end, max_GC_3_end):
            report.loc[index, "Failed Tests"] += "#GC_at_3'|"
    return report

def filter_summary(report):
    for index, entry in report.iterrows():
        if entry["Failed Tests"] == "":
            report.loc[index, "Filters"] = "PASS"
        else:
            report.loc[index, "Filters"] = "FAIL"
    return report

def primer_cross_dimer_check(report, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):    
    groups = report.Group.unique()
    report_F_v_R = {group: None for group in groups}
    logger.info("Checking for cross dimers...")
    for group in groups:
        group_primers_R = report.loc[(report["Group"] == group) & (report["Type"] == "Primer") & \
                                     (report["Orientation"] == "F")]
        group_primers_F = report.loc[(report["Group"] == group) & (report["Type"] == "Primer") & \
                                     (report["Orientation"] == "R")]
        if group_primers_F.empty or group_primers_R.empty:
            report_F_v_R[group] = pd.DataFrame()
        else:
            table = pd.DataFrame(columns=["Group", "Primer_F", "Primer_R", "dG", "Filters"])                          
            for i, primer_F in group_primers_F.iterrows():
                if primer_F["Filters"] != "PASS":
                    continue
                # with Pool() as pool:
                    # ret = pool.map(partial(evaluate_dimers_ANY,
                        # seq2=primer_F["Disambiguated Sequence"],
                        # dna_conc=dna_conc,
                        # single_ion_conc=single_ion_conc,
                        # double_ion_conc=double_ion_conc,
                        # dntps_conc=dntps_conc),
                        # [primer_R["Disambiguated Sequence"] 
                            # for _, primer_R in group_primers_R.iterrows() if primer_R["Filters"] == "PASS"])
                # hack_idx = 0
                # for j, primer_R in group_primers_R.iterrows():
                    # if primer_R["Filters"] != "PASS":
                        # continue
                    # table = table.append([[group, i, j, ret[hack_idx][1]]], ignore_index=True)
                    # hack_idx += 1
                    output, dG = evaluate_dimers_ANY(primer_F["Disambiguated Sequence"],
                                                     primer_R["Disambiguated Sequence"],
                                                     dna_conc, single_ion_conc, 
                                                     double_ion_conc, dntps_conc)
                    table = table.append([[group, i, j, dG]], ignore_index=True)
            report_F_v_R[group] = table
    return report, report_F_v_R

def run(oligos, output_dir, config, cross_check=False, num_threads=1):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    oligos = list(SeqIO.parse(oligos, "fasta"))
    oligo_report = pd.DataFrame(columns=[
        "ID", "Group", "Disambiguated Sequence", 
        "Original Sequence", "Type", "Orientation", "Length",
        "Tm", "Monohomomers", "Max_Mono_Length", 
        "Self_dimers_ANY", "Self_dimers_END1", "Self_dimers_END2",
        "dG_ANY", "dG_END1", "dG_END2", "dG_HAIRPIN"
        "Hairpins", "GC", "Avoid_G_at_5\'", "#GC_at_3\'", 
        "Dinucleotide Repeats", "Failed Tests", "Filters"])

    oligo_report = fill_in_seqeunces(oligos, oligo_report)
    oligo_report = evaluate_tm(
        oligo_report,
        config.getfloat("Chemistry", "DNA_conc_nano"), 
        config.getfloat("Chemistry", "Single_ion_con_milli"),
        config.getfloat("Chemistry", "Double_ion_con_milli"), 
        config.getfloat("Chemistry", "dNTPs_con_milli"),
        num_threads)
    oligo_report = evaluate_mono_homomers(
        oligo_report, 
        config.getint("Other", "homomonomer_min_count"),
        num_threads)
    oligo_report = evaluate_self_dimers_ANY(
        oligo_report,
        config.getfloat("Chemistry", "DNA_conc_nano"), 
        config.getfloat("Chemistry", "Single_ion_con_milli"),
        config.getfloat("Chemistry", "Double_ion_con_milli"), 
        config.getfloat("Chemistry", "dNTPs_con_milli"))
    oligo_report = evaluate_self_dimers_END(
        oligo_report,
        config.getfloat("Chemistry", "DNA_conc_nano"), 
        config.getfloat("Chemistry", "Single_ion_con_milli"),
        config.getfloat("Chemistry", "Double_ion_con_milli"), 
        config.getfloat("Chemistry", "dNTPs_con_milli"))
    oligo_report = evaluate_hairpins(
        oligo_report,
        config.getfloat("Chemistry", "DNA_conc_nano"), 
        config.getfloat("Chemistry", "Single_ion_con_milli"),
        config.getfloat("Chemistry", "Double_ion_con_milli"), 
        config.getfloat("Chemistry", "dNTPs_con_milli"))
    oligo_report = evaluate_gc_content(oligo_report)
    oligo_report = evaluate_5_end_probe(oligo_report)
    oligo_report = evaluate_primer_gc_clamp(oligo_report)
    oligo_report = evaluate_dinucleotide_repeats(oligo_report)

    oligo_report = gc_test(
        oligo_report, 
        config.getfloat("Primer", "GC_min"), config.getfloat("Primer", "GC_max"),
        config.getfloat("Probe", "GC_min"), config.getfloat("Probe", "GC_max"))
    # TODO just do this in the tm calculation function
    oligo_report = tm_test(
        oligo_report, 
        config.getfloat("Primer", "Tm_min"), config.getfloat("Primer", "Tm_max"),
        config.getfloat("Probe", "Tm_min"), config.getfloat("Probe", "Tm_max"))
    # oligo_report = length_test(oligo_report, 
        # config.getfloat("Primer", "Length_min"), config.getfloat("Primer", "Length_max"),
        # config.getfloat("Probe", "Length_min"), config.getfloat("Probe", "Length_max"))
    oligo_report = sequence_ends_tests(oligo_report, 
        config.getboolean("Probe", "check_G_at_5_end"),
        config.getint("Primer", "min_GC_at_3_end"), config.getint("Primer", "max_GC_at_3_end"))
    oligo_report = filter_summary(oligo_report)

    oligo_report.to_csv(os.path.join(output_dir, "validator-report.csv"))
    passed_oligos_records = []
    for idx, row in pd.read_csv(os.path.join(output_dir, "validator-report.csv")).iterrows():
        if row["Filters"] == "PASS":
            passed_oligos_records.append(SeqRecord(
                Seq(row["Disambiguated Sequence"]),
                description=row["ID"],
                name=row["ID"],
                id=row["ID"]))

    SeqIO.write(passed_oligos_records, os.path.join(output_dir, "validator-passed.fasta"), "fasta")

    # logger.info(oligo_report)
    if cross_check:
        oligo_report, report_F_v_R = primer_cross_dimer_check(
            oligo_report,
            config.getfloat("Chemistry", "DNA_conc_nano"), 
            config.getfloat("Chemistry", "Single_ion_con_milli"),
            config.getfloat("Chemistry", "Double_ion_con_milli"), 
            config.getfloat("Chemistry", "dNTPs_con_milli"))
        report_F_v_R = pd.concat(report_F_v_R.values(), keys=report_F_v_R.keys(), sort=False)
        report_F_v_R.to_csv(os.path.join(output_dir, "validator-FvR.csv"))

def main():
    """ Main script that runs all evaluations and aggreagtes results into a report."""
    parser = argparse.ArgumentParser(prog="OligoValidator",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required_args = parser.add_argument_group("Required named args")
    required_args.add_argument("-s", "--oligos", help="path to the oligos FASTA file", type=str)
    required_args.add_argument("-o", "--output", help="Prefix to the output file. Output file \
                                                       will be at [PREFIX]-report.csv",
                               default="out", type=str)
    required_args.add_argument("-c", "--config", help="path to the configuration file", 
                               type=str, default="data/config.ini")

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)
    run(args.oligos, args.output, config)

if __name__ == "__main__":
    main()

