import flet as ft
from funciones.borrar_duplicados import find_duplicates, hash_file, delete_file

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Borrar duplicados"
    page.window_width = 1000
    page.window_height = 700
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    # Variables globales del estado
    state = {
        "current_duplicates": []
    }

    # Texto para mostrar el directorio seleccionado
    selected_dir_text = ft.Text(
        value="No se ha seleccionado un directorio",
        size=20,
        color=ft.Colors.BLUE,
    )

    # Texto para mostrar los resultados
    result_text = ft.Text(
        value="",
        size=14,
        weight=ft.FontWeight.BOLD,
    )

    # Lista para mostrar los archivos duplicados
    duplicates_list = ft.ListView(
        spacing=10,
        expand=True,  # Para asegurarnos de que ocupa el espacio disponible
        height=300,   # Establece una altura inicial
    )

    delete_all_buttom = ft.ElevatedButton(
        text="Eliminar todos los duplicados",
        icon=ft.Icons.DELETE_SWEEP,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )

    # Maneja la selección de carpeta
    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            selected_dir_text.value = f"Directorio seleccionado: {e.path}"
            selected_dir_text.update()
            scan_directory(e.path)

    # Escanea el directorio en busca de duplicados
    def scan_directory(directory):
        # Limpia la lista antes de agregar nuevos duplicados
        duplicates_list.controls.clear()
        duplicates_list.update()  # Forzar la limpieza visualmente

        # Llama a la función personalizada para buscar duplicados
        state["current_duplicates"] = find_duplicates(directory)

        if not state["current_duplicates"]:
            # Si no se encontraron duplicados
            result_text.value = "No se encontraron archivos duplicados"
            result_text.color = ft.Colors.GREEN
            delete_all_buttom.visible = False
            result_text.update()
        else:
            # Si se encontraron duplicados
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados"
            result_text.color = ft.Colors.ORANGE
            delete_all_buttom.visible = True
            result_text.update()

            # Agregar cada archivo duplicado a la lista
            for dup_file, original in state["current_duplicates"]:
                duplicates_list.controls.append(
                    ft.Container(
                        content= ft.Row(
                            [
                                ft.Text(f"Duplicado: {dup_file} \n Original {original}", size=14, color=ft.Colors.RED),
                                ft.ElevatedButton(
                                    text="Eliminar",
                                    icon=ft.Icons.DELETE,
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED,
                                    on_click=lambda e, path=dup_file: delate_duplicate(path)
                                )
                            ]
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=5,
                        margin=ft.margin.only(bottom=5),
                        bgcolor=ft.Colors.GREY_900,
                    )
                )
            # Actualiza la lista después de agregar todos los duplicados
            duplicates_list.update()
            delete_all_buttom.update()

    def delate_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Se eliminó el archivo {filepath}"
            result_text.color = ft.Colors.GREEN
            result_text.update()
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
                    state["current_duplicates"] = [(dup, orig) for dup,orig in state["current_duplicates"] if dup != filepath]
            if not state["current_duplicates"]:
                delete_all_buttom.visible = False
        else:
            result_text.value = f"No se pudo eliminar el archivo {filepath}"
            result_text.color = ft.Colors.RED
        duplicates_list.update()
        delete_all_buttom.update()
        result_text.update()

    # Elimina todos los archivos duplicados
    def delete_all_duplicates():
        deleted_count = 0
        failed_count = 0
        for dup_file, _ in state["current_duplicates"][:]:
            if delete_file(dup_file):
                deleted_count += 1
            else:
                failed_count += 1
        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_buttom.visible = False
        if failed_count == 0:
            result_text.value = f"Se eliminaron {deleted_count} archivos duplicados"
            result_text.color = ft.Colors.GREEN
        else:
            result_text.value = f"Se eliminaron {deleted_count} archivos duplicados, {failed_count} archivos no se pudieron eliminar"
            result_text.color = ft.Colors.RED
        result_text.update()
        duplicates_list.update()
        delete_all_buttom.update()

    # Configuración del selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)

    # Vista principal de la aplicación
    duplicate_files_view = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    value="Eliminar archivos duplicados",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Seleccionar directorio",
                            icon=ft.Icons.FOLDER_OPEN,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_900,
                            on_click=lambda e: folder_picker.get_directory_path(),
                        ),
                        delete_all_buttom,
                    ]
                ),
                selected_dir_text,
                result_text,
                ft.Container(
                    content=duplicates_list,
                    border=ft.border.all(2, ft.Colors.PINK_600),
                    border_radius=10,
                    padding=10,
                    margin=ft.margin.only(top=10),
                    expand=True,  # Expande el contenedor para ocupar espacio
                ),
            ],
            expand=True,
            spacing=10,
        ),
        padding=20,
        expand=True,
    )

    page.add(duplicate_files_view)

ft.app(target=main)
