#!/usr/bin/python3

import sys
import graphviz as gv
import tensorflow as tf

class visualizer():
    def __init__(self, title="My-Neural-Network", file_type='png', savepdf=False, orientation='LR'):
        self.title = title
        self.color_encoding = {'input': 'yellow', 'hidden': 'green', 'output': 'red'}

        if savepdf:
            self.file_type = 'pdf'
        else:
            self.file_type = file_type

        if orientation in ['LR', 'TB', 'BT', 'RL']:
            self.orient = orientation
        else:
            print('Invalid orientation')
            sys.exit()

        self.network = gv.Graph(title, directory='./graphs', format=self.file_type,
              graph_attr=dict(ranksep='2', rankdir=self.orient, color='white', splines='line'),
              node_attr=dict(label='', shape='circle', width='0.5'))

        self.layers = 0
        self.layer_names = list()
        self.layer_types = list()
        self.layer_units = list()
        self.tmp_units = list()

    def __str__(self):
        return self.title

    def add_layer(self, layer_type, nodes):
        if self.layers == 0:
            layer_name = layer_type.capitalize()+'_input'
        else:
            layer_name = layer_type.capitalize()+'_hidden'+str(self.layers)

        self.layer_types.append(layer_type)
        self.layer_names.append(layer_name)
        self.layer_units.append(nodes)
        self.layers = self.layers + 1

        with self.network.subgraph(name=f'cluster_{layer_name}') as layer:
            if nodes > 10:
                layer.attr(labeljust='right', labelloc='bottom', label='+'+str(nodes - 10))
                nodes = 10
            self.tmp_units.append(nodes)

            for i in range(nodes):
                if self.layers == 1:
                    color = self.color_encoding['input']
                else:
                    color = self.color_encoding['hidden']
                layer.node(f'{layer_name}_{i}', shape='point', style='filled', fillcolor=color)

        return

    def _connect_layers(self, l1_nodes, l2_nodes, l1_name, l2_name):
        for l1 in range(l1_nodes):
            for l2 in range(l2_nodes):
                n1 = l1_name+'_'+str(l1)
                n2 = l2_name+'_'+str(l2)

                self.network.edge(n1, n2)

        return

    def _build_network(self):
        for i in range(self.layers - 1):
            nodes1 = self.layer_units[i]
            nodes2 = self.layer_units[i+1]

            if self.layer_units[i] > 10:
                nodes1 = 10
            if self.layer_units[i+1] > 10:
                nodes2 = 10

            self._connect_layers(nodes1, nodes2, self.layer_names[i], self.layer_names[i+1])

        # Updating the color of output dense layer to red
        with self.network.subgraph(name=f'cluster_{self.layer_names[-1]}') as layer:
            for i in range(self.tmp_units[-1]):
                layer.node(f'{self.layer_names[-1]}_{i}', style='filled', fillcolor='red')

        return

    def from_tensorflow(self, model):
        for layer in model.layers:
            if type(layer) == tf.keras.layers.Dense:
                self.add_layer('dense', layer.units)

        return

    def get_meta_data(self):
        meta_data = dict()
        meta_data['Number of Layers'] = self.layers
        meta_data['Layer names'] = self.layer_names
        meta_data['Layer Types'] = self.layer_types
        meta_data['Node in Layers'] = self.layer_units

        return meta_data

    def summarize(self):
        title = "Neural Network Architecture"
        hline = "+"+"-"*69+"+"

        print(hline)
        print("|"+title.center(69)+"|")
        print(hline)
        print("|"+"Layer Name".center(28)+"|"+"Layer Type".center(24)+"|"+"Layer Units".center(15)+"|")
        print(hline)
        for i in range(self.layers):
            col1 = self.layer_names[i].center(28)
            col2 = self.layer_types[i].capitalize().center(24)
            col3 = str(self.layer_units[i]).center(15)
            print("|"+col1+"|"+col2+"|"+col3+"|")
            print(hline)

        return

    def visualize(self):
        if self.layers < 2:
            print("Cannot draw Neural Network")
            print("Add atleast two layers to the network")
            sys.exit()
        self._build_network()
        self.network.view()

        return

if __name__ == '__main__':
    input_nodes = 7
    hidden_nodes = 12
    output_nodes = 6

    net = visualizer()

    # net.add_layer('dense', input_nodes)
    # net.add_layer('dense', hidden_nodes)
    # net.add_layer('dense', output_nodes)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='sigmoid'),
        tf.keras.layers.Dense(64, activation='sigmoid'),
        tf.keras.layers.Dense(32, activation='sigmoid'),
        tf.keras.layers.Dense(16, activation='sigmoid'),
        tf.keras.layers.Conv2D(16, 3)
    ])

    net.from_tensorflow(model)
    net.visualize()
    net.summarize()
