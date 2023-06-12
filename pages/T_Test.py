import streamlit as st
import pandas as pd
from scipy.stats import shapiro, ttest_1samp
from scipy.stats import norm

def main():
    st.title("Statistik Deskriptif dan Uji t")
    
    with st.expander('Input Data'):
        data = st.text_input("Enter data (comma-separated)")
        input_button = st.button("Submit")
    
    df = pd.DataFrame()  # Inisialisasi DataFrame kosong
    
    if input_button:
        # Convert the user input into a DataFrame
        data_list = data.split(',')
        df = pd.DataFrame(data_list, columns=['data'])
    
        # Transpose the DataFrame
        df_transposed = df.transpose()
    
        # Display the transposed DataFrame
        st.dataframe(df_transposed)
    
    with st.expander('View Statistics'):
        if not df.empty:  # Memastikan DataFrame tidak kosong
            st.dataframe(df.describe().transpose())
        else:
            st.warning("Tidak ada data yang dimasukkan. Silakan masukkan data terlebih dahulu.")
    
    st.write('## Constructing')
    st.latex('H_{0} : \mu = \mu_{0}')
    st.latex('H_{1} : \mu \\neq \mu_{1}') # \neq stands for not eq
    
    alpha = st.number_input('Masukkan Nilai α', step=0.001, min_value=0., max_value=1.0)
    null_mean = st.number_input('Masukkan Nilai $\\mu_{0}$', step=0.001)
    
    clicked = st.button('Do The t Test !!')
    
    if clicked:
        alpha_t = norm.ppf(1 - alpha / 2)
        t_statistic, p_value = ttest_1samp(df['data'], popmean=null_mean)
        
        if abs(t_statistic) > alpha_t:
            st.latex('REJECT H_{0}')
        else:
            st.latex('CAN NOT REJECT H_{0}')
        
        st.write(f'TITIK KRITIS = {alpha_t}, hitung t = {t_statistic}, p_value = {p_value}')
    
    st.write('CHECK NORMALITY')
    
    clicked_2 = st.button('Do The Shapiro Test !!')
    
    if clicked_2:
        if not df.empty:  # Memastikan DataFrame tidak kosong
            result = shapiro(df['data'])
            st.write(result)
            st.bar_chart(df['data'])
        else:
            st.warning("Tidak ada data yang dimasukkan. Silakan masukkan data terlebih dahulu.")

if __name__ == '__main__':
    main()
