import streamlit as st
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.stats.mstats import winsorize
from funciones_auxiliares import winsorize_transform, log_transform, LowFrequencyGrouper
import pickle

# --- Cargar modelo y pipeline ---
@st.cache_resource
def load_model_and_pipeline():
    try:
        # Cargar el modelo desde el archivo .pkl
        with open("./sprint_9/best_logistic_model.pkl", "rb") as model_file:
            model = pickle.load(model_file)

        # Cargar la pipeline desde el archivo .pkl
        with open("./sprint_9/data_transformation_pipeline.pkl", "rb") as pipeline_file:
            pipeline = pickle.load(pipeline_file)

        return model, pipeline

    except FileNotFoundError as e:
        st.error(f"Error al cargar el modelo o pipeline: {e}")
        st.stop()

# --- Configuración de la página ---
st.set_page_config(page_title="Predicción de Depósitos a Plazo", page_icon="💰", layout="wide")

# --- Encabezado ---
st.image("https://raw.githubusercontent.com/neiluz/project_machine_learning/main/sprint_9/banner.jpg", use_container_width=True)
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Predicción de Depósitos a Plazo</h1>", unsafe_allow_html=True)

# Descripción
st.markdown("""
    <style>
    .descripcion {
        font-size: 20px;  /* Ajusta el tamaño de la fuente */
        text-align: center;
        color: gray;
        margin-top: -20px;
        margin-bottom: 30px;
    }
    </style>
    <p class="descripcion">
        Esta aplicación utiliza un modelo de Machine Learning para predecir si un cliente suscribirá un depósito a plazo fijo.
        Por favor, complete el formulario a continuación para realizar una predicción.
    </p>
""", unsafe_allow_html=True)

# --- Función para inicializar valores predeterminados ---
def get_default_values():
    return {
        "education": 'unknown',
        "month": 'jan',
        "job": "management",
        "marital": "married",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "poutcome": "unknown",
        "balance": 0.0,
        "duration": 0.0,
        "pdays": 999,
        "age": 30,
        "campaign": 1,
        "previous": 0,
    }

# --- Inicializar valores predeterminados en session_state ---
if "form_values" not in st.session_state:
    st.session_state.form_values = get_default_values()

# --- Botón para limpiar formulario ---
if st.button("Limpiar Formulario"):
    st.session_state.form_values = get_default_values()

# --- Formulario de datos del cliente ---
st.header("Formulario de Datos del Cliente")

with st.form("prediction_form"):
    # Variables ordinales
    education = st.selectbox("Nivel Educativo", ['unknown', 'primary', 'secondary', 'tertiary'])
    month = st.selectbox("Mes de Contacto", ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])

    # Variables nominales
    job = st.selectbox("Ocupación", ["management", "blue-collar", "technician", "admin.", "services", "retired", "Otros"])
    marital = st.selectbox("Estado Civil", ["married", "single", "divorced"])
    default = st.selectbox("Historial de Incumplimiento", ["yes", "no"])
    housing = st.selectbox("Préstamo Hipotecario", ["yes", "no"])
    loan = st.selectbox("Préstamo Personal", ["yes", "no"])
    contact = st.selectbox("Tipo de Contacto", ["cellular", "unknown", "telephone"])
    poutcome = st.selectbox("Resultado de Campañas Anteriores", ["unknown", "failure", "success", "Otros"])

    # Variables numéricas con outliers
    balance = st.number_input("Saldo Promedio del Cliente", step=100.0, value=0.0)
    duration = st.number_input("Duración de la Última Llamada (segundos)", step=1.0, value=0.0)
    pdays = st.number_input("Días desde el Último Contacto (999 si no aplicable)", min_value=0, max_value=999, step=1, value=999)

    # Variables numéricas sin outliers
    age = st.number_input("Edad", min_value=18, max_value=100, step=1, value=30)
    campaign = st.number_input("Número de Contactos Durante la Campaña", min_value=0, step=1, value=1)
    previous = st.number_input("Número de Contactos Previos", min_value=0, step=1, value=0)

    # Botón para enviar el formulario
    submitted = st.form_submit_button("Predecir")

# --- Procesar datos al enviar el formulario ---
if submitted:
    # Guardar los valores actuales en session_state
    st.write("Formulario enviado correctamente.")
    st.session_state.form_values = {
        "education": education,
        "month": month,
        "job": job,
        "marital": marital,
        "default": default,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "poutcome": poutcome,
        "balance": balance,
        "duration": duration,
        "pdays": pdays,
        "age": age,
        "campaign": campaign,
        "previous": previous,
    }

    model, pipeline = load_model_and_pipeline()

    # Crear DataFrame con los datos ingresados
    input_data = pd.DataFrame(st.session_state.form_values, index=[0])

    # Transformar los datos
    try:
        input_data_transformed = pipeline.transform(input_data)
    except Exception as e:
        st.error(f"Error al transformar los datos: {e}")
        st.stop()

    # Hacer predicción
    prediction = model.predict(input_data_transformed)
    prediction_proba = model.predict_proba(input_data_transformed)[0, 1]

    # Mostrar resultados
    st.subheader("Resultados de la Predicción")
    if prediction[0] == 1:
        st.markdown("<p style='color: green; font-size: 24px;'>El cliente probablemente suscribirá un depósito.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: red; font-size: 24px;'>El cliente probablemente NO suscribirá un depósito.</p>", unsafe_allow_html=True)

    st.write(f"**Probabilidad de suscripción:** {prediction_proba:.2%}")
