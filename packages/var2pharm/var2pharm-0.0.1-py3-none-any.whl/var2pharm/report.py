import pkgutil
import csv
import sys
import datetime
from typing import TextIO, Optional

def _overview_table(gt, pairs, genes):
    table = (
        "<table>\n"
        "<tr>\n"
        "  <th style='width: 10%;'>No.</th>\n"
        "  <th style='width: 10%;'>Gene</th>\n"
        "  <th style='width: 20%;'>Genotype</th>\n"
        "  <th style='width: 10%;'>Total AS</th>\n"
        "  <th style='width: 30%;'>Predicted Phenotype</th>\n"
        "</tr>\n"
    )
    words = ["normal", "unknown", "-"]
    for i, gene in enumerate(genes, 1):
        if any([x in gt[gene]["phenotype"] for x in words]):
            color = "black"
        else:
            color = "red"
        genotype = gt[gene]["hap1_main"] + "/" + gt[gene]["hap2_main"]
        score = gt[gene]["dip_score"]
        phenotype = gt[gene]["phenotype"]
        table += (
            f"<tr style='color: {color};'>\n"
            f"  <td>{i}</td>\n"
            f"  <td>{gene.upper()}</td>\n"
            f"  <td>{genotype}</td>\n"
            f"  <td>{score}</td>\n"
            f"  <td>{phenotype}</td>\n"
            "</tr>\n"
        )
    return table + "</table>"


def report(
        fn: str,
        f: Optional[TextIO] = None
    ) -> str:
    """
    Create HTML report using Stargazer data.

    Returns:
        str: HTML report.

    Args:
        fn (str): Genotype file.
        f (TextIO, optional): Genotype file.
    """

    # Get the list of genes targeted by Stargazer.
    genes = []
    text = pkgutil.get_data(__name__, "resources/sg/gene_table.txt").decode()
    for line in text.strip().split("\n"):
        fields = line.split("\t")
        gene = fields[1]
        type_ = fields[2]
        if type_ == "target":
            genes.append(gene)

    # Read the actions file.
    actions = {}
    text = pkgutil.get_data(__name__, "resources/pgkb/actions.txt").decode()
    for line in text.strip().split("\n"):
        fields = line.split("\t")
        chemical = fields[0]
        gene = fields[1]
        url = fields[2]
        summary = fields[4]
        phenotype = fields[5]
        action = fields[6]
        if chemical == "chemical":
            header = fields
            continue
        if chemical not in actions:
            actions[chemical] = {}
        if gene not in actions[chemical]:
            actions[chemical][gene] = {
                "summary": summary,
                "url": url,
                "pt": {},
            }
        if phenotype not in actions[chemical][gene]["pt"]:
            actions[chemical][gene]["pt"][phenotype] = action

    # Read the genotype file.
    if fn:
        f = open(fn)
    gt = {}
    id = ""
    header = next(f).strip().split("\t")
    for line in f:
        fields = line.strip().split("\t")
        gene = fields[0]
        if not id:
            id = fields[1]
        gt[gene] = dict(zip(header, fields))
    for gene in genes:
        if gene not in gt:
            gt[gene] = dict(zip(header, ["-" for x in header]))
    assessed = [x for x in genes if gt[x]["status"] != "-"]
    typed = [x for x in genes if gt[x]["status"] == "g"]
    if fn:
        f.close()

    # Read the gene-drug paris file.
    pairs = []
    text = pkgutil.get_data(__name__, "resources/cpic/cpicPairs.csv").decode()
    f = csv.reader(text.strip().split("\n"))
    updated = next(f)[0].replace("Date last updated: ", "")
    header = next(f)
    for fields in f:
        pairs.append(dict(zip(header, [x if x else '-' for x in fields])))

    string = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "<title>Var2Pharm Report</title>\n"
        "<style>\n"
        "* {\n"
        "  font-family: Arial, Helvetica, sans-serif;\n"
        "}\n"
        "table {\n"
        "  border-collapse: collapse;\n"
        "  width: 100%;\n"
        "  font-size: 80%;\n"
        "}\n"
        "th, td {\n"
        "  border: 1px solid black;\n"
        "  padding: 4px;\n"
        "}\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Var2Pharm Report</h1>\n"
        "<p>\n"
        f"  Sample ID: {id}<br />\n"
        f"  Date: {datetime.datetime.now()}<br />\n"
        f"  Genes examined: {len(assessed)}/{len(genes)}<br />\n"
        f"  Genotypes called: {len(typed)}/{len(assessed)}<br />\n"
        "</p>\n"
        "<p>\n"
        "  Disclaimer: This report is still very much in development. \n"
        "</p>\n"
        "<h2>Sections</h2>\n"
        "<ul>\n"
        "  <li>Overview</li>\n"
        "</ul>\n"
        "<p style='page-break-before: always;'>\n"
        "<h2>Overview</h2>\n"
        "<p>\n"
        "  PGx genes whose genotype leads to altered phenotype are \n"
        "  shown in <span style='color: red;'>red</span>.\n"
        "</p>\n"
        f"{_overview_table(gt, pairs, genes)}\n"
        "</body>\n"
        "</html>\n"
    )

    return string