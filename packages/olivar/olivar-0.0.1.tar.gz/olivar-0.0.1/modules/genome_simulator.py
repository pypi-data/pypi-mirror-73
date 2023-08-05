'''simulate genomes based on read data set'''
import subprocess
import os
import argparse
import csv
from collections import defaultdict
import vcf
import pysam
import numpy as np
from Bio import SeqIO
from modules.utils import get_logger

logger = get_logger(__name__)

def simulate_consensus(sample_prefix, reference_file, output_dir):
    '''simulate consensus based on vcf file'''
    # vcf file zipping, indexing, and consensus generation
    subprocess.run([
            "bgzip",
            os.path.join(output_dir, 'filtered_vcf_files', f"{sample_prefix}.vcf"),
            '--force'],
        check=True)
    subprocess.run([
            "bcftools",
            "index",
            os.path.join(output_dir, 'filtered_vcf_files', f"{sample_prefix}.vcf.gz")],
        check=True)
    subprocess.run([
            "bcftools",
            "consensus",
            os.path.join(output_dir, "filtered_vcf_files", sample_prefix + ".vcf.gz"),
            "-f",
            reference_file,
            "-o",
            os.path.join(output_dir, "simulated_genomes", sample_prefix + ".fasta")],
        stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
        stderr=open(os.path.join(output_dir, "simulation.err"), "a"),
        check=True)
    # unzip vcf file
    subprocess.run([
            "bgzip",
            "-d",
            os.path.join(output_dir, 'filtered_vcf_files', f"{sample_prefix}.vcf.gz")],
        check=True)

def vcf_split(sample, reference_file, output_dir):
    '''split vcf file into multiple if different alt at same position'''
    def write_vcf_flies():
        for record in vcf_reader:
            if len(record_dict[record.POS]) == 1:
                vcf_writer.write_record(record)
            else:
                try:
                    if record_dict[record.POS][i] == record.ALT:
                        vcf_writer.write_record(record)
                except IndexError:
                    continue

        vcf_writer.close()
        simulate_consensus(f'{sample}_{i}', reference_file, output_dir)

    vcf_reader = vcf.Reader(
        filename=os.path.join(output_dir, "filtered_vcf_files", f"{sample}.vcf"))
    record_dict = defaultdict(list)

    for record in vcf_reader:
        record_dict[record.POS].append(record.ALT)

    if bool(record_dict):
        max_alt = len(max(record_dict.values(), key=len))
        if max_alt == 1:
            simulate_consensus(sample, reference_file, output_dir)
        elif max_alt > 1:
            for i in range(max_alt):
                prefix = os.path.join(output_dir, "filtered_vcf_files", f"{sample}")
                vcf_writer = vcf.Writer(open(f'{prefix}_{i}.vcf', 'w'), vcf_reader)
                vcf_reader = vcf.Reader(filename=f'{prefix}.vcf')
                write_vcf_flies()

def parse_metadata(csv_file):
    '''parse the metadata csv file'''
    sample_dict = dict()
    with open(csv_file, "r") as metadata_file:
        record_dict = csv.DictReader(metadata_file)
        for row in record_dict:
            sample_dict[row['Run']] = [row['LibraryLayout'], row['Platform']]
    return sample_dict

def bowtie2_index(reference_file, output_dir):
    '''create bowtie2 index'''
    bowtie_output_dir = os.path.join(output_dir, "bowtie2_ref_index")
    if not os.path.exists(bowtie_output_dir):
        os.mkdir(bowtie_output_dir)

    # build bowtie2 reference index
    subprocess.run([
            "bowtie2-build",
            "--quiet",
            reference_file,
            os.path.join(bowtie_output_dir, "reference")],
        stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
        stderr=open(os.path.join(output_dir, "simulation.err"), "a"),
        check=True)

