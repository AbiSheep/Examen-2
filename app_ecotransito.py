"""
app_ecotransito.py  -  TAREA 4: prototipo interactivo en Streamlit + Plotly
=============================================================================
QUE HACE:
    App web con filtro de zonas (barra lateral), 3 KPIs y 2 pestanas
    (dispersion Plotly y heatmap de correlacion Seaborn).

QUE PROBLEMA RESUELVE:
    Los analistas de gobierno no ejecutan notebooks: la app les deja explorar
    los datos limpios sin programar.

NOTAS:
    - Streamlit re-ejecuta TODO el script en cada interaccion, por eso la
      carga de datos va en una funcion con @st.cache_data.
    - Lee data/df_clean.csv (lo genera tareas_1_a_3.py). Ese CSV debe estar
      SUBIDO al repo o la app fallara en Streamlit Cloud.
    - La ruta se arma desde la ubicacion de este archivo, asi funciona igual
      en tu PC y en la nube.

USO LOCAL:
    streamlit run app_ecotransito.py
"""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
import plotly.express as px      # noqa: F401
import seaborn as sns            # noqa: F401
import streamlit as st

CSV_LIMPIO = Path(__file__).parent / "data" / "df_clean.csv"

# --------------------------------------------------------------------------
# 1. Configuracion de la pagina (DEBE ser el primer comando de Streamlit)
# --------------------------------------------------------------------------
# Configura el titulo y el ancho de la aplicacion para una mejor experiencia
# de analisis en pantalla amplia.
st.set_page_config(page_title="Sistema EcoTránsito CDMX", layout="wide")

# --------------------------------------------------------------------------
# 2. Carga de datos
# --------------------------------------------------------------------------
# Carga el CSV limpio una sola vez mediante cache para no volver a leerlo en
# cada interaccion y mantener la app rapida.
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Lee el CSV limpio una sola vez (cache) para que la app sea rapida."""
    return pd.read_csv(CSV_LIMPIO)


df = cargar_datos()

# Titulo principal de la app.
st.title("Sistema EcoTránsito CDMX")

# --------------------------------------------------------------------------
# 3. Barra lateral: filtro dinamico por zona
# --------------------------------------------------------------------------
# Muestra todas las zonas disponibles en la barra lateral para filtrar el
# conjunto de datos y permitir explorar cada region por separado.
opciones = sorted(df["Zona_Estacion"].dropna().unique())
seleccion = st.sidebar.multiselect("Zonas", opciones, default=opciones)
df_f = df[df["Zona_Estacion"].isin(seleccion)]

# Proteccion: si el usuario limpia la seleccion, no hay datos para calcular
# promedios ni graficos, por lo que se detiene la ejecucion con aviso.
if df_f.empty:
    st.warning("Selecciona al menos una zona en la barra lateral.")
    st.stop()

# --------------------------------------------------------------------------
# 4. KPIs (3 tarjetas)
# --------------------------------------------------------------------------
# Las metricas resumen el volumen de datos, la concentracion promedio de PM2.5
# y el mayor indice de trafico observado en la seleccion actual.
c1, c2, c3 = st.columns(3)
c1.metric("Lecturas activas", len(df_f))
c2.metric("PM2.5 promedio (µg/m³)", f"{df_f['Concentracion_PM25'].mean():.1f}")
c3.metric("Índice máx. de tráfico", f"{df_f['Indice_Trafico_Vehicular'].max():.1f}")

# --------------------------------------------------------------------------
# 5. Pestanas de visualizacion
# --------------------------------------------------------------------------
# Se usan dos tabs para separar la exploracion visual: una dispersion para la
# relacion entre trafico y contaminacion y otra matriz de correlacion entre
# variables numericas.
tab1, tab2 = st.tabs(["Dispersión (Plotly)", "Correlación (Seaborn)"])

with tab1:
    # Scatter plot de Plotly para ver la relacion entre el indice de trafico y
    # la concentracion de PM2.5, diferenciando visualmente por zona.
    fig = px.scatter(
        df_f,
        x="Indice_Trafico_Vehicular",
        y="Concentracion_PM25",
        color="Zona_Estacion",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Heatmap de correlacion con Seaborn para identificar asociaciones entre
    # variables numericas. La escala va de -1 a 1 para interpretar fuerza y
    # direccion de la relacion.
    fig2, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(
        df_f.corr(numeric_only=True),
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        ax=ax,
    )
    plt.tight_layout()
    st.pyplot(fig2)
