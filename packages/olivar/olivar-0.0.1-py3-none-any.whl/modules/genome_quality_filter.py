'''filter genomes based on quality of the sequence'''
import os
import argparse
import logging
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support

from Bio import SeqIO
from Bio import Align
from Bio.SubsMat.MatrixInfo import blosum62


VERBOSITY = logging.INFO
logger = logging.getLogger("Quality Filter")
logger.setLevel(VERBOSITY)
ch = logging.StreamHandler()
ch.setLevel(VERBOSITY)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def count_n(seq):
    '''count the number of Ns in a sequence, as well as the maximum number of contiguous Ns'''
    total_n = 0
    contiguous_n = 0
    max_contiguous_n = 0
    for base in seq:
        if base in ('N', 'n'):
            total_n += 1
            contiguous_n += 1
            if contiguous_n > max_contiguous_n:
                max_contiguous_n = contiguous_n
        else:
            contiguous_n = 0
    return max_contiguous_n, total_n

def is_length_valid(reference, record, threshold):
    ''' return if the length of the genome is valid '''
    return  len(reference.seq)-threshold <= len(record.seq) <= len(reference.seq)+threshold

def is_pairwise_aligned(reference, record, end_cutoff):
    '''remove any sequence with insertions, deletions, and ambiguous base in core region'''
    # initialize pair-wise aligner parameters
    aligner = Align.PairwiseAligner()
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -0.5
    aligner.extend_gap_score = -0.1
    aligner.target_end_gap_score = 0.0
    aligner.query_end_gap_score = 0.0
    aligner.mode = 'global'

    def check_forward_reverse(aligner, reference, query_seq, end_cutoff):
        alignments = aligner.align(reference.seq, query_seq)
        alignment = format(alignments[0]).strip().split("\n") # first alignment
        aligned_reference = alignment[0]
        aligned_query = alignment[-1]

        is_filter_passed = True
        # - in reference genome indicates insertion
        if '-' in aligned_reference[end_cutoff:len(aligned_reference)-end_cutoff]:
            is_filter_passed = False
        # - in query genome indicates deletion
        if '-' in aligned_query[end_cutoff:len(aligned_query)-end_cutoff] or\
               'n' in aligned_query[end_cutoff:len(aligned_query)-end_cutoff] or\
               'N' in aligned_query[end_cutoff:len(aligned_query)-end_cutoff]:
            is_filter_passed = False
        return is_filter_passed

    try:
        return check_forward_reverse(aligner, reference, record.seq.upper(), end_cutoff) \
               or check_forward_reverse(aligner, reference, record.seq.reverse_complement().upper(), end_cutoff)
    except ValueError as e:
        bad_letters = set(list(record.seq)) - set(["A", "T", "G", "C"])
        logger.error(f"\n\tSequence {record.id} contains letters not in the alphabet. Filtering it out")
        logger.error(f"\n\tBad letters: {', '.join(bad_letters)}")
        return False

def pass_filter(genome, reference, end_cutoff, contiguous_n_threshold, total_n_threshold, length_threshold):
    record = SeqIO.read(genome, "fasta")
    max_contiguous_n, total_n = count_n(record.seq)
    bad_letters = set(list(record.seq)) - set(["A", "T", "G", "C", "N", "a", "t", "g", "c", "n"])
    return max_contiguous_n < contiguous_n_threshold and total_n <= total_n_threshold \
            and len(bad_letters) == 0 \
            and is_length_valid(reference, record, length_threshold) \
            and is_pairwise_aligned(reference, record, end_cutoff)

