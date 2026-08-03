# Conway's Game of Life Cellular Automaton

A simulation pipeline of **Conway's Game of Life** cellular automaton rules. It generates cell coordinate grids, initializes preset structures (blocks, beehives, blinkers, gliders), computes generations using periodic toroidal boundary wrapping, and saves cell state map configurations.

## Features
- **Preset Patterns Library**: Initializes stable state blocks/beehives, blinker oscillators, and glider moving structures.
- **Toroidal Wrapping Coordinates**: Uses rolling coordinate shifts to implement periodic boundary conditions wrapping borders around the grid.
- **Conway's Transition Rules**: Implements survival, birth, underpopulation, and overpopulation rules.
- **Grid State Map Exporter**: Plots binary active/dead cell maps.

## Project Structure
- `conway_simulator.py`: State rules, coordinate wrapping, and plotters.
- `main.py`: Command-line interface driver.
- `test_simulator.py`: Unit test suite verifying stable states and oscillator periods.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To simulate cells:
```bash
python main.py --pattern glider --generations 20 --output conway_state.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_simulator.py
```
