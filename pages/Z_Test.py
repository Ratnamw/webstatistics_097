import streamlit as st
import pandas as pd
from scipy.stats import shapiro, norm, zscore

def main():
    st.title("Statistik Deskriptif dan Uji Z")
    
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
    
    clicked = st.button('Do The Z Test !!')
    
    if clicked:
        alpha_z = norm.ppf(1 - alpha / 2)
        
        # Check normality using Shapiro-Wilk test
        shapiro_stat, shapiro_pvalue = shapiro(df['data'])
        
        if shapiro_pvalue < alpha:
            st.write("Data tidak terdistribusi normal")
            st.write(f'Shapiro-Wilk Test: Test Statistic = {shapiro_stat}, p-value = {shapiro_pvalue}')
        else:
            st.write("Data terdistribusi normal")
            st.write(f'Shapiro-Wilk Test: Test Statistic = {shapiro_stat}, p-value = {shapiro_pvalue}')
            
            # Perform Z-test
            z_scores = zscore(df['data'])
            z_statistic = (df['data'].mean() - null_mean) / (df['data'].std() / len(df['data'])**0.5)
            p_value = norm.sf(abs(z_statistic)) * 2
            
            if abs(z_statistic) > alpha_z:
                st.latex('REJECT H_{0}')
            else:
                st.latex('CAN NOT REJECT H_{0}')
            
            st.write(f'TITIK KRITIS = {alpha_z}, hitung z = {z_statistic}, p_value = {p_value}')
    
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
