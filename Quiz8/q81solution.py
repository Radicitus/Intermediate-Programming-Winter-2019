from random import randrange
from influence import find_influencers
from goody import irange
from performance import Performance

global grph

def random_graph (nodes : int, edges : int) -> {str:{str}}:
    g = {str(n) :set() for n in range(nodes)}
    
    for i in range(int(edges)):
        n1 = str(randrange(nodes))
        n2 = str(randrange(nodes))
        if n1 != n2 and n1 in g and n2 not in g[n1]:
            g[n1].add(n2)
            g[n2].add(n1)
    return g


# Put code here to generate data for Quiz 8 problem #1
def create_random():
    global grph
    grph = random_graph(nodes, nodes * 5)


nodes = 100
while nodes <= 12800:
    create_random()
    performance = Performance(code=lambda: find_influencers(graph=grph), setup=lambda: create_random(),
                              times_to_measure=5, title="find_influencers of size " + str(nodes))
    for i in irange(5):
        performance.evaluate()
    performance.analyze()
    nodes = nodes * 2
    print()

