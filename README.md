# Examen-2 · EcoTránsito CDMX
Examen de ciencia de datos (Unidad 3): diagnóstico de calidad del aire y tráfico vehicular.

## Estructura

```
├── app_ecotransito.py          Tarea 4: app Streamlit (lee data/df_clean.csv)
├── tareas_1_a_3.py             Tareas 1-3: diagnóstico, limpieza, EDA; genera df_clean.csv
├── requirements.txt            Dependencias (sin versiones, para Streamlit Cloud)
├── data/
│   ├── cdmx_air_traffic_dirty.csv   Datos crudos
│   └── df_clean.csv                 Datos limpios (lo crea tareas_1_a_3.py)
└── .gitignore
```

## Ejecutar

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python tareas_1_a_3.py
streamlit run app_ecotransito.py
```
