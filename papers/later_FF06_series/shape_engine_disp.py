# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Shape Engine -- a geometry engine for the multiplicative world.
Numbers are BOXES: volume = product of (prime_side ^ dimension_exponent).
Operations are volume-conserving reshapings. Values are never computed unless forced.
Verified reference implementation (Python). Transcribes to OmniForge Rust cdylib.
Honest boundary: ADDITION has no box-merge -> explicit exit to arithmetic, flagged.
"""
from sympy import factorint, prime, primepi, isprime
import math
from functools import reduce

class Shape:
    """A number as a box: {prime_side: dimension_exponent}. The empty box is 1 (unit volume)."""
    __slots__=("sides",)
    def __init__(self, sides=None):
        # invariant enforced structurally: only positive exponents are stored (no zero-dim sides)
        self.sides = {p:e for p,e in sides.items() if e>0} if sides else {}

    # ---- constructors ----
    @classmethod
    def from_int(cls, n):
        if n<1: raise ValueError("shape volume must be >=1 (0 and negatives are not boxes)")
        return cls(factorint(n)) if n>1 else cls()

    # ---- the only forced projection: compute the volume (leaves geometry) ----
    def volume(self):
        v=1
        for p,e in self.sides.items(): v*=p**e
        return v

    # ================= SHAPE-NATIVE OPERATIONS (no volume computed) =================
    def merge(a,b):                      # MULTIPLY = stack boxes, dimensions add
        s=dict(a.sides)
        for p,e in b.sides.items(): s[p]=s.get(p,0)+e
        return Shape(s)

    def scale(self,k):                   # POWER = scale every dimension by k
        if k<0: raise ValueError("negative power leaves the box world")
        if k==0: return Shape()          # anything^0 = 1 = empty box (no zero-exponent sides)
        return Shape({p:e*k for p,e in self.sides.items()})

    def contains(big,small):             # DIVISIBILITY = does small box nest in big box?
        return all(big.sides.get(p,0)>=e for p,e in small.sides.items())

    def divide(big,small):               # EXACT DIVISION = remove the nested box (must be contained)
        if not big.contains(small): raise ValueError("not divisible: box does not nest")
        s=dict(big.sides)
        for p,e in small.sides.items():
            s[p]-=e
            if s[p]==0: del s[p]
        return Shape(s)

    def common_box(a,b):                 # GCD = largest shared sub-box (min dimensions)
        return Shape({p:min(a.sides[p],b.sides.get(p,0)) for p in a.sides if p in b.sides})

    def enclosing_box(a,b):              # LCM = smallest box containing both (max dimensions)
        s=dict(a.sides)
        for p,e in b.sides.items(): s[p]=max(s.get(p,0),e)
        return Shape(s)

    # ================= SHAPE PROPERTIES (read the answer off the geometry) =================
    def is_atomic(self):                 # PRIMALITY = a single unit-dimension side, no non-trivial box
        return len(self.sides)==1 and next(iter(self.sides.values()))==1

    def is_unit(self):                   # the number 1 = empty box
        return len(self.sides)==0

    def symmetry_order(self):            # gcd of dimensions: g>=2 => perfect g-th power (symmetric box)
        if not self.sides: return 0
        return reduce(math.gcd, self.sides.values())

    def is_perfect_power(self):
        return self.symmetry_order()>=2

    def n_dimensions(self):              # number of distinct prime-sides (the box's dimensionality)
        return len(self.sides)

    def decompose(self):                 # FACTORIZATION = the box already IS its decomposition
        return dict(self.sides)

    # ---- glyph form: sides named by prime-index (the alias dictionary, built-once-shared) ----
    def glyph_word(self):
        return " · ".join(f"p{primepi(p)}"+(f"^{e}" if e>1 else "") for p,e in sorted(self.sides.items()))

    def __eq__(self,o): return self.sides==o.sides
    def __repr__(self):
        if not self.sides: return "Shape(1)"
        return "Shape("+"·".join(f"{p}^{e}" if e>1 else f"{p}" for p,e in sorted(self.sides.items()))+")"

# ================= THE ADDITION EXIT (the honest boundary) =================
def add_exit(a, b):
    """Addition has NO box-merge. This function EXITS geometry, computes the value, re-enters.
    It is explicitly named so every additive step is visible as a geometry-break."""
    return Shape.from_int(a.volume()+b.volume()), "GEOMETRY_EXIT: addition required value computation + refactor"
