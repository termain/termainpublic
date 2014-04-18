#! /usr/bin/python

from __future__ import print_function
#todo Redesign data storage and properly implement TablularData class

try:
    import yaml
except ImportError:
    print("""yaml module not found. Try package PyYAML on Fedora/Redhat and python-yaml on
       debian systems""")
    raise
    
import sys
from collections import defaultdict

class LabelIndexMaps:
    """Stores the back and forth relationship between string labels and integer indicies"""
    def __init__(self, label_list = []):
        self.label_to_index = {}
        self.index_to_label = label_list
        for index, label in enumerate( self.index_to_label ):
            self.label_to_index[label] = index

    def label( self, index ):
        """Return the label associated with a particular index"""
        return self.index_to_label[ index ]
   
    def index( self, label ):
        """Return the index associated with a particular label"""
        return self.label_to_index[label]

class TabularData:
    """Class for storing tabular (csv style) data"""
    def _parse_kwargs(self, kwargs ):
        #set defaults
        self.special_strings = {}
        self.special_strings["row_delimiter"] = "\n"
        self.special_strings["col_delimiter"] = ","
        self.special_strings["begin_quote"] = '"'
        self.special_strings["end_quote"] = '"'
        self.special_strings["escape"] = None
        self.special_strings["begin_comment"] = None
        self.special_strings["end_comment"] = None
        self.special_strings["line_comment"] = None

        self.special_strings.update( kwargs )
    def __init__(self, **kwargs):
        """Setup table to be ready to load data.

        Delimitters, comment and quote strings are given as regexes 
        or strings representing regexes passed through the keyword arguments.

        Keyword args:
            `row_delimiter`: Row delimiter expression. Default: `\n`
            `col_delimiter`: Column delimiter expression. Default: `,`
            `begin_quote`: Begin quotation character. Default: `"`
            `end_quote`: End quotation character. Default: `"`
            
            `escape`: Escape character. Default: None
            `begin_comment`: begin comment indicator. Default: None
            `end_comment`: end comment indicator. Default: None
            `line_comment`: line comment indicator. Default: None
        """
        self.number_of_rows = 0
        self.number_of_columns = 0
        self.data = []
        self.row_labels = None
        self.col_labels = None
        
        self.
        
