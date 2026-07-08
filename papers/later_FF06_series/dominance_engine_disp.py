"""
dominance_engine.py — the SIBLING primitive to the shape engine.
Handles NON-TRANSITIVE (rock-paper-scissors) constraints that box-containment structurally cannot encode.
Integer, exact, deterministic, no floats. Monotone elimination (hands only ever go down).
Verified reference; transcribes to an OmniForge Rust cdylib sibling of PolyShape.
"""

class Dominance:
    """A non-transitive dominance relation as a directed graph. 'a beats b' = edge (a,b)."""
    __slots__ = ("beats", "nodes")
    def __init__(self):
        self.beats = set()      # {(winner, loser)}
        self.nodes = set()
    def add(self, winner, loser):
        self.beats.add((winner, loser)); self.nodes.add(winner); self.nodes.add(loser); return self
    def wins(self, a, b):
        return (a, b) in self.beats
    def survivors(self, candidates, present):
        """MONOTONE elimination: a candidate survives iff NO present condition beats it.
        Adding conditions can only remove survivors (hands only drop)."""
        return [c for c in candidates if not any((p, c) in self.beats for p in present)]
    def is_transitive(self):
        """Detect whether this relation happens to be transitive (then a shape/order could encode it)."""
        for a, b in self.beats:
            for c in self.nodes:
                if (b, c) in self.beats and (a, c) not in self.beats:
                    return False
        return True
    def cycles_present(self):
        """True if a non-transitive cycle exists (the case boxes CANNOT represent)."""
        return not self.is_transitive()


# ============ THE TWO-ENGINE DISPATCHER (the Vixel reduction game) ============
# Each constraint is tagged by TYPE: 'containment' (transitive -> shape engine) or
# 'dominance' (non-transitive -> dominance engine). A Vixel survives iff it passes BOTH geometries.

from shape_engine import Shape

class Constraint:
    """A constraint is either a containment test (shape) or a dominance test (digraph)."""
    __slots__ = ("kind", "required_shape", "dominance", "present")
    def __init__(self, kind, required_shape=None, dominance=None, present=None):
        assert kind in ("containment", "dominance")
        self.kind = kind
        self.required_shape = required_shape    # for containment: a Shape the candidate must contain
        self.dominance = dominance              # for dominance: a Dominance graph
        self.present = present or []             # for dominance: which conditions are active

class Vixel:
    """A candidate: carries a structural shape (for containment) and an identity (for dominance)."""
    __slots__ = ("name", "shape")
    def __init__(self, name, shape=None):
        self.name = name
        self.shape = shape if shape is not None else Shape()

def reduce_vixels(vixels, constraints):
    """The reduction game: hands start up, drop as constraints eliminate. Monotone.
    A Vixel survives iff it passes EVERY constraint (containment AND dominance).
    Returns survivors in order; deterministic, integer, no floats."""
    standing = list(vixels)
    trace = []
    for i, c in enumerate(constraints):
        before = len(standing)
        if c.kind == "containment":
            standing = [v for v in standing if v.shape.contains(c.required_shape)]
        else:  # dominance
            survivors_names = set(c.dominance.survivors([v.name for v in standing], c.present))
            standing = [v for v in standing if v.name in survivors_names]
        trace.append((i, c.kind, before, len(standing)))   # monotone audit: count only drops
    return standing, trace