def read_mapping(sample_metadata, read_dir, reference_file, output_dir, num_cores):
    '''map the read to the reference'''
    sam_output_dir = os.path.join(output_dir, "sam_files")
    bam_output_dir = os.path.join(output_dir, "bam_files")
    if not os.path.exists(sam_output_dir):
        os.mkdir(sam_output_dir)

    mapped_list = []

    # TODO ERROR CHECK
    for sample in sample_metadata:
        platform = sample_metadata[sample][1]
        layout = sample_metadata[sample][0]
        if platform == "OXFORD_NANOPORE" \
            and os.path.exists(os.path.join(read_dir, sample, f"{sample}.fastq")):
            with open(os.path.join(output_dir, "simulation.log"), "a") as log:
                log.write(f"{sample}\t{platform}\t{layout}")
            subprocess.run([
                    "minimap2",
                    "-ax",
                    "map-ont",
                    reference_file,
                    os.path.join(read_dir, sample, f"{sample}.fastq"),
                    "--sam-hit-only",
                    "-o", os.path.join(sam_output_dir, f"{sample}.sam")],
                stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
                stderr=open(os.path.join(output_dir, "simulation.err"), "a"),
                check=True)
            mapped_list.append(sample)
        else:
            if layout == "PAIRED" and \
                    os.path.exists(os.path.join(read_dir, sample, f"{sample}_1.fastq")) \
                    and os.path.exists(os.path.join(read_dir, sample, f"{sample}_1.fastq")):
                with open(os.path.join(output_dir, "simulation.log"), "a") as log:
                    log.write(f"{sample}\t{platform}\t{layout}")
                subprocess.run([
                        "bowtie2",
                        "-p", str(num_cores),
                        "--local",
                        "--quiet",
                        "--no-unal",
                        "-x", os.path.join(output_dir, "bowtie2_ref_index", "reference"),
                        "-1", os.path.join(read_dir, sample, f"{sample}_1.fastq"),
                        "-2", os.path.join(read_dir, sample, f"{sample}_2.fastq"),
                        "-S", os.path.join(sam_output_dir, f"{sample}.sam")],
                    stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
                    stderr=open(os.path.join(output_dir, "simulation.err"), "a"),
                    check=True)
                mapped_list.append(sample)
            if layout == "SINGLE" and os.path.exists(f"{read_dir}/{sample}/{sample}.fastq"):
                logger.info(f"{sample}, {platform}, {layout}")
                subprocess.run([
                        "bowtie2",
                        "-p", str(num_cores),
                        "--local",
                        "--quiet",
                        "-x", os.path.join(output_dir, "bowtie2_ref_index", "reference"),
                        "-U", os.path.join(read_dir, sample, f"{sample}.fastq"),
                        "-S", os.path.join(sam_output_dir, f"{sample}.sam")],
                    stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
                    stderr=open(os.path.join(output_dir, "simulation.err"), "a"),
                    check=True)
                mapped_list.append(sample)

    return mapped_list

def variant_call(mapped_list, reference_file, output_dir, min_af_threshold, num_cores):
    '''variant calling using loFreq'''
    bam_files = os.path.join(output_dir, "bam_files")
    sam_files = os.path.join(output_dir, "sam_files")
    vcf_files = os.path.join(output_dir, "vcf_files")
    filtered_vcf_files = os.path.join(output_dir, "filtered_vcf_files")
    if not os.path.exists(bam_files):
        os.mkdir(bam_files)
    if not os.path.exists(vcf_files):
        os.mkdir(vcf_files)
    if not os.path.exists(filtered_vcf_files):
        os.mkdir(filtered_vcf_files)

    for sample in mapped_list:
        # covert sam file to binary bam file
        subprocess.run([
            "samtools",
            "view",
            "-bS", os.path.join(sam_files, f"{sample}.sam"),
            "-o", os.path.join(bam_files, f"{sample}.bam")])
        # sort the bam file for variant caller
        subprocess.run([
            "samtools",
            "sort",
            "-o", os.path.join(bam_files, f"{sample}_sort.bam"),
            "-O", "BAM", os.path.join(bam_files, f"{sample}.bam")])
        subprocess.run([
            "samtools",
            "index",
            os.path.join(bam_files, f"{sample}_sort.bam")])
        # Lofreq is used as variant caller, outputs in .vcf
        if os.path.exists(os.path.join(vcf_files, f"{sample}.vcf")):
            os.remove(os.path.join(vcf_files, f"{sample}.vcf"))
        subprocess.run([
                "lofreq",
                "call-parallel",
                "--pp-threads", str(num_cores),
                "--call-indels",
                "-f", f"{reference_file}",
                "-o",
                os.path.join(vcf_files, f"{sample}.vcf"),
                os.path.join(bam_files, f"{sample}_sort.bam")],
            stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
            stderr=open(os.path.join(output_dir, "simulation.err"), "a"))
        # additional filter to remove variants with low AF
        if os.path.exists(os.path.join(filtered_vcf_files, f"{sample}.vcf")):
            os.remove(os.path.join(filtered_vcf_files, f"{sample}.vcf"))
        subprocess.run([
                "lofreq",
                "filter",
                "-a",
                f"{min_af_threshold}",
                "-i",
                os.path.join(vcf_files, f"{sample}.vcf"),
                "-o",
                os.path.join(filtered_vcf_files, f"{sample}.vcf")],
            stdout=open(os.path.join(output_dir, "simulation.log"), "a"),
            stderr=open(os.path.join(output_dir, "simulation.err"), "a"))

