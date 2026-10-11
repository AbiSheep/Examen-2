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
# 1. Configuracion de pagina (DEBE ser el primer comando de Streamlit)
# --------------------------------------------------------------------------
# TODO 4a: st.set_page_config(page_title="Sistema EcoTránsito CDMX", layout="wide")


# --------------------------------------------------------------------------
# 2. Carga de datos
# --------------------------------------------------------------------------
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Lee el CSV limpio una sola vez (cache) para que la app sea rapida."""
    return pd.read_csv(CSV_LIMPIO)


df = cargar_datos()

st.title("Sistema EcoTránsito CDMX")

# --------------------------------------------------------------------------
# 3. Barra lateral: filtro dinamico por zona
# --------------------------------------------------------------------------
# TODO 4b: opciones = sorted(df["Zona_Estacion"].unique())
# TODO 4c: seleccion = st.sidebar.multiselect("Zonas", opciones, default=opciones)
# TODO 4d: df_f = df[df["Zona_Estacion"].isin(seleccion)]
df_f = df  # <- reemplazar por el DataFrame filtrado del TODO 4d

# Proteccion: con el selector vacio no hay datos y los promedios darian NaN.
if df_f.empty:
    st.warning("Selecciona al menos una zona en la barra lateral.")
    st.stop()

# --------------------------------------------------------------------------
# 4. KPIs (3 tarjetas)
# --------------------------------------------------------------------------
# TODO 4e: c1, c2, c3 = st.columns(3)
# TODO 4f: c1.metric("Lecturas activas", len(df_f))
# TODO 4g: c2.metric("PM2.5 promedio (µg/m³)", f"{df_f['Concentracion_PM25'].mean():.1f}")
# TODO 4h: c3.metric("Índice máx. de tráfico", f"{df_f['Indice_Trafico_Vehicular'].max():.1f}")

# --------------------------------------------------------------------------
# 5. Pestanas de visualizacion
# --------------------------------------------------------------------------
# TODO 4i: tab1, tab2 = st.tabs(["Dispersión (Plotly)", "Correlación (Seaborn)"])
# TODO 4j (tab1): px.scatter(df_f, x="Indice_Trafico_Vehicular",
#                            y="Concentracion_PM25", color="Zona_Estacion")
#                 -> st.plotly_chart(fig, use_container_width=True)
# TODO 4k (tab2): fig2, ax = plt.subplots()
#                 sns.heatmap(df_f.corr(numeric_only=True), annot=True,
#                             cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
#                 -> st.pyplot(fig2)
