import networkx as nx
import numpy as np
import time


class Entity:
    def __init__(self, string):
        self.number,  self.name = string.split(':')

    def __str__(self):
        return self.name + '-' + str(self.number)


class Action:
    def __init__(self, string):
        self.action = string.split(':')[1]

    def __str__(self):
        return self.action


class Vizualize:
    def __init__(self, graph):
        self.graph = graph

    def create_graph_by_matrox(self, matrix):
        ...
    

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
    relatons = {}
    actions = []
    entitys = []
    relations = []

    def __init__(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.readlines()
            text = [row.replace('\n', '') for row in text]
            print(text)
            for ind, row in enumerate(text):
                if row == '#1':
                    ind1 = ind
                elif row == '#2':
                    ind2 = ind
                elif row == '#3':
                    ind3 = ind

            for row in text[ind1+1:ind2]:
                entity = Entity(row)
                self.entitys[entity.number] = entity

            for row in text[ind2+1:ind3]:
                self.actions.append(
                    Action(row)
                )
            for row in text[ind3+1:len(text)]:
                ind1, ind2, ind3 = row.split(':')
                self.relations.append(
                    Relation(
                        self.decode(ind1),
                        self.decode(ind2),
                        self.decode(ind3),
                    )
                )
            print(text)

    def decode(self, number):
        return self.relations[number]

start = time.time()

scrapper = Scrapper('base.txt')

end = time.time()
print(f"Runtime of the program before vizualize is {end - start}")




end = time.time()
print(f"Runtime of the program with vizualize is {end - start}")
