from search import *

class MissCannibalsVariant(Problem):
    """ The problem of Missionaries and Cannibals. 
    N1 and N2 are the total number of missionaries and cannibals starting from the left bank.
    A state is represented as a 3-tuple, two numbers and a boolean:
    state[0] is the number of missionaries on the left bank (note: the number of missionaries on the right bank is N1-m)
    state[1] is the number of cannibals on the left bank (note: the number of cannibals on the right bank is N2-c)
    state[2] is true if the boat is at the left bank, false if at the right bank.
    """

    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        """Define goal state and initialize a problem."""
        initial = (N1, N2, True)
        self.N1 = N1
        self.N2 = N2
        super().__init__(initial, goal)

    def actions(self, state):
        """Return a list of valid actions from the given state."""
        m, c, onLeft = state
        possible_actions = ['M', 'C', 'MM', 'MC', 'CC', 'MMM', 'MMC', 'MCC', 'CCC']
        valid_actions = []
        direction = 1 if onLeft else -1

        for action in possible_actions:
            num_m = action.count('M')
            num_c = action.count('C')
            new_m = m - direction * num_m
            new_c = c - direction * num_c

            if 0 <= new_m <= self.N1 and 0 <= new_c <= self.N2:
                if (new_m == 0 or new_m >= new_c) and \
                   (self.N1 - new_m == 0 or self.N1 - new_m >= self.N2 - new_c):
                    valid_actions.append(action)

        return valid_actions

    def result(self, state, action):
        """Return the resulting state after applying an action."""
        m, c, onLeft = state
        num_m = action.count('M')
        num_c = action.count('C')
        direction = 1 if onLeft else -1
        new_m = m - direction * num_m
        new_c = c - direction * num_c
        new_onLeft = not onLeft

        return (new_m, new_c, new_onLeft)

if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    print(mc.actions((3, 3, True)))
    print(mc.result((3, 3, True), 'MC'))
    path = depth_first_graph_search(mc).solution()
    print("DFS Solution:", path)
    path = breadth_first_graph_search(mc).solution()
    print("BFS Solution:", path)

    assert mc.actions((0, 0, False)) == [], "No actions should be available when goal is reached" #test egde cases 
    path_dfs = depth_first_graph_search(mc).solution() #test for search algos 
    path_bfs = breadth_first_graph_search(mc).solution()
    assert isinstance(path_dfs, list), "DFS should return a list"
    assert path_dfs != [], "DFS should return a solution"
    assert isinstance(path_bfs, list), "BFS should return a list"
    assert path_bfs != [], "BFS should return a solution"