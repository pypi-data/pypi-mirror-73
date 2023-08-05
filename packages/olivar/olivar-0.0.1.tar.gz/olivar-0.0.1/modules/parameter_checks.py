import subprocess

def evaluate_tm(seq, dna_conc, single_ion_conc, double_ion_conc, dntps_conc):
    """ Evaluates melting temperature using oligotm from Primer 3."""
    completed_process = subprocess.check_output(args=f"oligotm -tp 1 -sc 1 \
                                                       -mv {single_ion_conc} \
                                                       -dv {double_ion_conc} \
                                                       -n {dntps_conc} \
                                                       -d {dna_conc} {seq}",
                                                shell=True, encoding='UTF-8')
    seq_tm = float(completed_process)
    return seq_tm

def evaluate_self_ntthal(seq, dna_conc, single_ion_conc, double_ion_conc, dntps_conc, align_type):
    """ Determines self-dimer/hairpin potential for the oligo."""
    completed_process = subprocess.check_output(args=f"ntthal \
                                                       -mv {single_ion_conc} \
                                                       -dv {double_ion_conc} \
                                                       -n {dntps_conc} \
                                                       -d {dna_conc} \
                                                       -a {align_type} \
                                                       -s1 {seq} -s2  {seq} 2>&1",
                                                shell=True, encoding='UTF-8')
    return completed_process

def evaluate_mono_homomers(seq, min_count):
    """ Adds annotated sequences with monohomomer stretches marked."""
    cur_base = seq[0]
    cur_seq = cur_base
    subseqs = []
    for base in seq[1:]:
        if base != cur_base:
            subseqs.append(cur_seq)
            cur_base = base
            cur_seq = cur_base
        else:
            cur_seq += base
    subseqs.append(cur_seq)
    max_subseq_length = 0
    for i, subseq in enumerate(subseqs):
        if len(subseq) > max_subseq_length:
            max_subseq_length = len(subseq)
        if len(subseq) >= min_count:
            subseqs[i] = "|" + subseq + "|"
    return (subseqs, max_subseq_length)
