"""
Redis-like LRU Cache & AOF Persistence Simulator
Author: Portfolio Creator
Description: Simulates an in-memory key-value database with Least Recently Used (LRU)
             eviction limits and Append-Only File (AOF) recovery logs.
Language: English (100%)
"""

import os
from collections import OrderedDict

class RedisCacheSimulator:
    """In-memory key-value store with LRU cache eviction and AOF log replayer."""
    
    def __init__(self, capacity: int = 3, aof_path: str = "appendonly.aof"):
        self.capacity = capacity
        self.aof_path = aof_path
        self.cache = OrderedDict()
        self.replay_aof()

    def replay_aof(self):
        """Replays AOF log file transactions to restore database state on startup."""
        if not os.path.exists(self.aof_path):
            return
            
        with open(self.aof_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' ', 2)
                cmd = parts[0]
                
                if cmd == "SET" and len(parts) == 3:
                    key, val = parts[1], parts[2]
                    self._set_memory(key, val)
                elif cmd == "DEL" and len(parts) >= 2:
                    key = parts[1]
                    self._delete_memory(key)

    def _set_memory(self, key: str, value: str):
        """Sets value in-memory and handles LRU eviction rules."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Evict least recently used (first element) if capacity exceeded
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def _delete_memory(self, key: str):
        """Deletes key from memory dictionary."""
        if key in self.cache:
            del self.cache[key]

    def _write_aof(self, line: str):
        """Appends database transaction line to AOF file."""
        with open(self.aof_path, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    def set(self, key: str, value: str):
        """Sets key-value in database and writes SET log to AOF."""
        self._set_memory(key, value)
        self._write_aof(f"SET {key} {value}")

    def get(self, key: str) -> str:
        """Retrieves value from database, shifting key to most recently used."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def delete(self, key: str) -> bool:
        """Deletes key from database and writes DEL log to AOF."""
        if key in self.cache:
            self._delete_memory(key)
            self._write_aof(f"DEL {key}")
            return True
        return False

    def clear_aof(self):
        """Deletes the append-only file log on disk."""
        if os.path.exists(self.aof_path):
            os.remove(self.aof_path)
        self.cache.clear()
