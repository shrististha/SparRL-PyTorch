from collections import defaultdict

community_file = 'amazontop5000_dedup.txt'
graph_file = 'graph.txt'
output_file = 'filtered_graph_top500.txt'

community_id = 0
community_to_nodes = defaultdict(list)

with open(community_file, 'r') as f:
    for line in f:
        nodes = line.strip().split()
        if not nodes:
            continue
        for node in nodes:
            community_to_nodes[community_id].append(node)
        community_id += 1

print(f"Loaded {community_id} communities.")

community_sizes = {cid: len(nodes) for cid, nodes in community_to_nodes.items()}
top_500_communities = set(sorted(community_sizes, key=community_sizes.get, reverse=True)[:500])
nodes_in_top_communities = {
    node for cid in top_500_communities for node in community_to_nodes[cid]
}
print(f"Total nodes in top 500 communities: {len(nodes_in_top_communities)}")

with open(graph_file, 'r') as infile, open(output_file, 'w') as outfile:
    kept = 0
    for line in infile:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        u, v = parts
        if u in nodes_in_top_communities and v in nodes_in_top_communities:
            outfile.write(f"{u}\t{v}\n")
            kept += 1

print(f"Filtered edge list written to {output_file} ({kept} edges kept).")
