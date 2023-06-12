import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def summary_statistics():
    st.title("Statistika Deskriptif")
    st.write("Selamat datang di aplikasi Statistika Deskriptif!")
    st.write("Statistika deskriptif adalah metode statistik yang digunakan untuk menganalisis, merangkum, dan menggambarkan data secara numerik dan grafis. Tujuannya adalah untuk memberikan pemahaman yang lebih baik tentang pola dan karakteristik data yang diamati.")
    st.write("Aplikasi ini menyediakan berbagai fitur untuk membantu Anda menjalankan analisis statistika deskriptif secara interaktif. Anda dapat memasukkan data Anda, melihat ringkasan statistik, dan menampilkan diagram statistika dengan mudah.")
    st.write("Aplikasi ini memiliki dua halaman utama:")
    st.subheader("1. Ringkasan Statistik")
    st.write("Pada halaman ini, Anda dapat memasukkan data Anda dan mendapatkan ringkasan statistik yang komprehensif. Ringkasan ini mencakup berbagai ukuran statistik seperti rata-rata, median, modus, kuartil, rentang, simpangan baku, dan lainnya. Selain itu, Anda juga dapat melihat distribusi data melalui histogram dan diagram boxplot.")
    st.subheader("2. Diagram Statistika")
    st.write("Pada halaman ini, Anda dapat memilih dari berbagai jenis diagram statistika untuk membantu visualisasi data Anda. Beberapa diagram yang tersedia termasuk histogram, diagram batang, diagram lingkaran, dan scatter plot. Diagram ini memungkinkan Anda melihat pola, hubungan, dan perbandingan data secara grafis.")
    st.write("Dengan menggunakan aplikasi ini, Anda dapat dengan mudah menjalankan analisis statistika deskriptif tanpa perlu menguasai pemrograman atau perangkat lunak yang kompleks. Semoga aplikasi ini membantu Anda memahami dan menggambarkan data Anda dengan lebih baik!")


    # Menampilkan pilihan input data
    st.header("Input Data")
    input_option = st.radio("Pilih opsi input data:", ("Manual", "Unggah File"))

    if input_option == "Manual":
        # Memasukkan data secara manual
        st.subheader("Masukkan Data")
        st.write("Masukkan data Anda dalam format yang sesuai.")
        st.write("Contoh : 3, 5, 6, 7")
        data_input = st.text_area("Ketik data di sini", height=200)
        if st.button("Proses"):
            try:
                # Membaca data dari input teks
                data_list = data_input.split("\n")
                data = [list(map(float, row.split(","))) for row in data_list]
                df = pd.DataFrame(data, columns=[f"Column {i+1}" for i in range(len(data[0]))])
                show_summary_statistics(df)

            except Exception as e:
                st.error("Terjadi kesalahan dalam membaca data. Pastikan format data Anda benar.")

    else:
        # Mengunggah file CSV atau Excel
        st.subheader("Unggah File")
        uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                # Membaca data dari file yang diunggah
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                show_summary_statistics(df)

            except Exception as e:
                st.error("Terjadi kesalahan dalam membaca data. Pastikan file Anda memiliki format yang benar.")

def show_summary_statistics(df):
    # Menampilkan data setelah diunggah
    st.subheader("Data yang Diunggah")
    st.dataframe(df)

    # Menghitung ringkasan statistik
    st.subheader("Ringkasan Statistik")
    summary = df.describe()
    st.dataframe(summary)

    # Menampilkan histogram
    st.subheader("Histogram")
    column = st.selectbox("Pilih kolom", options=df.columns)
    fig, ax = plt.subplots()
    ax.hist(df[column])
    st.pyplot(fig)

    # Menampilkan diagram boxplot
    st.subheader("Diagram Boxplot")
    fig, ax = plt.subplots()
    ax.boxplot(df[column])
    st.pyplot(fig)

# Panggil fungsi untuk menjalankan halaman "Ringkasan Statistik"
summary_statistics()

# Muat data dari file CSV
data = pd.read_csv("data.csv")

# Tampilkan tabel data
st.subheader("Contoh Tabel Data")
st.dataframe(data)

# Tampilkan deskripsi statistik
st.subheader("Deskripsi Statistik")
st.write(data.describe())

# Tampilkan histogram
st.subheader("Histogram")
selected_column = st.selectbox("Pilih kolom:", data.columns)
plt.hist(data[selected_column].dropna())
st.pyplot(plt)

# Tampilkan scatter plot
st.subheader("Scatter Plot")
x_column = st.selectbox("Pilih kolom x:", data.columns)
y_column = st.selectbox("Pilih kolom y:", data.columns)
plt.scatter(data[x_column], data[y_column])
plt.xlabel(x_column)
plt.ylabel(y_column)
st.pyplot(plt)



