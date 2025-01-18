import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# App Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Prediksi Biaya Kesehatan</h1>", unsafe_allow_html=True)

# Sidebar for navigation with custom CSS for white background
st.markdown("""
    <style>
        .css-1d391kg {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Input Data", "Hasil Prediksi", "Tentang Aplikasi", "Data Pengguna"])

if page == "Input Data":
    # Main Section: Input + Prediction
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>📂Silahkan Masukan Data</h2>", unsafe_allow_html=True)

    # Layout Grid: 2 columns for input fields
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Usia (Tahun):", min_value=0, max_value=120, value=30, step=1)
        bmi = st.number_input("Indeks Massa Tubuh:", min_value=0.0, max_value=100.0, value=25.0, step=0.1)

    with col2:
        children = st.number_input("Jumlah Anak:", min_value=0, max_value=10, value=0, step=1)
        sex = st.selectbox("Jenis Kelamin:", options=["Laki-laki", "Perempuan"])
        smoker = st.selectbox("Riwayat Asma:", options=["Ya", "Tidak"])
        region = st.selectbox("Wilayah:", options=["Jawa", "Kalimantan", "Sulawesi", "Papua"])

    # Convert categorical inputs
    sex = 1 if sex == "Laki-laki" else 0
    smoker = 1 if smoker == "Ya" else 0
    region_mapping = {"Jawa": 0, "Kalimantan": 1, "Sulawesi": 2, "Papua": 3}
    region = region_mapping[region]

    # Create DataFrame for input data
    input_data = pd.DataFrame({
        'age': [age],
        'children': [children],
        'smoker': [smoker],
        'region': [region],
        'bmi': [bmi],
        'sex': [sex]
    })

    # Adding a Progress Bar for Model Prediction
    if st.button("Prediksi Biaya"):
        with st.spinner('Memproses data dan menghasilkan prediksi...'):
            time.sleep(2)  # Simulate model processing time
            
            # Simulated prediction logic (replace with actual model prediction)
            prediction = (age * 200) + (bmi * 100) + (children * 500) + (smoker * 1000) + (region * 300)

            # Store the prediction in session state
            st.session_state.prediction = prediction

        # Recommendations based on conditions
        if smoker == 1:
            st.warning("Kurangi tidur larut malam untuk mengurangi resiko kesehatan anda.")
        if bmi > 30:
            st.warning("BMI Anda menunjukkan obesitas. Segera lakukan olahraga dan.")

        # Plot the input data vs prediction
        fig = px.bar(
            x=['Usia', 'Jumlah Anak', 'BMI', 'Status Merokok', 'Wilayah', 'Jenis Kelamin'],
            y=[age, children, bmi, smoker, region, sex],
            labels={'x': 'Fitur', 'y': 'Nilai'},
            title="Input Data vs Prediksi Biaya Medis"
        )
        st.plotly_chart(fig)

elif page == "Hasil Prediksi":
    st.markdown("<h2 style='text-align: center; color: #34495e;'>Hasil Prediksi</h2>", unsafe_allow_html=True)
    
    # Display the prediction if it exists
    if "prediction" in st.session_state:
        prediction = st.session_state.prediction
        st.markdown(f"""
            <div style='background-color: #e74c3c; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
                <h3 style='text-align: center; color: #ffffff;'>Hasil Prediksi</h3>
                <h4 style='text-align: center; color: #ffffff;'>Prediksi Biaya Kesehatan Anda: <span style='color: #ffffff;'>${prediction:,.2f}</span></h4>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Silakan masukkan data terlebih dahulu untuk melihat hasil prediksi.")

elif page == "Tentang Aplikasi":
    st.markdown("<h2 style='text-align: center; color: #34495e;'>Tentang Aplikasi</h2>", unsafe_allow_html=True)
    st.write("""
    Aplikasi ini digunakan untuk memprediksi biaya kesehatan berdasarkan faktor-faktor seperti usia, BMI, jumlah anak, jenis kelamin, riwayat asma, dan wilayah tempat tinggal.
    Prediksi ini hanya bersifat simulasi dan tidak menggantikan konsultasi medis profesional.
    """)

elif page == "Data Pengguna":
    st.markdown("<h2 style='text-align: center; color: #34495e;'>Data Pengguna</h2>", unsafe_allow_html=True)
    st.write("""
    Data pengguna yang telah dimasukkan akan ditampilkan di sini.
    Anda dapat melacak dan mengelola data prediksi berdasarkan input yang telah diberikan.
    """)

    # Load the regression data from CSV
    try:
        regression_data = pd.read_csv('Regression.csv')
        st.write("Data dari file Regression.csv:")
        st.dataframe(regression_data)

        # Create a scatter plot for Age vs Predicted Cost
        if 'age' in regression_data.columns and 'predicted_cost' in regression_data.columns:
            scatter_fig = px.scatter(
                regression_data,
                x='age',
                y='predicted_cost',
                color='bmi',  # Assuming 'bmi' is a column in the CSV
                size='bmi',   # Size of the points based on BMI
                hover_name='bmi',  # Show BMI on hover
                title="Hubungan Usia dan Biaya Kesehatan yang Diprediksi",
                labels={'age': 'Usia (Tahun)', 'predicted_cost': 'Biaya Kesehatan yang Diprediksi'},
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(scatter_fig)
        else:
            st.error("Kolom 'age' atau 'predicted_cost' tidak ditemukan dalam dataframe.")

    except FileNotFoundError:
        st.error("File 'Regression.csv' tidak ditemukan. Pastikan file tersebut ada di direktori yang sama dengan aplikasi.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")

    # Display Distribution Chart for Medical Costs (Simulated)
    st.markdown("<div class='card-header'>📈 Distribusi Biaya Medis (Simulasi)</div>", unsafe_allow_html=True)

    # Example: Simulated distribution of medical costs for visualization
    np.random.seed(42)
    simulated_data = np.random.normal(loc=5000, scale=2000, size=1000)  # Example distribution

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(simulated_data, kde=True, color='orange', bins=30)
    ax.set_title('Distribusi Biaya Medis (Simulasi)')
    ax.set_xlabel('Biaya Medis')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)

# Footer
st.markdown("""
    <style>
    .footer {
        text-align: center;
        font-size: 14px;
        color: #7f8c8d;
        margin-top: 50px;
        font-style: italic;
    }
    </style>
    <div class="footer">
        Dibuat oleh Aldi Juliansyah • 211220117 ©2025
    </div>
""", unsafe_allow_html=True)

# Additional Styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #27ae60;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #219150;
    }
    .stSelectbox, .stNumberInput {
        background-color: black;
        border-radius: 5px;
        border: 1px solid #d1d1d1;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)