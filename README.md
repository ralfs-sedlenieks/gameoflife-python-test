# Usage

From the project folder, run `python gameoflife.py`

Parameters:

* Height (default: 100)
* Width (default: 100)
* Multiplier (default: 1)
* Input file

Running with params: `python gameoflife.py 100 100 4`

Loading existing state: `python gameoflife.py -f state.txt`

State file format:

```
HEIGHT WIDTH MULTIPLIER
X1 Y1
X2 Y2
... (only specify coordinates for live cells)
```

# Requirements:

* Python 3
* numpy
* pygame
