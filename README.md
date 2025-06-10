
# Chord Intersection Count Algorithm
## Algorithm Description
For a given instance, let $n$ be the number of chords, $c_i$ be the $ith$ choord (in order of start radian measure), and $c_i[s]$ and $c_i[e]$ denote the start and end radian measures of $c_i$, respectively. The algorithm calculates the number of chord intersections as:
```math
[\sum_{i=0}^{n-1} \sum_{j=0}^{n-1} Q(c_i, c_j)]- 2 I([c_0[e], ..., c_{n-1}[e]]).
```
```math
Q(c_i, c_j) =
\begin{cases}
2\text{, if } \; c_i[s] < c_j[s] < c_j[e] < c_i[e]\\
1\text{, if } \; c_i[s] < c_j[s] < c_i[e] < c_j[e]\\
0\text{, otherwise} 
\end{cases}
```
```math
I(\textit{nums}) = \text{the number of inversions in } \textit{nums}
```

Both terms in the computation can be framed as inversion count problems, which can be solved by the standard mergesort method.

The dominant factor in the runtime complexity calculation is the invocation of mergesort with input size $n$; thus the algorithm runs in _O(nlog(n))_ time.
## Input
The program expects textfile inputs with one instance per line, formatted like the example below. I have provided an initial set of input instances in _input.txt_; please feel free to extend this file!
```
[], []
[0, 2], ['s1', 'e1']
[0, 1, 2, 4], ['s1', 's2', 'e1', 'e2']
```
## Running the Program
Prerequisites: Matplotlib, Numpy

The program expects the name of the input file name as a command line argument and can be run with the following command.
```
$ python count_chord_inters.py input.txt
```
The program outputs the file output.png which, for each input instance, displays  the chord count and the circle/chord diagram for convenience.
## Contact
Gordon Su - gsu37@gatech.edu
