from collections import defaultdict

class Solution:
    """
    There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.

    You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must 
    take course bi first if you want to take course ai.

    For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

    Return true if you can finish all courses. Otherwise, return false.
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        - We are given an integer numCourses representing the number of courses we need to take
        - Each course is labeled 0, 1, ..., numCourses - 1
        - We are given a list prerequisites where prerequisites[i] = [ai, bi] defines prerequesite bi for ai
            - In other words, we must take bi before we can take ai
            - In other words, prerequisites is an EDGE LIST that defines DIRECTIONAL EDGES ai --> bi
        - We are asked to return true if it is possible to finish all courses, else false

        Observation:
        - It is always possible to finish all courses so long as there are no CYCLES in the graph
            - A cycle represents a case where (directly or indirectly) two courses depend on each other
        - So, this question can be reframed: Return true if this graph is ACYCLIC, else false

        Algorithm:
        - How do we detect cycles in a graph?
            - This is a DIRECTIONAL graph
            - We can iterate over each node on the graph (since there may be non-connected components) and execute DFS to explore
              the entire graph
            - If we encounter a node twice, that must be a cycle!
        - ... Almost ...
            - If we encounter a node twice, i.e., we've already marked it as visited, it may have been visited along another path (another DFS)
            - Therefore, for each DFS must track what it has visited (for cycle detection), PLUS the overall visited set (for avoiding duplicate work)
        """
        # first, convert the edge list to an adjacency map
        def convert_edge_list_to_adjacencies(edge_list):
            adjacencies = defaultdict(list)
            for src, dst in edge_list: # src = course, dst = prereq (a dependency graph)
                adjacencies[src].append(dst)
            
            return adjacencies
        
        adjacencies = convert_edge_list_to_adjacencies(prerequisites)

        # we are going to use DFS to traverse the graph
        # at each step, we need to track two things:
        # 1. What we've seen *in total* (skip duplicate work)
        # 2. What we've seen *in this search* (detect cycles)
        # (why not one tracking list? it's very possible to visit node i multiple times as a terminating point of multiple paths)

        # since our courses are along [0, numCourses], we can use an array instead of a visited set
        visited = [False] * numCourses
        visited_in_search = [False] * numCourses

        # next, perform the actual cycle check
        def is_completable(course):
            # if we have visited the course in this search, we have definitionally found a cycle
            if visited_in_search[course]:
                return False
            
            # if we have visited the course elsewhere, we KNOW this course does not have a cycle
            if visited[course]:
                return True
            
            # now, mark the course as visited
            visited[course] = True

            # we are going to use backtracking to check for cycles:
            # 1. mark the course as visited in this search
            # 2. search all of its dependencies for cycles
            # 3. if we did not find a cycle, "undo" our choice and backtrack to the parent (reporting our result)

            # mark the course as visited
            visited_in_search[course] = True

            # search its dependencies for cycles
            for pre_req in adjacencies[course]:
                if not is_completable(pre_req):
                    return False # if a pre-req is not completable, THIS course is not completable
                
            # all of the pre-reqs can be completed, so this course can, too!
            # undo our "choice" and unmark the course as visited (so that other paths may terminate here safely)
            visited_in_search[course] = False

            return True
        
        for course in range(numCourses): # visit every course in case we have non-connected components
            if not visited[course] and not is_completable(course):
                return False
            
        return True

