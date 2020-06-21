# Submitter: cencenzo(Encenzo, Chloe)
# Partner  : crsherry(Sherry, Cameron)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import copy


class GraphError(Exception):
    pass
 
 
class Graph:
    def legal_tuple2(self,t):
        return type(t) is tuple and len(t) == 2 and\
               type(t[0]) is str and type(t[1]) is str

    def legal_tuple3(self,t):
        return type(t) is tuple and len(t) == 3 and\
               type(t[0]) is str and type(t[1]) is str and self.is_legal_edge_value(t[2])

    def __init__(self,legal_edge_value_predicate,*args):           
        self.is_legal_edge_value = legal_edge_value_predicate
        self.edges = {}
        for a in args:
            if self.legal_tuple3(a):
                og_node, dest_node, edge = a[0], a[1], a[2]
                if og_node in self.edges.keys():
                    if dest_node not in self.edges[og_node].keys():
                        self.edges[og_node].update({dest_node: edge})
                    else:
                        raise GraphError
                else: self.edges[og_node] = {dest_node: edge}
                if dest_node not in self.edges.keys():
                    self.edges[dest_node] = {}
            elif type(a) == str:
                if a not in self.edges.keys():
                    self.edges[a] = {}
                else:
                    raise GraphError
            else:
                raise GraphError

    def __str__(self):
        graph = []
        for og_node, map in self.edges.items():
            if len(map) == 0:
                s = og_node + ':\n'
            else:
                s = og_node + ': '
                for dest_node, edge in map.items():
                    s += dest_node + '('+str(edge)+'), '
                s = s.rstrip(', ') + '\n'
            graph.append(s)
        return "\nGraph:\n  " + '  '.join(graph).rstrip('\n')

    def __getitem__(self, item):    
        if type(item) == str and item in self.edges:
            return self.edges[item]
        elif self.legal_tuple2(item):
            og_node, dest_node = item[0], item[1]
            if og_node in self.edges and dest_node in self.edges and item[1] in self.edges[og_node]:
                return self.edges[og_node][dest_node]
            else:
                raise GraphError
        else:
            raise GraphError

    def __setitem__(self, item, value):
        if self.legal_tuple2(item) and self.is_legal_edge_value(value):
            og_node, dest_node = item[0], item[1]
            if og_node in self.edges:
                self.edges[og_node][dest_node] = value
            else:
                self.edges[og_node] = {dest_node : value}
            if dest_node not in self.edges:
                self.edges[dest_node] = {}
        else:
            raise GraphError

    def node_count(self):
        return len([k for k in self.edges.keys()])
    
    def __len__(self):
        return sum([len([k for k in map.keys()]) for map in self.edges.values()])
    
    def out_degree(self, node):
        if type(node) == str and node in self.edges:
            return len([k for k in self.edges[node].keys()])
        else:
            raise GraphError
    
    def in_degree(self, node):
        if type(node) == str and node in self.edges:
            in_degree = 0
            for map in self.edges.values():
                if node in map.keys():
                    in_degree += 1
            return in_degree
        else:
            raise GraphError
    
    def __contains__(self, item):
        if type(item) == str:
            return item in self.edges
        elif self.legal_tuple2(item):
            return item[0] in self.edges and item[1] in self.edges[item[0]]
        elif self.legal_tuple3(item):
            if item[0] in self.edges and item[1] in self.edges[item[0]]:
                return self.edges[item[0]][item[1]] == item[2]
        else:
            raise GraphError

    def __delitem__(self, item):
        if type(item) == str:
            node = item
            if node in self.edges:
                del self.edges[node]
                for map in self.edges.values():
                    if node in map:
                        del map[node]
        elif self.legal_tuple2(item):
            og_node, dest_node = item[0], item[1]
            if og_node in self.edges and dest_node in self.edges[og_node]:
                del self.edges[og_node][dest_node]
        else:
            raise GraphError

    def __call__(self, d):
        new_d = {}
        if type(d) == str and d in self.edges:
            for og_node,map in self.edges.items():
                for dest_node,edge in map.items():
                    if dest_node == d:
                        new_d[og_node] = edge
        else:
            raise GraphError
        return new_d

    def clear(self):
        self.edges.clear()

    def dump(self, file, sep=':', conv_string=str):
        sorted_d = dict(sorted(self.edges.items(), key=lambda x:(x[0], x[1])))
        for og_node, map in sorted_d.items():
            line = og_node
            for dest_node, edge in map.items():
                line += sep + dest_node + sep + conv_string(edge)
            file.write(line + '\n')
        file.close()

    def load(self, file, sep, conv_edge=int):
        self.clear()
        for line in file:
            items = line.rstrip('\n').split(sep)
            if len(items) == 1:
                self.edges[items[0]] = {}
            else:
                og_node, dest_nodes, edges = items[0], items[1::2], items[2::2]
                edges = [conv_edge(e) for e in edges]
                self.edges[og_node] = dict(zip(dest_nodes, edges))
        file.close()

    def reverse(self):
        new_graph = []
        for og_node, map in self.edges.items():
            if len([m for m in map.items()]) == 0:
                new_graph.append(og_node)
            else:
                for dest_node, edge in map.items():
                    new_graph.append(tuple([dest_node, og_node, edge]))
        mapped = set()
        for arg in new_graph:
            if type(arg) == tuple:
                for node in arg[0:1]:
                    mapped.add(node)
        for arg in new_graph:
            if type(arg) == str and arg in mapped:
                new_graph.remove(arg)
        legal_edge_value_predicate = self.is_legal_edge_value
        return Graph(legal_edge_value_predicate, *new_graph)

    def natural_subgraph(self, *args):
        graph = Graph(self.is_legal_edge_value)
        del graph.edges
        new_edges = {}
        for arg in args:
            if type(arg) is not str:
                raise GraphError
            if arg not in self.edges:
                continue
            else:
                new_edges[arg] = {}
                for d_n in self.edges[arg]:
                    if d_n in args:
                        new_edges[arg].update({d_n: self.edges[arg][d_n]})
        graph.edges = new_edges
        return graph
      
    def __iter__(self):
        sorted_d = sorted(self.edges.items(), key=lambda x: (x[0], x[1]))
        sorted_items = []
        for item in sorted_d:
            node, map = item[0], item[1]
            if self.in_degree(node) == 0 and self.out_degree(node) == 0:
                sorted_items.append(node)
            else:
                og_node = node
                for d,e in map.items():
                    dest_node, edge = d, e
                    sorted_items.append(tuple([og_node, dest_node, edge]))
        return iter(sorted_items)

    def __eq__(self, right):
        if isinstance(self, Graph) and isinstance(right, Graph):
            g1_items = sorted(self.edges.items(), key=lambda x: (x[0], x[1]))
            g2_items = sorted(right.edges.items(), key=lambda x: (x[0], x[1]))
            return g1_items == g2_items

    def __ne__(self, right):
        return not(self == right)

    def __le__(self, right):
        if isinstance(self, Graph) and isinstance(right, Graph):
            g1_nodes = {node for node in self.edges.keys()}
            g2_nodes = {node for node in right.edges.keys()}
            if g1_nodes.issubset(g2_nodes):
                for node in g1_nodes:
                    mapped = [dest_node for dest_node in self.edges[node].keys()]
                    if len(mapped) > 0:
                        for dest_node in mapped:
                            edge = self.edges[node][dest_node]
                            if right.edges[node][dest_node] == edge:
                                continue
                            else:
                                return False
                return True
            else:
                return False

    def __add__(self, right):
        new_graph = Graph(self.is_legal_edge_value)
        del new_graph.edges
        new_edges = copy.deepcopy(self.edges)
        if isinstance(right, Graph):
            for node, map in right.edges.items():
                if node not in new_edges:
                    new_edges.update({node: map})
                else:
                    for dest_node, edge in map.items():
                        if dest_node not in new_edges[node].keys():
                            new_edges[node].update({dest_node: edge})
                        else:
                            continue
        elif type(right) == str:
            if right not in new_edges.keys():
                new_edges.update({right: {}})
        elif self.legal_tuple3(right):
            og_node, dest_node, edge = right[0], right[1], right[2]
            if og_node in new_edges.keys():
                if dest_node in new_edges[og_node].keys():
                    new_edges[og_node][dest_node] = edge
                else:
                    new_edges[og_node].update({dest_node: edge})
                    if dest_node not in new_edges:
                        new_edges.update({dest_node: {}})
            else:
                new_edges.update({og_node: {dest_node: edge}})
        else:
            raise GraphError
        new_graph.edges = new_edges
        return new_graph
        
    def __radd__(self, left):
        return self + left

    def __iadd__(self, right):
        if isinstance(right, Graph):
            for node, map in right.edges.items():
                if node not in self.edges:
                    self.edges.update({node: map})
                else:
                    for dest_node, edge in map.items():
                        if dest_node not in self.edges[node].keys():
                            self.edges[node].update({dest_node: edge})
                        else:
                            continue
        elif type(right) == str:
            if right not in self.edges.keys():
                self.edges.update({right: {}})
        elif self.legal_tuple3(right):
            og_node, dest_node, edge = right[0], right[1], right[2]
            if og_node in self.edges.keys():
                if dest_node in self.edges[og_node].keys():
                    self.edges[og_node][dest_node] = edge
                else:
                    self.edges[og_node].update({dest_node: edge})
                    if dest_node not in self.edges:
                        self.edges.update({dest_node: {}})
            else:
                self.edges.update({og_node: {dest_node: edge}})
        else:
            raise GraphError
        return self

    def __setattr__(self, name, value):
        if name in ['is_legal_edge_value', 'edges']:
            if name not in self.__dict__:
                self.__dict__[name] = value
            else:
                raise AssertionError
        else:
            raise AssertionError

if __name__ == '__main__':
    print('Start simple testing')
    g = Graph( (lambda x : type(x) is int), ('a','b',1),('a','c',3),('b','a',2),('d','b',2),('d','c',1),'e')
    print(g)
    print(g['a'])
    print(g['a','b'])
    print(g.node_count())
    print(len(g))
    print(g.out_degree('c'))
    print(g.in_degree('a'))
    print('c' in g)
    print(('a','b') in g)
    print(('a','b',1) in g)
    print(g('c'))
    print(g.reverse())
    print(g.natural_subgraph('a','b','c'))
    print()

    import driver
    driver.default_file_name = 'bscp22W19.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
