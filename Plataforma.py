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
        
 # MÉTODOS PARA REGISTRAR USUARIOS
    def registrar_usuario(self, tipo, nombre, email):
        """Registra un nuevo usuario en el sistema"""
        # Verificar si el email ya está registrado
        for usuario in self._usuarios.values():
            if usuario.email == email:
                raise UsuarioYaRegistradoError(f"El email {email} ya está registrado")
        
        # Crear usuario según el tipo
        if tipo.lower() == "estudiante":
            usuario = Estudiante(self._proximo_id_usuario, nombre, email)
        elif tipo.lower() == "instructor":
            usuario = Instructor(self._proximo_id_usuario, nombre, email)
        else:
            raise ValueError("Tipo de usuario no válido")
        
        # Agregar usuario al sistema
        self._usuarios[usuario.id] = usuario
        self._proximo_id_usuario += 1
        return usuario
    
    # MÉTODOS PARA GESTIONAR CURSOS
    def crear_curso(self, nombre, instructor_id):
        """Crea un nuevo curso en el sistema"""
        if instructor_id not in self._usuarios or not isinstance(self._usuarios[instructor_id], Instructor):
            raise ValueError("ID de instructor no válido")
        
        curso = Curso(self._proximo_id_curso, nombre, instructor_id)
        self._cursos[curso.id] = curso
        self._proximo_id_curso += 1
        return curso
    
    def inscribir_estudiante_curso(self, estudiante_id, curso_id):
        """Inscribe un estudiante en un curso"""
        if estudiante_id not in self._usuarios or not isinstance(self._usuarios[estudiante_id], Estudiante):
            raise ValueError("ID de estudiante no válido")
        
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        # Inscribir estudiante en el curso
        self._cursos[curso_id].inscribir_estudiante(estudiante_id)
        
        # Registrar el curso en el perfil del estudiante
        estudiante = self._usuarios[estudiante_id]
        estudiante.inscribir_curso(curso_id)
