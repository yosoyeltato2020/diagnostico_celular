
# 📱 BATTDoctor

**BATTDoctor** es una aplicación de escritorio creada con **Python y Tkinter** que permite diagnosticar el estado de la batería de un dispositivo Android conectado por USB, utilizando `adb shell dumpsys battery`.

---

## 🛠️ Funcionalidades principales

✅ **Análisis completo de batería:**
- Nivel de carga actual (%)
- Voltaje (V)
- Temperatura (ºC)
- Estado de carga (cargando, completo, etc.)
- Salud general reportada por el sistema
- Estimación de capacidad total en mAh
- Estimación de salud en % basada en una batería de 4500 mAh

✅ **Recomendaciones automáticas:**
- El sistema te dice si debes cambiar la batería o no, según el nivel de salud.

✅ **Diagnóstico extendido (avanzado):**
- Fecha de fabricación del dispositivo
- Días desde la última calibración
- Temperatura máxima registrada
- Corriente máxima histórica
- Advertencias si detecta condiciones peligrosas o problemas de envejecimiento

✅ **Interfaz gráfica amigable:**
- Aplicación de escritorio moderna y clara
- Emojis grandes para mejor visualización
- Colores llamativos para destacar recomendaciones
- Tamaño ajustado para evitar el uso de scroll

✅ **Exportación automática de análisis:**
- Todos los diagnósticos se guardan automáticamente en `resumen.txt`

---

## 🧰 Requisitos
- Python 3.8+
- `adb` instalado y funcionando en tu sistema
- Conexión USB con el modo Depuración USB activado en tu dispositivo Android

Instalación de dependencias (si no las tienes):
```bash
pip install tk
```

---

## 🚀 Cómo se usa

1. Conecta tu dispositivo Android al ordenador por USB
2. Activa la **Depuración USB** desde las opciones de desarrollador
3. Ejecuta `battdoctor.py`
4. Pulsa el botón "📲 Iniciar análisis"
5. Revisa los resultados en pantalla y en `resumen.txt`

---

## 👨‍💻 Autor
**Desarrollado por Ismael López**

Este proyecto es educativo y experimental. Si deseas contribuir o extenderlo con exportación PDF, gráficas o histórico de análisis, ¡estás invitado!

---

## 🧩 Archivos del proyecto

- `battdoctor.py` → Interfaz principal
- `informacion_adicional.py` → Módulo con análisis avanzado
- `resumen.txt` → Resultado del último análisis guardado

---

## 📎 Licencia
MIT License
