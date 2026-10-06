from shared.herramientas import normalizar_materia


# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = {}
        if notas is not None:
            for materia, lista_notas in notas.items():
                materia = normalizar_materia(materia)
                if materia not in self.notas:
                    self.notas[materia] = []
                for nota in lista_notas:
                    self.notas[materia].append(nota)

        # CONJUNTO: materias en las que está inscrito, sin repetidos
        self.materias = set()
        if materias is not None:
            for materia in materias:
                self.materias.add(normalizar_materia(materia))
        for materia in self.notas:
            self.materias.add(materia)

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # add() no duplica: si ya estaba inscrito, no pasa nada
        self.materias.add(normalizar_materia(materia))

    def agregar_nota(self, materia, nota):
        materia = normalizar_materia(materia)
        self.inscribir_materia(materia)
        if materia not in self.notas:
            self.notas[materia] = []
        self.notas[materia].append(nota)

    def obtener_promedio(self):
        total = 0
        cantidad = 0
        for lista_notas in self.notas.values():
            for nota in lista_notas:
                total = total + nota
                cantidad = cantidad + 1
        if cantidad == 0:
            return 0
        return round(total / cantidad, 2)

    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"], datos.get("notas", {}), datos.get("materias", []),
        )

    def __str__(self):
        return (f"[{self.carnet}] {self.obtener_nombre_completo()} "
                f"- Promedio: {self.obtener_promedio()}")
