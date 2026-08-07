"""
Redis Simulator CLI
Author: Portfolio Creator
Description: CLI driver to execute cache commands and demonstrate AOF state recovery.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from redis_simulator import RedisCacheSimulator

def main():
    parser = argparse.ArgumentParser(
        description="Redis-like Cache Simulator - Play with LRU eviction and AOF persistence."
    )
    parser.add_argument(
        "-c", "--capacity",
        type=int,
        default=3,
        help="In-memory cache capacity (default: 3)."
    )
    parser.add_argument(
        "-a", "--aof",
        default="appendonly.aof",
        help="Path to Append-Only File (default: appendonly.aof)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Redis-like Cache Simulator with LRU and AOF Persistence")
    print("=" * 60)
    print(f"[*] Max Capacity: {args.capacity} items")
    print(f"[*] AOF Path    : {args.aof}")

    try:
        # Initialize (replays existing AOF logs)
        print("[*] Replaying AOF transaction logs to restore memory...")
        db = RedisCacheSimulator(capacity=args.capacity, aof_path=args.aof)
        
        print(f"[+] Loaded state: {dict(db.cache)}")
        
        # Run some demo writes
        print("\n[*] Performing SET operations...")
        db.set("user:101", "Alice")
        db.set("user:102", "Bob")
        db.set("user:103", "Charlie")
        print(f"[+] Cache State: {dict(db.cache)}")
        
        print("\n[*] Accessing 'user:101' (makes it most recently used)...")
        db.get("user:101")
        print(f"[+] Cache State: {dict(db.cache)}")
        
        print("\n[*] Setting new key 'user:104' (triggers LRU eviction of 'user:102')...")
        db.set("user:104", "David")
        print(f"[+] Cache State: {dict(db.cache)}")
        
        print("\n[*] Deleting 'user:103'...")
        db.delete("user:103")
        print(f"[+] Cache State: {dict(db.cache)}")
        
        # Verify persistence
        print("\n[*] Re-initializing database to verify AOF recovery...")
        db2 = RedisCacheSimulator(capacity=args.capacity, aof_path=args.aof)
        print(f"[+] Reconstructed Cache State: {dict(db2.cache)}")
        
        # Clean up for demo
        print("\n[*] Cleaning up AOF logs...")
        db2.clear_aof()
        print("[+] Log files deleted successfully.")
        
    except Exception as e:
        print(f"[-] Database simulator failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
