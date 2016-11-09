import os
import io
import logging
import argparse
logging.basicConfig(level=logging.INFO)


def parse_node(node):
    if '(' in node and ')' in node:
        items = node.strip().split('(')
        assert len(items) == 2, 'node can contain a full name and one extra short name'
        name = items[0].strip()
        short_name = items[1].split(')')[0].strip()
    else:
        name = node.strip()
        short_name = ''
    return name, short_name


def parse_lines(lines):
    nodes = []
    edges = []
    for line in lines:
        logging.info('%s', line)
        if len(line.strip()) == 0:
            continue
        elif '--' in line:  # line contains edges
            items = line.strip().split('--')
            assert len(items) == 2, 'data structure: name (short name) -- parent 1, parent 2, ...'
            name, short_name = parse_node(items[0].strip())
            nodes.append([name, short_name])
            parent_nodes = items[1].strip().split(',')
            for parent_node in parent_nodes:
                edges.append([parent_node.strip(), name])
        else:  # line contains only node
            name, short_name = parse_node(line.strip())
            nodes.append([name, short_name])
    return nodes, edges


def create_node_id(nodes):
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
    return node_ids


def write_to_dot_file(file_name, nodes, edges, node_ids):
    # Write to a dot file
    handle = open(file_name, 'w')
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
    handle.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default='knowledge_graph.txt')
    parser.add_argument('--output_dot_file', default='ai.dot')
    parser.add_argument('--output_pdf_file', default='ai.pdf')
    args = parser.parse_args()

    lines = io.open(args.input_file, 'r').readlines()
    nodes, edges = parse_lines(lines)
    node_ids = create_node_id(nodes)
    write_to_dot_file(args.output_dot_file, nodes, edges, node_ids)
    os.system('dot -Tpdf ' + args.output_dot_file + ' > ' + args.output_pdf_file)


if __name__ == '__main__':
    main()
