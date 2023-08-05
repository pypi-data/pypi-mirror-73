''' multiple sequence alignment and filtering MSA result '''
import os
import argparse



def run(genomes: str,
	output_dir: str,
	num_threads: int):
    filtered_msa_fasta = os.path.join(output_dir, "filtered_msa.fasta")
    msa_ret = os.system(f"mafft --adjustdirection --quiet  --thread {num_threads} {genomes}> {filtered_msa_fasta}")
    return msa_ret
        

# def main():
    # '''main function of the script'''
    # parser = argparse.ArgumentParser(description="MSA with mafft and filtering")
    # parser.add_argument("genomes", type=str, help="input genomes in multifasta format")
    # parser.add_argument("-t", "--threads", type=int, default=3,
                        # help="Number of threads to use")
    # args = parser.parse_args()


# if __name__ == "__main__":
    # main()

