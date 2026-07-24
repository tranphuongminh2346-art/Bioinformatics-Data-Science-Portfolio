"""
DNA Sequence Analyzer CLI Tool
Author: Portfolio Creator
Description: Command-line interface to analyze DNA sequences, detect motifs, and plot GC content sliding windows.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dna_analyzer import parse_fasta, DNASequence

def main():
    parser = argparse.ArgumentParser(
        description="DNA Sequence Analyzer & Visualizer - Analyze sequences, transcribe, translate, search motifs, and plot GC content."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input FASTA file containing DNA sequence(s)."
    )
    parser.add_argument(
        "-w", "--window",
        type=int,
        default=50,
        help="Sliding window size for GC content calculation (default: 50)."
    )
    parser.add_argument(
        "-s", "--step",
        type=int,
        default=10,
        help="Sliding window step size (default: 10)."
    )
    parser.add_argument(
        "-p", "--plot",
        help="File path to save the generated GC content sliding window plot (e.g., gc_plot.png)."
    )
    parser.add_argument(
        "-m", "--motif",
        help="Optional DNA motif to search for in the sequence (e.g., ATG)."
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Parsing FASTA file: {args.input}...")
        sequences = parse_fasta(args.input)
        print(f"Found {len(sequences)} sequence(s).\n")
    except Exception as e:
        print(f"Error parsing FASTA file: {e}", file=sys.stderr)
        sys.exit(1)

    if not sequences:
        print("No sequences found in the file.", file=sys.stderr)
        sys.exit(1)

    # Process each sequence
    for idx, dna_seq in enumerate(sequences, 1):
        print("=" * 60)
        print(f"Sequence #{idx}: {dna_seq.header}")
        print("=" * 60)
        
        # Length & Nucleotide Frequencies
        seq_len = dna_seq.get_length()
        print(f"Length: {seq_len} bp")
        print(f"Overall GC Content: {dna_seq.gc_content():.2f}%\n")
        
        print("Nucleotide Frequencies:")
        freqs = dna_seq.nucleotide_frequencies()
        for base, stats in freqs.items():
            print(f"  {base}: {stats['count']} ({stats['percentage']:.2f}%)")
        print()

        # Transcription (First 60 bases for summary)
        rna = dna_seq.transcribe()
        rna_summary = rna[:60] + "..." if len(rna) > 60 else rna
        print(f"RNA Transcript (transcribed, first 60 bp):")
        print(f"  {rna_summary}\n")

        # Translation (First 20 amino acids for summary)
        protein = dna_seq.translate()
        prot_summary = protein[:20] + "..." if len(protein) > 20 else protein
        print(f"Protein Sequence (translated, first 20 aa):")
        print(f"  {prot_summary} (Total Length: {len(protein)} aa)\n")

        # Motif Search
        if args.motif:
            motif_positions = dna_seq.find_motifs(args.motif)
            print(f"Motif Search for '{args.motif.upper()}':")
            print(f"  Matches Found: {len(motif_positions)}")
            if motif_positions:
                pos_str = ", ".join(map(str, motif_positions[:10]))
                if len(motif_positions) > 10:
                    pos_str += ", ..."
                print(f"  Start positions (0-based): [{pos_str}]")
            print()

        # Plot GC content
        if args.plot:
            # If multiple sequences are present, modify the filename to avoid overwriting
            plot_path = args.plot
            if len(sequences) > 1:
                base, ext = os.path.splitext(args.plot)
                plot_path = f"{base}_{idx}{ext}"
                
            try:
                print(f"Generating GC content plot with window size {args.window} and step size {args.step}...")
                dna_seq.plot_gc_content(plot_path, window_size=args.window, step_size=args.step)
                print(f"Plot successfully saved to: {plot_path}\n")
            except Exception as e:
                print(f"Error generating plot: {e}", file=sys.stderr)

    print("Analysis complete.")

if __name__ == "__main__":
    main()
