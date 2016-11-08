import os
import io

if __name__ == '__main__':
    lines = io.open('knowledge_tree.txt', 'r').readlines()
    nodes = []
    edges = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        elif '->' in line:  # an edge
            items = line.strip().split('->')
            assert len(items) == 2, 'edges should contain in nodes and a out node'
            in_nodes = items[0].strip().split(',')
            out_node = items[1].strip()
            for in_node in in_nodes:
                edges.append([in_node.strip(), out_node])
        else:  # a node
            if '(' in line and ')' in line:
                items = line.strip().split('(')
                assert len(items) == 2, 'node can contain a full name and one extra short name'
                name = items[0].strip()
                short_name = items[1].split(')')[0].strip()
            else:
                name = line.strip()
                short_name = ''
            nodes.append([name, short_name])

    # Assign a unique id to each node
    node_ids = {}
    for node in nodes:
        name = node[0]
        name = name.replace(' ', '_')
        name = name.lower()
        name = name.replace('-', '_')
        name = name.replace('/', '_')
        name = name.replace("'", '_')
        node_ids[node[0]] = name
        node_ids[node[1]] = name

    # Write to a dot file
    handle = open('ai.dot', 'w')
    handle.write('digraph {' + '\n')
    for node in nodes:
        node_str = '\t' + node_ids[node[0]] + ' [label = "' + node[0]
        if len(node[1]) == 0:
            node_str += '"];' + '\n'
        else:
            node_str += ' (' + node[1] + ')"];' + '\n'
        handle.write(node_str)
    handle.write('\n')
    for edge in edges:
        # Replace node name with the unique id in each edge
        edge_str = '\t' + node_ids[edge[0]] + ' -> ' + node_ids[edge[1]] + ';' + '\n'
        handle.write(edge_str)
    handle.write('}')

    os.system('dot -Tpdf ai.dot > ai.pdf')
