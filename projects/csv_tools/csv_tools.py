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
import re
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

    def __getitem__(self, index ):
        return self.label(index)

class TabularData:
    """Class for storing tabular (csv style) data"""
    def _setup_full_parser(self, kwargs ):
        """
        Note: "Full" parser in development.

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
            `line_comment`: line comment indicator. Default: None"""

        raise NotImplemented
        #set defaults

        self.special_strings["row_delimiter"] = "\n"
        self.special_strings["col_delimiter"] = ","
        self.special_strings["begin_quote"] = '"'
        self.special_strings["end_quote"] = '"'
        self.special_strings["escape"] = None
        self.special_strings["begin_comment"] = None
        self.special_strings["end_comment"] = None
        self.special_strings["line_comment"] = None

        self.special_strings.update( kwargs )

    def _compile_regexes( self, special_strings ):
        """Compile regexes from the special strings"""
        compiled_regexes = {}
        for key in special_strings:
            compiled_regexes[key] = re.compile( special_strings[key] )

        return compiled_regexes

    def _parse_init_kwargs(self, kwargs):
        """Parse the keyword arguments given to init"""
        defaults = {
            "full_parser": False,
            "row_labels" : True,
            "col_labels" : True,
            "row_delimiter": "\\n",
            "col_delimiter": ",",
            "empty_field": ""
            }

        defaults.update(kwargs)
        self.extract_row_labels = kwargs["row_labels"]
        self.extract_col_labels = kwargs["col_labels"]

        if defaults["full_parser"]:
            self.full_parsing = True
            self._setup_full_parser( kwargs )
        else:
            self.special_strings["row_delimiter"] = defaults["row_delimiter"]
            self.special_strings["col_delimiter"] = defaults["col_delimiter"]
            self.special_strings["empty_field"] = defaults["empty_field"]

        self.compiled_regexes = self._compile_regexes( self.special_strings )

    def __init__(self, **kwargs):
        """Setup table to be ready to load data.

        Keyword arguments include:
            `full_parser`: boolean. Use full parser (not yet implemented)
                instead of simple parser. Defaults to `False`
            `row_labels`: boolean. Rows have labels. Defaults to `True`
            `col_labels`: boolean. Columns have labels. Defaults to `True`
            `strip_whitespace`: boolean. Strip whitespace between fields.
            `row_delimiter`: Regex string for row delimiters. Defaults to '\\n'
            `col_delimiter`: Regex string for col delimiters. Defaults to ','
            `empty_field`: Empty field representation. Defaults to ''
        """
        self.special_strings = {}
        self.number_of_rows = 0
        self.number_of_columns = 0
        self.data = {}
        self.extract_row_labels = True
        self.extract_col_labels = True
        self.row_labels = None
        self.col_labels = None
        self.full_parsing = False
        self.strip_whitespace = True

    def get_field_from_indices( self, row_index, column_index ):
        return self.data[ (row_index, column_index) ]

    def set_field_from_indicies( self, row_index, column_index, value ):
        self.data[ (row_index, column_index) ] = value

    def load_row( self, row_index, row_string ):
        """Take a single row (with the row delimiter stripped) and convert
        it into self.data"""
        
        split_row = re.split( self.compiled_regexes["col_delimiter"], row_string )
        for col_index, field in enumerate(split_row):
            if(self.strip_whitespace):
                field = field.strip()
            set_field_from_indices( row_index, col_index, field )

        if len( split_row ) > self.number_of_rows:
            self.number_of_columns = len( split_row )

    def load_all( self, data_string ):
        """Take entire data as string and load"""
        rows = re.split( self.compiled_regexes["row_delimiter"], data_string )
        for row_index, row in enumerate(rows):
            self.load_row( row_index, row )
            if row_index > self.number_of_rows:
                self.number_of_rows = row_index
        

    def generate_column_labels( self ):
        """Generate the column labels"""
        if self.extract_column_labels:
            labels = LabelIndexMaps( 
                [ get_field_from_indices( 0, col_index) for col_index in range(self.number_of_columns) ] )
        else:
            labels = LabelIndexMaps( [str(index) for index in range( self.number_of_columns ) ] )
        return labels

    def generate_row_labels( self ):
        """Generate row labels"""
        if self.extract_row_labels:
            labels = LabelIndexMaps(
                [ get_field_from_indices( row_index, row_index) for row_index in range(self.number_of_rows) ] )
        else:
            labels = LabelIndexMaps( [str(index) for index in range( self.number_of_rows ) ] )

    def as_dict( self, use_labels=True,metdadata="__metadata" ):
        """Return tabular data as a dictionary of dictionaries"""
        
        



