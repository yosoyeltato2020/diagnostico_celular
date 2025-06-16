import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import sys

ARCHIVO_BATERIA = "bateria_actual.txt"
ARCHIVO_RESUMEN = "resumen.txt"

def ejecutar_adb_y_guardar():
    try:
        resultado = subprocess.check_output(["adb", "shell", "dumpsys", "battery"], text=True)
        with open(ARCHIVO_BATERIA, "w") as f:
            f.write(resultado)
        return ARCHIVO_BATERIA
    except Exception as e:
        messagebox.showerror("❌ Error ADB", f"No se pudo ejecutar ADB:\n{e}")
        return None

def analizar_bateria(file_path):
    datos = {}
    try:
        with open(file_path, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if ':' in linea:
                    clave, valor = linea.split(':', 1)
                    datos[clave.strip()] = valor.strip()

        level = int(datos.get("level", 0))
        voltage = int(datos.get("voltage", 0)) / 1000
        temperature = int(datos.get("temperature", 0)) / 10
        charge_counter = int(datos.get("charge counter", 0))
        current_now = int(datos.get("current now", 0))
        status = int(datos.get("status", -1))
        health = int(datos.get("health", -1))

        estado = {
            1: "Unknown",
            2: "Charging",
            3: "Discharging",
            4: "Not charging",
            5: "Full"
        }.get(status, "Desconocido")

        salud = {
            1: "Unknown",
            2: "Good",
            3: "Overheat",
            4: "Dead",
            5: "Over voltage",
            6: "Unspecified failure",
            7: "Cold"
        }.get(health, "Desconocida")

        capacidad_nominal = 4500
        capacidad_actual = charge_counter / 1000
        porcentaje_salud = (capacidad_actual / capacidad_nominal) * 100

        if porcentaje_salud >= 85:
            recomendacion = "✅ La batería está en buen estado. No es necesario cambiarla."
        elif porcentaje_salud >= 70:
            recomendacion = "⚠️ La batería está aceptable, pero comienza a degradarse."
        elif porcentaje_salud >= 50:
            recomendacion = "❗ Notarás menos duración. Considera reemplazarla pronto."
        else:
            recomendacion = "🔴 Muy degradada. Se recomienda reemplazar la batería."

        linea_salud = f"📉 Salud estimada: {porcentaje_salud:.1f}% de 4500 mAh"
        linea_recomendacion = f"📢 Recomendación: {recomendacion}"

        resumen = (
            f"📁 Archivo analizado: {file_path}\n\n"
            f"🔋 Nivel de batería: {level}%\n"
            f"⚡ Voltaje: {voltage:.2f} V\n"
            f"🌡️ Temperatura: {temperature:.1f} ºC\n"
            f"🔌 Estado de carga: {estado}\n"
            f"🩺 Salud reportada: {salud}\n"
            f"🔋 Capacidad estimada: {capacidad_actual:.0f} mAh\n"
            f"{linea_salud}\n\n"
            f"{linea_recomendacion}"
        )

        with open(ARCHIVO_RESUMEN, "w") as f:
            f.write(resumen)

        return resumen, linea_salud, linea_recomendacion

    except Exception as e:
        return f"❌ Error al analizar el archivo:\n{e}", None, None

def iniciar_analisis():
    salida_texto.delete("1.0", tk.END)
    archivo = ejecutar_adb_y_guardar()
    if archivo:
        resultado, linea_salud, linea_recomendacion = analizar_bateria(archivo)
        salida_texto.insert(tk.END, resultado + "\n")

        if linea_salud:
            start_idx = salida_texto.search(linea_salud, "1.0", tk.END)
            if start_idx:
                end_idx = f"{start_idx} lineend"
                salida_texto.tag_add("salud", start_idx, end_idx)

        if linea_recomendacion:
            start_idx = salida_texto.search(linea_recomendacion, "1.0", tk.END)
            if start_idx:
                end_idx = f"{start_idx} lineend"
                salida_texto.tag_add("recomendacion", start_idx, end_idx)

        messagebox.showinfo("Guardado", f"✅ El resumen ha sido guardado en '{ARCHIVO_RESUMEN}'.")

# 🎨 Interfaz visual
ventana = tk.Tk()
ventana.title("BATTDoctor - Diagnóstico de batería")
ventana.geometry("750x540")
ventana.configure(bg="#e0f7fa")  # Azul celeste claro

# 🏷️ Título principal
titulo = tk.Label(
    ventana,
    text="👋 Bienvenido a BATTDoctor",
    font=("Arial", 20, "bold"),
    bg="#e0f7fa",
    fg="#01579b"
)
titulo.pack(pady=10)

# 🧾 Instrucción
label = tk.Label(
    ventana,
    text="🔌 Conecta tu móvil por USB y pulsa el botón para iniciar el análisis",
    font=("Arial", 14),
    bg="#e0f7fa",
    fg="#333"
)
label.pack(pady=5)

# 📲 Botón de análisis
boton = tk.Button(
    ventana,
    text="📲 Iniciar análisis",
    font=("Arial", 14, "bold"),
    bg="#ffd54f",
    fg="#000",
    padx=20,
    pady=10,
    command=iniciar_analisis
)
boton.pack(pady=10)

# 🖥️ Área de resultados
salida_texto = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    width=85,
    height=18,
    font=("Courier New", 12),
    bg="#ffffff",
    fg="#000000",
    borderwidth=2,
    relief="groove"
)
salida_texto.tag_configure("salud", font=("Courier New", 14, "bold"), foreground="#d84315")
salida_texto.tag_configure("recomendacion", font=("Courier New", 13, "bold"), foreground="#ff8f00")
salida_texto.pack(padx=20, pady=10)

# 👤 Créditos
creditos = tk.Label(
    ventana,
    text="Desarrollado por Ismael López",
    font=("Arial", 10),
    bg="#e0f7fa",
    fg="#555555"
)
creditos.pack(pady=5)

ventana.mainloop()
