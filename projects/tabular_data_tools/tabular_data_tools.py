#! /usr/bin/python

from __future__ import print_function

from collections import defaultdict

class IndexLabels:
    """Associate indices with labels and vice versa. If queried for a label
    and label is not found return index"""
    def __init__(self):
        self.mapping = {}
        self.max_index = 0


    def add_label( self, index, label=None ):
        if label is None:
            self.mapping[index]=index
        else:
            self.mapping[index]=label

        if self.max_index < index:
            self.max_index = index

    def __getitem__( self, key ):
        if key in self.mapping:
            return self.mapping[key]
        elif key <= self.max_index:
            return key
        else:
            raise KeyError

class SparseIndexedTabularData:
    """Table data"""
    def __init__(self, number_of_dimensions = 1):
        self.data = {}
        self.dimension_sizes = [0]*number_of_dimensions
        self.number_of_dimensions = number_of_dimensions

    def add_dimension( self ):
        """Add a new dimension to the data. Any already present data will have it's
        index for that dimension set to 0"""
        self.dimension_sizes.append( 0 )
        self.number_of_dimensions += 1

        old_keys = self.data.keys()
        for old_key in old_keys:
            new_key = old_key+(0,)
            self.data[ new_key ] = self.data.pop( old_key )

    def set_datum(self, index_tuple, datum ):
        if len( index_tuple ) != self.number_of_dimensions:
            raise KeyError("Index tuple must have the same dimensionality as table")
 
        self.data[index_tuple] = datum

    def get_datum( self, index_tuple ):
        if len( index_tuple ) != self.number_of_dimensions:
            raise KeyError("Index tuple must have the same dimensionality as table")
        return self.data[index_tuple]
        

    def switch( self, index_tuple1, index_tuple2 ):
        temporary = self.get_datum[index_tuple1]
        self.set_datum( index_tuple1, self.get_datum( index_tuple2 ) )
        self.set_datum( index_tuple2, temporary )

        
