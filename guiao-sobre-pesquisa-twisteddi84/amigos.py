from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]


def make_domain(amigos):
    return {a: [(b,c) for b in amigos for c in amigos] for a in amigos}

def make_constraint_graph(amigos):
    return {(X,Y):constraint for X in amigos for Y in amigos if X!= Y}

def constraint(a1,i1,a2,i2):
    b1,c1 = i1
    b2,c2 = i2
    
    if a1 in i1 or a2 in i2:
        return False
    
    if b1==c1 or b2==c2:
        return False
    
    if c1=="Claudio" and b1 != "Bernardo":
        return False
    
    return True
    

cs = ConstraintSearch(make_domain(amigos),make_constraint_graph(amigos))

print(cs.search())
