import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import pearsonr

st.set_page_config(layout='wide')

st.title("Korelasi Tingkat Kriminalitas di Indonesia dengan Ekonomi dan Pendidikan")
st.subheader("Oleh: Aditya Fahrezantara")
st.markdown('---')

col1, col2 = st.columns([1, 1.75])

with col1:
    st.header("Bisakah Memprediksi Tingkat Kriminalitas?")
    st.write("""
    Mungkin beberapa dari kita berpikir bahwa tingkat kriminalitas suatu daerah dapat ditebak dengan melihat kondisi ekonomi dan pendidikannya.
    Semakin rendah ekonominya, semakin rendah pendidikannya, semakin tinggi pula tingkat kriminalitasnya.
    Tentu, sebagian besar kejahatan dilatarbelakangi oleh masalah ekonomi dan tentu saja perilaku kejahatan tidak sesuai dengan apa yang diajarkan di sekolah.
    Namun, apakah kedua parameter tersebut bisa *benar-benar* menebak tingkat kriminalitas?
    """)

labels = ['Kejahatan Bermotif Ekonomi', 'Kejahatan Lainnya']
values = [112661, 78419]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)],)

with col2:
    st.plotly_chart(fig, use_container_width=True)


st.header("Mari Kita Lihat Distribusi Tingkat Kriminalitas Tiap Provinsi")
st.write("Tingkat kriminalitas didapatkan dari persamaan berikut:")
st.latex('\\frac{Jumlah\ Kejahatan}{Populasi}\\times100000')
df = pd.read_csv('./Dataset/Dataset.csv', sep=';')
df = df.iloc[:-1]
heatmap = pd.read_csv('./Dataset/heatmap.csv')
df_ = df.rename(columns={
    "daerah": "Provinsi",
    "crime_rate": "Tingkat Kriminalitas",
    "tingkat_pengangguran": "Tingkat Pengangguran",
    "umr": "Upah Minimum Provinsi",
    "tidak_tamat_sma": "Populasi yang Tidak Tamat SMA"
    })

fig = px.bar(df_, x="Provinsi", y="Tingkat Kriminalitas", barmode="group")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Peta Distribusi Tingkat Kriminalitas per Provinsi")
midpoint = [np.average(df['latitude']), np.average(df['longitude'])+5]
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state = pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=4,
        pitch=30,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data = heatmap,
            get_position = '[longitude, latitude]',
            radius=2*10000,
            auto_highlight=True,
            elevation_scale=500,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
     ],
     tooltip={"html": "<b>Tingkat Kriminalitas:</b> {elevationValue}", "style": {"color": "white"}},
 ))

st.write("Dapat dilihat bahwa setiap provinsi memiliki tingkat kriminalitas yang berbeda-beda")

st.markdown("#")
st.header("Lalu, Bagaimana Hubungannya Dengan Ekonomi dan Pendidikan?")
option = st.selectbox("Pilih variabel: ", ("Tingkat Pengangguran", "Upah Minimum Provinsi", "Populasi yang Tidak Tamat SMA"))
graph, cor = st.columns([2, 1])
with graph:
    fig = px.scatter(df_, x=option, y='Tingkat Kriminalitas')
    st.plotly_chart(fig, use_container_width=True)
with cor:
    eco, _ = pearsonr(df_['Tingkat Kriminalitas'], df_[option])
    eco = round(eco*100, 2)
    st.subheader("Korelasi antara {} dan tingkat kriminalitas adalah:".format(option.lower()))
    st.subheader("{}%".format(eco))
st.write("""
Dari hasil perhitungan korelasi antar variabel, didapatkan nilai yang rendah.
Hal ini menandakan bahwa ketiga variabel yang digunakan kurang berpengaruh terhadap tingkat kriminalitas.
""")

st.header("Kesimpulannya?")
st.write("""
Dapat disimpulkan bahwa memprediksi tingkat kriminalitas suatu daerah tidak cukup hanya dengan menggunakan variabel ekonomi dan pendidikan.
Diperlukan penelitian lebih lanjut mengenai perilaku masyarakat, psikologis masyarakat, budaya, dan berbagai macam aspek lainnya
untuk kemudian dapat ditentukan faktor-faktor utama terjadinya kriminalitas.
""")