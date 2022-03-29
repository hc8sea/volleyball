import math
import requests
import pymysql
import time
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from pprint import pprint
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from streamlit import caching

st.set_page_config(
        page_title="Superliga Feminine Volleyball Championship")


def main():

    st.header('Superliga Feminine Volleyball Championship')

    st.write(
    """
    This dashboard intends to display:

        1) Webscraping using Selenium and BeautifulSoup (see WebScraping.py)
        2) SQL Queries with databased hosted on AWS RDS
        4) K-Nearest Neighbors model training
        5) ML Prediction with input data
        6) Geolocation using GeoPy and PyDeck
        7) Stacked Areas Plot via Plotly
        8) WebApp deployment using Streamlit

         """)

    st.write('repository link: https://github.com/hc8sea/volleyball')

    #AWS RDS credentials:

    credentials = 'mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball'

    page1 = 'Results prediction'
    page2 = 'Itambé Minas Team Stats'
    page3 = 'Itambé Minas Team on the Map'

    page = st.selectbox('Select an option', (page1, page2, page3))

    st.write('')
    st.write('')
    st.write('')

    if page == page1:

        #Querying the data table created on WebScraping.py via BeautifulSoup and Selenium
        #Each line in the df DataFrame corresponds to a match and most relevant parameter according to the official statistics found on the 'Superliga' website.
        df = pd.read_sql(
                            """
                            SELECT * from volleyball.allchamp
                            """,

                            con = credentials)

        #Rearranging the parameters to create another table:

        times = np.unique(np.concatenate((df['home'].values, df['guest'].values)))
        hcriterios = ['homesets', 'homepts', 'homeace', 'homeblock']
        gcriterios = ['guestsets', 'guestpts', 'guestace', 'guestblock']

        #Creating a generic array to populate a new DataFrame with the same skeleton as df

        arr = np.ndarray(shape=df.shape)
        dfmeans = pd.DataFrame(arr, columns = [ 'id',
                                                'homesets','homepts','homeace','homeblock',
                                                'guestsets','guestpts','guestace','guestblock',
                                                'home','guest','vincitore'])

        #In dfmeans, each line corresponds to a match and the mean values of each parameters until the day before the match.
	#The goeal here is to create a link between the result's match and the combination of the relevant parameters mean values so we can create a ML model

        #Populating the home team stats:

        for time in times:
          for hcriterio in hcriterios:
              shape = df[df['home'] == time].shape[0]

              for i in range(1,shape+1):

                index = df.loc[df['id'] == df[df['home'] == time].sort_values(by='id')['id'].values[-i]].index[0]
                column = df.columns.get_loc(hcriterio)
                value = df[df['home'] == time].sort_values(by='id')[hcriterio].values[:-i].mean()
                dfmeans.iat[index,column] = value

        #Populating the guest team stats:

        for time in times:
          for gcriterio in gcriterios:
              shape = df[df['guest'] == time].shape[0]

              for i in range(1,shape+1):

                index = df.loc[df['id'] == df[df['guest'] == time].sort_values(by='id')['id'].values[-i]].index[0]
                column = df.columns.get_loc(gcriterio)
                value = df[df['guest'] == time].sort_values(by='id')[gcriterio].values[:-i].mean()
                dfmeans.iat[index,column] = value


        dfmeans['id'] = df['id']                 #Some columns will be just the sabe as df's.
        dfmeans['home'] = df['home']
        dfmeans['guest'] = df['guest']
        dfmeans['vincitore'] = df['vincitore']
        dfmeans.set_index('id',inplace=True)     #Setting the match ID as index
        dfmeans.dropna(inplace=True)             #Remove null values (the first match of each team will be useless in our analysys)
        #Separando features de labels:

        Y_ = dfmeans['vincitore']
        X_ = dfmeans.drop('vincitore', axis=1)

        #Fazendo o Encoding de atributos categóricos:

        X_dummies =  pd.get_dummies(X_,columns=['home','guest'])

        #Normalizando os valores de atributos:

        scaler_X = StandardScaler()
        scaler = scaler_X.fit(X_dummies.to_numpy())
        X_dummies_scaled = scaler.transform(X_dummies.to_numpy())

        #Renaming and normalizing the features and labels.

        y = Y_.to_numpy(dtype='float64')
        X = X_dummies_scaled

        #Training the ML model - the algorhytmn chosen is K-Nearest Neighbors, for this is a first commit and KNN tends to be a good first guess.

        X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=8)
        k = 7
        neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train,y_train)

        #At this point the user select two teams for the model to perform the prediction


        st.header('Choose two volleyball teams and find out which one would win in a match taking place today')

        player_home = st.selectbox('Choose the home team',times)
        player_guest = st.selectbox('Choose the guest team',times)

        #The feature values of the new datapoint needs to be generated
        #get_pred function does the job

        def get_pred(player_home,player_guest):

          arr_pred = np.ndarray(shape=(1,12))
          df_pred = pd.DataFrame(arr_pred, columns = ['id','homesets','homepts','homeace','homeblock','guestsets','guestpts','guestace','guestblock','home','guest','vincitore'])

          for hcriterio in hcriterios:

                column = df.columns.get_loc(hcriterio)
                value = df[df['home'] == player_home].sort_values(by='id')[hcriterio].values[:-1].mean()
                df_pred.iat[0,column] = value

          for gcriterio in gcriterios:

                column = df.columns.get_loc(gcriterio)
                value = df[df['guest'] == player_guest].sort_values(by='id')[gcriterio].values[:-1].mean()
                df_pred.iat[0,column] = value

          return df_pred

        #Calling df_pred for the chosen teams

        pred = get_pred(player_home, player_guest)

        #Finding the respective column generated by get_dummies

        column_home = f'home_{player_home}'
        column_guest = f'guest_{player_guest}'

        #Encoding the data

        X_pred = pd.DataFrame(pred, columns = X_dummies.columns)
        X_pred[column_home]=1
        X_pred[column_guest]=1
        X_pred.fillna(0,inplace=True)

        #Scaling the new data in the same fashion as done in the training stage.

        new_data = X_pred.to_numpy()
        new_data_scaled = scaler.transform(new_data)

        #Finally, the prediction:
        if st.button('Faça a previsão'):
            if player_home == player_guest:
                st.write('Escolha dois times diferentes')
            else:
                p = neigh.predict(new_data_scaled)
                if p == 1:
                    st.write('Vencedor: ', str(player_home))
                else:
                    st.write('Vencedor: ', str(player_guest))
        else:
            st.write('')

    if page == page2:

        #In this page, we will compare the contributions of 3 players across the championship in terms of 3 criteria:

        criterio = st.selectbox('Select a criteria', ('Best Attacker', 'Best Server', 'Best Blocker'))

        #The get_xy function obtains the needed information from a specific player.

        def get_xy(player,criteria):
                df = pd.read_sql(f"""
                        SELECT A.ID, A.DATE,
                        A.{criteria},
                        B.HOMEPTS, B.GUESTPTS
                        FROM volleyball.stats A JOIN volleyball.map B
                        ON A.ID = B.ID
                        WHERE A.NOME = '{player}'
                        """, con = credentials)

                df.replace(r'^\s*$', '0', regex=True,inplace=True) #Data Cleaning
                df.replace('-', '0',inplace=True)                  #Data Cleaning

                df['SETS']=df.apply(lambda x: x['HOMEPTS']+x['GUESTPTS'],axis=1)
                df['PPS']=df.apply(lambda x: float(x[f'{criteria}'])/float(x['SETS']),axis=1)
                df['DATE']=df.apply(lambda x: (x['DATE'].split()[1] + ' '+ x['DATE'].split()[3][:3] + ' ' + x['DATE'].split()[5][-2:]),axis=1)
                return df['DATE'], df['PPS']

        #The function gofigure create the Staked Areas plot, comparing 3 hand-picked players according to each criteria

        def gofigure(player1,player2,player3,criteria,recorte):
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=get_xy(player1,criteria)[0],
                    y=get_xy(player1,criteria)[1],
                    name=str(player1),
                    hoverinfo='x+y',
                    mode='lines',
                    line=dict(width=0.5, color='blue'),
                    stackgroup='one'
                ))
                fig.add_trace(go.Scatter(
                    x=get_xy(player2,criteria)[0],
                    y=get_xy(player2,criteria)[1],
                    name=str(player2),
                    hoverinfo='x+y',
                    mode='lines',
                    line=dict(width=0.5, color='gold'),
                    stackgroup='one'
                ))
                fig.add_trace(go.Scatter(
                    x=get_xy(player3,criteria)[0],
                    y=get_xy(player3,criteria)[1],
                    name=str(player3),
                    hoverinfo='x+y',
                    mode='lines',
                    line=dict(width=0.5, color='orangered'),
                    stackgroup='one'
                ))


                fig.update_layout(yaxis_range=(0, recorte))

                return st.plotly_chart(fig)

        #Now the graphs are generated according to the user's choice.


        if st.button('Build the graph'):

            if criterio == 'Best Attacker':

                gofigure('THAISA DAHER','NERIMAN OZSOY','DANIELLE CUTTINO','PONTOS_TOT', 15) #The last parameter sets the superior limit of the graph

            elif criterio == 'Best Server':

                gofigure('THAISA DAHER','JULIA KUDIESS','PRISCILA DAROIT','SERVICO_ACE', 2)

            elif criterio == 'Best Blocker':

                gofigure('THAISA DAHER','JULIA KUDIESS','CAROL GATTAZ','BLOQUEIO_PTS', 4)

    if page == page3:

        #In this section, all Itambé Minas games are shown via geolocation
        #It is possible to navigate the map and see details of each match

        latlon = pd.read_sql("""
                    SELECT DISTINCT B.ID, A.LAT, A.LON, A.VICTOR,
                    A.HOME, A.HOMEPTS, A.GUEST, A.GUESTPTS,
                    B.DATE
                    from volleyball.map A JOIN volleyball.stats B
                    ON A.ID = B.ID

                    """, con = credentials)

        latlon.replace('Ã§','ç', regex=True, inplace=True) #Correcting an issue with the ç character (dates in portuguese)

 	#Removing datapoints with failed geolocation
        latlon.drop(3,inplace=True)
        latlon.drop(4,inplace=True)
        latlon.drop(8,inplace=True)
        #latlon.drop(22,inplace=True)

        #Structuring the dataframe according to pydeck_chart's requirements

        latlon['LON'] = latlon.apply(lambda x: x['LON'] + np.random.rand()/4000, axis=1)
        latlon['LAT'] = latlon.apply(lambda x: x['LAT'] + np.random.rand()/4000, axis=1)
        latlon['COORDINATES'] = latlon.apply(lambda x: [x['LON'], x['LAT']], axis=1)
        latlon['RACKS'] = latlon.apply(lambda x: 1, axis=1)
        latlon['SPACES'] = latlon.apply(lambda x: 1, axis=1)
        latlon['tags'] = latlon.apply(lambda x: x['HOME']+' '+str(x['HOMEPTS'])+' x '+str(x['GUESTPTS'])+' '+x['GUEST']+'\n'+x['DATE'],axis=1)

        #Won/Lost Icon definition, conditioning and formatting

        ICON_URL = 'https://img.icons8.com/color-glass/452/trophy.png'
        ICON_URL_LOST = "https://img.icons8.com/emoji/452/broken-heart.png"

        icon_data = {

            "url": ICON_URL,
            "width": 242,
            "height": 242,
            "anchorY": 242,
        }

        icon_data_lost = {

            "url": ICON_URL_LOST,
            "width": 242,
            "height": 242,
            "anchorY": 242,
        }

        latlon["icon_data"] = latlon.apply(lambda x: icon_data if x['VICTOR'] == 'ITAMBE MINAS' else icon_data_lost, axis=1)

        #Criação do mapa

        icon_layer = pdk.Layer(
            type="IconLayer",
            data=latlon,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position=["LON", "LAT"],
            pickable=True,
        )

        view_state = pdk.ViewState(latitude=-22, longitude=-47, zoom=4.5, bearing=0, pitch=0)
        s = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{tags}"})

        #Map exibition

        st.pydeck_chart(s)

        #End of code

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
