import flet as ft
import threading
import time
import exerciseController as ec


def main(page: ft.Page):
    """
    Función principal de Flet con UI
    """
    
    # Configuración de la ventana
    page.title = "PoseFit Trainer"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1600
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#0a0e27"
    
    # =========================================
    # Variables de estado
    # =========================================
    is_video_running = False

    # =========================================
    # Componentes de la interfaz
    # =========================================
    
    video_image = ft.Image(
        src_base64=ec.obtener_placeholder(),
        width=800,
        height=575,
        fit=ft.ImageFit.CONTAIN,
        border_radius=15,
    )
    
    status_text = ft.Text(
        value="Selecciona un ejercicio para comenzar",
        size=16,
        color=ft.Colors.WHITE70,
        text_align=ft.TextAlign.CENTER,
        italic=True,
    )
    
    exercise_name_text = ft.Text(
        value="",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN_400,
        text_align=ft.TextAlign.CENTER,
    )
    
    # =========================================
    # Elementos de estadísticas (CREADOS COMO VARIABLES)
    # =========================================
    
    # Textos para las estadísticas
    counter_text = ft.Text(
        "0",
        size=60,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_400,
        text_align=ft.TextAlign.CENTER,
    )
    
    angle_text = ft.Text(
        "0°",
        size=60,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_400,
        text_align=ft.TextAlign.CENTER,
    )
    

    # =========================================
    # Funciones para los botones
    # =========================================

    def iniciar_video():
        nonlocal is_video_running
        if not is_video_running:
            is_video_running = True
            video_thread = threading.Thread(target=procesar_video, daemon=True)
            video_thread.start()

    def stop_video():
        nonlocal is_video_running
        is_video_running = False
    
    def on_curl_click(e):
        mensaje = ec.boton_curl_presionado("left")  # Siempre lado izquierdo
        exercise_name_text.value = "💪 Curl de Bíceps izquierdo "
        status_text.value = mensaje
        page.update()
        iniciar_video()
    
    def on_squat_click(e):
        mensaje = ec.boton_squat_presionado("left")  # Siempre lado izquierdo
        exercise_name_text.value = "🦵 Sentadillas "
        status_text.value = mensaje
        page.update()
        iniciar_video()
    
    def on_pushup_click(e):
        mensaje = ec.boton_pushup_presionado()
        exercise_name_text.value = "🤸 Flexiones"
        status_text.value = mensaje
        page.update()
        iniciar_video()
    
    def on_reset_click(e):
        mensaje = ec.boton_reset_presionado()
        # Actualizar contador a 0
        counter_text.value = "0"
        angle_text.value = "0°"
        page.update()
    
    # =========================================
    # Thread para procesar video
    # =========================================
    
    def procesar_video():
        nonlocal is_video_running
        
        while is_video_running:
            try:
                frame_base64, count, angle, ok = ec.obtener_frame()
                
                if ok and frame_base64:
                    # Actualizar video
                    video_image.src_base64 = frame_base64
                    
                    # Actualizar estadísticas
                    counter_text.value = str(count)
                    angle_text.value = f"{angle}°"
                    
                    page.update()
                
                time.sleep(0.03)
            except Exception as e:
                print(f"Error en procesar_video: {e}")
                break
    
    # =========================================
    # Construcción de la interfaz mejorada
    # =========================================
    
    # Header con título mejorado
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.FITNESS_CENTER, size=40, color=ft.Colors.CYAN_400),
            ft.Text(
                "PoseFit Trainer",
                size=36,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.CYAN_400,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(top=15, bottom=15),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#1a1f3a", "#0a0e27"],
        ),
    )

    # Panel del video principal
    video_panel = ft.Container(
        content=ft.Column([
            # Nombre del ejercicio actual
            ft.Container(
                content=exercise_name_text,
                padding=ft.padding.only(top=5, bottom=5),
            ),
            
            # Video
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=video_image,
                        bgcolor="#1a1f3a",
                        border_radius=15,
                        padding=5,
                        border=ft.border.all(2, ft.Colors.CYAN_700),
                        alignment=ft.alignment.center,
                    ),
                ], spacing=5),
                alignment=ft.alignment.center,
            ),
            
            # Estado
            #ft.Container(
            #    content=status_text,
            #    padding=ft.padding.only(top=10),
            #),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        ),
        padding=20,
        expand=True,
        alignment=ft.alignment.center,
    )
    
    # Panel de controles lateral
    control_panel = ft.Container(
        content=ft.Column([
            # Título
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SPORTS, size=28, color=ft.Colors.CYAN_400),
                    ft.Text(
                        "EJERCICIOS",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.CYAN_400,
                    ),
                ], spacing=10),
                padding=ft.padding.only(bottom=10),
            ),
            ft.Divider(color=ft.Colors.CYAN_700, height=2),
            
            # Botones de ejercicios
            ft.ElevatedButton(
                "💪 Curl de Bíceps",
                icon=ft.Icons.FITNESS_CENTER,
                on_click=on_curl_click,
                width=280,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor={"": ft.Colors.PURPLE_700},
                    color=ft.Colors.WHITE,
                    padding=20,
                ),
            ),
            
            ft.ElevatedButton(
                "🦵 Sentadillas",
                icon=ft.Icons.ACCESSIBILITY_NEW,
                on_click=on_squat_click,
                width=280,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor={"": ft.Colors.BLUE_700},
                    color=ft.Colors.WHITE,
                    padding=20,
                ),
            ),
            
            ft.ElevatedButton(
                "🤸 Flexiones",
                icon=ft.Icons.SPORTS_GYMNASTICS,
                on_click=on_pushup_click,
                width=280,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor={"": ft.Colors.GREEN_700},
                    color=ft.Colors.WHITE,
                    padding=20,
                ),
            ),
            
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

            # Estadísticas
            ft.Container(
                content=ft.Row([
                    # Contador de repeticiones
                    ft.Column([
                        ft.Text("REPETICIONES", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70),
                        counter_text,  # Usando la variable de texto
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    
                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                    
                    # Ángulo actual
                    ft.Column([
                        ft.Text("ÁNGULO ACTUAL", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70),
                        angle_text,  # Usando la variable de texto
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#1a1f3a",
                border_radius=10,
                padding=15,
                margin=ft.margin.only(bottom=10),
            ),
            
            # Controles
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, size=28, color=ft.Colors.CYAN_400),
                    ft.Text(
                        "CONTROLES",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.CYAN_400,
                    ),
                ], spacing=10),
                padding=ft.padding.only(bottom=10),
            ),
            ft.Divider(color=ft.Colors.CYAN_700, height=2),
            
            # Botón de reinicio
            ft.ElevatedButton(
                "🔄 Reiniciar Contador",
                icon=ft.Icons.REFRESH,
                on_click=on_reset_click,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor={"": ft.Colors.ORANGE_700},
                    color=ft.Colors.WHITE,
                    padding=15,
                ),
            ),

            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            
            # Espaciador
            ft.Container(expand=True),
            
            # Información
            ft.Container(
                content=ft.Column([
                    ft.Divider(color=ft.Colors.WHITE24),
                    ft.Text(
                        "PoseFit Trainer v1.0",
                        size=12,
                        color=ft.Colors.WHITE54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ], spacing=5),
                padding=ft.padding.only(top=20),
            ),
            
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        ),
        bgcolor="#1a1f3a",
        padding=25,
        width=350,
        border_radius=ft.border_radius.only(top_right=15, bottom_right=15),
    )
    
    # Layout principal
    main_content = ft.Row([
        control_panel,
        video_panel,
    ], 
    expand=True, 
    spacing=0,
    vertical_alignment=ft.CrossAxisAlignment.START,
    )
    
     # Estructura completa
    page.add(
        ft.Column([
            header,
            main_content,
        ], 
        spacing=0, 
        expand=True)
    )
    
    # Limpiar al cerrar
    page.on_close = stop_video


if __name__ == "__main__":
    ft.app(target=main)