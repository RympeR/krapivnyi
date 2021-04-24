import networkx as nx
import matplotlib.pyplot as plt
from networkx.exception import NetworkXNoPath


class Entity:
    def __init__(self, string):
        self.number,  self.name = string.split(':')
        self.number = int(self.number)
        self.entity = {
            self.number: self.name,
            self.name: self.number,
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
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.edge_labels = {}
        self.num_action_edges = {}

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, edge, label, num_edge, num_action):
        self.graph.add_edge(*edge)
        self.edge_labels[edge] = label
        self.num_action_edges[str(edge[0])+'-'+str(edge[1])] = {
            'num_edge': num_edge,
            'num_action': num_action
        }

    def create_graph(self):
        self.pos = nx.circular_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, self.pos)
        nx.draw_networkx_edges(self.graph, self.pos)
        nx.draw_networkx_labels(self.graph, self.pos)
        nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels)
        plt.axis('off')
        plt.savefig("path.png")
        plt.show()

    def get_answers(self, entity, action, endpoint=True, entitys=None, action_name=None, actions=None):
        answers = []
        for node in nx.nodes(self.graph):
            if endpoint:
                path = list(nx.all_simple_paths(
                    self.graph,
                    source=node, target=entity
                ))
            else:
                path = list(nx.all_simple_paths(
                    self.graph,
                    source=entity, target=node
                ))
            if len(path) > 0:
                print(path)
                first_el = path[0]
                last_action_num = actions[self.num_action_edges[str(
                    first_el[-2]) + '-' + str(first_el[-1])]['num_action']]
                print(action_name)
                print(action)
                print(last_action_num)
                print(last_action_num.action)
                print(last_action_num.code)
                print('-'*10)
                if int(action) == int(last_action_num.code) and action_name == last_action_num.action:
                    answers.append(
                        (entitys[first_el[0]].entity[first_el[0]],
                            action_name,
                            entitys[first_el[-1]].entity[first_el[-1]],)
                    )
        return answers


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
        graph = nx.DiGraph()
        num_graph = nx.DiGraph()
        self.vizualizer = Vizualize(graph)
        self.num_vizualizer = Vizualize(num_graph)

        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.readlines()
            text = [row.strip() for row in text]
            for ind, row in enumerate(text):
                if row == '#1':
                    ind1 = ind
                elif row == '#2':
                    ind2 = ind
                elif row == '#3':
                    ind3 = ind

            for row in text[ind1+1:ind2]:
                self.text_entitys.append(row)
                entity = Entity(row)
                self.entitys[entity.number] = entity

            for row in text[ind2+1:ind3]:
                self.text_actions.append(row)
                action = Action(row)
                self.actions[action.code] = action
                self.actions[action.action] = action

            for row in text[ind3+1:len(text)]:
                _ind1, _ind2, _ind3 = row.split(':')
                self.relations.append(row)
                self.vizualizer.add_edge(
                    (
                        self.decode_entity(_ind1).name,
                        self.decode_entity(_ind3).name,
                    ),
                    str(self.decode_action(_ind2).action_type) +
                    ' ' + self.decode_action(_ind2).action,
                    self.decode_action(_ind2).action_type,
                    self.decode_action(_ind2).action
                )
                self.num_vizualizer.add_edge(
                    (
                        self.decode_entity(_ind1).number,
                        self.decode_entity(_ind3).number,
                    ),
                    str(self.decode_action(_ind2).action_type) +
                    ' ' + self.decode_action(_ind2).action,
                    self.decode_action(_ind2).action_type,
                    self.decode_action(_ind2).action
                )
                self.decoded_relations.append(
                    Relation(
                        self.decode_entity(_ind1),
                        self.decode_action(_ind2),
                        self.decode_entity(_ind3),
                    )
                )

    def get_entitys(self):
        return '\n'.join(self.text_entitys)

    def get_actions(self):
        return '\n'.join(self.text_actions)

    def get_db(self):
        return '\n'.join(self.relations)

    def get_node_answers(self, entity, endpoint=True):
        possible_answers = []
        for _ in self.actions.values():
            print(_.action)
            possible_answers.append(
                self.num_vizualizer.get_answers(
                    int(entity), _.action_type, endpoint,
                    entitys=self.entitys,
                    action_name=_.action,
                    actions=self.actions)
            )
        result = []
        for possible_answer in possible_answers:
            if len(possible_answer) > 0:
                for _possible_answer in possible_answer:
                    result.append(_possible_answer)
        return result

    def decode_num_sentence(self, first_entity, action, second_entity):
        if '?' == first_entity and '?' == action and '?' == second_entity:
            possible_answers = []
            nodes = nx.nodes(self.num_vizualizer.graph)
            for node in nodes:
                possible_answers.append(
                    self.get_node_answers(
                        node, endpoint=True
                    )
                )
                possible_answers.append(
                    self.get_node_answers(
                        node
                    )
                )
            result = []
            for possible_answer in possible_answers:
                if len(possible_answer) > 0:
                    for _possible_answer in possible_answer:
                        result.append(_possible_answer)
            return list(set(result))

        if '?' == first_entity and '?' == action:
            return list(set(self.get_node_answers(int(second_entity))))

        if '?' == second_entity and '?' == action:
            return list(set(self.get_node_answers(int(first_entity), endpoint=False)))

        if action != '?':
            action_name = self.actions[int(action)].action
        if '?' == first_entity:
            first_possible_answers = self.num_vizualizer.get_answers(
                int(second_entity), 
                action, 
                entitys=self.entitys, 
                action_name=action_name, 
                actions=self.actions
            )
            return list(set(first_possible_answers))

        if '?' == second_entity:
            sec_possible_answers = self.num_vizualizer.get_answers(
                int(first_entity),
                action,
                entitys=self.entitys,
                action_name=action_name,
                endpoint=False,
                actions=self.actions
            )
            return list(set(sec_possible_answers))

        if action != '?':
            action = self.actions[int(action)].code
        try:
            path = list(nx.shortest_simple_paths(self.num_vizualizer.graph,
                                                 source=int(first_entity),
                                                 target=int(second_entity)))
            path = path[0]
            if len(path) < 3:
                last_action_num = self.actions[self.num_vizualizer.num_action_edges[str(
                    path[0]) + '-' + str(path[1])]['num_action']]
                if action != '?':
                    if int(action) == int(last_action_num.code):
                        return True
                    return False
            else:
                pre_final, final = path[-2], path[-1]
                last_action_num = self.actions[self.num_vizualizer.num_action_edges[str(
                    pre_final) + '-' + str(final)]['num_action']]
            if action == '?':
                action = last_action_num.action

                return list(set([(
                    self.entitys[int(first_entity)].entity[int(first_entity)],
                    action,
                    self.entitys[int(second_entity)
                                 ].entity[int(second_entity)],
                ), ]))

            if int(last_action_num.code) == int(action):
                return True
            else:
                return False
        except NetworkXNoPath:
            return False

    def vizualize(self):
        self.vizualizer.create_graph()

    def vizualize_with_num_nodes(self):
        self.num_vizualizer.create_graph()

    def decode_entity(self, number):
        return self.entitys[int(number)]

    def decode_action(self, number):
        return self.actions[int(number)]
