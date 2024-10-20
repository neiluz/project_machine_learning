# **Documentación del Proceso de Recolección de Datos para el Proyecto de Predicción de Suscripción de Depósitos Bancarios**

## **1. Fuentes de Datos**

### **Identificación de Fuentes:**
- **Base de datos relacional** del banco, alojada en un servidor seguro.
  
### **Descripción de las Fuentes:**
- **Base de datos relacional (MySQL/PostgreSQL)**: Almacena información detallada sobre los clientes del banco, incluyendo datos demográficos, información financiera (saldo anual promedio, préstamos) y registros de campañas de marketing.

#### **¿Por qué utilizar una base de datos?**
- **Base de datos**: Se utiliza porque la mayoría de los datos bancarios son de gran volumen y se modifican continuamente. Una base de datos relacional permite gestionar estas actualizaciones de manera eficiente, ofreciendo seguridad y consistencia. Además, permite realizar consultas complejas para extraer datos específicos y garantiza acceso a datos actualizados en tiempo real.

---

## **2. Métodos de Recolección de Datos**

### **Procedimientos y Herramientas:**
1. **Base de datos**: Los datos se recolectan y actualizan continuamente a través de los sistemas CRM del banco. El sistema automatiza la recolección de datos financieros, registros de transacciones e información de campañas.

### **Frecuencia de Recolección:**
- **Base de datos**: En tiempo real (los registros se actualizan continuamente con nuevas transacciones e interacciones).

### **Scripts de Extracción de Datos desde la Base de Datos**:

**Ejemplo de conexión a la base de datos y consulta SQL en Python:**

````python
import pymysql
import pandas as pd

# Conectar a la base de datos
conexion = pymysql.connect(
    host='servidor_banco',  # Dirección del servidor de la base de datos
    user='usuario',         # Usuario de la base de datos
    password='tu_contraseña',  # Contraseña
    db='nombre_base_datos'   # Nombre de la base de datos
)

# Crear un cursor para ejecutar consultas
consulta = """
    SELECT client_id, nombre, edad, estado_civil, educacion, saldo_anual, tiene_prestamo
    FROM clientes
    WHERE saldo_anual > 10000;
"""

df_clientes = pd.read_sql(consulta, conexion)

# Cerrar la conexión
conexion.close()

# Visualizar los datos extraídos
print(df_clientes.head())

````
---

### **3. Formato y Estructura de los Datos**

**Tipos de Datos:**
- **Numéricos**: `age`, `balance`, `duration`, `campaign`, `pdays`, `previous`
- **Categóricos**: `job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `outcome`
- **Binarios**: `deposit` (indica si el cliente ha suscrito un depósito a plazo fijo: `yes` o `no`)

**Formato de Almacenamiento:**
- **Base de datos**: Los datos están estructurados en tablas relacionales (MySQL/PostgreSQL), lo que permite realizar consultas específicas para el análisis de datos y el entrenamiento de modelos de machine learning.

---

### **4. Limitaciones de los Datos**

- **Actualización desincronizada**: Los datos de transacciones pueden actualizarse en tiempo real, pero la información sobre las campañas de marketing puede tener un retraso de varias horas o días, dependiendo de la sincronización del CRM.
- **Calidad de los datos**: Algunos clientes pueden tener información incompleta o desactualizada, lo que puede afectar el análisis predictivo.

---

### **5. Consideraciones sobre Datos Sensibles**

**Tipos de Datos Sensibles:**
- **Información Personal Identificable (PII)**: Aunque el dataset no contiene directamente nombres o correos electrónicos, se podría inferir PII de columnas como `job` (tipo de empleo) o `education` (nivel educativo), que podrían ayudar a identificar personas si se combinan con otras fuentes.
- **Información Financiera Sensible**: `balance` (saldo de la cuenta bancaria).
- **Datos de Comportamiento Bancario**: `duration` (duración de la llamada en segundos), `campaign` (número de contactos realizados durante la campaña), `pdays` (días desde el último contacto), `previous` (número de contactos previos), y `poutcome` (resultado de campañas anteriores).

### **Medidas de Protección:**

1. **Anonimización y Pseudonimización**:
   - Dado que el dataset no incluye información como correos electrónicos o direcciones, no es necesario aplicar hashing en este caso. Sin embargo, para datos como `job` (trabajo) o `education` (educación), que podrían inferir información personal, se pueden aplicar técnicas de pseudonimización para proteger la identidad del cliente.
   
2. **Acceso Restringido**:
   - El acceso a datos sensibles como el `balance` (saldo de la cuenta bancaria) o datos de comportamiento (`duration`, `campaign`, etc.) está restringido a personal autorizado dentro del departamento de IT y al equipo de análisis. El acceso sigue el principio de **necesidad de conocer** para garantizar que solo las personas con un propósito específico puedan acceder a los datos.

3. **Cumplimiento de Regulaciones**:
   - Todo el proceso de gestión y análisis de datos cumple con el **Reglamento General de Protección de Datos (GDPR)**, asegurando que los datos financieros y comportamentales se manejen de forma ética y segura, respetando la privacidad de los clientes y protegiendo sus datos contra accesos no autorizados.

