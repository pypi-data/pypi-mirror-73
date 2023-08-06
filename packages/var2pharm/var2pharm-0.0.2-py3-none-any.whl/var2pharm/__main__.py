import sys
import argparse

from .version import __version__

from .common import logging
from .report import report
from .bam2report import bam2report
from .sdf2gdf import sdf2gdf
from .bam2sdf import bam2sdf
from .bam2gdf import bam2gdf
from .cpa import cpa
from .plotcov import plotcov

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        action="version",
        version=f"var2pharm v{__version__}",
        help="print the var2pharm version number and exit"
    )

    subparsers = parser.add_subparsers(
        dest="tool",
        metavar="tool",
        help="name of the tool",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="create HTML report using Stargazer data",
    )
    report_parser.add_argument(
        "gt",
        help="genotype file",
    )
    report_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    bam2report_parser = subparsers.add_parser(
        "bam2report",
        help="run per-sample genotyping with Stargazer",
    )
    bam2report_parser.add_argument(
        "conf",
        help="configuration file",
    )

    bam2gdf_parser = subparsers.add_parser(
        "bam2gdf",
        help="create GDF file from BAM file(s)",
    )
    bam2gdf_parser.add_argument(
        "gb",
        help="genome build (hg19, hg38)",
    )
    bam2gdf_parser.add_argument(
        "tg",
        help="target gene",
    )
    bam2gdf_parser.add_argument(
        "cg",
        help="control gene or region",
    )
    bam2gdf_parser.add_argument(
        "bam",
        nargs="+",
        help="BAM file",
    )
    bam2gdf_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    return parser

def output(fn, result):
    if fn:
        with open(fn, "w") as f:
            f.write(result)
    else:
        sys.stdout.write(result)

def main():
    parser = get_parser()
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.info(f"var2pharm v{__version__}")
    logger.info(f"""Command: '{" ".join(sys.argv)}'""")


    if args.tool == "report":
        result = report(args.gt)
        output(args.o, result)


    elif args.tool == "bam2report":
        bam2report(args.conf)

    elif args.tool == "bam2gdf":
        result = bam2gdf(args.gb, args.tg, args.cg, args.bam)
        output(args.o, result)

    else:
        pass

    logger.info("var2pharm finished")

if __name__ == "__main__":
    main()
