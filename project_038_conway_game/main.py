"""
Conway Simulator CLI
Author: Portfolio Creator
Description: CLI driver to execute cellular automata grid cycles.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conway_simulator import ConwaySimulator

def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Run cellular automata grid simulations."
    )
    parser.add_argument(
        "-p", "--pattern",
        default="glider",
        choices=["block", "beehive", "blinker", "glider", "random"],
        help="Initial grid pattern (default: glider)."
    )
    parser.add_argument(
        "-o", "--output",
        default="conway_state.png",
        help="Path to save final grid plot (default: conway_state.png)."
    )
    parser.add_argument(
        "-g", "--generations",
        type=int,
        default=20,
        help="Number of simulation steps to run (default: 20)."
    )
    parser.add_argument(
        "-r", "--rows",
        type=int,
        default=30,
        help="Number of rows in simulation grid (default: 30)."
    )
    parser.add_argument(
        "-c", "--cols",
        type=int,
        default=30,
        help="Number of columns in simulation grid (default: 30)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Conway's Game of Life Simulation Pipeline")
    print("=" * 60)
    print(f"[*] Grid Dimensions: {args.rows}x{args.cols}")
    print(f"[*] Initial Pattern: {args.pattern.upper()}")
    print(f"[*] Generations:     {args.generations} steps")
    print(f"[*] Output Plot:     {args.output}")

    try:
        simulator = ConwaySimulator(rows=args.rows, cols=args.cols)
        print("[*] Populating initial grid presets...")
        simulator.set_pattern(args.pattern)
        
        print(f"[*] Running simulation loop for {args.generations} steps...")
        for step in range(args.generations):
            simulator.step_generation()
            
        print("\n" + "=" * 60)
        print("Simulation Metrics Results")
        print("=" * 60)
        active_cells = int(simulator.grid.sum())
        total_cells = args.rows * args.cols
        active_ratio = (active_cells / total_cells) * 100
        print(f"[*] Active (Live) Cells: {active_cells} / {total_cells} ({active_ratio:.2f}%)")
        
        print("\n[*] Saving final grid state plot...")
        simulator.plot_grid(args.output, generation=args.generations)
        print(f"[+] Output state plot successfully saved.")
        
    except Exception as e:
        print(f"[-] Simulation pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
