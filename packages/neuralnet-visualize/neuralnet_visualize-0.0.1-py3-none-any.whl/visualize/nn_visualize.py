#!/usr/bin/python3

import graphviz as gv

class visualizer():
    def __init__(self, title="My-Neural-Network"):
        self.title = title
        self.network = gv.Graph(title, directory='./graphs', format='png',
              graph_attr=dict(ranksep='2', rankdir='LR', color='white', splines='line'),
              node_attr=dict(label='', shape='circle', width='0.5'))

        self.layers = 0
        self.layer_names = list()
        self.layer_units = list()

    def __str__(self):
        return self.title

    def add_layer(self, layer_name, nodes):
        with self.network.subgraph(name=f'cluster_{layer_name}') as layer:
            if nodes > 10:
                layer.attr(labeljust='right', labelloc='bottom', label='+'+str(nodes - 10))
                nodes = 10
            layer.attr(body=layer_name)

            for i in range(nodes):
                layer.node(f'{layer_name}_{i}', style='filled', fillcolor='yellow')

        self.layer_names.append(layer_name)
        self.layer_units.append(nodes)
        self.layers = self.layers + 1

    def _connect_layers(self, l1_nodes, l2_nodes, l1_name, l2_name):
        for l1 in range(l1_nodes):
            for l2 in range(l2_nodes):
                n1 = l1_name+'_'+str(l1)
                n2 = l2_name+'_'+str(l2)

                self.network.edge(n1, n2)

    def _build_network(self):
        for i in range(self.layers - 1):
            self._connect_layers(self.layer_units[i], self.layer_units[i+1], self.layer_names[i], self.layer_names[i+1])

    def visualize(self):
        self._build_network()
        self.network.view()

if __name__ == '__main__':
    input_nodes = 6
    hidden_nodes = 12
    output_nodes = 4

    net = visualizer()

    net.add_layer('input', input_nodes)
    net.add_layer('hidden', hidden_nodes)
    net.add_layer('output', output_nodes)

    net.visualize()