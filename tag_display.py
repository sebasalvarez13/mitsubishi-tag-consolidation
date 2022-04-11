import encodings
from multiprocessing import connection
import sqlalchemy
import pymysql
import os
import csv
import pandas

def create_csv(df, filename):
    path = '/mnt/c/Users/SA55851/Desktop/Projects/Development/Tag consolidation/csv-files/tags/{}'.format(filename)
    header = df.head()

    if os.path.exists(path):
        df.to_csv(path, mode = 'w', index=False, header=True, encoding='utf-16', sep='\t')
    else:
        header.to_csv(path, index=False)
        df.to_csv(path, mode = 'w', index=False, header=True, encoding='utf-16', sep='\t')


if __name__ == '__main__':
    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")

    #Create sql connection
    connection = engine.connect()

    df = pandas.read_sql_table('B_tags_complete', con = engine)
    create_csv(df, 'b_complete_tags.csv')
    
    