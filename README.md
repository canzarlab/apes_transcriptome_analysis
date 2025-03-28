# Mappability and transcript assembly of long RNA-seq – Ape Genome Study

This repository contains scripts used in the **gene annotation section** of:

> **Complete sequencing of ape genomes**  
> bioRxiv [Preprint]. 2024 Oct 5:2024.07.31.605654  
> Originally published 2024 Jul 31. [Version 2]  
> [doi:10.1101/2024.07.31.605654](https://doi.org/10.1101/2024.07.31.605654)

## Study Summary

We present haplotype-resolved reference genomes and comparative analyses of six ape species: chimpanzee, bonobo, gorilla, Bornean orangutan, Sumatran orangutan, and siamang. With chromosome-level contiguity, we fully sequence 215 gapless chromosomes and resolve highly repetitive immune and centromeric regions. This enables unbiased annotation and evolutionary analysis of gene families, segmental duplications, and other complex loci.

### This repository focuses on the **impact of T2T assemblies on mappability and transcript assembly**, leveraging long-read IsoSeq data.

### Mapping statistics

We used PacBio Iso-Seq long reads from testis RNA samples of four great apes (chimpanzee, Sumatran orangutan, gorilla, and bonobo) to quantify the potential impact of T2T genome assemblies on read mapping and observed improvements in mappability, soft-clipping, and error rates. Iso-Seq reads were mapped with minimap2 v2.24-r112227 with parameters recommended for PacBio Iso-Seq cDNA (-ax splice:hq -uf) allowing up to 15 alignments per read (-N 15) to both T2T assemblies and previous assemblies. 
Mismatch and indel rates were computed based on primary alignments only using Perbase v0.9.0 (Stadick 2023 https://github.com/sstadick/perbase).
Transcripts were assembled from aligned reads using StringTie2 v2.2.128 with default parameters. We did not provide a reference annotation file to be able to attribute differences in transcript assembly to the quality of the reference sequence alone. 

### StringTie bundles analysis

StringTie2 and most other existing algorithms infer transcripts locus by locus. If not relying on a gene annotation, loci are identified by sets of reads, i.e., read bundles, that together span a (almost) contiguous genomic region. We ran StringTie2 with option -v and parsed the output to collect read bundles that allow for gaps, i.e., genomic regions that are not covered by any reads, of length at most 50 bp. The similarity of bundles formed by reads mapped to T2T and to previous assemblies was measured by the Jaccard index.

## Scripts for mapping statistics

### `calculate_stats.py`

Usage

The script requires four positional arguments:

    old_bam_file: Path to the first (old) BAM file.

    new_bam_file: Path to the second (new) BAM file.

    equivalence_file: CSV file containing chromosome equivalence mappings. Each line must include at least three comma-separated values (old name, new name, common name).

    output_file: Path where the output CSV file will be written.

Command-Line Example
```{python}
python script.py old.bam new.bam chromosome_equivalences.csv output.csv
```

Input File Formats
Chromosome Equivalence File

    Format: CSV

    Columns: The file must contain at least three columns per line:

        Column 1: Old chromosome name.

        Column 2: New chromosome name.

        Column 3: Common name to map both names.

    Note: Lines with fewer than three fields will be skipped.

BAM Files

    Standard BAM files used for alignment data.

    Ensure that the BAM files are valid and indexed if necessary.

Output

The script creates an output CSV file with the following columns:

    Chromosome: The common chromosome name.

    Old Soft Clipped: Count of significant soft-clipped reads in the old BAM file.

    New Soft Clipped: Count of significant soft-clipped reads in the new BAM file.

    Old Mismatch Rate: Mismatch rate for the old BAM file (mismatches / total bases).

    New Mismatch Rate: Mismatch rate for the new BAM file.

    Old Multimap Rate: Proportion of secondary/supplementary reads in the old BAM file.

    New Multimap Rate: Proportion of secondary/supplementary reads in the new BAM file.

    Unmapped_old: Number of reads that transitioned from unmapped in the old file to mapped in the new file.

    Unmapped_new: Number of reads that transitioned from unmapped in the new file to mapped in the old file.



## Scripts for bundle analysis

### `compare_transcripts_csv.py`

**Purpose**: Compare read bundles between old and new datasets based on StringTie logs and output to CSV.

**Inputs**:

**Output**:

**Usage**:

```
compare_transcripts_index_csv.py [-h] --log_old LOG_OLD --log_new LOG_NEW --bam_old
                                        BAM_OLD --bam_new BAM_NEW --output_csv OUTPUT_CSV
                                        
options:
  -h, --help            show this help message and exit
  --log_old LOG_OLD     Path to old StringTie log file
  --log_new LOG_NEW     Path to new StringTie log file
  --bam_old BAM_OLD     Path to old BAM file
  --bam_new BAM_NEW     Path to new BAM file
  --output_csv OUTPUT_CSV
                        Output path for the CSV file
```

### `bundlecompare.py`

**Purpose**: Compare read bundles within the same assembly based on StringTie logs.

**Inputs**:

**Output**:

**Usage**:
```
self_compare_csv.py [-h] --log_new LOG_NEW --bam_new BAM_NEW --output_csv OUTPUT_CSV

options:
  -h, --help            show this help message and exit
  --log_new LOG_NEW     Path to new StringTie log file
  --bam_new BAM_NEW     Path to new BAM file
  --output_csv OUTPUT_CSV
                        Output path for the CSV file
```

### `totalbundles.py`

**Purpose**: Count reads per bundle from a StringTie log and a BAM file.

**Inputs**:

**Output**:

**Usage**:
```
bundletotal.py [-h] --log_new LOG_NEW --bam_new BAM_NEW --output_csv OUTPUT_CSV

options:
  -h, --help            show this help message and exit
  --log_new LOG_NEW     Path to StringTie log file.
  --bam_new BAM_NEW     Path to BAM file.
  --output_csv OUTPUT_CSV
                        Output CSV file path.
```
                        


## Files

The files are respectively in the folders: 

- Data/alignments
- 




# Stats




    python master.py ~/group/apes_transcriptome_analysis/non_T2T/data/alignments/long_reads/GGO.bam ~/group/apes_transcriptome_analysis/T2T_v2/data/alignments/long_reads/GGO.bam ~/group/apes_transcriptome_analysis/non_T2T/data/chromosomal_equivalences/GGO_equiv.csv GGO_stats1.csv 


## Per chromomsome stats

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.



# Stringtie assemblies


    stringtie ../../../data/alignments/long_reads/PPY.bam -v -o PPY_long.gtf > PPY_long.log 2>&1



# Bundles

### compare_transcripts_csv.py


     python compare_transcripts_index_csv.py --help
usage: compare_transcripts_index_csv.py [-h] --log_old LOG_OLD --log_new LOG_NEW --bam_old
                                        BAM_OLD --bam_new BAM_NEW --output_csv OUTPUT_CSV

Compare read bundles between old and new datasets based on StringTie logs and output to CSV.

options:
  -h, --help            show this help message and exit
  --log_old LOG_OLD     Path to old StringTie log file
  --log_new LOG_NEW     Path to new StringTie log file
  --bam_old BAM_OLD     Path to old BAM file
  --bam_new BAM_NEW     Path to new BAM file
  --output_csv OUTPUT_CSV
                        Output path for the CSV file


### bundlecompare.py


    python self_compare_csv.py --help
usage: self_compare_csv.py [-h] --log_new LOG_NEW --bam_new BAM_NEW --output_csv OUTPUT_CSV

Compare read bundles within the same assembly based on StringTie logs.

options:
  -h, --help            show this help message and exit
  --log_new LOG_NEW     Path to new StringTie log file
  --bam_new BAM_NEW     Path to new BAM file
  --output_csv OUTPUT_CSV
                        Output path for the CSV file


### totalbundles.py

    python bundletotal.py --help
usage: bundletotal.py [-h] --log_new LOG_NEW --bam_new BAM_NEW --output_csv OUTPUT_CSV

Count reads per bundle from a StringTie log and a BAM file.
options:
  -h, --help            show this help message and exit
  --log_new LOG_NEW     Path to StringTie log file.
  --bam_new BAM_NEW     Path to BAM file.
  --output_csv OUTPUT_CSV
                        Output CSV file path.