def simulate_genomes(mapped_list, reference_file, output_dir):
    '''simulate genomes in the list'''
    if not os.path.exists(os.path.join(output_dir, "simulated_genomes")):
        os.mkdir(os.path.join(output_dir, "simulated_genomes"))
    for sample in mapped_list:
        vcf_split(sample, reference_file, output_dir)

def mapping_coverage(sample_name, reference_file, output_dir, quality_threshold=0):
    '''calculate mapping coverage'''
    samfile = pysam.AlignmentFile(
        os.path.join(output_dir, "bam_files", f"{sample_name}_sort.bam"), "rb")

    unmapped_count = 0

    ref = SeqIO.read(reference_file, "fasta").seq
    chromosome = SeqIO.read(reference_file, "fasta").id

    pileupcolumns = samfile.pileup(chromosome)
    consensus_coverage = np.zeros(len(ref))

    for pileupcolumn in pileupcolumns:
        pileupcolumn.set_min_base_quality(quality_threshold)
        max_count = 0
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                max_count += 1

        consensus_coverage[pileupcolumn.reference_pos] = max_count

    for pileupcolumn in samfile.pileup(chromosome):
        index = pileupcolumn.reference_pos
        if consensus_coverage[index] == 0:
            unmapped_count += 1

    samfile.close()
    return 1-unmapped_count/len(ref)

def remove_duplicates_multi_fasta(genome_dir, output_dir):
    '''remove duplicate sequences and generate multi fasta file'''
    genome_list = os.listdir(genome_dir)
    genome_set = set()
    duplicate_removed_records = []

    for genome in genome_list:
        record = SeqIO.read(f"{genome_dir}/{genome}", "fasta")
        record.id = genome + " " + record.id
        if record.seq not in genome_set:
            genome_set.add(record.seq)
            duplicate_removed_records.append(record)

    logger.info("Total number of genomes: {}".format(len(duplicate_removed_records)))
    SeqIO.write(
        duplicate_removed_records, os.path.join(output_dir, "simulated_genomes.fasta"), "fasta")

def mapping_quality_check(mappings, reference_file, output_dir, coverage_threshold=0.5, min_base_quality=0):
    '''check mapping quality based on sam file'''
    filtered_mappings = []

    for sample in mappings:
        if mapping_coverage(sample, reference_file, output_dir, min_base_quality) > coverage_threshold:
            filtered_mappings.append(sample)

    return filtered_mappings

def simulate(
        csv_file: str,
        reference_file: str,
        read_dir: str,
        output_dir: str,
        coverage_threshold: float,
        min_base_quality: int,
        min_af_threshold: float,
        threads: int):
    sample_metadata = parse_metadata(csv_file)
    subprocess.run(["samtools", "faidx", reference_file],
                    check=True,
                    stdout=open(os.path.join(output_dir, "simulation.log"), "w"),
                    stderr=open(os.path.join(output_dir, "simulation.err"), "w"))
    bowtie2_index(reference_file, output_dir)
    mappings = read_mapping(sample_metadata, read_dir, reference_file, output_dir, threads)
    variant_call(mappings, reference_file, output_dir, min_af_threshold, threads)
    filtered_mappings = mapping_quality_check(mappings, reference_file, output_dir, coverage_threshold, min_base_quality)
    simulate_genomes(filtered_mappings, reference_file, output_dir)

def main():
    '''main function'''
    parser = argparse.ArgumentParser(description="Genome simulator")
    parser.add_argument("csv", type=str, help="input matadata in csv format")
    parser.add_argument("reference", type=str, help="input reference genome in fasta format")
    parser.add_argument("readdir", type=str, help="input dir that stores the read datasets")
    parser.add_argument("-o", "--output", type=str, help="Output directory")
    parser.add_argument("-c", "--coveragethreshold", type=float, default=0.5,
        help="input coverage threshold, mappings above the threshold would be \
        taken into consideration for generating simulated genome")
    parser.add_argument("-m", "--minbasequality", type=int, default=0,
        help="input min base quality, bases with quality above this threshold \
        would be takin into consideration during mapping quality check")
    parser.add_argument("--min-af-threshold", type=float, default=0.01,
        help="Minimum allele frequency threshold, variants with allele frequency \
        above this threshold would be used to simulate genomes.")
    parser.add_argument("-t", "--threads", type=int, default=3,
        help="Default number of threads to use")
    args = parser.parse_args()

    csv_file = args.csv
    reference_file = args.reference
    read_dir = args.readdir
    coverage_threshold = args.coveragethreshold
    min_base_quality = args.minbasequality
    min_af_threshold = args.min_af_threshold
    threads = args.threads
    simulate(
        csv_file,
	reference_file,
	read_dir,
	args.output,
	coverage_threshold,
	min_base_quality,
	min_af_threshold,
	threads)

if __name__ == "__main__":
    main()
