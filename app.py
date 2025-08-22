import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Comparación de Obligaciones Negociables - Arbitraje DNC3O vs DNC5O")

# Ingresar datos manualmente
st.write("✍️ Editá los precios directamente en la tabla:")
data = st.data_editor(
    pd.DataFrame({
        "Fecha": ["2025-08-20","2025-08-21","2025-08-22"],
        "DNC3O": [135500, 138270, 136350],
        "DNC5O": [133800, 133800, 135000]
    }),
    num_rows="dynamic"
)

# Convertir fechas y ordenar
data["Fecha"] = pd.to_datetime(data["Fecha"])
data = data.sort_values("Fecha")

# Calcular ratio y bandas
data["Ratio"] = data["DNC3O"] / data["DNC5O"]
data["Ratio_MA31"] = data["Ratio"].rolling(window=31).mean()
data["Upper"] = data["Ratio_MA31"] * 1.03
data["Lower"] = data["Ratio_MA31"] * 0.97

# Graficar
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(data["Fecha"], data["Ratio"], label="Ratio DNC3O/DNC5O", color="blue")
ax.plot(data["Fecha"], data["Ratio_MA31"], label="Media Móvil 31d", color="orange")
ax.plot(data["Fecha"], data["Upper"], label="Banda Superior (3%)", linestyle="--", color="green")
ax.plot(data["Fecha"], data["Lower"], label="Banda Inferior (3%)", linestyle="--", color="red")

# Señales
signals_upper = data[data["Ratio"] >= data["Upper"]]
signals_lower = data[data["Ratio"] <= data["Lower"]]
ax.scatter(signals_upper["Fecha"], signals_upper["Ratio"], color="green", marker="^", label="Rotar a DNC5O")
ax.scatter(signals_lower["Fecha"], signals_lower["Ratio"], color="red", marker="v", label="Rotar a DNC3O")

ax.set_title("Comparación Ratio DNC3O / DNC5O con Bandas ±3%")
ax.set_xlabel("Fecha")
ax.set_ylabel("Ratio")
ax.legend()
ax.grid(True)

st.pyplot(fig)
