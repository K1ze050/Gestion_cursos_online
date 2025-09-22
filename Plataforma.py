from entidades import Estudiante, Instructor, Curso, Examen, Tarea
from excepciones import UsuarioYaRegistradoError, CursoInexistenteError
from datetime import datetime

class PlataformaCursos:
    """
    Clase principal que gestiona toda la plataforma.
    Aplica composición para manejar usuarios, cursos y evaluaciones.
    """
    
    def __init__(self):
        self._usuarios = {}  # Diccionario: {id: objeto Usuario}
        self._cursos = {}    # Diccionario: {id: objeto Curso}
        self._proximo_id_usuario = 1
        self._proximo_id_curso = 1
        self._proximo_id_evaluacion = 1
