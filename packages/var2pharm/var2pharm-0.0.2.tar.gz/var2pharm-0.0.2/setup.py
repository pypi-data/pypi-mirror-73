from setuptools import setup, find_packages

exec(open("var2pharm/version.py").read())

requirements = ["requests>=2", "pandas>=1.0.0", "bs4>=0.0.1",
    "lxml>=4.5.0", "pysam>=0.16.0",]

setup(
    name="var2pharm",
    version=__version__,
    author='Konstantinos Kyriakidis',
    author_email="kokyriakidis@gmail.com",
    description="End-to-end pharmacogenomics research tool that enables personalized drug dosing based on individual's variants",
    long_description=open("README.md").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/PGxAUTH/Var2Pharm/",
    packages=find_packages(),
    package_data={
        "var2pharm.resources.cpic": ["cpicPairs.csv"],
        "var2pharm.resources.sg": [
            "gene_table.txt",
            "phenotype_table.txt",
            "snp_table.txt",
            "star_table.txt",
        ],
        "var2pharm.resources.pgkb": ["actions.txt"],
        "var2pharm.resources.r": ["cpa.R", "plotcov.R"],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={"console_scripts": ["var2pharm=var2pharm.__main__:main"]}
)
