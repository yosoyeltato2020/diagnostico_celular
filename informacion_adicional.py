import datetime

def extraer_informacion_adicional(datos):
    info = []
    advertencias = []

    # Fecha de fabricación
    fecha_cal = datos.get("LLB CAL", "")
    try:
        fecha_fabricacion = datetime.datetime.strptime(fecha_cal, "%Y%m%d")
        hoy = datetime.datetime.today()
        antiguedad = hoy - fecha_fabricacion
        años = antiguedad.days // 365
        meses = (antiguedad.days % 365) // 30
        info.append(f"📅 Fecha de fabricación: {fecha_fabricacion.date()} (hace {años} años y {meses} meses)")
    except:
        info.append("📅 Fecha de fabricación: No disponible")

    # Días desde calibración
    dias_desde_cal = int(datos.get("LLB DIFF", 0))
    info.append(f"🕓 Días desde último calibrado: {dias_desde_cal}")
    if dias_desde_cal >= 180:
        advertencias.append("🔁 Recomendación: Han pasado más de 6 meses desde la última calibración. Considera realizar una carga completa (0% a 100%).")

    # Temperatura máxima
    temp_max_raw = int(datos.get("mSavedBatteryMaxTemp", 0))
    temp_max = temp_max_raw / 10
    info.append(f"🔥 Temp. máxima registrada: {temp_max:.1f} ºC")
    if temp_max >= 60:
        advertencias.append("⚠️ Advertencia: La batería ha alcanzado temperaturas muy altas. Evita exponer el móvil al sol o cargarlo mientras usas apps exigentes.")

    # Corriente máxima
    corriente_max = int(datos.get("mSavedBatteryMaxCurrent", 0))
    info.append(f"⚡ Corriente máxima registrada: {corriente_max} mA")

    return info, advertencias
