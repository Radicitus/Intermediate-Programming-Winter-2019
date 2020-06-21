import prompt
from goody       import safe_open
from math        import ceil 
from collections import defaultdict


def read_graph(open_file : open) -> {str:{str}}:
    graph = defaultdict(set)
    for line in open_file:
        if ';' not in line:
            if line not in graph:
                graph[line] = set()
        else:
            s,d = line.rstrip().split(';')
            graph[s].add(d)
            graph[d].add(s)
    open_file.close()
    return graph


def graph_as_str(graph : {str:{str}}) -> str:
#     answer =''
#     for s,d in sorted(graph.items()):
#         answer += '  '+s+' -> '+str(sorted(d))+'\n'
#     return answer
    return '\n'.join('  '+s+' -> '+str(sorted(d)) for s,d in sorted(graph.items()))+'\n'


def find_influencers(graph : {str:{str}}, tip : float = .5, trace : bool = False) -> {str}:
    infl_dict = {v:[len(friends)-ceil(len(friends)*tip) if len(friends) != 0 else -1, len(friends),v] for v,friends in graph.items()}
    while True:
        remove_candidates = [(dist,friends,v) for (dist,friends,v) in infl_dict.values() if dist >= 0]
        if trace: print('influencer dictionary =',infl_dict, '\nremoval candidates    =',remove_candidates)
        if remove_candidates == []:
            return set(infl_dict)
        d,f,v =min(remove_candidates)
        if trace: print((d,f,v),'is the smallest candidate\nRemoving',v,'as key from influencer dictionary; decrementing friend\'s values there\n')
        del infl_dict[v]
        for f in graph[v]:
            if f in infl_dict:
                infl_dict[f][0] -= 1
                infl_dict[f][1] -= 1

def find_influencers2(graph : {str:{str}}, tip : float = .5, trace : bool = False) -> {str}:
    core = {v for v in graph.keys()}
    infl_dict = {v:[len(friends)-ceil(len(friends)*tip) if len(friends) != 0 else -1,len(friends),v] for v,friends in graph.items()}
    while True:
        remove_candidates = [t for t in infl_dict.values() if t[0]>=0]
        if trace:
            print('influencer dictionary =',infl_dict)
            print('candidates for removal =',remove_candidates)
        if remove_candidates == []:
            return core
        d,f,v = min(remove_candidates)
        if trace:
            print('Removing',(d,f,v),'from influencer dictionary; decrementing friend\'s values there')
            print()
        del infl_dict[v]
        core.remove(v)
        for f in graph[v]:
            if f in infl_dict:
                infl_dict[f][0] -= 1


def find_influencers3(graph : {str:{str}}, tip : float = .5, trace : bool = False) -> {str}:
    from adjustablepriorityqueue import PriorityQueue
    answer    = {v for v,friends in graph.items() if len(friends) == 0}
    infl_dict = {v:[len(friends)-ceil(len(friends)*tip),len(friends),v] for v,friends in graph.items() if len(friends) > 0}
    pq        = PriorityQueue(initial_contents = set(infl_dict.keys())-answer, key = lambda x : infl_dict[x], reverse = True)
    while not pq.is_empty():
        if trace:
            print('influencer dictionary =',infl_dict)
            print('priority queue =',pq)
            print('answer =',answer)
        v = pq.remove()
        d,f,v = infl_dict[v]
        if trace:
            print('Removing',(d,f,v),'from influencer dictionary; decrementing friend\'s values there')
            print()
        del infl_dict[v]
        for f in graph[v]:
            if f in infl_dict:
                infl_dict[f][0] -= 1
                pq.updated(f)
                if infl_dict[f][0] < 0:
                    answer.add(f)
                    del infl_dict[f]
                    pq.remove()
    return answer                  


def all_influenced(graph : {str:{str}}, influencers : {str}, tip : float = .5) -> {str}:
    influenced_dict = {v:(v in influencers) for v in graph.keys()}
    influenced_num  = len(influencers)
    while True:
        for v,i in influenced_dict.items():
            if not i:
                if len(graph[v]) != 0 and sum(influenced_dict[f] for f in graph[v]) >= ceil(len(graph[v])*tip):
                    influenced_dict[v] = True
        old_influenced, influenced_num = influenced_num, sum(i for i in influenced_dict.values())
        if influenced_num == old_influenced:
            return set(v for v in influenced_dict if influenced_dict[v])
       
            
    
if __name__ == '__main__':
    graph_file = safe_open('Enter a file storing a friendship graph', 'r', 'Could not find that file',default='graph1.txt')
    graph = read_graph(graph_file)
    print('Graph: node -> list of all friend nodes\n' + graph_as_str(graph))
    
    tip = .5 #tip = prompt.for_float('Enter tip percentage', is_legal = lambda x : 0 <=x<=1, default = .5)
    influencers = find_influencers(graph,tip,prompt.for_bool('Trace the Algorithm',default=True))
    print('Influencers =', influencers)
    
    while True:
        influencer_set = prompt.for_string('\nEnter influencers set (or else quit)', default=str(influencers), is_legal = lambda core : core == 'quit' or all(c in graph for c in eval(core)))
        if influencer_set == 'quit':
            break;
        influenced = all_influenced(graph,eval(influencer_set),tip)
        print('All Influenced ('+str(100*len(influenced)/len(graph))+'% of graph)=',influenced,'\n')
            
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()

