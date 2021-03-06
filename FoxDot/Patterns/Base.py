from random import choice, shuffle
from Operations import *
from Comparisons import *
from Parse import Parse

class dots:
    def __repr__(self):
        return '...'
    def __str__(self):
        return '...'

class metaPattern(object):
    """ Abstract base class """

    data = None
    _now = None

    def __init__(self, data=[]):
        
        if type(data) is str:
            
            self.fromString(data)
            
        else:
            
            self.data = data
            self.make()
            
    def __len__(self):
        return len(self.data)
    def __str__(self):
        if len(self.data) > 10:
            val = self.data[:3] + [dots()] + self.data[-3:]
        else:
            val = self.data
        return self.BRACKETS % str(val)[1:-1]
    def __repr__(self):
        return str(self)
    def string(self):
        """ Returns a string made up of all the values:

            PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" """
        string = ""
        for item in self.data:
            try:
                string += item.string()
            except:
                string += str(item)
        return string
    #: Container methods
    def __getitem__(self, key):
        self._now = self.data[key] # store last value retrieved
        return self._now
    def __setitem__(self, key, value):
        self.data[key] = value
    def __iter__(self):
        for data in self.data:
            yield data
    def items(self):
        for i, data in enumerate(self.data):
            yield i, data
    def __getslice__(self, i, j):
        return Pattern( self.data[i:j] )
    def __setslice__(self, i, j, item):
        self.data[i:j] = item
    def count(self, item):
        return self.data.count(item)
    #: Operators
    def __add__(self, other):  return PAdd(self, other)
    def __radd__(self, other): return PAdd(self, other)
    def __sub__(self, other):  return PSub(self, other)
    def __rsub__(self, other): return PSub(other, self)
    def __mul__(self, other):  return PMul(self, other)
    def __rmul__(self, other): return PMul(other, self)
    def __div__(self, other):  return PDiv(self, other)
    def __rdiv__(self, other): return PDiv(other, self)
    def __mod__(self, other):  return PMod(self, other)
    def __rmod__(self, other): return PMod(other, self)
    def __pow__(self, other):  return PPow(self, other)
    def __rpow__(self, other): return PPow(other, self)
    def __xor__(self, other):  return PPow(self, other)
    def __rxor__(self, other): return PPow(other, self)
    def __truediv__(self, other):  return PDiv(self, other)
    def __rtruediv__(self, other): return PDiv(other, self)
    #: Piping patterns
    def __or__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return Pattern(self.pipe(other))
    def __ror__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return Pattern(asStream(other).pipe(self))
    #: Comparisons
    def __eq__(self, other): return Peq(self, other)
    def __ne__(self, other): return Pne(self, other)
    def __gt__(self, other): return Pgt(self, other)
    def __ge__(self, other): return Pge(self, other)
    def __lt__(self, other): return Plt(self, other)
    def __le__(self, other): return Ple(self, other)

    #: Methods for strings as pattern

    def fromString(self, string):
        self.data = Parse(string)
        return self

    def flat(self):
        """ P.flat() -> un-nested pattern """
        new = []
        for item in self.data:
            try:
                item = item.flat()
                new += [i for i in item]
            except:
                new.append(item)
        return Pattern(new)
    
    def coeff(self):
        """ Returns a duration value relative to the type of pattern. Most patterns return val unchanged """
        return 1.0

    # Methods that return augmented versions of original

    def shuf(self):
        new = asStream(self.data)
        shuffle(new.data)
        return new
    
    def stretch(self, size):
        """ Stretches (repeats) the contents until len(Pattern) == size """
        new = []
        for n in range(size):
            new.append( modi(self.data, n) )
        self.data = new
        return self

    def loop(self, n):
        """ Repeats this pattern n times """
        new = []
        for i in range(n):
            new += list(self)
        return Pattern(new)

    def sort(self):
        """ Used in place of sorted(pattern) to force type """
        return Pattern(sorted(self.data))

    def reverse(self):
        new = [self.data[i-1] for i in range(len(self.data), 0, -1)]
        return Pattern(new)

    def invert(self):
        new = []
        lrg = float(max(self.data))
        for item in self.data:
            try:
                new.append(item.invert())
            except:
                new.append((((item / lrg) * -1) + 1) * lrg)
        return Pattern(new)

    def rotate(self, n=1):
        new = self.data[n:] + self.data[0:n]
        return Pattern(new)

    def stutter(self, n=2):
        n = asStream(n)
        lrg = max(len(self.data), len(n))
        new = []
        for i in range(lrg):
            for j in range(modi(n,i)):
                new.append(modi(self.data,i))
        return Pattern(new)

    # Changing the pattern in place

    def append(self, item):
        self[len(self):] = [item]
        return self

    def i_rotate(self, n=1):
        self.data = self.data[n:] + self.data[0:n]
        return self

    def i_reverse(self):
        self.data.reverse()
        return self

    def i_sort(self):
        self.data = Pattern(sorted(self.data))
        return self

    def i_shuf(self):
        shuffle(self.data)
        return self

    # Boolean tests

    def contains_nest(self):
        """ Returns true if the pattern contains a nest """
        pass

    def startswith(self, prefix):
        return self.data[0] == prefix
    
    def all(self, func=(lambda x: bool(x))):
        """ Returns true if all of the patterns contents satisfies func(x) - default is nonzero """
        if len(self.data) is 0:
            return False
        
        for item in self.data:
            if not func(item):
                return False
        return True
        
    def pipe(self, pattern):
        """ Concatonates this patterns stream with another """
        data = list(self)
        for item in asStream(pattern):
            data.append(item)
        return Pattern(data)

    # Returns individual elements / slices

    def choose(self):
        """ Returns one randomly selected item """
        return choice(self.data)

    def trim(self, size):
        return self[:size]

    def ltrim(self, size):
        return self[-size:]


    # Automatic expansion of nested patterns

    def make(self):
        """ This method automatically laces and groups the data """

        #: Force data into an iterable form
        if isinstance(self.data, str):

            self.data = list(self.data)
            
        if not isinstance(self.data, list):
    
            self.data = [self.data]

        #: Put any data in a tuple into a PGroup
        for i, data in enumerate(self.data):
            if type(data) is tuple:
                self.data[i] = PGroup(data)

        #: Lace any nested lists
        self.data = Place(self.data)
        
        return self

