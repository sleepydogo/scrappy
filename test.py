from playsound import playsound

def reproducir_alarma_continuamente(ruta_archivo):
    reproduciendo = True

    # Función que se ejecuta para detener la reproducción
    def detener_reproduccion():
        nonlocal reproduciendo
        input("Presiona Enter para detener la alarma...")
        reproduciendo = False

    # Reproducir la alarma en un bucle hasta que se presione Enter
    while reproduciendo:
        playsound(ruta_archivo)
        detener_reproduccion()
    # Llama a la función para detener la reproducción


reproducir_alarma_continuamente('utils/alarma.mp3')