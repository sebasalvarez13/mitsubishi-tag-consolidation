import os
import pandas as pd
import sqlalchemy
import pymysql
import time
import re


engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")


def comments():
    """Open unicode csv file from GX Works program and convert to dataframe. Then upload the dataframe as a table to mysql database"""

    #file_path = f"/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/comments/ge6_cc_ac1_comments.csv"
    
    #f = io.open(file_path, mode = 'r', encoding = 'utf-16')--THIS ONE WORKS
    #f = io.open(file_path, mode = 'rb', encoding = 'utf-8') #ValueError: binary mode doesn't take an encoding argument
    #f = io.open(file_path, mode = 'r', encoding = 'utf-8') #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
    #f = io.open(file_path, mode = 'rb') #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
    
    #Source path for csv files
    source_path = "/mnt/c/Users/SA55851/Desktop/Projects/Development/tag-consolidation/csv-files/comments/"
    source_files_list = os.listdir(source_path)

    for file in source_files_list:
        if file.endswith(".csv") or file.endswith(".CSV"):
            file_path = f"{source_path}/{file}"

            #Open unicode csv file from GX Works program and convert to dataframe
            with open(file_path, encoding = 'utf-16') as f:
                df = pd.read_csv(f, skiprows=1, delimiter='\t')
                print("csv file read and convert to dataframe succesfully")
            
            #Rename column names
            df.rename({'Device Name': 'device_name', 'Comment': 'comment'}, axis=1, inplace=True)
            
            """Upload dataframe to mysql database"""
            #Removes the .csv extension of file name to generate the table name
            match = re.search("(.+)(.csv)", file)
            table_name = match.group(1)
            #Convert dataframe to sql table
            df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)
            print('Dataframe upload to database')

            

if __name__ == "__main__":
    start_time = time.time()
 
    comments()
    
    print("--- %s seconds ---" % (time.time() - start_time)) 