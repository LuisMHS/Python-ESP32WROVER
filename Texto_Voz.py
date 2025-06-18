import flet as ft
from gtts import gTTS
from multiprocessing import Process
from playsound import playsound

#Instalar las siguiente librerias
#pip install flet gTTS playsound

def reproducir_audio(filename):
    playsound(filename)

def main(page: ft.Page):
    page.title = "Generador de Audio y Conexión Bluetooth"
    page.window.width=350
    page.window.height=350
    

    text_field = ft.TextField(label="Escribe un mensaje", multiline=True, width=400)
    status_text = ft.Text("")
    

    def generar_audio(e):
        texto = text_field.value.strip()
        if texto:
            filename = "hola.mp3"
            tts = gTTS(text=texto, lang='es')
            tts.save(filename)

            p = Process(target=reproducir_audio, args=(filename,))
            p.start()  # Inicia la reproducción en segundo plano

            status_text.value = f"Reproduciendo audio..."
            page.update()
        else:
            status_text.value = "Por favor escribe un mensaje."
            page.update()


    page.add(
        ft.Column([
            text_field,
            ft.Row([
                ft.ElevatedButton("Generar Audio", on_click=generar_audio)
            ]),
            status_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  # Necesario para Windows
    ft.app(target=main)


