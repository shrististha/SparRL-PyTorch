import networkx as nx
import community as community_louvain
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import graph_tool
import graph_tool.all as gt
import random
import networkit as nk

class Graph:
    def __init__(self, args):
        self.args = args
        if self.args.is_dir:
            print("Making directed.")
            self._G = nx.read_edgelist(self.args.edge_list, nodetype=int, create_using=nx.DiGraph)
        else:
            if self.args.obj == "spearman":
                print("Making directed.")
                self._G = nx.read_edgelist(self.args.edge_list, nodetype=int, create_using=nx.DiGraph)
            else:
                print("Making undirected.")
                self._G = nx.read_edgelist(self.args.edge_list, nodetype=int)
        
        self._relabel_nodes()
        self.gt_graph = None
        self.nk_graph = None
        print("self.get_num_edges()", self.get_num_edges())

    def get_sub_graph_len(self, args):
        if args.eta is None:
            return self.args.subgraph_len
        else:
            return int(args.eta * self.get_num_edges())

    def _relabel_nodes(self):
        """Relabel nodes to [1, |V|]."""
        mapping = dict(zip(self._G.nodes, range(1,self.num_nodes+1)))
        self._G = nx.relabel_nodes(self._G, mapping)

    def add_edge(self, src_id, dst_id):
        if not isinstance(src_id, int):
            src_id = int(src_id)
        if not isinstance(dst_id, int):
            dst_id = int(dst_id)

        assert not self._G.has_edge(src_id, dst_id)
        self._G.add_edge(src_id, dst_id)
    
    def del_edge(self, src_id, dst_id):
        if not isinstance(src_id, int):
            src_id = int(src_id)
        if not isinstance(dst_id, int):
            dst_id = int(dst_id)

        assert self._G.has_edge(src_id, dst_id)
        self._G.remove_edge(src_id, dst_id)
    
    def get_num_edges(self):
        # Get the number of edges in the graph
        return self._G.number_of_edges()

    def get_page_ranks(self):
        return nx.pagerank(self._G, tol=1e-4)

    def set_gt_graph(self):
        # Create a new Graph-tool graph
        nx_graph = self._G
        gt_graph = gt.Graph(directed=nx_graph.is_directed())

        # Add nodes to the Graph-tool graph
        node_map = {}
        for node in nx_graph.nodes():
            node_map[node] = gt_graph.add_vertex()

        # Add edges to the Graph-tool graph
        for u, v in nx_graph.edges():
            gt_graph.add_edge(node_map[u], node_map[v])
        self.gt_graph = gt_graph

    def set_nk_graph(self):
        nx_graph = self._G
        if nx_graph.is_directed():
            nk_graph = nk.Graph(directed=True)  # Create directed Networkit graph
        else:
            nk_graph = nk.Graph()

        node_map = {}
        for node in nx_graph.nodes():
            node_map[node] = nk_graph.addNode()
        # Add edges from NetworkX to Networkit, using the mapped indices
        for u, v in nx_graph.edges():
            nk_graph.addEdge(node_map[u], node_map[v])

        self.nk_graph = nk_graph

    def get_random_vertex_gt(self):
        return random.choice(list(self.gt_graph.vertices()))

    def get_diameter(self):
        return self.get_distance_values('Diameter')

    def get_betweenness_list(self):
        return self.get_centrality_values('Betweenness')

    def get_betweenness_nx(self):
        scores = nx.betweenness_centrality(self._G, k=4, normalized=True, endpoints=True)
        return list(scores.values())

    def get_closeness_list(self):
        return self.get_centrality_values('Closeness')

    def get_distance_values(self, metrics):
        self.set_gt_graph()
        distance_methods = self.get_method_from_metrics_type('Distance')
        distance_method, dict_params = distance_methods[metrics]
        if metrics == "Diameter":
            return distance_method(self.gt_graph, source=self.get_random_vertex_gt())

    def get_centrality_values(self, metrics):
        """
        Get metrics value list using the given Centrality Metrics
        Args:
            metrics: Centrality Metrics

        Returns: A metrics value list
        """
        self.set_nk_graph()
        centrality_methods = self.get_method_from_metrics_type('Centrality', self.num_nodes)
        centrality_method, dict_params = centrality_methods[metrics]
        if metrics == "Closeness":
            # TODO: Need to change the closeness score order to match the node order
            closeness_model_run = centrality_method(self.nk_graph, **dict_params).run()
            topscores =closeness_model_run.topkScoresList()
            topnodes = closeness_model_run.topkNodesList()
            sorted_values = [v for _, v in sorted(zip(topnodes, topscores))]
            return sorted_values
        else:
            scores = centrality_method(self.nk_graph, **dict_params).run().scores()
            return scores


    @staticmethod
    def get_method_from_metrics_type(metrics_type, nodes=0):
        """
        Get the dictionary of metrics method for the metrics type.
        Args:
            metrics_type: Metrics type: Centrality/Distance

        Returns:
            A dict of metrics types and a tuple of method and it's parameters
        """
        if metrics_type == 'Centrality':
            return {
                "Betweenness": (nk.centrality.EstimateBetweenness, {"normalized": True, "nSamples": nodes}),
                "Closeness": (nk.centrality.TopCloseness, {"k": nodes}),
                # "Eigenvector": (nk.centrality.EigenvectorCentrality, {}),
            }
        elif metrics_type == 'Distance':
            return {
                'Diameter': (graph_tool.topology.pseudo_diameter, {})
            }

    def get_shortest_path(self, src_id, dst_id):
        try:
            path = nx.shortest_path(self._G, src_id, dst_id)
        except nx.exception.NetworkXNoPath as e:
            #print(e)
            path = []
        
        return path
        #return snap.GetShortPath(self._G, int(src_id), int(dst_id))
    
    def degree(self, node_ids: list):
        if isinstance(self._G, nx.DiGraph):
            # Get in and out degrees
            out_degrees = [d[1] for d in self._G.out_degree(node_ids)]
            in_degrees = [d[1] for d in self._G.in_degree(node_ids)]
            return out_degrees, in_degrees 
        else:
            degrees = [d[1] for d in self._G.degree(node_ids)]
            
            return degrees        
    
    @property
    def num_nodes(self):
        return self._G.number_of_nodes()
    
    def get_neighbors(self, node):
        return self._G.neighbors(node)
    
    def sample_edges(self, size: int) -> list:
        """Sample edges from the graph."
        
        Args:
            size: number of samples.
        """
        return random.sample(list(self._G.edges), size)
    def copy(self):
        return Graph(self.args)

    def get_node_ids(self) -> list:
        # node_ids = []
        return list(self._G.nodes())
        # for node in self._G:
        #     node_ids.append(node)
        # return node_ids
    
    def partition(self):
        """Partition the graph

        Returns:
            Tuple of edgecuts and partition of nodes.
        """
        return nxmetis.partition(self._G.to_undirected(), self.args.num_parts)
    
    def get_edges(self, node_ids):
        """Get edges."""
        return list(self._G.edges(node_ids))
    
    def has_edge(self, src_id, dst_id):
        return self._G.has_edge(src_id, dst_id)
    
    def draw(self, node_colors=None, with_labels=True):
        nx.draw(self._G, node_color=node_colors, with_labels=with_labels)
        plt.show()

    def louvain(self, should_plot=False):
        partition = community_louvain.best_partition(self._G, randomize=False)
        if should_plot:
            pos = nx.spring_layout(self._G)
            # color the nodes according to their partition
            cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
            nx.draw_networkx_nodes(self._G, pos, partition.keys(), node_size=40,
                           cmap=cmap, node_color=list(partition.values()))
            nx.draw_networkx_edges(self._G, pos, alpha=0.5)
            plt.show()
        return partition
    
    def modularity_communities(self):
        """Find communities in graph using Clauset-Newman-Moore 
        greedy modularity maximization."""
        partition = list(greedy_modularity_communities(self._G))
        parts = [0] * self.get_num_nodes()
        for i, part in enumerate(partition):
            for node in list(part):
                parts[node] = i
        return parts

    def get_G(self):
        """Get the underlying networkx graph."""
        return self._G
    
    def replace_G(self, G):
        """Replace underlying graph with a new graph."""
        self._G = G
        self._relabel_nodes()
    
    def write_edge_list(self, edge_filename):
        with open(edge_filename, "w") as f:
            edges = list(self._G.edges())
            for i, edge in enumerate(edges):
                line = f"{edge[0] - 1} {edge[1] - 1}"
                if i + 1< len(edges):
                    line += "\n"
                f.write(line)

    def single_source_shortest_path(self, node_id: int, cutoff=50):
        return nx.single_source_shortest_path_length(self._G, node_id, cutoff=cutoff)

