# Proyecto/graficas.py
import flet as ft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import time
import threading

def ventana_grafica(queue):
    def view(page: ft.Page):
        
        
        page.title = "Gráficas en vivo"
        page.window_width = 950
        page.window_height = 650
        page.bgcolor = "#FFFFFF"
        # --- Data lists for each graph ---
        x_data_ultrasonido = []
        y_data_ultrasonido = []

        x_data_humedad = []
        y_data_humedad = []

        x_data_temperatura = []
        y_data_temperatura = []

        x_data_objetos = []
        y_data_objetos = []

        # --- Figure and axes for each graph ---
        fig_ultrasonido, ax_ultrasonido = plt.subplots(figsize=(6, 4))
        line_ultrasonido, = ax_ultrasonido.plot([], [], '-', label="Ultrasonido")
        ax_ultrasonido.set_xlim(0, 200)
        ax_ultrasonido.set_ylim(-100, 100)
        ax_ultrasonido.set_xlabel("Tiempo")
        ax_ultrasonido.set_ylabel("Ultrasonido")
        ax_ultrasonido.legend()
        ax_ultrasonido.set_title("Ultrasonido")
        chart_ultrasonido = MatplotlibChart(fig_ultrasonido, expand=True)

        fig_humedad, ax_humedad = plt.subplots(figsize=(6, 4))
        line_humedad, = ax_humedad.plot([], [], '-', label="Humedad")
        ax_humedad.set_xlim(0, 200)
        ax_humedad.set_ylim(-100, 100)
        ax_humedad.set_xlabel("Tiempo")
        ax_humedad.set_ylabel("Humedad")
        ax_humedad.legend()
        ax_humedad.set_title("Humedad")
        chart_humedad = MatplotlibChart(fig_humedad, expand=True)

        fig_temperatura, ax_temperatura = plt.subplots(figsize=(6, 4))
        line_temperatura, = ax_temperatura.plot([], [], '-', label="Temperatura")
        ax_temperatura.set_xlim(0, 200)
        ax_temperatura.set_ylim(-100, 100)
        ax_temperatura.set_xlabel("Tiempo")
        ax_temperatura.set_ylabel("Temperatura")
        ax_temperatura.legend()
        ax_temperatura.set_title("Temperatura")
        chart_temperatura = MatplotlibChart(fig_temperatura, expand=True)

        fig_objetos, ax_objetos = plt.subplots(figsize=(6, 4))
        line_objetos, = ax_objetos.plot([], [], '-', label="Objetos")
        ax_objetos.set_xlim(0, 200)
        ax_objetos.set_ylim(-100, 100)
        ax_objetos.set_xlabel("Tiempo")
        ax_objetos.set_ylabel("Objetos")
        ax_objetos.legend()
        ax_objetos.set_title("Objetos")
        chart_objetos = MatplotlibChart(fig_objetos, expand=True)

        def actualizar_datos():
            max_points = 180
            time_counter = 0
            while True:
                if not queue.empty():
                    ultrasonido, humedad, temperatura, objetos = queue.get()
                    print(f"Ultrasonido={ultrasonido} - Humedad={humedad}-Temperatura={temperatura}-objetos={objetos}")
                    
                    # Add data to each graph
                    x_data_ultrasonido.append(time_counter)
                    y_data_ultrasonido.append(ultrasonido)

                    x_data_humedad.append(time_counter)
                    y_data_humedad.append(humedad)

                    x_data_temperatura.append(time_counter)
                    y_data_temperatura.append(temperatura)

                    x_data_objetos.append(time_counter)
                    y_data_objetos.append(objetos)
                    
                    time_counter += 1

                    # Keep only the last points for each graph
                    if len(x_data_ultrasonido) > max_points:
                        x_data_ultrasonido.clear()
                        y_data_ultrasonido.clear()
                        x_data_humedad.clear()
                        y_data_humedad.clear()
                        x_data_temperatura.clear()
                        y_data_temperatura.clear()
                        x_data_objetos.clear()
                        y_data_objetos.clear()
                        time_counter = 0

                    # Update each line
                    line_ultrasonido.set_data(x_data_ultrasonido, y_data_ultrasonido)
                    line_humedad.set_data(x_data_humedad, y_data_humedad)
                    line_temperatura.set_data(x_data_temperatura, y_data_temperatura)
                    line_objetos.set_data(x_data_objetos, y_data_objetos)

                    # Update the x-axis for each graph
                     # mover la ventana en X
                    
                    
                    ax_humedad.set_xlim(time_counter-max_points,time_counter)                   
                    ax_temperatura.set_xlim(time_counter-max_points,time_counter)
                    ax_objetos.set_xlim(time_counter-max_points, time_counter)                 
                    ax_ultrasonido.set_xlim(time_counter-max_points, time_counter)
                    # Update each chart
                    chart_ultrasonido.update()
                    chart_humedad.update()
                    chart_temperatura.update()
                    chart_objetos.update()
                time.sleep(0.01)

        # Thread that updates the graphs
        threading.Thread(target=actualizar_datos, daemon=True).start()

        # --- Layout in two rows and two columns ---
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(chart_ultrasonido, expand=True, padding=10),
                            ft.Container(chart_humedad, expand=True, padding=10),
                        ],
                        expand=True
                    ),
                    ft.Row(
                        [
                            ft.Container(chart_temperatura, expand=True, padding=10),
                            ft.Container(chart_objetos, expand=True, padding=10),
                        ],
                        expand=True
                    )
                ],
                expand=True
            )
        )

    ft.app(target=view)