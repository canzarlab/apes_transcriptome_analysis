# Directory structure

.
├── chromosomal_equivalences
├── non_T2T
│   ├── data
│   │   ├── alignments
│   │   │   ├── long_reads
│   │   │   └── short_reads
│   │   └── reference_and_annotation
│   │       ├── GGO_GCF_008122165.1
│   │       │   └── hisat_indexes
│   │       ├── PAB_GCF_002880775.1
│   │       │   └── hisat_indexes
│   │       ├── PPA_GCF_000258655.2
│   │       │   └── hisat_indexes
│   │       └── PTR_GCF_002880755.1
│   │           └── hisat_indexes
│   └── results
│       └── assemblies
│           ├── GGO
│           ├── GGO_15
│           ├── PAB
│           ├── PAB_15
│           ├── PPA
│           ├── PPA_15
│           ├── PPY
│           ├── PPY_15
│           ├── PTR
│           ├── PTR_15
│           ├── PTR_15_04
│           ├── PTR_15_05
│           └── PTR_15_05_sp
├── output_analysis
├── raw
│   ├── long_reads
│   │   ├── GGO
│   │   ├── PAB
│   │   ├── PPA
│   │   ├── PPY
│   │   └── PTR
│   └── short_reads
│       ├── GGO
│       ├── PAB
│       ├── PPA
│       ├── PPY
│       └── PTR
├── scripts
│   ├── PTR
│   ├── results
│   └── scripts
├── stats
└── T2T_v2
    ├── data
    │   ├── alignments
    │   │   ├── long_reads
    │   │   └── short_reads
    │   │       └── no_secondary
    │   └── reference_and_annotation
    │       ├── GGO_GCF_029281585.2
    │       │   └── hisat_indexes
    │       ├── PAB_GCF_028885655.2
    │       │   └── hisat_indexes
    │       ├── PPA_GCF_029289425.2
    │       │   └── hisat_indexes
    │       ├── PPY_GCF_028885625.2
    │       │   └── hisat_indexes
    │       └── PTR_GCF_028858775.2
    │           └── hisat_indexes
    └── results
        └── assemblies
            ├── GGO
            ├── GGO_15
            ├── PAB
            ├── PAB_15
            ├── PPA
            ├── PPA_15
            ├── PPY
            ├── PPY_15
            ├── PTR
            ├── PTR_15
            ├── PTR_15_04
            ├── PTR_15_05
            └── PTR_15_05_sp



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




