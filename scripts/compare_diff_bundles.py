import os
import re
import argparse
import sys
import subprocess
from functools import lru_cache

# Ensure required packages are installed
def ensure_packages_installed():
    try:
        import pysam
        from SetSimilaritySearch import SearchIndex
    except ImportError as e:
        print(f"Required package not found: {e.name}. Attempting to install...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', e.name])
        # Re-import after installation
        global pysam, SearchIndex
        import pysam
        from SetSimilaritySearch import SearchIndex

# Function to read StringTie log files and extract unique bundle information
def read_stringtie_log(file_path):
    bundle_info = []
    with open(file_path) as file:
        for line in file:
            if ">bundle" in line:
                match = re.search(r">bundle (\S+):(\d+)-(\d+)", line)
                if match:
                    chromosome, start, end = match.groups()
                    bundle_info.append((chromosome, int(start), int(end)))
    # Removing duplicates and returning unique bundles
    return list(set(bundle_info))

# Cache the extraction of read names from BAM files based on bundle information
@lru_cache(maxsize=None)
def extract_read_names(bam_path, bundle_info):
    seqname, start, end = bundle_info
    read_names = set()
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam.fetch(seqname, start, end):
            read_names.add(read.query_name)
    return read_names

# Main processing function
def process_bundles(log_old, log_new, bam_old, bam_new, output_csv):
    ensure_packages_installed()
    bundles_old = read_stringtie_log(log_old)
    bundles_new = read_stringtie_log(log_new)
    
    # Preparing sets for the search index from both old and new bundles
    sets_old = [extract_read_names(bam_old, bundle) for bundle in bundles_old]
    sets_new = [extract_read_names(bam_new, bundle) for bundle in bundles_new]

    # Create separate indexes for old and new sets to ensure cross-comparison only
    index_old = SearchIndex(sets_old, similarity_func_name="jaccard", similarity_threshold=0.1)
    index_new = SearchIndex(sets_new, similarity_func_name="jaccard", similarity_threshold=0.1)

    with open(output_csv, 'w') as csv_file:
        csv_file.write("Bundle1, Bundle2, Size1, Size2, Jaccard\n")
        # Compare new bundles against old bundles
        for i, bundle_new in enumerate(bundles_new):
            read_names_new = sets_new[i]
            results = index_old.query(read_names_new)
            for result in results:
                index_matched, similarity = result
                if similarity >= 0.1:
                    bundle1 = f"{bundle_new[0]}:{bundle_new[1]}-{bundle_new[2]}"
                    matched_bundle = bundles_old[index_matched]
                    bundle2 = f"{matched_bundle[0]}:{matched_bundle[1]}-{matched_bundle[2]}"
                    size1 = len(read_names_new)
                    size2 = len(sets_old[index_matched])
                    csv_line = f"{bundle1}, {bundle2}, {size1}, {size2}, {similarity:.4f}\n"
                    csv_file.write(csv_line)
                    
        # Optionally: Compare old bundles against new bundles if bidirectional comparison is needed
        # Repeat the block above with roles of old and new swapped

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare read bundles between old and new datasets based on StringTie logs and output to CSV.")
    parser.add_argument('--log_old', required=True, help='Path to old StringTie log file')
    parser.add_argument('--log_new', required=True, help='Path to new StringTie log file')
    parser.add_argument('--bam_old', required=True, help='Path to old BAM file')
    parser.add_argument('--bam_new', required=True, help='Path to new BAM file')
    parser.add_argument('--output_csv', required=True, help='Output path for the CSV file')

    args = parser.parse_args()

    # Echo used command for debugging
    print(f"Command used: {' '.join(sys.argv)}")

    process_bundles(args.log_old, args.log_new, args.bam_old, args.bam_new, args.output_csv)
    print(f"Output CSV saved to: {os.path.abspath(args.output_csv)}")

