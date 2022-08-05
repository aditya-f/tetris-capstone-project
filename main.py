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

st.header("Bisakah Memprediksi Tingkat Kriminalitas?")
col1, col2 = st.columns([1, 1])
with col1:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("""
    Mungkin beberapa dari kita berpikir bahwa tingkat kriminalitas suatu daerah dapat ditebak dengan melihat kondisi ekonomi dan pendidikannya.
    Semakin rendah ekonominya, semakin rendah pendidikannya, semakin tinggi pula tingkat kriminalitasnya.
    Tentu, sebagian besar kejahatan dilatarbelakangi oleh masalah ekonomi dan tentu saja perilaku kejahatan tidak sesuai dengan moral yang diajarkan di sekolah.
    Namun, apakah kedua parameter tersebut bisa *benar-benar* mengukur tingkat kriminalitas?
    """)

with col2:
    labels = ['Kejahatan Bermotif Ekonomi', 'Kejahatan Lainnya']
    values = [112661, 78419]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textfont_size=24)
    fig.update_layout(
        width=100,
        height=300,
        margin=dict(
        l=0,
        r=0,
        b=50,
        t=0,
        pad=10
    ),
    # paper_bgcolor="LightSteelBlue",
    )
    st.plotly_chart(fig, use_container_width=True)


st.header("Mari Kita Lihat Distribusi Tingkat Kriminalitas Tiap Provinsi")
st.write("Tingkat kriminalitas didapatkan dari persamaan berikut:")
st.latex('Tingkat\ Kriminalitas\ = \ \\frac{Jumlah\ Kejahatan}{Populasi}\\times100.000')
df = pd.read_csv('./Dataset/Dataset.csv', sep=';')
df = df.iloc[:-1]
heatmap = pd.read_csv('./Dataset/heatmap.csv')
df_ = df.rename(columns={
    "daerah": "Provinsi",
    "crime_rate": "Tingkat Kriminalitas",
    "tingkat_pengangguran": "Tingkat Pengangguran",
    "umr": "Upah Minimum Provinsi",
    "lama_sekolah": "Rerata Lama Sekolah",
    "jumlah_penduduk_miskin": "Jumlah Penduduk Miskin",
    })
df_.drop(['longitude', 'latitude'], inplace=True, axis=1)
df_['Tingkat Kriminalitas'] = df_['Tingkat Kriminalitas'].astype(int)
df_['Jumlah Penduduk'] = df_['Jumlah Penduduk'].astype(int)
df_['Jumlah Penduduk Miskin'] = df_['Jumlah Penduduk Miskin'].astype(int)
df_['Upah Minimum Provinsi'] = df_['Upah Minimum Provinsi'].astype(int)

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

st.header("Lalu, Bagaimana Hubungannya Dengan Ekonomi dan Pendidikan?")

var = ["Rerata Lama Sekolah", "Upah Minimum Provinsi", "Jumlah Penduduk Miskin", "Tingkat Pengangguran"]
st.write("Variabel yang digunakan adalah:")
st.write("- "+var[0]+" (Tahun)")
st.write("- "+var[1]+" (Juta Rupiah)")
st.write("- "+var[2]+" (Jiwa)")
st.write("- "+var[3]+" (Persen Penduduk)")


option = st.selectbox("Pilih variabel: ", (var[0], var[1], var[2], var[3]))
graph, cor = st.columns(2)
with graph:
    fig = px.scatter(df_, x=option, y='Tingkat Kriminalitas')
    st.plotly_chart(fig, use_container_width=True)
with cor:
    eco, _ = pearsonr(df_['Tingkat Kriminalitas'], df_[option])
    eco = round(eco, 3)

    st.write("\n")
    st.write("\n")
    st.write("\n")

    st.subheader("Korelasi antara {} dan tingkat kriminalitas adalah:".format(option.lower()))
    st.subheader("{}".format(eco))
    st.caption("Catatan:")
    st.caption("Nilai korelasi berada di antara -1 dan 1, dengan nilai 0 menyatakan tidak ada korelasi.")
    st.caption("Nilai positif berarti jika satu variabel naik, variabel yang lain juga naik.")
    st.caption("Nilai negatif berarti jika satu variabel naik, variabel yang lain turun.")

# st.write("""
# Dari hasil perhitungan korelasi antar variabel, didapatkan nilai yang rendah.
# Hal ini menandakan bahwa ketiga variabel yang digunakan kurang berpengaruh terhadap tingkat kriminalitas.
# """)

def corr(option):
    eco, _ = pearsonr(df_['Tingkat Kriminalitas'], df_[option])
    eco = round(eco, 3)
    return eco

st.header("Kesimpulannya?")
teks, tabel = st.columns(2)
with teks:
    st.write("""
    Dapat disimpulkan bahwa dari empat variabel yang digunakan, hanya variabel tingkat pengangguran yang kurang berkorelasi dengan tingkat kriminalitas.

    Namun, berbeda dengan hipotesis awal, semakin tinggi rerata lama sekolah dan upah minimum, tingkat kriminalitas tidak menurun.
    Jumlah penduduk miskin yang rendah pun tidak membuat suatu daerah memiliki tingkat kriminalitas yang rendah.

    Oleh karena itu, untuk memprediksi tingkat kriminalitas suatu daerah tidak cukup hanya dengan menggunakan variabel ekonomi dan pendidikan.
    Diperlukan penelitian lebih lanjut mengenai perilaku masyarakat, psikologis masyarakat, budaya, dan berbagai macam aspek lainnya
    untuk kemudian dapat ditentukan faktor-faktor utama terjadinya kriminalitas.
    """)
with tabel:
    st.write("\n")
    cor = {'No.':[1, 2, 3, 4], 'Variabel': var, 'Nilai Korelasi': [corr(var[0]), corr(var[1]), corr(var[2]), corr(var[3])]}
    cor = pd.DataFrame(data=cor)
    cor.set_index('No.', inplace=True)
    st.dataframe(cor)

with st.expander("Data yang Digunakan"):
    st.dataframe(df_)