class Pattern(metaPattern):
    """
        Pattern Base Class
        ==================
        
    """

    NEST_ME = True
    BRACKETS = "[%s]"

class PatternContainer(metaPattern):
    NEST_ME = False
    BRACKETS = "[%s]"
    def make(self):
        return self
    def __str__(self):
        return str(["%s()" % item.__class__.__name__ for item in self.data])
    def __repr__(self):
        return str(self)
    

class PGroup(metaPattern):
    """
        Class to represent any groupings of notes as denoted by brackets.
        PGroups should only be found within a Pattern object.
        
    """

    NEST_ME = False
    BRACKETS = "(%s)"

    def __init__(self, data=[], *args):
        if not args:
            if type(data) is tuple:
                data = list(data)
        else:
            data = [data] + list(args)
        metaPattern.__init__(self, data)
    
    def make(self):
        """
            Overrides the Pattern.make() method to allow PGroup to invert nesting:

            i.e. (0,[1,2]) -> [(0,1),(0,2)] and NEST_ME flag is set to False
            i.e. (0,[1,2],[3,4]) -> [(0,1,3),(0,2,4)]

        """

        if not isinstance(self.data, (list, metaPattern)):
    
            self.data = [self.data]

        #: Inverts the nested and grouped data if PGroup has a nested Pattern
        if contains_nest(self.data):
            
            sub = Place(self.data)

            step = len(self.data)

            self.data = [self.__class__(sub[n:n+step]) for n in range(0, len(sub), step)]

            # Make this a pseudo-normal pattern          
            self.NEST_ME  = Pattern.NEST_ME
            self.BRACKETS = Pattern.BRACKETS
            
        return self

    def coeff(self):
        return 0.5

    def scale_dur(self, n):
        """ Scales the dur values for all the items in self.data by n """
        for item in self.data:
            item.scale_dur(n)
        return

    def fromString(self, s, dur=1):
        metaPattern.fromString(self, s, dur)
        self.scale_dur(self.coeff())
        return self

Pgroup = PGroup #: Alias for PGroup

class Shared_Time_PGroup(PGroup):
    BRACKETS = "{%s}"
    def coeff(self):
        return 1.0 / len(self)


# Functions used to separate Groups and Nests from within Patterns

def nested(data):
    """ Returns true is data is any kind of pattern (inc. lists) EXCEPT PGroups or TimeVars """
    try:
        return data.NEST_ME
    except:
        return isinstance(data, list)

def contains_nest(data):
    """ Returns true if any items in data are 'nest-able' patterns """
    try:
        return any([nested(item) for item in data])
    except:
        return False

def Place(data):
    """ nested patterns are stretched
        e.g. [[1,0],0,1,0] would be returned as [1,0,1,0,0,0,1,0] """

    if contains_nest(data):

        #: Works out the largest sub-patterns and loops the overall pattern until it is stretched out
        
        sub = LCM(*[len(item) for item in data if nested(item)])
        new = []

        for i in range( sub ):
            for j in range(len(data)):
                item = data[j]
                if nested(item):
                    item = modi(item, i)
                    if type(item) is tuple:
                        item = PGroup(item)
                new.append(item)
        return new
    
    else:
         #: If the pattern doesn't need lacing, return original
        return data


# Used to force any non-pattern data into a Pattern
                
def asStream(data):
    """ Forces any data into a [pattern] form """
    if isinstance(data, Pattern):
        return data
    return Pattern(data)

def Dominant(*patterns):
    for p in patterns:
        if isinstance(p, (Pattern, list)):
           return Pattern 
    return PGroup      

def Convert(*args):
    """ Returns tuples/PGroups as PGroups, and anything else as Patterns """
    PatternTypes = []
    for val in args:
        if isinstance(val, (Pattern, PGroup)):
            PatternTypes.append(val)
        elif isinstance(val, tuple):
            PatternTypes.append(PGroup(val))
        else:
            PatternTypes.append(Pattern(val))
    return PatternTypes



