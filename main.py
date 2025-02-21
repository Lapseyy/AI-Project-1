# We have missionaries and Cannibals
# The boat capacity is at maximum 3

from search import *


class MissCannibalsVariant(Problem):


    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        """ Define goal state and initialize a problem """
        initial = (N1, N2, True)
        self.N1 = N1
        self.N2 = N2
        super().__init__(initial, goal)


if __name__ == '__main__':
    mc = MissCannibalsVariant(4,4)
