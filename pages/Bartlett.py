import streamlit as st
import pandas as pd
import scipy.stats as stats

# Judul aplikasi
st.title('Uji Bartlett')

# Deskripsi aplikasi
st.markdown('Aplikasi ini melakukan uji Bartlett untuk membandingkan homogenitas varians antara beberapa kelompok.')

# Memasukkan jumlah kelompok
num_groups = st.number_input('Jumlah Kelompok', min_value=2, step=1, value=2)

# Menginisialisasi data
data = []
for i in range(num_groups):
    data_input = st.text_area(f'Masukkan data kelompok {i+1} (pisahkan dengan koma)', '')
    data_values = [x.strip() for x in data_input.split(',')]
    data.append(data_values)

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

            # Melakukan uji Bartlett jika setidaknya ada 2 kelompok dengan data yang valid
            if len(df.columns) >= 2:
                result = stats.bartlett(*[group for _, group in df.iteritems()])
                st.subheader('Hasil Uji Bartlett')
                st.write('Nilai p-value:', result.pvalue)

                # Memeriksa homogenitas varians berdasarkan nilai p-value
                alpha = 0.05
                if result.pvalue < alpha:
                    st.write('Kesimpulan: Terdapat perbedaan signifikan dalam varians kelompok-kelompok')
                else:
                    st.write('Kesimpulan: Tidak terdapat perbedaan signifikan dalam varians kelompok-kelompok')

            else:
                st.write('Masukkan setidaknya dua kelompok dengan data yang valid untuk melakukan uji Bartlett.')
        else:
            st.write('Pastikan memasukkan angka untuk setiap kelompok.')
    else:
        st.write('Masukkan setidaknya satu data untuk setiap kelompok.')
