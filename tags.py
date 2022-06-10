import csv
import os
import pandas
import sqlalchemy
import pymysql
import io
import re
import json
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
        y = re.sub("([A-Z])[0]([A-Z])", str(x.group()[0] + x.group()[2]), device_str)
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


def used_devices():
    '''Generates a list of devices being used'''
    #Define lists for bits
    B_devices_list = []
    #Define dictionary to append the created list
    devices_dict = {}

    #Source path for csv files
    source_path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/"
    source_files_list = os.listdir(source_path)
    
    #Iterate and transform csv files from GXworks2
    for file in source_files_list:
        if file.endswith(".csv") or file.endswith(".CSV"):
            file_path = f"{source_path}/{file}"
        
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

                if device_str_fltrd.startswith('B') and device_str_fltrd not in B_devices_list:
                    B_devices_list.append(device_str_fltrd) 

        
        else:
            print('Not csv file')

    B_devices_list.sort()

    #Used devices dictionary
    used_devices_dict = {
        'device_name': B_devices_list
    }
    df = pandas.DataFrame.from_dict(used_devices_dict, orient='index')
    df = df.transpose()

    return(df)


def json_to_csv():
    path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/complete"
    df = pandas.read_json(f'{path}/B_complete.json')
    df.to_csv(f'{path}/B_complete.csv', mode = 'w', index=False, header=True, encoding = 'utf-16', sep='\t')


if __name__ == "__main__":
    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")
    
    #Get B devices with comments. Used or not used
    df1 = comments()
    df1.to_sql('B_comments', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')

    #Defining devices type and range
    link_relay = Device(start='0x0', end='0x3FFF', device_type='B')
    df2 = link_relay.address_df()
    df2.to_sql('B_range', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')

    #Get used B devices
    df3 = used_devices()
    df3.to_sql('B_used_devices', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')

    #Convert exported table from sql (json) to csv
    json_to_csv()

                 