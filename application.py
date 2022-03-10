import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import *
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy.engine import result
from sqlalchemy import text
import numpy as np
import requests

def main():

    #application = Flask(__name__)

    #application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball'
    #engine = create_engine('mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball')
    credentials = 'mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball'

    df = pd.read_sql("""
                SELECT * from volleyball.out
                """, con = credentials)

    # return your first five rows
    #html = dataframe.head().to_html()

    #meta = MetaData(bind=engine)
    #MetaData.reflect(meta)
    #db = SQLAlchemy(application)

    #out = db.Table('out', db.metadata, autoload=True, autoload_with=db.engine)

    #sql = text('SELECT * from volleyball.out')
    #results = engine.execute(sql)

    # View the records
    #for record in results:
    #    print("\n", record)


    #df = pd.DataFrame(columns={'um','dois'})
    st.write(df)
    st.write(type(df))
    a = 'This will be a volleyboard dashball. Or something like that ok'

    #engine = db.create_engine('mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball', engine_opts={})

    #meta_data = db.MetaData(bind=engine)
    #db.MetaData.reflect(meta_data)

    #out_table = meta_data.tables['out']

    #result = db.select([db.func.count()]).select_from(out_table).scalar()

    #print("Count:", result)


if __name__ == '__main__':
    main()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#@application.route('/')
#def index():
#    return html



    #results = db.session.query(out).all()
    #print(type(results))
