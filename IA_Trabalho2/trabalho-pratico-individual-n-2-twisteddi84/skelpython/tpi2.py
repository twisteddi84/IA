#encoding: utf8

# YOUR NAME: Diogo Almeida
# YOUR NUMBER: 108902

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        self.assoc_stats = {}

    def query_local(self, user=None, e1=None, rel=None, e2=None):
        self.query_result = []

        for current_user in self.declarations:
            for key in self.declarations[current_user]:
                if (
                    (user is None or current_user == user) and  # Add 'and' here
                    (e1 is None or e1 == key[0]) and
                    (rel is None or rel == key[1]) and
                    (e2 is None or e2 == self.declarations[current_user][key])
                ):
                    relation_instance = self.declarations[current_user][key]
                    if isinstance(relation_instance, set):
                        for value in relation_instance:
                            declaration_instance = Declaration(
                                current_user, Relation(key[0], key[1], value)
                            )
                            self.query_result.append(declaration_instance)
                    else:
                        declaration_instance = Declaration(
                            current_user,
                            Relation(key[0], key[1], relation_instance),
                        )
                        self.query_result.append(declaration_instance)

        return self.query_result

    def query(self,entity,assoc=None):
        self.query_result = []

        decl = self.query_local(e1=entity, rel=assoc)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity)]

        for p in pred:
            decl += self.query(p, assoc=assoc)

        self.query_result = [d for d in decl if d.relation.name not in ['member', 'subtype']]

        return self.query_result
    
    def update_assoc_stats(self, assoc, user=None):
        #crias dois dicts um para e1 outro para e2 para as estatisticas
        dict1 = {}
        dict2 = {}
        dict_soma_1 = {}
        dict_soma_2 = {}

        #usas o query_local para ir buscar as declarations
        declarations = self.query_local(user=user, rel=assoc)
        numero_objetos = 0

        #depois fazes um for por elas todas*
        for decl in declarations:
            #depois para cada uma vais ter dois objetos o e1 e o e2
            obj1 = decl.relation.entity1
            obj2 = decl.relation.entity2
            if obj1 is not None:
                types1 = self.get_types(obj1, user=user)

                if len(types1) == 0:
                    obj1_unknown +=1
                for type in types1:
                    if type not in dict1:
                        dict1[type] = 1
                    else:
                        dict1[type] += 1

            if obj2 is not None:
                types2 = self.get_types(obj2, user=user)

                if len(types2) == 0:
                    obj2_unknown +=1
                for type_ in types2:
                    if type_ not in dict2:
                        dict2[type_] = 1
                    else:
                        dict2[type_] += 1
            
            print(dict1)
            print(dict2)



    def get_types(self,obj,user=None):
        types = set()
        y = self.query_local(user=user, e1=obj)

        for d in y:
            if str(d.relation).startswith("subtype"):
                if d.relation.entity1 == obj:
                    types.add(d.relation.entity2)
            if str(d.relation).startswith("member"):
                if d.relation.entity1 == obj:
                    types.add(d.relation.entity2)


    # def update_assoc_stats(self, assoc, user=None):
    #     obj_decls = [decl for decl in self.query_local(user=user, rel=assoc)]
    #     known_entities1 = [obj.relation.entity1 for obj in obj_decls if isObjectName(obj.relation.entity1)]
    #     known_entities2 = [obj.relation.entity2 for obj in obj_decls if isObjectName(obj.relation.entity2)]
    #     ent1_types = self.entity_types(user, known_entities1)
    #     ent2_types = self.entity_types(user, known_entities2)
    #     type1_count_dict = self.types_counter(ent1_types)
    #     type2_count_dict = self.types_counter(ent2_types)
    #     freq1 = self.frequencies(type1_count_dict, known_entities1)
    #     freq2 = self.frequencies(type2_count_dict, known_entities2)
    #     self.assoc_stats[(assoc, user)] = (freq1, freq2)
    #     return self.assoc_stats[(assoc, user)]

    # def entity_types(self, user, entities):
    #     types = []
    #     for entity in entities:
    #         types += [rel.relation.entity2 for rel in self.query_local(user=user, rel="member", e1=entity)]
    #     return self.recursive_get_subtype(user, types) + types

    # def types_counter(self, types):
    #     type_count_dict = {}
    #     for type in types:
    #         if type not in type_count_dict:
    #             type_count_dict[type] = 1
    #         else:
    #             type_count_dict[type] += 1
    #     return type_count_dict

    # def frequencies(self, type_count_dict, known_entities):
    #     frequencies = {}
    #     for type, count in type_count_dict.items():
    #         val = count
    #         N = len(known_entities)
    #         K = len(known_entities) - len(set(known_entities))
    #         if len(type_count_dict) == 1:
    #             frequencies[type] = val / N
    #         else:
    #             frequencies[type] = max(0,min(1,val / (N - K + K**(1/2))))
    #     return frequencies

    # def recursive_get_subtype(self, user, types):
    #     if not types:
    #         return []
    #     new_types = [rel.relation.entity2 for rel in self.query_local(user=user, rel="subtype", e1=types[0])]
    #     return new_types + self.recursive_get_subtype(user, types[1:] + new_types)  


        
class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        domains = {var: set(values) for var, values in domains.items()}

    def search_all(self, domains=None, xpto=None, index=0):
        xpto = xpto if xpto is not None else []
        domains = domains or self.domains

        if not all(lv for lv in domains.values()):
            return None

        if all(len(lv) == 1 for lv in domains.values()):
            xpto.append({v: next(iter(lv)) for v, lv in domains.items()})
            return xpto

        var = list(domains.keys())[index]
        index += 1

        if len(domains[var]) > 1:
            for val in domains[var]:
                newdomains = {v: values.copy() for v, values in domains.items()}
                newdomains[var] = {val}
                edges = []
                for v1, v2 in self.constraints:
                    if v2 == var:
                        edges.append((v1, v2))
                newdomains = self.propagation(newdomains, edges)
                self.search_all(newdomains, xpto, index)
        elif index < len(list(domains.keys())):
            self.search_all(domains, xpto, index)

        return xpto

    def update_domain(self, domains, var1, domain):
        if len(domain) < len(domains[var1]):
            domains[var1] = domain
            return True
        return False

    def process_edge(self, domains, var1, var2, constraint):
        domain = []
        for x in domains[var1]:
            if any(constraint(var1, x, var2, y) for y in domains[var2]):
                domain.append(x)
        return domain

    def propagation(self, domains, edges):
        while edges:
            var1, var2 = edges.pop(0)
            constraint = self.constraints[var1, var2]

            domain = self.process_edge(domains, var1, var2, constraint)
            if self.update_domain(domains, var1, domain):
                edges.extend((v1, v2) for (v1, v2) in self.constraints if v2 == var1)

        return domains
    