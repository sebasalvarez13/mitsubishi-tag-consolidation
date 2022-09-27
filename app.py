from urllib import request
import sqlalchemy
import pandas as pd
import pymysql
from flask import Flask, render_template, request




app = Flask(__name__)
#syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
engine = sqlalchemy.create_engine("mysql+pymysql://sebasalvarez13:BlueYeti27@localhost/tags")
    
@app.route('/', methods = ['GET', 'POST'])
def tags():
    df = pd.read_sql_table('B_complete', con = engine)

    #Converts dataframe to html table    
    tags_html = df.to_html(classes = "table table-dark table-striped", justify = 'left', index = False)

    return render_template('dashboard.html', table = tags_html)  


@app.route('/updatetag', methods = ['GET', 'POST'])
def update_tags():
    if request.method == 'POST':
        new_comment = request.form['new_comment']
        device = request.form['device']
        query = "UPDATE B_complete SET comment = %s, status = 'Used' WHERE device_name = %s"

        #Create sql connection
        connection = engine.connect()

        connection.execute(query, (new_comment, device))

        print('tag updated')

    return render_template('update.html') 


@app.route('/deletetag', methods = ['GET', 'POST'])
def delete_tags():
    if request.method == 'POST':
        device = request.form['device']
        query = "UPDATE B_complete SET comment = '', status = 'Not Used' WHERE device_name = %s"

        #Create sql connection
        connection = engine.connect()

        connection.execute(query, (device))

        print('tag comment deleted')

    return render_template('delete.html') 



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)