import streamlit as st
import pandas as pd
import scipy.stats as stats

# Set judul halaman
st.title("Analysis of Variance (ANOVA)")

# Tambahkan deskripsi atau penjelasan singkat
st.write("Selamat datang di aplikasi Analisis Variansi (ANOVA)!")
st.write("ANOVA adalah metode statistik yang digunakan untuk membandingkan rata-rata dari tiga atau lebih kelompok yang berbeda untuk melihat apakah ada perbedaan yang signifikan di antara mereka.")
st.write("Dengan menggunakan ANOVA, kita dapat menentukan apakah ada perbedaan yang signifikan antara kelompok-kelompok tersebut berdasarkan variabel dependen yang diamati.")
st.write("ANOVA merupakan salah satu teknik penting dalam statistika dan digunakan dalam berbagai bidang, seperti ilmu sosial, ilmu biologi, ilmu ekonomi, dan ilmu kesehatan. Dengan menggunakan ANOVA, kita dapat mendapatkan pemahaman yang lebih baik tentang perbedaan kelompok dan faktor-faktor yang mempengaruhinya.")
st.write("Aplikasi ini memberikan kemudahan untuk melakukan analisis ANOVA secara interaktif. Anda dapat memasukkan data Anda, memilih jenis ANOVA yang sesuai, dan melihat hasil analisis dengan mudah melalui antarmuka aplikasi.")

st.subheader("One-Way ANOVA")
st.write("One-Way ANOVA digunakan ketika kita ingin membandingkan rata-rata dari tiga atau lebih kelompok yang dihasilkan dari satu faktor atau variabel independen.")
st.write("Pada halaman ini, Anda dapat memasukkan data kelompok, memilih metode pengujian hipotesis, dan melihat hasil analisis yang mencakup rata-rata kelompok, variabilitas dalam kelompok, dan keberartian perbedaan antara kelompok.")

# Memasukkan jumlah kelompok
num_groups = st.number_input('Jumlah Kelompok', min_value=2, step=1, value=2)

# Menginisialisasi data
data = []
for i in range(num_groups):
    data_input = st.text_area(f'Masukkan data kelompok {i+1} (pisahkan dengan koma)', '')
    data_values = [x.strip() for x in data_input.split(',')]
    data.append(data_values)

# Memasukkan taraf signifikansi (alpha)
alpha = st.number_input('Taraf Signifikansi (alpha)', min_value=0.01, max_value=0.5, step=0.01, value=0.05)

# Tombol untuk memproses data
if st.button('Proses'):
    # Memeriksa apakah ada data yang dimasukkan
    if all(data):
        # Menginisialisasi DataFrame
        df = pd.DataFrame()

        # Memeriksa validitas data
        valid_data = True
        for i, group_data in enumerate(data):
            group_values = []
            for value in group_data:
                try:
                    if '.' in value:
                        group_values.append(float(value))
                    else:
                        group_values.append(int(value))
                except ValueError:
                    valid_data = False
                    st.write(f'Data kelompok {i+1} tidak valid. Pastikan hanya memasukkan angka.')

            df[f'Kelompok {i+1}'] = group_values

        if valid_data:
            # Menampilkan data
            st.subheader('Data')
            st.write(df)

            # Melakukan uji ANOVA jika setidaknya ada 2 kelompok dengan data yang valid
            if len(df.columns) >= 2:
                result = stats.f_oneway(*[df[group] for group in df.columns])
                st.subheader('Hasil Uji ANOVA')
                st.write('Nilai p-value:', result.pvalue)
                # Menghitung titik kritis berdasarkan nilai alpha
                df_between = len(df.columns) - 1
                df_within = df.size - len(df.columns)
                critical_value = stats.f.ppf(1 - alpha, df_between, df_within)
                st.write('Titik Kritis:', critical_value)

                if result.pvalue < alpha:
                    st.write('Kesimpulan: Terdapat perbedaan signifikan antara kelompok-kelompok')
                else:
                    st.write('Kesimpulan: Tidak terdapat perbedaan signifikan antara kelompok-kelompok')

                # Menghitung jumlah kuadrat
                sum_sq_between = sum((df[group].mean() - df.values.mean()) ** 2 for group in df.columns) * len(df)
                sum_sq_within = sum((df[group] - df[group].mean()).pow(2).sum() for group in df.columns)
                sum_sq_total = sum_sq_between + sum_sq_within


                # Menghitung derajat kebebasan
                df_total = df.size - 1

                # Menghitung rata-rata kuadrat
                mean_sq_between = sum_sq_between / df_between
                mean_sq_within = sum_sq_within / df_within

                # Menghitung statistik F
                f_value = mean_sq_between / mean_sq_within

                # Membuat tabel ANOVA
                anova_table = pd.DataFrame({
                    'Sumber Variasi': ['Antar Kelompok', 'Dalam Kelompok', 'Total'],
                    'Derajat Kebebasan': [df_between, df_within, df_total],
                    'Jumlah Kuadrat': [sum_sq_between, sum_sq_within, sum_sq_total],
                    'Rata-rata Kuadrat': [mean_sq_between, mean_sq_within, None],
                    'F-Value': [f_value, None, None]
                })
                st.subheader('Tabel ANOVA')
                st.write(anova_table)

            else:
                st.write('Masukkan setidaknya dua kelompok dengan data yang valid untuk melakukan uji ANOVA.')
        else:
            st.write('Pastikan memasukkan angka untuk setiap kelompok.')
    else:
        st.write('Masukkan setidaknya satu data untuk setiap kelompok.')
