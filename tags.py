import csv
import os
import pandas
import sqlalchemy
import pymysql
import io
import re
from hexadecimal import *
from device import Device


def csv_to_df(file_path):
        '''Function takes a .csv file and returns a df'''
        with open(file_path, 'rb') as csv_file:
            #For CPU logger csv files, skip the first 3 rows to get the actual header row and data
            df = pandas.read_csv(csv_file, skiprows=2)
        
        return(df)
           

def create_csv(df, filename):
    path = '/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/tags/{}'.format(filename)
    header = df.head()

    if os.path.exists(path):
        df.to_csv(path, mode = 'w', index=False, header=True)
    else:
        header.to_csv(path, index=False)
        df.to_csv(path, mode = 'w', index=False, header=True)


def remove_zero(device_str):
    #Use regex to remove '0' between two letters. E.g: B0A3 --> BA3
    x = re.search("(^[A-Z])[0]([A-Z])", device_str)
    if x != None:
        y = re.sub("([A-Z])[0]([A-Z])", str(x.group()[0] + x.group()[2]), device)
        return(y)
    else:
        return(device_str)

def comments():
    '''Transforms COMMENT file exported from gxworks2 and uploads it to sql database'''

    file_path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/comments/COMMENT_B.csv"
    #Open unicode csv file from GX Works program and convert to dataframe
    f = io.open(file_path, mode = 'r', encoding = 'utf-16')
    df = pandas.read_csv(f, skiprows=1, delimiter='\t')
    #Rename column names
    df.rename({'Device Name': 'device_name', 'Comment': 'comment'}, axis=1, inplace=True)

    return(df)

def device_range():
    '''Creates a df with all devices inside determined range. Ex: B0 to B3FFF'''
    pass
    

if __name__ == "__main__":
    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")
    
    df1 = comments()
    #Convert df to SQL table
    df1.to_sql('B_comments', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')

    #Defining devices type and range
    link_relay = Device(start='0x0', end='0x3FFF', device_type='B')
    df2 = link_relay.address_df()
    df2.to_sql('B_range', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')


    """
    #Source path for csv files
    source_path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/"

    source_files_list = os.listdir(source_path)

    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")
    
    source_files_list = os.listdir(source_path)
    
    #Define lists for bits
    link_relay_list = []
    internal_relay_list = []
    inputs_list = []
    outputs_list = []
    used_tags = []

    #Define dictionary to append the created list
    devices_dict = {}

    for file in source_files_list:
        if file.endswith(".csv") or file.endswith(".CSV"):
            file_path = "{source_path}{file}".format(source_path = source_path, file = file)
            print(file_path)
            
            #Open unicode csv file from GX Works program and convert to dataframe
            f = io.open(file_path, mode = 'r', encoding = 'utf-16')
            df = pandas.read_csv(f, skiprows=2, delimiter='\t')
            
            #Drop Line Statement column
            df = df.drop(['Line Statement'], axis=1)

            #Drop duplicates for I/O Device name
            df = df.drop_duplicates(subset=['I/O(Device)'])
            
            for device in df['I/O(Device)']:
                device_str = str(device)
                #Use regex to remove '0' between two letters. E.g: B0A3 --> BA3
                device_str_fltrd = remove_zero(device_str)

                if device_str_fltrd.startswith('B') and device_str_fltrd not in link_relay_list:
                    link_relay_list.append(device_str_fltrd) 
                '''
                elif device_str_fltrd.startswith('M') and device_str_fltrd not in internal_relay_list:
                    internal_relay_list.append(device_str_fltrd)
                elif device_str_fltrd.startswith('X') and device_str_fltrd not in inputs_list:
                    inputs_list.append(device_str_fltrd)
                elif device_str_fltrd.startswith('Y') and device_str_fltrd not in outputs_list:
                    outputs_list.append(device_str_fltrd)        
                '''
        else:
            print('Not csv file')

    #Sort lists
    link_relay_list.sort()
    '''
    internal_relay_list.sort()
    inputs_list.sort()
    outputs_list.sort()
    '''
    #Defining devices type and range
    link_relay = Device(start='0x0', end='0x3FFF', device_type='B')
    '''    
    internal_relay = Device(start='0x0', end='0x20479', device_type='M')
    inputs = Device(start='0x0', end='0x1FFF', device_type='X')
    outputs = Device(start='0x0', end='0x1FFF', device_type='Y')
    '''
    #Creating df for each device type and all possible tags
    print(link_relay.device_df)
    #Device dictionary
    devices_dict = {
        'id': (x for x in range(1, 16385)),
        'link_relay':link_relay.range
        #'internal_relay':internal_relay.range,
        #'inputs':inputs.range,
        #'outputs':outputs.range
    }
    #df = pandas.DataFrame.from_dict(devices_dict, orient='index')
    df = pandas.DataFrame(devices_dict)
    #df = df.transpose()
    #print(df)
    #create_csv(df, 'all_addresses.csv')

    #Used Devices dictionary
    used_devices_dict = {
        'link_relay': link_relay_list
        #'internal_relay':internal_relay_list,
        #'inputs':inputs_list,
        #'outputs':outputs_list
    }
    df2 = pandas.DataFrame.from_dict(used_devices_dict, orient='index')
    df2 = df2.transpose()
    print(df2)
    create_csv(df2, 'used_addresses.csv')

    '''
    #Convert df to SQL table
    df.to_sql('ge6_ac1_available_tags', con = engine, if_exists = 'replace', index = False)
    df2.to_sql('ge6_ac1_used_tags', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')
    '''

    """
                 