import numpy as np
import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
#python -m streamlit run huff/huff.py

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "shops.csv")
shops = pd.read_csv(csv_path)
print(shops)

st.title("광주 복합쇼핑몰 입지에 따른 인구 유입 시뮬레이션")

def huff_probability(area, distance, alpha=1, beta=2):
    attraction = (area ** alpha) / (distance ** beta)
    return attraction

def choice_probability(areas, distances):
    scores=[]
    for i in range(len(areas)):
        scores.append(huff_probability(areas[i], distances[i]))
    results = []
    for i in range(len(areas)):
        results.append(scores[i] / np.sum(scores))
    return results

def distance(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)



def simulate(mall_area,x,y,population=10000):
    shops.loc[shops["상권명"] == "복합쇼핑몰", "면적"] = mall_area
    

    distances = shops.apply(lambda row:distance(x,y,row['위도'],row['경도']),axis=1)

    print(shops['면적'].values)
    probs = choice_probability(shops['면적'].values, distances.values)
    shops['유입인구'] = list(map(lambda x: x*population, probs))
    return shops

area = st.slider(
    "복합쇼핑몰 면적 (㎡)",
    10000, 100000, 30000, step=5000
)
st.subheader("소비자 위치")

consumer_x = st.slider(
    "(위도)",
    35.1,35.2,35.150, step=0.001
)

consumer_y = st.slider(
    "(경도)",
    126.9,127.0,126.92, step=0.001
)

result = simulate(area,consumer_x,consumer_y)

st.subheader("상권별 유입 인구")
st.dataframe(result[["상권명", "면적", "유입인구"]])
