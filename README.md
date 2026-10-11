# 📊 Tech Jobs EDA — Stack Overflow Developer Survey 2025

Exploratory Data Analysis interactivo del Stack Overflow Developer Survey 2025, construido con Python y Streamlit.

## 🔍 ¿Qué analiza?

- **Salarios** globales por país, modalidad de trabajo y experiencia
- **Tecnologías** más usadas: lenguajes, bases de datos, frameworks
- **Satisfacción laboral** y distribución de roles
- **Nivel educativo** y años de experiencia de los desarrolladores
- **Mapa mundial** de participación por país

## 🛠️ Stack tecnológico

| Herramienta | Uso |
|-------------|-----|
| Python 3.11 | Lenguaje principal |
| Streamlit | Dashboard interactivo |
| Pandas | Procesamiento de datos |
| Plotly | Visualizaciones |
| pycountry | Códigos ISO para mapa coroplético |

## 📁 Estructura del proyecto

```
tech-jobs-eda/
├── app.py                          # Aplicación principal
├── survey_results_public_2025.csv  # Dataset (Stack Overflow 2025)
├── requirements.txt                # Dependencias
└── .streamlit/
    └── config.toml                 # Tema oscuro personalizado
```

## 🚀 Correr localmente

```bash
# Clonar el repo
git clone https://github.com/DuvanJ/tech-jobs-eda.git
cd tech-jobs-eda

# Instalar dependencias
pip install -r requirements.txt

# Iniciar la app
streamlit run app.py
```

> **Nota:** El archivo CSV está versionado con Git LFS. Asegúrate de tener [Git LFS instalado](https://git-lfs.com/) antes de clonar.

## 📊 Dataset

**Stack Overflow Developer Survey 2025** — encuesta anual con más de 65,000 desarrolladores de todo el mundo.  
Fuente: [survey.stackoverflow.co](https://survey.stackoverflow.co/)

## 👤 Autor

**Duvan** 
[GitHub](https://github.com/DuvanJ)