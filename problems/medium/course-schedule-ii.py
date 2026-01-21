from collections import defaultdict, deque

class Solution:
    """
    There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
    
    You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must
    take course bi first if you want to take course ai.

    For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

    Return the ordering of courses you should take to finish all courses. 
    
    If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
    """

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Task:
        - We are given an integer numCourses that we have to take, each labeled [0, numCourses - 1]
        - We are given an array of prerequisites where prerequisites[i] = [ai, bi] defines bi as a prerequisite of ai
        - We are asked to return the ORDERING of courses
            - If there are many valid answers, return any
            - If there are no valid answers, return an empty array
        
        Observations:
        - We are given an EDGE LIST prerequisites that defines DIRECTIONAL EDGES in a prerequisite graph FROM bi TO ai
        - It is IMPOSSIBLE to complete all of the courses if there is a single cycle in the graph
        - Possible orderings can be obtained from a TOPOLOGICAL SORT of the directed graph
        - That is, we should start from courses with no requirements and then turn to the courses those unlock, and so on...

        Algorithm:
        - We can use KHAN'S ALGORITHM and BFS to return the DIRECTED ACYCLIC GRAPH in topological order
            - In Khan's algorithm, we need an ADJACENCY MAP, so we first construct this from our edge list (O(p), p = len(prerequisites))
            - We then take the ADJACENCY MAP and build an IN-DEGREE array where we track how many incoming edges each node has
            - We run BFS, starting with the nodes with in-degree = 0, and decrementing the in-degree of each neighbor by one
            - Every time we decrement the in-degree of a neighbor and find that its in-degree is equal to zero, we add it to the queue
            - Any neighbor that doesn't reach in-degree of zero will not be added to the queue (or the result set), so there must be
              a cycle leading to it
        - If it is NOT a DAG, then we must return an empty array
        - How do we know it's not a DAG? The result of Khan's algorithm will be of a shorter length than numCourses!
        """

        # first, convert the edge list to a more usable adjacency map, and track the in-degrees of each course
        # in other words, create:
        # 1. a map of pre-req --> dependent courses
        # 2. an array of the NUMBER of pre-reqs for each course
        adjacencies = defaultdict(list)
        in_degrees = [0] * numCourses

        for course, pre_req in prerequisites: # O(p), p = len(prerequisites)
            adjacencies[pre_req].append(course)
            in_degrees[course] += 1

        # next, execute Khan's algorithm
        # because Khan's algorithm uses BFS, we must use a queue
        # we don't need a visited set because we only visit courses once they become "takable" (so visit exactly once)
        queue = deque()

        for course, in_degree in enumerate(in_degrees): # O(n), n = numCourses
            if in_degree == 0:
                queue.append(course)

        # track the result set
        courses = []

        while queue: # continue until queue exhausted (worst case is we traverse the entire graph, O(n))
            course = queue.popleft()

            # this course had no remaining pre-reqs, so we can safely "take" the course
            courses.append(course)

            for dependency in adjacencies[course]: # if we explore each node, this will (in sum) be O(p)
                # for each course that DEPENDS on this course as a pre-req, reduce its in-degree by one
                # (there is one fewer class we need to take in order to take it!)
                in_degrees[dependency] -= 1

                # if there are no more pre-requisites to take the dependent course, we can take it next!
                if in_degrees[dependency] == 0:
                    queue.append(dependency)
                
        if len(courses) < numCourses:
            # if there were any cycles in the graph, we would stop running BFS while leaving some courses unvisited
            return []

        return courses

        
### Testing
# numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
# in_degrees = [0, 1, 1, 2], queue = [0], courses = []
# first iteration: in_degrees = [0, 0, 0, 2], queue = [1, 2], courses = [0]
# second iteration: in_degrees = [0, 0, 0, 1], queue = [2], courses = [0, 1]
# third iteration: in_degrees = [0, 0, 0, 0], queue = [3], courses = [0, 1, 2]
# fourth iteration: in_degrees = [0, 0, 0, 0], queue = [], courses = [0, 1, 2, 3] // return [0, 1, 2, 3]