def filter_genome(genome_list, reference, output_dir, simulated_genome_dir=None, contiguous_n_threshold=20, \
    total_n_threshold=30, length_threshold=145, end_cutoff=200, num_threads=1):
    '''filtering genome by contiguous number of Ns in the sequence and the ratio of total_n/len(seq)
    If simulated genomes are taken into consideration, pass simulated_genome_dir as a parameter
    all filtered genomes are combined into a multi-fasta file with duplicates removed'''

    # genome_list = [os.path.join(genome_dir, g) for g in os.listdir(genome_dir)]
    genome_set = set()
    filtered_genome_list = []
    masked_genome_list = []
    with Pool(num_threads) as pool:
        is_passed_ret = pool.map(partial(pass_filter, 
                reference=reference, 
                end_cutoff=end_cutoff, 
                contiguous_n_threshold=contiguous_n_threshold, 
                total_n_threshold=total_n_threshold,
                length_threshold=length_threshold), 
            genome_list)

    for idx, genome in enumerate(genome_list):
        record = SeqIO.read(genome, "fasta")
        if is_passed_ret[idx] and record.seq not in genome_set:
            genome_set.add(record.seq)
            record.id = record.description.replace("-", "_").replace(" ","_")
            record.name = ""
            record.description = ""
            filtered_genome_list.append(record)
        else:
            masked_genome_list.append(genome)

    #logging information of thresholds used and the marked sequences
    with open(os.path.join(output_dir, "quality_check.log"), "w") as quality_check_log:
        quality_check_log.write(f"contiguous_n_threshold: {contiguous_n_threshold}\n")
        quality_check_log.write(f"total_n_threshold: {total_n_threshold}\n")
        quality_check_log.write("masked_genomes\n")
        quality_check_log.write("\n".join(masked_genome_list))

    if simulated_genome_dir is not None:
        simulated_genome_list = []
        simulated_genome_files = os.listdir(simulated_genome_dir)

        for genome_file in simulated_genome_files:
            record = SeqIO.read(os.path.join(simulated_genome_dir, genome_file), "fasta")
            record.id = genome_file + " " + record.id
            if record.seq not in genome_set:
                genome_set.add(record.seq)
                simulated_genome_list.append(record)

    logger.info("Total number of unsimulated filtered genomes: {}".format(str(len(filtered_genome_list))))
    #  TODO somehow describe that file contains simulated
    SeqIO.write(
        filtered_genome_list, 
        os.path.join(output_dir, "filtered_genomes.fasta"), 
        "fasta")
    all_genomes = filtered_genome_list
    if simulated_genome_dir:
        logger.info("Total number of simulated genomes: {}".format(len(simulated_genome_list)))
        all_genomes += simulated_genome_list
        SeqIO.write(
            simulated_genome_list + filtered_genome_list, 
            os.path.join(output_dir, "filtered_genomes_wsim.fasta"), 
            "fasta")
    if not os.path.exists(os.path.join(output_dir, "filtered_genomes")):
        os.mkdir(os.path.join(output_dir, "filtered_genomes"))
    for idx, genome in enumerate(all_genomes):
        SeqIO.write(genome, os.path.join(output_dir, "filtered_genomes", f"{idx}.fasta"), "fasta")

def main():
    '''main function of the script'''
    parser = argparse.ArgumentParser(description="Genome quality filter")
    parser.add_argument("genomes", type=str, help="input dir that stores the downloaded genomes")
    parser.add_argument("reference", type=str, help="reference genome in fasta format")
    parser.add_argument("-s", "--simulated-dir", type=str,
        help="optional: input dir that stores the simulated genomes")
    parser.add_argument("-c", "--contiguous-n", type=int, default=20,
        help="contiguous N threshold, sequences with number of \
            contiguous N above this threshold are filtered out")
    parser.add_argument("-n", "--total-n-threshold", type=int, default=30,
        help="Total N threshold, sequences with number of ambiguous base over \
            this threshold are filtered out")
    parser.add_argument("-l", "--len-threshold", type=int, default=145,
        help="Genome length threshold, sequences with length not in range \
            of plus/minus threshold bp compare to reference are filtered out")
    parser.add_argument("-e", "--end-cutoff", type=int, default=200,
        help="Ignore bases at both end while filtering genomes")
    parser.add_argument("-o", "--output-dir", type=str,
        help="Output directory")
    args = parser.parse_args()

    genome_dir = args.genomes
    simulated_genome_dir = args.simulated_dir
    contiguous_n_threshold = args.contiguous_n
    total_n_threshold = args.total_n_threshold
    length_threshold = args.len_threshold
    output_dir = args.output_dir
    reference = SeqIO.read(args.reference, "fasta")
    filter_genome(genome_dir, reference, output_dir, simulated_genome_dir,
                  contiguous_n_threshold, total_n_threshold,
                  length_threshold, args.end_cutoff)

if __name__ == "__main__":
    main()
