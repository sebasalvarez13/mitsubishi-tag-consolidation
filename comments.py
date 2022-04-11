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
            df = pandas.read_csv(csv_file, skiprows=1)
        
        return(df)
           

def create_csv(df, filename):
    path = '/mnt/c/Users/SA55851/Desktop/Projects/Development/Tag consolidation/csv-files/tags/{}'.format(filename)
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


if __name__ == "__main__":
    #Source path for csv files
    source_path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/Tag consolidation/csv-files/comments/"

    source_files_list = os.listdir(source_path)

    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")
    
    source_files_list = os.listdir(source_path)
    
    for file in source_files_list:
        if file.endswith(".csv") or file.endswith(".CSV"):
            file_path = "{source_path}{file}".format(source_path = source_path, file = file)
            print(file_path)
            
            #Open unicode csv file from GX Works program and convert to dataframe
            f = io.open(file_path, mode = 'r', encoding = 'utf-16')
            df = pandas.read_csv(f, skiprows=1, delimiter='\t')
            
            for index, row in df.iterrows():
                device_str = str(row['Device Name'])
                #Use regex to remove '0' between two letters. E.g: B0A3 --> BA3
                row['Device Name'] = remove_zero(device_str)

        else:
            print('Not csv file')
    
    #Rename column name
    df = df.rename(columns={'Device Name': 'device_name', 'Comment':'comment'})
    create_csv(df, 'tag_comments.csv')
  
    #Convert df to SQL table
    df.to_sql('ge6_ac1_tag_comments', con = engine, if_exists = 'replace', index = False)
    print('Dataframe upload to database')

                 