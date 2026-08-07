# Redis-like LRU Cache & AOF Persistence Simulator

A software systems engineering utility that simulates an in-memory key-value database featuring bounded capacity rules (Least Recently Used - **LRU Cache Eviction**) and **Append-Only File (AOF)** database persistence log replay.

## Features
- **LRU Cache Eviction**: Bounded memory capacity implemented using Python `OrderedDict` counters, automatically evicting the least recently accessed keys when capacity limits are exceeded.
- **Write-Ahead logging / AOF Persistence**: Writes database modifications (`SET`, `DEL`) in real-time to a flat `appendonly.aof` file stream.
- **Crash Recovery Replayer**: Automatically parses and replays the AOF log file on database startup to reconstruct the memory state.

## Project Structure
- `redis_simulator.py`: OrderedDict cache layers, AOF writers, and command replays.
- `main.py`: Command-line interface driver.
- `test_simulator.py`: Unit test suite verifying LRU state evictions and AOF file logs.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To run the database simulator:
```bash
python main.py --capacity 3 --aof appendonly.aof
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_simulator.py
```
