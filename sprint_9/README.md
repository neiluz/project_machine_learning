# Proyecto: Predicción de Suscripción a Depósitos a Plazo

## Descripción
Esta aplicación utiliza un modelo de **Machine Learning** para predecir la probabilidad de que un cliente suscriba un depósito a plazo fijo. Ha sido diseñada para ofrecer una interfaz interactiva con **Streamlit**, permitiendo a los usuarios introducir datos de cliente y obtener predicciones en tiempo real.

## Funcionalidades
1. **Carga dinámica del modelo y pipeline:**
   - El modelo de regresión logística y la pipeline de preprocesamiento fueron entrenados y exportados en formato `.pkl` para su uso en producción.
   - Estos archivos son cargados dinámicamente en la aplicación utilizando rutas relativas.

2. **Formulario interactivo:**
   - Los usuarios pueden introducir las características del cliente (edad, saldo, ocupación, etc.) a través de un formulario interactivo en la interfaz de Streamlit.

3. **Predicciones en tiempo real:**
   - La aplicación devuelve una predicción binaria (Sí/No) sobre la probabilidad de suscripción y muestra el porcentaje asociado.

4. **Interfaz visual profesional:**
   - Incluye una imagen de encabezado (`banner.jpg`) y estilos personalizados para ofrecer una experiencia de usuario atractiva y profesional.

---

## Funcionalidades Documentación del Código
El código está dividido en módulos bien documentados para mejorar la legibilidad:

* **bank_app.py:** Contiene el flujo principal de la aplicación.
  - Carga del modelo y pipeline.
  - Creación de la interfaz en Streamlit.
  - Procesamiento de datos y predicciones.

* **funciones_auxiliares.py:** Incluye transformaciones personalizadas como winsorización y agrupamiento de categorías de baja frecuencia.

* **Pipeline de preprocesamiento:** Incluye manejo de outliers, codificación de variables categóricas y escalado de datos.

---
## Dependencias
* Python 3.10+
* Paquetes principales:
* streamlit==1.40.1
* pandas==2.2.2
* numpy==1.26.4
* scikit-learn==1.4.2
* scipy==1.13.0

Todos los paquetes necesarios están especificados en el archivo requirements.txt.

---
## Uso de la Aplicación
* Formulario de entrada: Completar el formulario con datos del cliente, como ocupación, estado civil, edad, saldo, entre otros.
* Resultados de predicción: La aplicación mostrará si el cliente probablemente suscribirá un depósito junto con la probabilidad estimada.
* Restablecer formulario:Se incluye un botón para limpiar todos los campos y permitir nuevas predicciones.
* Link de la app: https://bankapppy-h97e4umreppqtjz7v3dp9t.streamlit.app/
