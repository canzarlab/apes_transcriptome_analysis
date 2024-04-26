import pysam
import sys
import pandas as pd
import re

# Global regular expression to capture 'JA' chromosomes
ja_pattern = re.compile(r'^JA\w+\.1$')

def read_chromosome_equivalences(equiv_file):
    """
    Reads chromosome equivalences from a file, returning a dictionary for mapping to common chromosome names.
    Handles 'JA' chromosomes by mapping them to 'chrY'.
    """
    chrom_mapping = {}
    with open(equiv_file, 'r', encoding='utf-8-sig') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue
            old, new, common = parts[0].strip(), parts[1].strip(), parts[2].strip()
            chrom_mapping[old] = common
            chrom_mapping[new] = common
    return chrom_mapping

def analyze_bam(bam_file, chrom_mapping):
    """
    Analyzes the BAM file using the provided chromosome mapping to calculate metrics.
    """
    bam = pysam.AlignmentFile(bam_file, "rb")
    results = {}
    for read in bam.fetch():
        if read.is_unmapped:
            continue

        chrom = read.reference_name
        common_name = chrom_mapping.get(chrom, 'Unrecognized')

        if ja_pattern.match(chrom):
            common_name = 'chrY'

        if common_name not in results:
            results[common_name] = {'soft_clipped': 0, 'mismatches': 0, 'mapped_reads': 0, 'total_bases': 0, 'multimaps': 0}

        significant_soft_clipping = sum(length for op, length in read.cigartuples if op == 4 and length >= 200)
        if significant_soft_clipping > 0:
            results[common_name]['soft_clipped'] += 1

        results[common_name]['mapped_reads'] += 1
        if read.has_tag('NM'):
            results[common_name]['mismatches'] += read.get_tag('NM')
            results[common_name]['total_bases'] += read.query_alignment_length
        if read.is_secondary or read.is_supplementary:
            results[common_name]['multimaps'] += 1

    bam.close()

    # Ensure all metrics are initialized properly
    for chrom, data in results.items():
        data.setdefault('mismatch_rate', 0 if data['total_bases'] == 0 else data['mismatches'] / data['total_bases'])
        data.setdefault('multimap_rate', 0 if data['mapped_reads'] == 0 else data['multimaps'] / data['mapped_reads'])

    return results

def track_transitions(bam_file, unmapped_set, chrom_mapping):
    """
    Tracks transitions of reads from unmapped in one BAM file to mapped in another.
    """
    bam = pysam.AlignmentFile(bam_file, "rb")
    transitions = {}
    for read in bam:
        if read.query_name in unmapped_set and not read.is_unmapped:
            chrom = read.reference_name
            common_name = chrom_mapping.get(chrom, "Unrecognized")
            transitions.setdefault(common_name, 0)
            transitions[common_name] += 1
    bam.close()
    return transitions

def main(old_bam, new_bam, equiv_file, output_file):
    chrom_mapping = read_chromosome_equivalences(equiv_file)
    
    old_unmapped_reads = {read.query_name for read in pysam.AlignmentFile(old_bam) if read.is_unmapped}
    new_unmapped_reads = {read.query_name for read in pysam.AlignmentFile(new_bam) if read.is_unmapped}

    old_results = analyze_bam(old_bam, chrom_mapping)
    new_results = analyze_bam(new_bam, chrom_mapping)
    old_to_new_mapped = track_transitions(new_bam, old_unmapped_reads, chrom_mapping)
    new_to_old_mapped = track_transitions(old_bam, new_unmapped_reads, chrom_mapping)

    with open(output_file, 'w') as f:
        header = "Chromosome,Old Soft Clipped,New Soft Clipped,Old Mismatch Rate,New Mismatch Rate,Old Multimap Rate,New Multimap Rate,Unmapped_old,Unmapped_new\n"
        f.write(header)
        for chrom in sorted(set(old_results.keys()).union(new_results.keys())):
            if chrom == "Unrecognized":
                continue  # Skip writing "Unrecognized" chromosomes to the output
            old = old_results.get(chrom, {'soft_clipped': 0, 'mismatches': 0, 'mapped_reads': 0, 'total_bases': 0, 'multimaps': 0})
            new = new_results.get(chrom, {'soft_clipped': 0, 'mismatches': 0, 'mapped_reads': 0, 'total_bases': 0, 'multimaps': 0})
            old_mapped = old_to_new_mapped.get(chrom, 0)
            new_mapped = new_to_old_mapped.get(chrom, 0)
            line = f"{chrom},{old['soft_clipped']},{new['soft_clipped']},{old.get('mismatch_rate', 0):.6f},{new.get('mismatch_rate', 0):.6f},{old.get('multimap_rate', 0):.6f},{new.get('multimap_rate', 0):.6f},{old_mapped},{new_mapped}\n"
            f.write(line)

    print(f"Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <old_bam_file> <new_bam_file> <equivalence_file> <output_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

