# Superliga VolleyBall Analysis

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)

If you're seeing this, you're probably a recruiter. Nice to meet you!
This project intends to display the following Data Science skills :

* Data Collection: Requests, Selenium, BeautifulSoup
* Cloud: AWS RDS Database
* Data Wrangling: SQL Queries, Pandas, Numpy
* Machine Learning: Sklearn, K-Nearest-Neighbors
* Geolocation: GeoPy, PyDeck
* Data Visualization: Plotly
* Deployment: Streamlit

## Overview

The Superliga VolleyBall Analysis is a three page dashboard exploring the available [stats](https://superliga.cbv.com.br/tabela-de-jogos-feminino) on the 'Superliga' Brazilian Volleyball Championship. Feel free to explore it: https://shrouded-beach-73431.herokuapp.com

# Page One: Results Prediction

Outputs a winner given a Guest Team and a Home Team selected by the user. The Model was trained with data from 10/28/21 to 03/08/22, with 86% accuracy. On March 18, it predicted correctly 5 out of 6 matches happening that day.

| Date          |    Home Team      |   Guest Team    | Predicted Winner   | Actual Winner |
|---------------|-------------------|-----------------|--------------------|---------------|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/134.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/131.png" alt="drawing" width="160"/>|Guest|Guest|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/141.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/156.png" alt="drawing" width="160"/>|Home|Home|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/142.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/154.png" alt="drawing" width="160"/>|Home|Guest|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/139.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/133.png" alt="drawing" width="160"/>|Home|Home|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/153.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/132.png" alt="drawing" width="160"/>|Guest|Guest|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/155.png" alt="drawing" width="160"/>|<img src="https://superliga.cbv.com.br/assets/images/equipes/138.png" alt="drawing" width="160"/>|Guest|Guest|

## Instalation


Please proceed to install Streamlit

`pip install streamlit`

And then, on your local folder, run the following

`streamlit run app.py`

## Table of Contents

## Table of Contents

