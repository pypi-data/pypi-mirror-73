# Standard library imports
import argparse
import os
# 3rd party imports
import jinja2
import pandas as pd

def load_report(report_file, sens_file):
    report = pd.read_csv(report_file, quotechar="\"")
    sens = pd.read_csv(sens_file, quotechar="\"")
    report = report.merge(sens, 'left', on="ID")
    return report

def load_template(template_path, template_file):
    templateLoader = jinja2.FileSystemLoader(searchpath=template_path)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)
    return template

def parse_monohomomers(report):
    """ Reads in monohomomer annotations from the report and creates a list of respective
        sequence subchunks. This step is needed due to the limitations of Jinja2 templating
        language."""
    mono = [[] for i in range(report.shape[0])]
    for i, row in report.iterrows():
        for j, subseq in enumerate(row.Monohomomers.split("|")):
            mono[i].append((j, subseq))
    return mono

def parse_dinucleotides(report):
    """ Reads in dinucleotide annotations from the report and creates a list of respective
        sequence subchunks. This step is needed due to the limitations of Jinja2 templating
        language."""
    dinuc = [[] for i in range(report.shape[0])]
    for i, row in report.iterrows():
        for j, subseq in enumerate(row["Dinucleotide Repeats"].split("|")):
            dinuc[i].append((j, subseq))
    return dinuc

def render_and_write_output(template, report, outfile, monohomomers):
    """ Renders the template with values provided in the report and saves the result
        to an HTML file."""
    output = template.render(report=report.iterrows(), monohomomers=monohomomers)
    with open(outfile, "w") as outf:
        outf.write(output)

def visualize(
        validator_input: str,
        sensitivity_input: str,
        output_dir: str,
        template_dir: str,
        template_file: str):
    viz_output_name = os.path.join(output_dir, "output.html")
    report = load_report(validator_input, sensitivity_input)
    template = load_template(template_dir, template_file)
    monohomomers = parse_monohomomers(report)
    render_and_write_output(template, report, viz_output_name, monohomomers)
    report.to_csv(os.path.join(output_dir, "final-joined-report.csv"))


def main():
    """ Main script that takes in a Validator report and generates an HTML output."""
    parser = argparse.ArgumentParser(prog="OligoValidator: Visualizer",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required_args = parser.add_argument_group("Required named args")
    required_args.add_argument("-i", "--report-input", help="path to the CSV report from Validator",
                               type=str)
    required_args.add_argument("-s", "--sens-input", help="path to the CSV report from Sens/Spec check",
                               type=str)
    required_args.add_argument("-o", "--output", help="path to the output HTML file",
                               default="out", type=str)
    optional_parameter_args = parser.add_argument_group("Optional parameters")
    # TODO we can jsut get the dir from the path name
    optional_parameter_args.add_argument("-t", "--template-file", help="Jinja2 HTML template file",
                                         default="visualization-template.html", type=str)
    optional_parameter_args.add_argument("-p", "--template-dir", help="path to the folder with \
                                         template file", default="./", type=str)
    args = parser.parse_args()
    visualize(args.report_input, args.sens_input, args.output, args.template_path, args.template_file)

if __name__ == "__main__":
    main()

