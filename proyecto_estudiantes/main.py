from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    obtener_promedio, materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def pedir_id(pregunta="Id del estudiante: "):
    try:
        return int(input(pregunta))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}{'PROMEDIO':<10}")
    print("-" * 83)
    for estudiante in estudiantes:
        promedio = estudiante.obtener_promedio()
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.carnet:<15}{promedio:<10.2f}")
    print("-" * 83)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")
    exito, mensaje = crear_estudiante(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)
    if not encontrados:
        imprimir_info("No hay estudiantes que coincidan con la búsqueda.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        datos = estudiante.a_diccionario()
        for clave, valor in datos.items():
            print(f"  {clave.capitalize()}: {valor}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        pausa()
        return
    print("Deje en blanco el campo que no quiera cambiar.\n")
    datos = estudiante.a_diccionario()
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        nuevo = input(f"{campo.capitalize()} [{datos[campo]}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        pausa()
        return
    imprimir_info(f"Se eliminará: {estudiante.obtener_nombre_completo()}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return
    materia = input("Materia: ")
    nota = input("Nota entre 0 y 20 (ejemplo decimal: 18.5): ")
    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return
    exito, mensaje = obtener_promedio(id_estudiante)
    mostrar_resultado(exito, mensaje)
    if exito:
        estudiante = obtener_por_id(id_estudiante)
        for materia, notas in estudiante.notas.items():
            print(f"  {materia}: {notas}")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    id_a = pedir_id("Id del primer estudiante: ")
    if id_a is None:
        pausa()
        return
    id_b = pedir_id("Id del segundo estudiante: ")
    if id_b is None:
        pausa()
        return
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif not resultado:
        imprimir_info("Los estudiantes no tienen materias en común.")
    else:
        for materia in sorted(resultado):
            print(f"  - {materia}")
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("Todavía no hay materias inscritas.")
    else:
        for materia in sorted(materias):
            print(f"  - {materia}")
    pausa()


def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue
        texto, funcion = OPCIONES[tecla]
        try:
            if funcion() == "salir":
                break
        except (ValueError, OSError) as error:
            imprimir_error(f"No se pudo completar la operación: {error}")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
