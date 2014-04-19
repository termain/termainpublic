#! /usr/bin/python

from __future__import print_function
from collections import defaultdict

none_factory = lambda: None
zero_factory = lambda: 0
empty_string_factory = lambda: ''

def force_tuple_length( length, tuple_value, extension_value = 0 ):
    """Force a tuple to be of a certain length either through truncation 
       or extension (as necessary)"""
    if len(tuple_value) == length:
        return tuple_value
    elif len(tuple_value) < length:
        return tuple_value[:length]
    else:
        return tuple_value + (extension_value)*(length-length(tuple_value))

def get_depth_dictionary( tree ):
    for key in tree:
        

def get_depth( tree ):
    for element in tree:
        
    
        

class DimensionList:
    """A list of sets for storing indicies of dimensions"""
    def __init__(self, number_of_dimensions = 0):
        self.sets = []
        self.add_multiple_dimensions( number_of_dimensions )

    def add_dimension( self ):
        self.sets.append( set() )

    def add_multiple_dimnensions( self, number_to_add ):
        for index in range(number_to_add):
            self.add_dimension()

    def add_index( self, dimension_index, index_value ):
        self.sets[ dimension_index ].add( index_value )

    def add_index_tuple( self, index_tuple ):
        """Add an index tuple to the sets. Tuple should be same length as
           the number of dimensions"""
        for dimension_index, index_value in enumerate( index_tuple ):
            self.add_index( dimension_index, index_value )

    def __len__(self):
        return len(self.sets)

class CartesianData:
    """Treating data (tables) as Cartesian products

        Indices can be any hashable object though I suspect integers
        will be prefered"""
    def __init__(self,  number_of_dimensions = 1, 
                        default_function = none_factory ):
        self.data = defaultdict( default_function )
        self.dimensions = DimensionList(number_of_dimensions)

    def set_datum( self, index_tuple, datum ):
        """Set datum. Force index_tuple length to be of right dimensionality
        by truncating or padding with zeros"""
        forced_index_tuple = force_tuple_length( index_tuple, len(self.dimensions) )
        self.dimensions.add_index_tuple( forced_index_tuple )
        self.data[forced_index_tuple] = datum

    def get_datum( self, index_tuple ):
        """Get datum. Force index_tuple length to be of right dimensionality
        by truncating or padding with zeros"""
        forced_index_tuple = force_tuple_length( index_tuple, len(self.dimensions) )
        return self.data[index_tuple] = datum

    def switch( self, index_tuple1, index_tuple2 ):
        """Switch values at index_tuple1 with index_tuple2"""
        temporary = self.get_datum( index_tuple1 )
        self.set_datum( index_tuple1, self.get_datum( index_tuple2 ) )
        self.set_datum( index_tuple2, temporary )

    def transpose( self, dimension1, dimension2 ):
       raise NotImplementedError

    def from_tree( self, tree ):
        """Load in a recursive structure (tree) of python lists and/or dicts. Each
        additional level is a new dimension"""
        
