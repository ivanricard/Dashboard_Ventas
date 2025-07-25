import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
os.system("cls")
# Configuracion de la pagina
# Se debe instalar el lector de archivos en excel
# pip install openpyxl
st.set_page_config(page_title="Dashboard de ventas", page_icon="📊", layout="centered")
st.title("Ventas Trimestre I de 2024")
df=pd.read_excel("ventas_supermercado.xlsx", skiprows=1, header=1)
st.write(df.head())

def formato(numero):
#Convierte numero a formato:1.234.567,89
    return f"{numero:,.2f}".replace(",", "X").replace(".",",").replace("X", ".")
#Calcular KPIs
total_ventas = df['Total'].sum()
ingreso_bruto = df['Ingreso bruto'].sum()
promedio_calificacion = df['Calificación'].mean()

#Mostrar KPIs en columnas con formato personalizado
st.metric("💰 Total Ventas", f"${formato(total_ventas)}")
st.metric("💸 Ingreso bruto", f"${formato(ingreso_bruto)}")
st.metric("💹 Calificacion promedio", f"{promedio_calificacion:.2f}")
# Organizar los datos en pestañas
col1, col2, col3 = st.columns([3,2,1])
with col1:
    st.metric("💰 Total Ventas", f"${formato(total_ventas)}")
    with col2:
        st.metric("📦 Ingreso Bruto", f"${formato(ingreso_bruto)}")
with col3:
    st.metric("⭐ Calificación Promedio", f"{formato(promedio_calificacion)}")
with st.sidebar:
    st.header("Filtros")
    # Selección de ciudades y líneas de producto
    ciudades = st.multiselect("Selecciona ciudades:",df['Ciudad'].unique(),default=df['Ciudad'].unique())

    lineas = st.multiselect("Selecciona líneas de producto:",df['Línea de producto'].unique(),default=df['Línea de producto'].unique())

# Filtrar datos
df_filtrado = df[(df['Ciudad'].isin(ciudades)) & (df['Línea de producto'].isin(lineas))]
#st.write(df_filtrado)#para imprimir
tab1, tab2, tab3 = st.tabs(["📅 Ventas por Mes", "📦 Por Línea", "📂 Datos"], width="stretch")

with tab1:
    st.subheader("📅 Ventas por Mes")
    df_filtrado["Mes"]=df_filtrado["Fecha"].dt.to_period("M").astype(str)
    df_filtrado["Mes"]=df_filtrado["Fecha"].dt.strftime("%m-%Y").astype(str)
    ventas_mes = df_filtrado.groupby('Mes')['Total'].sum().sort_index()

    fig1, ax1 = plt.subplots()
    ventas_mes.plot(kind='line', marker='o', ax=ax1, color='teal', title="Tendencia de Ventas Mensuales")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Total Ventas")
    ax1.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with tab2:
     st.subheader("📦 Ventas por Línea de Producto")
     ventas_linea = df_filtrado.groupby('Línea de producto')['Total'].sum(). sort_values()

     fig2, ax2 = plt.subplots()
     ventas_linea.plot(kind='barh', ax=ax2, color='orange', title="Ventas por línea de producto")
     ax2.set_xlabel(" ")
     ax2.set_ylabel("Ventas")
     st.pyplot(fig2)    
with tab3:
    st.subheader("📂 Datos")
    st.dataframe(df_filtrado)
    #.reset_index(drop=True), use_container_width=True)
    # 💾 Exportar a Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         df_filtrado.to_excel(writer, index=False, sheet_name='Ventas')

# ⬇️ Botón de descarga
    st.download_button(
    label="📥 Descargar datos en Excel",
    data=output.getvalue(),
    file_name="ventas_filtradas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
#ciudades=st.multiselect("Selecciona ciudades:",df['Ciudad'].unique(),default=df['Ciudad'].unique()) es ejemplo se unifico en el siguiente codigo

