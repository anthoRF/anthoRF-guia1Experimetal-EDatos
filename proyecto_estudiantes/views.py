from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido, normalizar_materia


gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def carnets_registrados(excepto_id=None):
    carnets = set()
    for registro in gestor.leer():
        if registro["id"] != excepto_id:
            carnets.add(registro["carnet"].strip().lower())
    return carnets


def siguiente_id():
    mayor = 0
    for registro in gestor.leer():
        if registro["id"] > mayor:
            mayor = registro["id"]
    return mayor + 1


def validar_datos(datos, excepto_id=None):
    for campo in CAMPOS_OBLIGATORIOS:
        if datos[campo] == "":
            return False, f"El campo {campo} es obligatorio"
    if not es_email_valido(datos["email"]):
        return False, "El email no tiene un formato válido"
    if " " in datos["email"]:
        return False, "El email no debe contener espacios"
    if datos["carnet"].lower() in carnets_registrados(excepto_id):
        return False, "Ese carnet ya está registrado"
    return True, "Datos válidos"


def crear_estudiante(datos):
    valores = {}
    for campo in CAMPOS_ESTUDIANTE:
        valores[campo] = str(datos.get(campo, "")).strip()

    exito, mensaje = validar_datos(valores)
    if not exito:
        return False, mensaje

    estudiante = Estudiante(
        siguiente_id(), valores["nombre"], valores["apellido"],
        valores["email"], valores["carnet"],
    )

    # 6) Agrego a la LISTA y guardo
    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"
    return True, f"Estudiante creado con id {estudiante.id}"


def obtener_todos():
    estudiantes = []
    for registro in gestor.leer():
        estudiantes.append(Estudiante.desde_diccionario(registro))
    return estudiantes


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    encontrados = []
    if termino == "":
        return encontrados
    for estudiante in obtener_todos():
        datos = estudiante.a_diccionario()
        for campo in CAMPOS_BUSCABLES:
            if termino in datos[campo].lower():
                encontrados.append(estudiante)
                break
    return encontrados


def actualizar_estudiante(id_estudiante, cambios):
    registros = gestor.leer()
    for posicion, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            if not cambios:
                return False, "No se indicó ningún cambio"
            nuevos_datos = registro.copy()
            for campo in cambios:
                if campo not in CAMPOS_ESTUDIANTE:
                    return False, f"El campo {campo} no se puede modificar"
                nuevos_datos[campo] = str(cambios[campo]).strip()

            exito, mensaje = validar_datos(nuevos_datos, id_estudiante)
            if not exito:
                return False, mensaje

            estudiante = Estudiante.desde_diccionario(nuevos_datos)
            registros[posicion] = estudiante.a_diccionario()
            if not gestor.guardar(registros):
                return False, "No se pudo guardar la actualización"
            return True, f"Estudiante {id_estudiante} actualizado"
    return False, f"No existe un estudiante con id {id_estudiante}"


def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = []
    encontrado = False
    for registro in registros:
        if registro["id"] == id_estudiante:
            encontrado = True
        else:
            quedan.append(registro)
    if not encontrado:
        return False, f"No existe un estudiante con id {id_estudiante}"
    if not gestor.guardar(quedan):
        return False, "No se pudo guardar la eliminación"
    return True, f"Estudiante {id_estudiante} eliminado"


def agregar_nota(id_estudiante, materia, nota):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    materia = normalizar_materia(materia)
    if materia == "":
        return False, "La materia es obligatoria"
    try:
        nota = float(str(nota).strip())
    except ValueError:
        return False, "La nota debe ser un número entre 0 y 20"
    if not (0 <= nota <= 20):
        return False, "La nota debe estar entre 0 y 20"

    estudiante.agregar_nota(materia, nota)
    registros = gestor.leer()
    for posicion, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[posicion] = estudiante.a_diccionario()
            break
    if not gestor.guardar(registros):
        return False, "No se pudo guardar la nota"
    return True, f"Nota {nota:g} agregada en {materia}"


def obtener_promedio(id_estudiante):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    promedio = estudiante.obtener_promedio()
    return True, f"Promedio de {estudiante.obtener_nombre_completo()}: {promedio:.2f}"


def materias_ofertadas():
    materias = set()
    for estudiante in obtener_todos():
        for materia in estudiante.materias:
            materias.add(materia)
    return materias


def estudiantes_en_comun(id_a, id_b):
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    if estudiante_a is None or estudiante_b is None:
        return False, "Uno o ambos estudiantes no existen"
    return True, estudiante_a.materias_en_comun(estudiante_b)
