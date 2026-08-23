# Crossnumber Solver

A Python-based constraint solver developed for the **Ritangle Challenge**, a mathematical crossnumber puzzle competition.

The solver represents each cell of a crossnumber grid as a set of possible digits and progressively eliminates impossible values using the mathematical constraints provided by the clues.

## Overview

Unlike a conventional crossword, a crossnumber uses numerical clues rather than words. Solving the puzzle requires combining mathematical properties with the constraints created where across and down numbers intersect.

This project automates that process using **constraint propagation**, candidate generation and recursive search.

```text
                  Mathematical Clues
                         │
                         ▼
                Generate Candidates
                         │
                         ▼
              ┌────────────────────┐
              │  Constraint Grid   │
              │                    │
              │  Possible digits   │
              │  for every cell    │
              └─────────┬──────────┘
                        │
                        ▼
                Propagate Constraints
                        │
                        ▼
                  Reduced Candidates
                        │
                        ▼
                 Search Remaining
                   Possibilities
                        │
                        ▼
                  Complete Grid
```

## How It Works

Each grid cell maintains a list of possible digits.

For example:

```text
Cell → [1, 3, 7]
```

As clues are processed, impossible candidates are removed.

When a clue has several possible numbers, those possibilities are compared against the digits already permitted by the intersecting cells. This allows information from one clue to constrain another.

The process is repeated until no further changes can be made.

```python
cross, clues = numberCruncher(cross, prev, clues)
```

The `numberCruncher` function repeatedly processes the clues until the state of the grid stops changing.

## Constraint Propagation

The core of the solver is iterative constraint propagation.

For each clue:

1. Generate all mathematically valid candidate numbers.
2. Compare candidates with the current grid state.
3. Remove candidates that conflict with intersecting digits.
4. Update the possible digits in the grid.
5. Repeat until the grid reaches a stable state.

This is particularly useful for crossnumbers because solving one clue can significantly restrict the possibilities for several other clues.

## Mathematical Constraints

The solver includes functions for generating candidates based on several mathematical properties, including:

* Prime numbers
* Powers
* Triangular numbers
* Multiples
* Factors
* Palindromes

For example, the solver can generate all numbers of a specified length satisfying a prime-number constraint or find numbers that are factors of a given value.

## Search and Backtracking

Some puzzles cannot be solved entirely through simple constraint propagation.

For these cases, the solver can explore possible combinations recursively.

The search process:

1. Select possible values for a set of clues.
2. Create a copy of the current grid.
3. Apply the selected values.
4. Check whether the resulting grid is valid.
5. Continue recursively if the state remains possible.
6. Reject branches that produce contradictions.

The recursive search is implemented through functions such as `findAllPossi` and `findAllClueSums`.

This effectively turns the problem into a **constraint satisfaction problem (CSP)**.

## Example Grid

The current implementation includes the grid structure for a Ritangle puzzle:

```text
┌───┬───┬───┐
│   │   │   │
├───┼───┼───┤
│   │   │   │
├───┼───┼───┤
│   │   │   │
└───┴───┴───┘
```

Across and down clues are represented using their coordinates within the grid.

## Project Structure

```text
Crossnumber-Solver/
│
├── crossnumber.py              # Main solver and puzzle configuration
├── crossnumbersolvertools.py   # Constraint and mathematical utilities
├── tests.txt                   # Test cases
├── README.md                   # Project documentation
├── LICENSE                     # GPL-3.0 licence
└── .gitignore
```

## Running

Clone the repository:

```bash
git clone https://github.com/TobyStanislaus/Crossnumber-Solver.git
cd Crossnumber-Solver
```

Run the solver with:

```bash
python crossnumber.py
```

The puzzle configuration is defined in `crossnumber.py`, including the grid layout and clue definitions.

## Technologies

* **Python**
* Constraint satisfaction
* Constraint propagation
* Recursive search
* Backtracking
* Combinatorial algorithms
* Number theory
* Permutations

## Key Concepts

This project explores several algorithmic concepts:

### Constraint Satisfaction

The solution is represented as a set of variables with restricted domains. Each grid digit has a domain containing its currently possible values.

### Constraint Propagation

Information from one clue is propagated through the grid to reduce the possible values of intersecting clues.

### Backtracking

When deterministic constraint propagation is insufficient, the solver explores possible assignments and abandons branches that lead to contradictions.

### Combinatorial Search

The solver uses permutations of clues when investigating combinations of values that satisfy more complicated mathematical relationships.

## Future Improvements

Possible improvements include:

* Generalising the solver to arbitrary grid sizes
* Creating a puzzle input format rather than hard-coding puzzles
* Improving the efficiency of candidate generation
* Adding stronger constraint-propagation heuristics
* Implementing a minimum-remaining-values variable-selection heuristic
* Adding automated benchmarking
* Expanding the supported mathematical clue types
* Adding a graphical interface for entering and solving puzzles
* Improving the test suite

## Licence

This project is licensed under the **GNU General Public License v3.0**.
