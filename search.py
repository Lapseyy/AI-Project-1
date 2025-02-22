#this is the search class refereneced in documentation
"""
Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions.
"""
import sys
from collections import deque
from utils import *

class Problem():
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError 

def depth_first_graph_search(problem):
    """Search the deepest nodes in the search tree first using graph search."""
    frontier = [(Node(problem.initial))]  # Stack
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                       if child.state not in explored and child not in frontier)
    return None

def breadth_first_graph_search(problem):
    """Search shallowest nodes in the search tree first using graph search."""
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])  # Queue
    explored = {node.state}
    while frontier:
        node = frontier.popleft()
        for child in node.expand(problem):
            s = child.state
            if problem.goal_test(s):
                return child
            if s not in explored and child not in frontier:
                explored.add(s)
                frontier.append(child)
    return None

class Node:
    """A node in a search tree."""
    
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self, problem):
        """Return a list of nodes reachable from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Return a child node, given an action."""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                        problem.path_cost(self.path_cost, self.state,
                                        action, next_state))
        return next_node
    
    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [] if self.parent is None else self.parent.solution() + [self.action]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    
    def __hash__(self):
        return hash(self.state)
    
    #tests
    def test_goal_test():
        problem = Problem(initial=0, goal=5)
        assert problem.goal_test(5) == True, "Failed: Goal state should return True"
        assert problem.goal_test(3) == False, "Failed: Non-goal state should return False"
        print("goal_test() passed all tests.")
