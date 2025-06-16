import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
from informacion_adicional import extraer_informacion_adicional

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

        with open(archivo, "r") as f:
            datos_adicionales = {}
            for linea in f:
                if ":" in linea:
                    k, v = linea.strip().split(":", 1)
                    datos_adicionales[k.strip()] = v.strip()

        info_extra, advertencias = extraer_informacion_adicional(datos_adicionales)

        salida_texto.insert(tk.END, "\n📖 Información adicional de diagnóstico:\n")
        for linea in info_extra:
            salida_texto.insert(tk.END, linea + "\n")

        if advertencias:
            salida_texto.insert(tk.END, "\n⚠️ Advertencias:\n")
            for adv in advertencias:
                salida_texto.insert(tk.END, adv + "\n")

        if linea_salud:
            start_idx = salida_texto.search(linea_salud, "1.0", tk.END)
            if start_idx:
                salida_texto.tag_add("salud", start_idx, f"{start_idx} lineend")

        if linea_recomendacion:
            start_idx = salida_texto.search(linea_recomendacion, "1.0", tk.END)
            if start_idx:
                salida_texto.tag_add("recomendacion", start_idx, f"{start_idx} lineend")

        messagebox.showinfo("Guardado", f"✅ El resumen ha sido guardado en '{ARCHIVO_RESUMEN}'.")

# GUI
ventana = tk.Tk()
ventana.title("BATTDoctor - Diagnóstico de batería")
ventana.geometry("1000x720")
ventana.configure(bg="#e0f7fa")

titulo = tk.Label(
    ventana,
    text="👋 Bienvenido a BATTDoctor",
    font=("Arial", 24, "bold"),
    bg="#e0f7fa",
    fg="#01579b"
)
titulo.pack(pady=10)

label = tk.Label(
    ventana,
    text="🔌 Conecta tu móvil por USB y pulsa el botón para iniciar el análisis",
    font=("Arial", 16),
    bg="#e0f7fa",
    fg="#333"
)
label.pack(pady=5)

boton = tk.Button(
    ventana,
    text="📲 Iniciar análisis",
    font=("Arial", 16, "bold"),
    bg="#ffd54f",
    fg="#000",
    padx=30,
    pady=15,
    command=iniciar_analisis
)
boton.pack(pady=10)

salida_texto = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    width=105,
    height=26,
    font=("Courier New", 14),
    bg="#ffffff",
    fg="#000000",
    borderwidth=2,
    relief="groove"
)
salida_texto.tag_configure("salud", font=("Courier New", 16, "bold"), foreground="#d84315")
salida_texto.tag_configure("recomendacion", font=("Courier New", 15, "bold"), foreground="#ff8f00")
salida_texto.pack(padx=20, pady=10)

creditos = tk.Label(
    ventana,
    text="Desarrollado por Ismael López",
    font=("Arial", 12),
    bg="#e0f7fa",
    fg="#555555"
)
creditos.pack(pady=5)

ventana.mainloop()
