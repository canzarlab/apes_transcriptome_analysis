import os
import re
import argparse
import pysam
from functools import lru_cache
from itertools import combinations

def read_stringtie_log(file_path):
    """
    Reads a StringTie log file and extracts unique bundle information (chromosome and coordinates).
    """
    bundle_info = []
    with open(file_path) as file:
        for line in file:
            if ">bundle" in line:
                match = re.search(r">bundle (\S+):(\d+)-(\d+)", line)
                if match:
                    chromosome = match.group(1)
                    start = int(match.group(2))
                    end = int(match.group(3))
                    bundle_info.append((chromosome, start, end))
    return list(set(bundle_info))  # Remove duplicates

@lru_cache(maxsize=None)
def extract_read_names(bam_path, chromosome, start, end):
    """
    Extracts read names from a BAM file for a given bundle.
    """
    read_names = set()
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam.fetch(chromosome, start, end):
            read_names.add(read.query_name)
    return read_names

def calculate_jaccard(set1, set2):
    """
    Calculates the Jaccard index for two sets of read names.
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

def compare_bundles(bam_path, bundles, output_csv_path, jaccard_threshold=0.1):
    """
    Compares bundles within the same assembly to find similarities.
    """
    with open(output_csv_path, 'w') as csv_file:
        csv_file.write("Bundle,Matched Bundle,Size of Original Bundle,Size of Matched Bundle,Overlapping Reads,Jaccard\n")
        
        for (bundle1, bundle2) in combinations(bundles, 2):
            read_names1 = extract_read_names(bam_path, *bundle1)
            read_names2 = extract_read_names(bam_path, *bundle2)
            overlapping_reads = len(read_names1 & read_names2)
            jaccard = calculate_jaccard(read_names1, read_names2)

            if jaccard >= jaccard_threshold:
                csv_file.write(f"{bundle1},{bundle2},{len(read_names1)},{len(read_names2)},{overlapping_reads},{jaccard}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare read bundles within the same assembly.")
    parser.add_argument('--log_new', required=True, help='Path to new StringTie log file')
    parser.add_argument('--bam_new', required=True, help='Path to new BAM file')
    parser.add_argument('--output_csv', required=True, help='Output CSV file path for comparison results')
    
    args = parser.parse_args()

    bundles = read_stringtie_log(args.log_new)
    compare_bundles(args.bam_new, bundles, args.output_csv)

