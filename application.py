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

        st.header()
        credentials = 'mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball'

        df = pd.read_sql("""
                    SELECT * from volleyball.out
                    """, con = credentials)


        a = 'This will be a volleyboard dashball. Or something like that ok'

if __name__ == '__main__':
    main()
