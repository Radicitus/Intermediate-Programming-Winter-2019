from random import randrange
from influence import find_influencers3
import cProfile
import pstats                    

def random_graph (nodes : int, edges : int) -> {str:{str}}:
    g = {str(n) :set() for n in range(nodes)}
    
    for _ in range(int(edges)):
        n1 = str(randrange(nodes))
        n2 = str(randrange(nodes))
        if n1 != n2 and n1 in g and n2 not in g[n1]:
            g[n1].add(n2)
            g[n2].add(n1)
    return g


# Put code here to generate data for Quiz 8 problem #2
grph = random_graph(10000, 50000)
cProfile.run('find_influencers3(grph)', 'profile')
p = pstats.Stats('profile')
p.strip_dirs().sort_stats('ncalls').print_stats(20)
p.strip_dirs().sort_stats('tottime').print_stats(20)