# Game of Life

CSPB 2270: Implementation of Conway's Game of Life
--------------------------------------------------

### Purpose

The goal of this project was to work with cellular automata for the first time in the context of
John Conway's Game of Life. A peripheral goal was to gain an introductory level of exposure to the
PyGame framework, as well as any performance challenges that arose from the implementation of the
simulation.

### Algorithm

The Game of Life is traditionally represented as an infinite grid of cells which each have eight
neighbors. Each cell is required to make a decision (whether to be born, continue living, die, or stay dead),
based on 3 simple rules:

1. Birth Rule: A dead cell with 3 live neighbors will become live in the next generation.
2. Death Rule
   - Isolation: A live cell with 0 or 1 live neighbors will die in the next generation.
   - Overcrowding: A dead cell with 4 or more live neighbors will die in the next generation.
3. Survival Rule: A live cell with 2 or 3 neighbors will remain alive in the next generation.

Every time a decision is made based on the above three rules, the state is represented in the next
generation.

### Implementation

The design of my simulation was straightforward. A `World` class was created with a single input that
is used to input the `width` of the grid. The representation of the grid was chosen to be a toroid
wrap-around 2-D grid, with simple modular arithmetic to find neighbors along the edges of the grid. The
`World` class stores a 2d list of booleans lists. A duplicate 2d list stores the state updates before
transitioning to the next generation, and once analysis is completed, the cells grid is swapped with
the transition grid. All of this is taken care of in the `tick` function. The tick function also updates
statistics such as population, board density (live cells per cell). On each tick, when a cell either
transitions to a dead or alive state, it then increments or decrements all eight of its neighbors. This
is an efficient way to handle the ticks without calculating neighbor counts of each cell redundantly.
Booleans where chose rather than using another class in order to maintain some efficiency on each cycle.

### Challenges

The first optimization to reduce redundant neighbor calculations was effective, but then I proceeded to
fall in the trap of getting obsessed over performance. One of the next steps I took was to try converting
all logical control flow structures into bitwise operations and matching on integers in switch statements.
Much to my surprise (and chagrin), I actually noticed a significant performance degradation. My next
step was to try some sort of parallelized implementation. Normal threads wouldn't do the job in Python
due to limitations imposed by the GIL (global interpreter lock), which would do little more than force
me into a plethora of context switches on every tick. The next step was to try using the `multiprocessing`
module to map chunks of rows across N process (where N = CPU count). Unsurprisingly, the overhead of
maintaining a process pool was still too much. I eventually found some success using Jython, which does
not suffer from limitations imposed by the GIL, but failed to get PyGame to function in that implementation.
Nonetheless, the performance is decent up to about 600 x 600 cells.

### Running the simulation

Python 3.11 or above is required. It may work on versions below this, however, I developed on these
versions and thus recommend 3.11 or above just to be safe. PyGame is also a dependency required to run
the program. After cloning this repo, go to the root of the repo and enter:

```
# activates a virtual environment
python -m venv venv
```

Next, we need to activate the virtual environment and install dependencies with:

```
# activate the environment
venv\Scripts\activate

# install dependencies using the requirements.txt file
pip install -r requirements.txt

# run the program
python src\main.py
```

A GUI will open up with brief instructions on what keybindings to use when running the simulation.
