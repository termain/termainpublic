#! /usr/bin/python

from __future__ import print_function

try:
    import yaml
except ImportError:
    print("""yaml module not found. Try package PyYAML on Fedora/Redhat and python-yaml on
       debian systems""")
    raise
    
import sys
from collections import defaultdict

class Debug:
    """Global Data for debugging"""
    data = {}
    def __init__(self, on=False):
        self.on = on
    def __call__(self, item, label ):
        if self.on:
            self.data[label] = item
        return item
    def __getitem__(self, key ):
        return self.data[key]

debug = Debug()

def split_line( line, delimitter=',' ):
    return [ element.strip() for element in line.split(delimitter) ]

def label_elements( label_list, element_list, efficient=True ):
    output = {}
    for index, label in enumerate( label_list ):
        #if set to efficient, only store values that have more than just
        #an empty string
        if not efficient or len( element_list[index] ) > 0:  
            output[label] = element_list[index]

    return output


def empty_string_factory():
    return ''


def csv_to_dictionary( csv_file, add_metadata = True ):
    """Convert a CSV to dictionary of lists using first column as labels/keys and 
       succeeding columns as
       list elements

        Returns the dictionary and an ordered list of the labels.
    
        When add_metadata flag is set, the labels list is stashed in "__labels"
    """
    dictionary = {}
    labels = []
    for line in csv_file:
        elements  = split_line( line )
        label = elements.pop(0)
        dictionary[label] = elements
        labels.append( label )

        if( add_metadata ):
            dictionary["__labels"] = labels

    return dictionary, labels

def csv_to_dictionary_with_labels( csv_file, add_metadata = True,
                                    efficient = True ):
    """Convert a CSV to dictionary of dictionaries using first column as labels/keys and 
       succeeding columns as key/values pairs with the corresponding column label as the key.
        
       1st (label row) is just a list of the labels.

       Returns the dictionary and an ordered list of the row labels

        When add_metadata flag is set, the labels lists are stashed in "__rlabels"
        and "__clabels"

        When efficient flag is set, don't store key/values of empty values.
    """
    dictionary = {}
    row_labels = []
    csv_lines = csv_file.readlines()
    label_line = split_line( csv_lines[0] ) #column label lines
    label_line_label = label_line[0]
    for line in csv_lines:
        elements = split_line( line )
        label = elements[0]
        dictionary[label] = label_elements( label_line, elements, efficient )
        row_labels.append( label )

    if( add_metadata ):
        dictionary["__rlabels"]=row_labels
        dictionary["__clabels"]=label_line

    return dictionary, row_labels, label_line
        
            

def dictionary_to_csv_string( dictionary, labels):
    """Convert a dictionary of lists to a csv string using the key as the first item in a row
    and the associated list's elements as the following elements of the row. Not a dictionary with labels"""
    csv_list = []
    for label in labels:
        row = [label]
        row.extend( dictionary[label] )
        csv_list.append( ','.join( row ) )

    return '\n'.join(csv_list)

def dictionary_with_labels_to_csv_string( dictionary, row_labels, col_labels ):
    """Convert a dictionary of lists to a csv string using the key as the first item in a row
    and the associated list's elements as the following elements of the row."""
    csv_list = []
    for rlabel in row_labels:
        line = []
        #convert row's value dict to default dict so that efficient mode works
        row_dict = defaultdict( empty_string_factory, dictionary[rlabel] )
        for clabel in col_labels:
            line.append( row_dict[clabel] )
        csv_list.append( ','.join(line) )

    csv_list.append('') #for final newline to match exe_config_sls.csv
    return '\n'.join(csv_list)

def dictionary_with_labels_and_metadata_to_csv_string( dictionary ):
    """Same as dictionary_with_labels_to_csv_string but with the row and col
        labels stashed in as metadata under __rlabels and __clabels respectively"""
    rlabels = dictionary["__rlabels"]
    clabels = dictionary["__clabels"]

    return dictionary_with_labels_to_csv_string( dictionary, rlabels, clabels )
    
def csv_to_yaml( csvfile, yamlfile ):
    csvid = open(csvfile)
    yamlid = open(yamlfile,"w")

    data, row_labels, col_labels = csv_to_dictionary_with_labels( csvid )
    yamlid.write( yaml.dump( data, default_flow_style=False) )

    csvid.close()
    yamlid.close()

def yaml_to_csv( yamlfile, csvfile ):
    csvid = open(csvfile, "w" )
    yamlid = open(yamlfile,"r")

    data = debug( 
                yaml.load( yamlid ),
           "data")

    csvid.write( dictionary_with_labels_and_metadata_to_csv_string( data ) )

    csvid.close()
    yamlid.close()


def main():
    """Usage: csv_tools.py [-h] <outputmode> <input_file> <output_file>
       
       Converts csv to yaml or vice-versa.

       outputmodes:
           csv  - convert yaml to csv
           yaml - convert csv to yaml
    """
    output_format = sys.argv[1].strip()
    if output_format == "-h":
        print(main.__doc__)
    else:
        infile = sys.argv[2].strip()
        outfile = sys.argv[3].strip()
        if output_format == "csv":
            yaml_to_csv( infile, outfile )
        elif output_format == "yaml":
            csv_to_yaml( infile, outfile )
        else:
            print(output_format + " unknown! Type csv_tools.py -h for help")

if __name__ == "__main__":
    main()



