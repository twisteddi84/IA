

class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep


    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob
    
    def individualProb(self, var, val):
        conjs = self._gen_conjunctions([v for v in self.dependencies.keys() if v != var])
        return sum([self.jointProb(conj + [(var, val)]) for conj in conjs])
    
    def _gen_conjunctions(self, vars):
        if len(vars) == 1:
            return [[(vars[0], True)], [(vars[0], False)]]
        
        res = []
        for conj in self._gen_conjunctions(vars[1:]):
            res.append(conj + [(vars[0], True)])
            res.append(conj + [(vars[0], False)])
        return res




# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

