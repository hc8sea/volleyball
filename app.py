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
        page_title="Superliga Feminina de Vôlei",
)


def main():

    st.header('Superliga Feminina de Vôlei')

    st.write(
    """
    Este Dashboard objetiva demonstrar a implementação de:

        1) Webscraping usando Selenium e BeautifulSoup (ver arquivo data_collection.py)
        2) Solicitações em SQL com database armazenada no AWS RDS
        4) Treinamento de modelo K-Nearest Neighbors
        5) Previsão via ML utilizando dados inseridos pelo usuário
        6) Geolocalização usando GeoPy e PyDeck
        7) Plot do tipo Stacked Areas via Plotly
        8) Deployment de webapp utilizando Streamlit

         """)

    st.write('Mais em: https://github.com/hc8sea/volleyball')

    #Credenciais para acesso da tabela armazenada no AWS RDS

    credentials = 'mysql+pymysql://hc8sea:portfoliopassword@volleyball.cf69hpkhvjyq.us-east-1.rds.amazonaws.com/volleyball'

    page1 = 'Previsão de Resultados Superliga'
    page2 = 'Estatísticas Itambé Minas'
    page3 = 'Mapa de jogos Itambé Minas'

    page = st.selectbox('Selecione uma opção', (page1, page2, page3))

    st.write('')
    st.write('')
    st.write('')

    if page == page1:

        #Solicitando a tabela de estatísticas, gerada no arquivo WebScraping.py via BeautifulSoup e Selenium
        #Cada linha do DataFrame df corresponde a uma partida e um recorte das pontuações envolvidas

        df = pd.read_sql(
                            """
                            SELECT * from volleyball.allchamp
                            """,

                            con = credentials)

        #Organizando os parâmetros utilizados para gerar uma outra tabela:

        times = np.unique(np.concatenate((df['home'].values, df['guest'].values)))
        hcriterios = ['homesets', 'homepts', 'homeace', 'homeblock']
        gcriterios = ['guestsets', 'guestpts', 'guestace', 'guestblock']

        #Gerando uma array genérica para popular um novo DataFrame dfmeans com o mesmo esqueleto de df

        arr = np.ndarray(shape=df.shape)
        dfmeans = pd.DataFrame(arr, columns = [ 'id',
                                                'homesets','homepts','homeace','homeblock',
                                                'guestsets','guestpts','guestace','guestblock',
                                                'home','guest','vincitore'])

        #Em dfmeans, cada linha corresponde a uma partida e aos valóres médios de cada parâmetro até então.
        #O objetivo é atrelar o resultado de cada partida com a média histórica, para criar um modelo de ML.

        #Populando as estatísticas dos times anfitriões:

        for time in times:
          for hcriterio in hcriterios:
              shape = df[df['home'] == time].shape[0]

              for i in range(1,shape+1):

                index = df.loc[df['id'] == df[df['home'] == time].sort_values(by='id')['id'].values[-i]].index[0]
                column = df.columns.get_loc(hcriterio)
                value = df[df['home'] == time].sort_values(by='id')[hcriterio].values[:-i].mean()
                dfmeans.iat[index,column] = value

        #Populando as estatísticas dos times convidados:

        for time in times:
          for gcriterio in gcriterios:
              shape = df[df['guest'] == time].shape[0]

              for i in range(1,shape+1):

                index = df.loc[df['id'] == df[df['guest'] == time].sort_values(by='id')['id'].values[-i]].index[0]
                column = df.columns.get_loc(gcriterio)
                value = df[df['guest'] == time].sort_values(by='id')[gcriterio].values[:-i].mean()
                dfmeans.iat[index,column] = value


        dfmeans['id'] = df['id']                 #Algumas colunas serão idênticas às de df.
        dfmeans['home'] = df['home']
        dfmeans['guest'] = df['guest']
        dfmeans['vincitore'] = df['vincitore']
        dfmeans.set_index('id',inplace=True)     #Coloca o ID de cada partida como índice
        dfmeans.dropna(inplace=True)             #Remove valores nulos

        #Separando features de labels:

        Y_ = dfmeans['vincitore']
        X_ = dfmeans.drop('vincitore', axis=1)

        #Fazendo o Encoding de atributos categóricos:

        X_dummies =  pd.get_dummies(X_,columns=['home','guest'])

        #Normalizando os valores de atributos:

        scaler_X = StandardScaler()
        scaler = scaler_X.fit(X_dummies.to_numpy())
        X_dummies_scaled = scaler.transform(X_dummies.to_numpy())

        #Renomeando e padronizando as arrays de features e labels.

        y = Y_.to_numpy(dtype='float64')
        X = X_dummies_scaled

        #Fazendo o treinamento do modelo de ML. A escolha foi pelo algoritmo KNN.

        X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=8)
        k = 7
        neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train,y_train)

        #Neste ponto, o usuário escolhe quais times deseja comparar


        st.header('Escolha dois times')

        player_home = st.selectbox('Escolha o time anfitrião',times)
        player_guest = st.selectbox('Escolha o time visitante',times)

        #Como a previsão depende da combinação da média histórica de cada time, estes dados precisam ser gerados
        #A função get_pred faz parte deste serviço

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

        #Chamando df_pred para os times escolhidos

        pred = get_pred(player_home, player_guest)

        #Encontrando a respectiva coluna gerada pelo get_dummies

        column_home = f'home_{player_home}'
        column_guest = f'guest_{player_guest}'

        #Fazendo o Encoding em concordância com o treinamento.

        X_pred = pd.DataFrame(pred, columns = X_dummies.columns)
        X_pred[column_home]=1
        X_pred[column_guest]=1
        X_pred.fillna(0,inplace=True)

        #Normalizando os novos dados usando o mesmo "molde" da etapa de treinamento.

        new_data = X_pred.to_numpy()
        new_data_scaled = scaler.transform(new_data)

        #Obtendo a previsão de vitória
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

        #Nesta página, comparamos as contribuições de 3 jogadoras ao longo das partidas em termos de três critérios

        criterio = st.selectbox('Selecione um critério', ('Maior Pontuadora', 'Melhor Sacadora', 'Melhor Bloqueadora'))

        #A função get_xy obtém as informações necessárias de uma jogadora específica.

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

        #A função gofigure cria o gráfico de Stacked Areas
        #A comparação se dá entre 3 jogadoras mediante o criterio selecionado ao longo do campeonato.

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

        #A seguir, os gráficos são gerados conforme a escolha do usuário.


        if st.button('Construa o gráfico'):

            if criterio == 'Maior Pontuadora':

                gofigure('THAISA DAHER','NERIMAN OZSOY','DANIELLE CUTTINO','PONTOS_TOT', 15) #O último parâmetro dá o limite superior do gráfico.

            elif criterio == 'Melhor Sacadora':

                gofigure('THAISA DAHER','JULIA KUDIESS','PRISCILA DAROIT','SERVICO_ACE', 2)

            elif criterio == 'Melhor Bloqueadora':

                gofigure('THAISA DAHER','JULIA KUDIESS','CAROL GATTAZ','BLOQUEIO_PTS', 4)

    if page == page3:

        #Nesta seção, todos os jogos do time Itambé Minas são mostrados via Geolocalização
        #É possível navegar o mapa e diferenciar jogos vitoriosos e não-vitoriosos.

        latlon = pd.read_sql("""
                    SELECT DISTINCT B.ID, A.LAT, A.LON, A.VICTOR,
                    A.HOME, A.HOMEPTS, A.GUEST, A.GUESTPTS,
                    B.DATE
                    from volleyball.map A JOIN volleyball.stats B
                    ON A.ID = B.ID

                    """, con = credentials)

        latlon.replace('Ã§','ç', regex=True, inplace=True) #Corrigindo um problema com o cedilha

 #Removendo pontos do mapa onde a localização não foi obtida
        latlon.drop(3,inplace=True)
        latlon.drop(4,inplace=True)
        latlon.drop(8,inplace=True)
        #latlon.drop(22,inplace=True)

        #Formatação do DataFrame nos moldes exigidos pelo pydeck_chart

        latlon['LON'] = latlon.apply(lambda x: x['LON'] + np.random.rand()/4000, axis=1)
        latlon['LAT'] = latlon.apply(lambda x: x['LAT'] + np.random.rand()/4000, axis=1)
        latlon['COORDINATES'] = latlon.apply(lambda x: [x['LON'], x['LAT']], axis=1)
        latlon['RACKS'] = latlon.apply(lambda x: 1, axis=1)
        latlon['SPACES'] = latlon.apply(lambda x: 1, axis=1)
        latlon['tags'] = latlon.apply(lambda x: x['HOME']+' '+str(x['HOMEPTS'])+' x '+str(x['GUESTPTS'])+' '+x['GUEST']+'\n'+x['DATE'],axis=1)

        #Escolha, formatação e condicionamento dos ícones de vitória e derrota

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

        #Exibição do mapa

        st.pydeck_chart(s)

        #Fim do código

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
