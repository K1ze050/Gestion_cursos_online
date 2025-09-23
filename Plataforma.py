from abc import ABC, abstractmethod
from datetime import datetime


# CLASE PADRE PARA USUARIOS (APLICANDO HERENCIA)
class Usuario(ABC):
    """
    Clase abstracta que representa un usuario de la plataforma.
    Aplica el principio de abstracción de POO.
    """
    
    def __init__(self, id_usuario, nombre, email):
        self._id = id_usuario  # Encapsulamiento: atributo protegido
        self._nombre = nombre
        self._email = email
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    @abstractmethod
    def obtener_tipo(self):
        """Método abstracto que deben implementar las subclases"""
        pass
    
    def __str__(self):
        return f"{self.obtener_tipo()}: {self._nombre} ({self._email})"

# Subclase de usuario (estudiante, aplicando herencia)
class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, email):
        super().__init__(id_usuario, nombre, email)
        self._cursos_inscritos = []  # Lista de IDs de cursos
    
    def obtener_tipo(self):
        return "Estudiante"
    
    def inscribir_curso(self, curso_id):
        """Inscribe al estudiante en un curso"""
        if curso_id not in self._cursos_inscritos:
            self._cursos_inscritos.append(curso_id)
    
    @property
    def cursos_inscritos(self):
        return self._cursos_inscritos
    

# Subclase de usuario (instructor, aplicando herencia)
class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, email):
        super().__init__(id_usuario, nombre, email)
        self._especialidad = "General"  # Especialidad por defecto
    
    def obtener_tipo(self):
        return "Instructor"
    
    @property
    def especialidad(self):
        return self._especialidad



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
        
         # MÉTODOS PARA GESTIONAR EVALUACIONES
    def crear_evaluacion(self, tipo, nombre, curso_id, puntaje_maximo, **kwargs):
        """Crea una nueva evaluación para un curso"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        # Crear evaluación según el tipo
        if tipo.lower() == "examen":
            tiempo_limite = kwargs.get('tiempo_limite', 60)
            evaluacion = Examen(self._proximo_id_evaluacion, nombre, curso_id, puntaje_maximo, tiempo_limite)
        elif tipo.lower() == "tarea":
            fecha_entrega = kwargs.get('fecha_entrega', datetime.now())
            evaluacion = Tarea(self._proximo_id_evaluacion, nombre, curso_id, puntaje_maximo, fecha_entrega)
        else:
            raise ValueError("Tipo de evaluación no válido")
        
        # Agregar evaluación al curso
        self._cursos[curso_id].agregar_evaluacion(evaluacion)
        self._proximo_id_evaluacion += 1
        return evaluacion
    
    def registrar_calificacion(self, evaluacion_id, estudiante_id, calificacion, curso_id):
        """Registra una calificación para una evaluación"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        # Buscar la evaluación en el curso
        evaluacion = None
        for eval_obj in self._cursos[curso_id].evaluaciones:
            if eval_obj.id == evaluacion_id:
                evaluacion = eval_obj
                break
        
        if not evaluacion:
            raise ValueError("Evaluación no encontrada")
        
        # Registrar la calificación
        evaluacion.registrar_calificacion(estudiante_id, calificacion)
    
    # MÉTODOS DE CONSULTA
    def obtener_estudiantes_curso(self, curso_id):
        """Obtiene la lista de estudiantes inscritos en un curso"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        return [self._usuarios[est_id] for est_id in self._cursos[curso_id].estudiantes_inscritos]
    
    def obtener_promedio_estudiante(self, estudiante_id, curso_id):
        """Calcula el promedio de un estudiante en un curso"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        if estudiante_id not in self._usuarios or not isinstance(self._usuarios[estudiante_id], Estudiante):
            raise ValueError("ID de estudiante no válido")
        
        curso = self._cursos[curso_id]
        calificaciones = []
        
        # Recopilar todas las calificaciones del estudiante en este curso
        for evaluacion in curso.evaluaciones:
            calificacion = evaluacion.obtener_calificacion(estudiante_id)
            if calificacion is not None:
                calificaciones.append(calificacion)
        
        # Calcular promedio
        if not calificaciones:
            return 0
        
        return sum(calificaciones) / len(calificaciones)
    
    def generar_reporte_promedios_bajos(self, curso_id, umbral=60):
        """Genera un reporte de estudiantes con promedio bajo en un curso"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        
        estudiantes_bajos = []
        
        for estudiante_id in self._cursos[curso_id].estudiantes_inscritos:
            promedio = self.obtener_promedio_estudiante(estudiante_id, curso_id)
            if promedio < umbral:
                estudiante = self._usuarios[estudiante_id]
                estudiantes_bajos.append({
                    'estudiante': estudiante,
                    'promedio': promedio
                })
        
        return estudiantes_bajos
    
 # MÉTODOS PARA OBTENER INFORMACIÓN (útiles para el menú)
    def obtener_usuarios_por_tipo(self, tipo):
        """Obtiene todos los usuarios de un tipo específico"""
        return [usuario for usuario in self._usuarios.values() if usuario.obtener_tipo().lower() == tipo.lower()]
    
    def obtener_todos_cursos(self):
        """Obtiene todos los cursos registrados"""
        return list(self._cursos.values())
    
    def obtener_evaluaciones_curso(self, curso_id):
        """Obtiene todas las evaluaciones de un curso"""
        if curso_id not in self._cursos:
            raise CursoInexistenteError(f"El curso con ID {curso_id} no existe")
        return self._cursos[curso_id].evaluaciones
