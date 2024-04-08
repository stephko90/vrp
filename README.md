# vrp
A Python solution for the VRP problem

This assessment is written in Python and has been tested against both Python 2&3
Please ensure that Python is installed in order to run this assessment properly

To run this project:
1. Clone the project `git clone git@github.com:stephko90/vrp.git`
2. (Optional) Change to the /vrp directory `cd /vrp`
3. Use Python to run the assessment against a *single file* `python assessment.py {path/to/problems}`
(This assessment uses the same logic that is used to run the `evaluateAssessment.py` in the provided package)

This assessment contains two solutions (I wanted to see if one resulted in a more optimal solution)

The first (`assessment.py`) uses a close approximation to the nearby neighbor algorithm with a greedy node selection process.
The solution can be further improved by improving the node selection process (in my head I'm imagining either a BFS selection process
or a weighted selection process that tries to select routes between trips that have close pickup and dropoff points)

The second solution (`assesssment2.py`) was an attempt to see if an adjacency graph would create a more optimal solution. The adjacency graph adds an edge containing
the distance between each node in the graph. The selection process will then attempt to group routes with minial distances between the
dropoff and pickup points while fitting in the max allotted time. This solution was created at the 11th hour so with more time and research 
I'm confident that this would be more optimal that the first assessment (at the cost of efficiency), but I wasn't able to get the optimal solution in the end.