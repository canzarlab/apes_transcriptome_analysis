import os
import re
import argparse
import pysam
from functools import lru_cache

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
                    bundle_info.append({"seqname": chromosome, "start": start, "end": end})
    # Ensure uniqueness of bundles
    unique_bundles = [dict(t) for t in {tuple(bundle.items()) for bundle in bundle_info}]
    print(f"Extracted {len(unique_bundles)} unique bundles from {file_path}")
    return unique_bundles

@lru_cache(maxsize=None)
def count_reads(bam_path, seqname, start, end):
    """
    Counts reads from a BAM file based on bundle information.
    Returns the total number of reads.
    """
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        return sum(1 for _ in bam.fetch(seqname, start, end))

def process_bundles(log_new, bam_new, output_csv):
    """
    Processes read bundles from a dataset based on a StringTie log,
    and outputs each bundle's total read count to a CSV file.
    """
    bundles_new = read_stringtie_log(log_new)
    
    # Prepare CSV output
    with open(output_csv, 'w') as csv_file:
        csv_file.write("Bundle, TotalReads, Coordinates\n")
        
        # Process bundles and count reads
        for bundle_new in bundles_new:
            total_reads = count_reads(bam_new, bundle_new['seqname'], bundle_new['start'], bundle_new['end'])
            bundle_name = f"{bundle_new['seqname']}:{bundle_new['start']}-{bundle_new['end']}"
            csv_line = f"{bundle_name}, {total_reads}, {bundle_new['seqname']}:{bundle_new['start']}-{bundle_new['end']}\n"
            csv_file.write(csv_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CSV file listing total read counts for each bundle based on StringTie log and corresponding BAM file.")
    parser.add_argument('--log_new', required=True, help='Path to StringTie log file')
    parser.add_argument('--bam_new', required=True, help='Path to BAM file')
    parser.add_argument('--output_csv', required=True, help='Output path for the CSV file')
    
    args = parser.parse_args()
    
    process_bundles(args.log_new, args.bam_new, args.output_csv)

