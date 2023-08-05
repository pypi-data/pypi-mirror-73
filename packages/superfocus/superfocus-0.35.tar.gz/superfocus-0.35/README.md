![](logo/superfocus_logo_small.png "Logo")

### SUPER-FOCUS: A tool for agile functional analysis of metagenomic data
* [Installation](#installation)
* [Dependencies](#dependencies)
* [Aligners](#aligners)
* [Download SUPER-FOCUS Database](#database)
* [Running SUPER-FOCUS](#run)
* [General Recomendations](#recomendations)
* [Ouput](#output)
* [Citing](#citing)

## Is SUPER-FOCUS right for you?
This [blog post](https://onestopdataanalysis.com/metagenome-functional-profile/) talks about SUPER_FOCUS. Please read it and make sure the tool is right for you.

## Installation
This will give you command line program:

	pip3 install superfocus

or

	# clone super-focus
	git clone https://github.com/metageni/SUPER-FOCUS.git

	# install super-focus
	cd SUPER-FOCUS && python setup.py install

	# if you do not have super user privileges, you can install it like this
	cd SUPER-FOCUS && python setup.py install --user


## Dependencies
- [Python >= 3.6](http://www.python.org/download)
- [Numpy 1.12.1](https://github.com/numpy/numpy)
- [SciPy 0.19.0](https://github.com/scipy/scipy)  

If you have Python 3.6, you can install both dependencies with:  
`pip3 install -r requirements.txt`

## Aligners
One of the below aligners, which can easily be installed with [`conda`](https://conda.io/docs/):
- [DIAMOND 0.9.14](http://ab.inf.uni-tuebingen.de/software/diamond)
- [RAPSearch2 2.24](http://rapsearch2.sourceforge.net)
- [BLAST 2.6.0](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

To install the aligners, having [`conda`](https://conda.io/docs/installation.html) installed, simply run:  
 `conda install -c bioconda <aligner>`

 Note that they are all available from the [`bioconda`](https://bioconda.github.io/) channel.

## Database

Some of the steps below could be automatized. However, many users have had problem with the database formatting, and it was requested for the initial steps to be manual.

#### Download and uncompress
First download the database with the steps below or using your favorite method to download and uncompress files:
```
# download
wget edwards.sdsu.edu/superfocus/downloads/db.zip
# uncompress
unzip db.zip
```
**NOTE**: You can also download the small file named `db_small.zip` and test the instalation before downloading the large file.

#### Format
Now that you downloaded the database, please use the instructions below to format it and move into the database folder.
```
superfocus_downloadDB -i <clusters_folder> -a <aligner> -c <clusters>
```
where
- `<clusters_folder>` is the path to the database you downloaded and uncompressed above (folder `clusters/`)
- `<aligner>` is `rapsearch`, `diamond`, or `blast` (or all of them separated by `,`). You
may choose as many aligners as you want among the three, as long as they are
installed.
- `<clusters>` is the cluster of the database you want to format which are `90`, `95`, `98`, and/or `100`. Default: `90`. If more than one, please separe by comma (e.g. 90,95,98,100).

**NOTE**: RAPSearch2 and DIAMOND won't work properly if you are trying to use a
database formatted with an incorrect version of the aligner. Thus, please
re-run `superfocus_downloadDB` in case any aligner was updated on your
system.


## Run
The main SUPER-FOCUS program is `superfocus`. Here is a list of the
available command line options:

    usage: superfocus    [-h] [-v] -q QUERY -dir OUTPUT_DIRECTORY
                         [-o OUTPUT_PREFIX] [-a ALIGNER] [-mi MINIMUM_IDENTITY]
                         [-ml MINIMUM_ALIGNMENT] [-t THREADS] [-e EVALUE]
                         [-db DATABASE] [-p AMINO_ACID] [-f FAST]
                         [-n NORMALISE_OUTPUT] [-m FOCUS] [-b ALTERNATE_DIRECTORY]
                         [-d] [-l LOG]

    SUPER-FOCUS: A tool for agile functional analysis of shotgun metagenomic data.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -q QUERY, --query QUERY
                            Path to FAST(A/Q) file or directory with these files.
      -dir OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                            Path to output files
      -o OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX
                            Output prefix (Default: output).
      -a ALIGNER, --aligner ALIGNER
                            aligner choice (rapsearch, diamond, or blast; default
                            rapsearch).
      -mi MINIMUM_IDENTITY, --minimum_identity MINIMUM_IDENTITY
                            minimum identity (default 60 perc).
      -ml MINIMUM_ALIGNMENT, --minimum_alignment MINIMUM_ALIGNMENT
                            minimum alignment (amino acids) (default: 15).
      -t THREADS, --threads THREADS
                            Number Threads used in the k-mer counting (Default:
                            4).
      -e EVALUE, --evalue EVALUE
                            e-value (default 0.00001).
      -db DATABASE, --database DATABASE
                            database (DB_90, DB_95, DB_98, or DB_100; default
                            DB_90)
      -p AMINO_ACID, --amino_acid AMINO_ACID
                            amino acid input; 0 nucleotides; 1 amino acids
                            (default 0).
      -f FAST, --fast FAST  runs RAPSearch2 or DIAMOND on fast mode - 0 (False) /
                            1 (True) (default: 1).
      -n NORMALISE_OUTPUT, --normalise_output NORMALISE_OUTPUT
                            normalises each query counts based on number of hits;
                            0 doesn't normalize; 1 normalizes (default: 1).
      -m FOCUS, --focus FOCUS
                            runs FOCUS; 1 does run; 0 does not run: default 0.
      -b ALTERNATE_DIRECTORY, --alternate_directory ALTERNATE_DIRECTORY
                            Alternate directory for your databases.
      -d, --delete_alignments
                            Delete alignments
      -l LOG, --log LOG     Path to log file (Default: STDOUT).

    superfocus -q input_folder -dir output_dir

## Recomendations
- The FOCUS reduction is not necessary if not wanted (it is off by default: set `-focus 1` to run FOCUS reduction)
- Run RAPSearch for short sequences, it is less sensitive for long sequences
- Primarily use DIAMOND for large datasets only. It is slower than blastx for small datasets
- BLAST is known for being really slow

## Output
SUPER-FOCUS output will be add the folder selected by the `-dir` argument.

## Citing
SUPER-FOCUS was written by Genivaldo G. Z. Silva. Feel free to create an [issue or ask questions](https://github.com/metageni/SUPER-FOCUS/issues)

If you use SUPER-FOCUS in your research, please cite:

#### Paper

    Silva, G. G. Z., Green K., B. E. Dutilh, and R. A. Edwards:
    SUPER-FOCUS: A tool for agile functional analysis of shotgun metagenomic data.
	Bioinformatics. 2015 Oct 9. pii: btv584. Website: https://edwards.sdsu.edu/SUPERFOCUS

#### Extended tool manual
    Silva, G. G. Z., F. A. Lopes, and R. A. Edwards
    An Agile Functional Analysis of Metagenomic Data Using SUPER-FOCUS.
	Protein Function Prediction: Methods and Protocols, 2017.
