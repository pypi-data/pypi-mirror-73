import logging
import subprocess
import sys

def get_logger(logname, loglevel=logging.INFO):
    VERBOSITY = loglevel
    logger = logging.getLogger(logname)
    logger.setLevel(VERBOSITY)
    ch = logging.StreamHandler()
    ch.setLevel(VERBOSITY)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


UNAMBIG_LIMIT = 1000
ALPHABET = ["A", "G", "T", "C"]
AMBIGUITYCODE = {
    "Y": ["C", "T"],
    "R": ["A", "G"],
    "W": ["A", "T"],
    "S": ["G", "C"],
    "K": ["T", "G"],
    "M": ["C", "A"],
    "D": ["A", "G", "T"],
    "V": ["A", "C", "G"],
    "H": ["A", "C", "T"],
    "B": ["C", "G", "T"],
    "X": ["A", "T", "C", "G"],
    "N": ["A", "T", "C", "G"]
}


def run_command(command, logger):
   logger.debug(command)
   p = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   fstdout,fstderr = p.communicate()
   rc = p.returncode

   fstdout = fstdout.decode("utf-8")
   fstderr = fstderr.decode("utf-8")
   if rc != 0:
      logger.critical("""The following command failed:
      >>$ {}
      Please veryify input data and restart Parsnp.
      If the problem persists please contact the Parsnp development team.
      
      STDOUT:
      {}
      
      STDERR:
      {}""".format(command, fstdout, fstderr))
    
      sys.exit(rc)
   else:
      logger.debug(fstdout)
      logger.debug(fstderr)

def disambiguate_seq(seq):
    """ Returns a list of disambiguated sequences."""
    ret = []
    if not any(c in seq for c in AMBIGUITYCODE):
        ret.append(seq)
    else:
        ambig_index = next(
            (i for i, c in enumerate(seq) if c in AMBIGUITYCODE), None)
        if ambig_index is not None:
            for c in AMBIGUITYCODE[seq[ambig_index]]:
                for disambiguated_seq in disambiguate_seq(seq[ambig_index +
                                                              1:]):
                    ret.append(seq[:ambig_index] + c + disambiguated_seq)
    return ret
