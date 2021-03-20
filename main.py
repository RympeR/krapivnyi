import networkx as nx
import numpy as np
import time


class Entity:
    def __init__(self, string):
        self.number,  self.name = string.split(':')
        self.number = int(self.number)
        self.entity = {
            self.number: self.name
        }

    def __str__(self):
        return self.name + '-' + str(self.number)


class Action:
    def __init__(self, string):
        self.code, self.action, self.action_type = string.split(':')
        self.code = int(self.code)
        self.action_type = int(self.action_type)

    def __str__(self):
        return self.action


class Vizualize:
    def __init__(self, graph:nx.Graph):
        self.graph = graph
        self.edge_labels = {}

    def create_graph_by_matrix(self, matrix):
        ...
    
    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, edge, label):
        self.graph.add_edge(edge)
        self.edge_labels[edge] = label

    def create_graph(self, edges, labels):
        self.pos = nx.circular_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, self.pos)
        nx.draw_networkx_edges(self.graph, self.pos)
        nx.draw_networkx_labels(self.graph, self.pos)
        nx.draw_networkx_edge_labels(self.graph, self.pos,self.edge_labels)
        plt.axis('off')
        plt.savefig("path.png");
        plt.show()


class Relation:
    def __init__(self, action, first_entity, sec_entity):
        self.action = action
        self.first_entity = first_entity
        self.sec_entity = sec_entity

    def __str__(self):
        return self.first_entity.name + ' ' + self.action + ' ' + self.sec_entity

    def form_string(self):
        return self.first_entity.name + ' ' + self.action + ' ' + self.sec_entity


class Scrapper:
    actions = {}
    text_actions = []
    entitys = {}
    text_entitys = []
    relations = []
    decoded_relations = []

    def __init__(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.readlines()
            text = [row.strip() for row in text]
            print(text)
            for ind, row in enumerate(text):
                if row == '#1':
                    ind1 = ind
                elif row == '#2':
                    ind2 = ind
                elif row == '#3':
                    ind3 = ind

            print(ind1, ind2, ind3)
            
            for row in text[ind1+1:ind2]:
                self.text_entitys.append(row)
                entity = Entity(row)
                self.entitys[entity.number] = entity

            for row in text[ind2+1:ind3]:
                self.text_actions.append(row)
                action = Action(row)
                self.actions[action.code] = action

            for row in text[ind3+1:len(text)]:
                ind1, ind2, ind3 = row.split(':')
                self.relations.append(row)
                self.decoded_relations.append(
                    Relation(
                        self.decode_entity(ind1),
                        self.decode_action(ind2),
                        self.decode_entity(ind3),
                    )
                )
                    
            print(text)

    def get_entitys(self):
        return '\n'.join(self.text_entitys) 

    def get_actions(self):
        return '\n'.join(self.text_actions) 

    def get_db(self):
        return '\n'.join(self.relations) 

    def decode_sentence(self, sentence):
        ...

    def decode_entity(self, number):
        return self.entitys[int(number)]

    def decode_action(self, number):
        return self.actions[int(number)]

# start = time.time()

# end = time.time()
# print(f"Runtime of the program before vizualize is {end - start}")




# end = time.time()
# print(f"Runtime of the program with vizualize is {end - start}")
