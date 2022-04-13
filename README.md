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
---

The Superliga VolleyBall Analysis is a three page dashboard exploring the available [stats](https://superliga.cbv.com.br/tabela-de-jogos-feminino) on the 'Superliga' Brazilian Volleyball Championship. Feel free to explore it: https://shrouded-beach-73431.herokuapp.com

# Page One: Results Prediction

Outputs a winner given a Guest Team and a Home Team selected by the user. The Model was trained until March 18 with 92% accuracy.

| Date          |    Home Team      |   Guest Team    | Predicted Winner   | Actual Winner |
|---------------|-------------------|-----------------|--------------------|---------------|
|18/03|<img src="https://superliga.cbv.com.br/assets/images/equipes/134.png" alt="drawing" width="160"/>|![Image](https://superliga.cbv.com.br/assets/images/equipes/131.png)|Guest|Guest|
|18/03|![Image](https://superliga.cbv.com.br/assets/images/equipes/141.png)|![Image](https://superliga.cbv.com.br/assets/images/equipes/156.png)|Guest|Guest|
|18/03|![Image](https://superliga.cbv.com.br/assets/images/equipes/142.png)|![Image](https://superliga.cbv.com.br/assets/images/equipes/154.png)|Guest|Guest|
|18/03|![Image](https://superliga.cbv.com.br/assets/images/equipes/139.png)|![Image](https://superliga.cbv.com.br/assets/images/equipes/133.png)|Guest|Guest|
|18/03|![Image](https://superliga.cbv.com.br/assets/images/equipes/153.png)|![Image](https://superliga.cbv.com.br/assets/images/equipes/132.png)|Guest|Guest|
|18/03|![Image](https://superliga.cbv.com.br/assets/images/equipes/155.png)|![Image](https://superliga.cbv.com.br/assets/images/equipes/138.png)|Guest|Guest|


## Instalation
---

Please proceed to install Streamlit

`pip install streamlit`

And then, on your local folder, run the following

`streamlit run app.py`

## Table of Contents
---
## Table of Contents
---
