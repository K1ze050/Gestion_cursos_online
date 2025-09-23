"""
SISTEMA DE GESTIÓN Y EVALUACIÓN DE CURSOS ONLINE
Implementación de los requerimientos del Proyecto 1 - Programación Avanzada
"""

from datetime import datetime
from abc import ABC, abstractmethod

# CLASE BASE PARA MANEJO DE EXCEPCIONES PERSONALIZADAS
class PlataformaError(Exception):
    """Excepción base para errores de la plataforma"""
    pass

class UsuarioYaRegistradoError(PlataformaError):
    """Excepción para cuando un usuario ya está registrado"""
    pass

class CursoInexistenteError(PlataformaError):
    """Excepción para cuando un curso no existe"""
    pass

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

# SUBCLASES DE USUARIO (APLICANDO HERENCIA)
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

class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, email):
        super().__init__(id_usuario, nombre, email)
        self._especialidad = "General"  # Especialidad por defecto
    
    def obtener_tipo(self):
        return "Instructor"
    
    @property
    def especialidad(self):
        return self._especialidad

# CLASE PARA REPRESENTAR CURSOS
class Curso:
    """
    Clase que representa un curso en la plataforma.
    Aplica encapsulamiento con propiedades.
    """
    
    def __init__(self, id_curso, nombre, instructor_id):
        self._id = id_curso
        self._nombre = nombre
        self._instructor_id = instructor_id
        self._estudiantes_inscritos = set()  # Usamos set para evitar duplicados
        self._evaluaciones = []
    
    def inscribir_estudiante(self, estudiante_id):
        """Inscribe un estudiante en el curso"""
        if estudiante_id in self._estudiantes_inscritos:
            raise UsuarioYaRegistradoError(f"El estudiante {estudiante_id} ya está inscrito")
        self._estudiantes_inscritos.add(estudiante_id)
    
    def agregar_evaluacion(self, evaluacion):
        """Agrega una evaluación al curso"""
        self._evaluaciones.append(evaluacion)
    
    # Propiedades para acceso controlado a los atributos
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def instructor_id(self):
        return self._instructor_id
    
    @property
    def estudiantes_inscritos(self):
        return list(self._estudiantes_inscritos)
    
    @property
    def evaluaciones(self):
        return self._evaluaciones

# CLASE BASE PARA EVALUACIONES (APLICANDO POLIMORFISMO)
class Evaluacion(ABC):
    """
    Clase abstracta base para evaluaciones.
    Aplica el principio de polimorfismo de POO.
    """
    
    def __init__(self, id_evaluacion, nombre, curso_id, puntaje_maximo):
        self._id = id_evaluacion
        self._nombre = nombre
        self._curso_id = curso_id
        self._puntaje_maximo = puntaje_maximo
        self._calificaciones = {}  # Diccionario: {estudiante_id: calificación}
    
    @abstractmethod
    def tipo_evaluacion(self):
        """Método abstracto que debe implementarse en subclases"""
        pass
    
    def registrar_calificacion(self, estudiante_id, calificacion):
        """Registra una calificación para un estudiante"""
        if calificacion < 0 or calificacion > self._puntaje_maximo:
            raise ValueError("Calificación fuera de rango válido")
        self._calificaciones[estudiante_id] = calificacion
    
    def obtener_calificacion(self, estudiante_id):
        """Obtiene la calificación de un estudiante"""
        return self._calificaciones.get(estudiante_id, None)
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def calificaciones(self):
        return self._calificaciones.copy()

# SUBCLASES DE EVALUACION (APLICANDO HERENCIA Y POLIMORFISMO)
class Examen(Evaluacion):
    def __init__(self, id_evaluacion, nombre, curso_id, puntaje_maximo, tiempo_limite):
        super().__init__(id_evaluacion, nombre, curso_id, puntaje_maximo)
        self._tiempo_limite = tiempo_limite  # en minutos
    
    def tipo_evaluacion(self):
        return "Examen"
    
    @property
    def tiempo_limite(self):
        return self._tiempo_limite

class Tarea(Evaluacion):
    def __init__(self, id_evaluacion, nombre, curso_id, puntaje_maximo, fecha_entrega):
        super().__init__(id_evaluacion, nombre, curso_id, puntaje_maximo)
        self._fecha_entrega = fecha_entrega
    
    def tipo_evaluacion(self):
        return "Tarea"
    
    @property
    def fecha_entrega(self):
        return self._fecha_entrega

# CLASE PRINCIPAL DEL SISTEMA
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

# FUNCIONES PARA EL MENÚ INTERACTIVO
def mostrar_menu_principal():
    """Muestra el menú principal de la plataforma"""
    print("\n" + "_"*10)
    print("PLATAFORMA DE GESTIÓN DE CURSOS ONLINE")
    
    print("1. Registrar usuario")
    print("2. Crear curso")
    print("3. Inscribir estudiante en curso")
    print("4. Crear evaluación")
    print("5. Registrar calificación")
    print("6. Consultar información")
    print("7. Generar reportes")
    print("8. Salir")
    print("_"*10)

def mostrar_menu_consultas():
    """Muestra el menú de consultas"""
    print("\n" + "."*30)
    print("CONSULTAS DE INFORMACIÓN")
    print("."*30)
    print("1. Listar todos los cursos")
    print("2. Listar estudiantes")
    print("3. Listar instructores")
    print("4. Ver estudiantes de un curso")
    print("5. Ver evaluaciones de un curso")
    print("6. Volver al menú principal")
    print("="*30)

def registrar_usuario_interactivo(plataforma):
    """Interfaz interactiva para registrar un usuario"""
    print("\n--- REGISTRAR USUARIO ---")
    tipo = input("Tipo de usuario (estudiante/instructor): ").strip().lower()
    
    if tipo not in ["estudiante", "instructor"]:
        print("Error: Tipo de usuario no válido")
        return
    
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    
    try:
        usuario = plataforma.registrar_usuario(tipo, nombre, email)
        print(f"Usuario registrado exitosamente: {usuario}")
    except PlataformaError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def crear_curso_interactivo(plataforma):
    """Interfaz interactiva para crear un curso"""
    print("\n- CREAR CURSO -")
    
    # Listar instructores disponibles
    instructores = plataforma.obtener_usuarios_por_tipo("instructor")
    if not instructores:
        print("No hay instructores registrados. Debe registrar un instructor primero.")
        return
    
    print("Instructores disponibles:")
    for i, instructor in enumerate(instructores, 1):
        print(f"{i}. {instructor.nombre} ({instructor.email}) - Especialidad: {instructor.especialidad}")
    
    try:
        seleccion = int(input("Seleccione el número del instructor: "))
        if seleccion < 1 or seleccion > len(instructores):
            print("Selección no válida")
            return
        
        instructor = instructores[seleccion - 1]
        nombre_curso = input("Nombre del curso: ").strip()
        
        curso = plataforma.crear_curso(nombre_curso, instructor.id)
        print(f"Curso creado exitosamente: {curso.nombre} (ID: {curso.id})")
    except ValueError:
        print("Error: Debe ingresar un número válido")
    except Exception as e:
        print(f"Error: {e}")

def inscribir_estudiante_interactivo(plataforma):
    """Interfaz interactiva para inscribir un estudiante en un curso"""
    print("\n--- INSCRIBIR ESTUDIANTE EN CURSO ---")
    
    # Listar estudiantes disponibles
    estudiantes = plataforma.obtener_usuarios_por_tipo("estudiante")
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    
    print("Estudiantes disponibles:")
    for i, estudiante in enumerate(estudiantes, 1):
        print(f"{i}. {estudiante.nombre} ({estudiante.email})")
    
    try:
        seleccion_est = int(input("Seleccione el número del estudiante: "))
        if seleccion_est < 1 or seleccion_est > len(estudiantes):
            print("Selección no válida")
            return
        
        estudiante = estudiantes[seleccion_est - 1]
        
        # Listar cursos disponibles
        cursos = plataforma.obtener_todos_cursos()
        if not cursos:
            print("No hay cursos registrados.")
            return
        
        print("Cursos disponibles:")
        for i, curso in enumerate(cursos, 1):
            print(f"{i}. {curso.nombre} (ID: {curso.id})")
        
        seleccion_curso = int(input("Seleccione el número del curso: "))
        if seleccion_curso < 1 or seleccion_curso > len(cursos):
            print("Selección no válida")
            return
        
        curso = cursos[seleccion_curso - 1]
        
        plataforma.inscribir_estudiante_curso(estudiante.id, curso.id)
        print(f"Estudiante {estudiante.nombre} inscrito exitosamente en el curso {curso.nombre}")
    except ValueError:
        print("Error: Debe ingresar un número válido")
    except PlataformaError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def crear_evaluacion_interactivo(plataforma):
    """Interfaz interactiva para crear una evaluación"""
    print("\n--- CREAR EVALUACIÓN ---")
    
    # Listar cursos disponibles
    cursos = plataforma.obtener_todos_cursos()
    if not cursos:
        print("No hay cursos registrados.")
        return
    
    print("Cursos disponibles:")
    for i, curso in enumerate(cursos, 1):
        print(f"{i}. {curso.nombre} (ID: {curso.id})")
    
    try:
        seleccion_curso = int(input("Seleccione el número del curso: "))
        if seleccion_curso < 1 or seleccion_curso > len(cursos):
            print("Selección no válida")
            return
        
        curso = cursos[seleccion_curso - 1]
        tipo = input("Tipo de evaluación (examen/tarea): ").strip().lower()
        
        if tipo not in ["examen", "tarea"]:
            print("Tipo de evaluación no válido")
            return
        
        nombre = input("Nombre de la evaluación: ").strip()
        puntaje_maximo = float(input("Puntaje máximo: "))
        
        if tipo == "examen":
            tiempo_limite = int(input("Tiempo límite (minutos): "))
            evaluacion = plataforma.crear_evaluacion(tipo, nombre, curso.id, puntaje_maximo, tiempo_limite=tiempo_limite)
        else:
            fecha_entrega = input("Fecha de entrega (YYYY-MM-DD): ").strip()
            evaluacion = plataforma.crear_evaluacion(tipo, nombre, curso.id, puntaje_maximo, fecha_entrega=fecha_entrega)
        
        print(f"Evaluación creada exitosamente: {evaluacion.nombre} (ID: {evaluacion.id})")
    except ValueError:
        print("Error: Debe ingresar valores válidos")
    except Exception as e:
        print(f"Error: {e}")

def registrar_calificacion_interactivo(plataforma):
    """Interfaz interactiva para registrar una calificación"""
    print("\n--- REGISTRAR CALIFICACIÓN ---")
    
    # Listar cursos disponibles
    cursos = plataforma.obtener_todos_cursos()
    if not cursos:
        print("No hay cursos registrados.")
        return
    
    print("Cursos disponibles:")
    for i, curso in enumerate(cursos, 1):
        print(f"{i}. {curso.nombre} (ID: {curso.id})")
    
    try:
        seleccion_curso = int(input("Seleccione el número del curso: "))
        if seleccion_curso < 1 or seleccion_curso > len(cursos):
            print("Selección no válida")
            return
        
        curso = cursos[seleccion_curso - 1]
        
        # Listar evaluaciones del curso
        evaluaciones = plataforma.obtener_evaluaciones_curso(curso.id)
        if not evaluaciones:
            print("El curso no tiene evaluaciones.")
            return
        
        print("Evaluaciones disponibles:")
        for i, evaluacion in enumerate(evaluaciones, 1):
            print(f"{i}. {evaluacion.nombre} ({evaluacion.tipo_evaluacion()}) - Puntaje máximo: {evaluacion._puntaje_maximo}")
        
        seleccion_eval = int(input("Seleccione el número de la evaluación: "))
        if seleccion_eval < 1 or seleccion_eval > len(evaluaciones):
            print("Selección no válida")
            return
        
        evaluacion = evaluaciones[seleccion_eval - 1]
        
        # Listar estudiantes del curso
        estudiantes = plataforma.obtener_estudiantes_curso(curso.id)
        if not estudiantes:
            print("El curso no tiene estudiantes inscritos.")
            return
        
        print("Estudiantes inscritos:")
        for i, estudiante in enumerate(estudiantes, 1):
            print(f"{i}. {estudiante.nombre} ({estudiante.email})")
        
        seleccion_est = int(input("Seleccione el número del estudiante: "))
        if seleccion_est < 1 or seleccion_est > len(estudiantes):
            print("Selección no válida")
            return
        
        estudiante = estudiantes[seleccion_est - 1]
        calificacion = float(input("Calificación: "))
        
        plataforma.registrar_calificacion(evaluacion.id, estudiante.id, calificacion, curso.id)
        print(f"Calificación registrada exitosamente para {estudiante.nombre} en {evaluacion.nombre}")
    except ValueError:
        print("Error: Debe ingresar valores válidos")
    except Exception as e:
        print(f"Error: {e}")

def consultar_informacion_interactivo(plataforma):
    """Interfaz interactiva para consultar información"""
    while True:
        mostrar_menu_consultas()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Listar todos los cursos
            cursos = plataforma.obtener_todos_cursos()
            print("\n- TODOS LOS CURSOS -")
            if not cursos:
                print("No hay cursos registrados.")
            else:
                for i, curso in enumerate(cursos, 1):
                    instructor = plataforma._usuarios.get(curso.instructor_id, None)
                    instructor_nombre = instructor.nombre if instructor else "Desconocido"
                    print(f"{i}. {curso.nombre} (ID: {curso.id}) - Instructor: {instructor_nombre}")
        
        elif opcion == "2":
            # Listar estudiantes
            estudiantes = plataforma.obtener_usuarios_por_tipo("estudiante")
            print("\n- TODOS LOS ESTUDIANTES -")
            if not estudiantes:
                print("No hay estudiantes registrados.")
            else:
                for i, estudiante in enumerate(estudiantes, 1):
                    print(f"{i}. {estudiante.nombre} ({estudiante.email}) - Cursos inscritos: {len(estudiante.cursos_inscritos)}")
        
        elif opcion == "3":
            # Listar instructores
            instructores = plataforma.obtener_usuarios_por_tipo("instructor")
            print("\n--- TODOS LOS INSTRUCTORES ---")
            if not instructores:
                print("No hay instructores registrados.")
            else:
                for i, instructor in enumerate(instructores, 1):
                    print(f"{i}. {instructor.nombre} ({instructor.email}) - Especialidad: {instructor.especialidad}")
        
        elif opcion == "4":
            # Ver estudiantes de un curso
            cursos = plataforma.obtener_todos_cursos()
            if not cursos:
                print("No hay cursos registrados.")
                continue
            
            print("Cursos disponibles:")
            for i, curso in enumerate(cursos, 1):
                print(f"{i}. {curso.nombre} (ID: {curso.id})")
            
            try:
                seleccion = int(input("Seleccione el número del curso: "))
                if seleccion < 1 or seleccion > len(cursos):
                    print("Selección no válida")
                    continue
                
                curso = cursos[seleccion - 1]
                estudiantes = plataforma.obtener_estudiantes_curso(curso.id)
                
                print(f"\n--- ESTUDIANTES INSCRITOS EN {curso.nombre} ---")
                if not estudiantes:
                    print("No hay estudiantes inscritos en este curso.")
                else:
                    for i, estudiante in enumerate(estudiantes, 1):
                        promedio = plataforma.obtener_promedio_estudiante(estudiante.id, curso.id)
                        print(f"{i}. {estudiante.nombre} ({estudiante.email}) - Promedio: {promedio:.2f}")
            except ValueError:
                print("Error: Debe ingresar un número válido")
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == "5":
            # Ver evaluaciones de un curso
            cursos = plataforma.obtener_todos_cursos()
            if not cursos:
                print("No hay cursos registrados.")
                continue
            
            print("Cursos disponibles:")
            for i, curso in enumerate(cursos, 1):
                print(f"{i}. {curso.nombre} (ID: {curso.id})")
            
            try:
                seleccion = int(input("Seleccione el número del curso: "))
                if seleccion < 1 or seleccion > len(cursos):
                    print("Selección no válida")
                    continue
                
                curso = cursos[seleccion - 1]
                evaluaciones = plataforma.obtener_evaluaciones_curso(curso.id)
                
                print(f"\n--- EVALUACIONES DE {curso.nombre} ---")
                if not evaluaciones:
                    print("No hay evaluaciones para este curso.")
                else:
                    for i, evaluacion in enumerate(evaluaciones, 1):
                        print(f"{i}. {evaluacion.nombre} ({evaluacion.tipo_evaluacion()}) - Puntaje máximo: {evaluacion._puntaje_maximo}")
            except ValueError:
                print("Error: Debe ingresar un número válido")
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == "6":
            # Volver al menú principal
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

def generar_reportes_interactivo(plataforma):
    """Interfaz interactiva para generar reportes"""
    print("\n--- GENERAR REPORTES ---")
    
    # Listar cursos disponibles
    cursos = plataforma.obtener_todos_cursos()
    if not cursos:
        print("No hay cursos registrados.")
        return
    
    print("Cursos disponibles:")
    for i, curso in enumerate(cursos, 1):
        print(f"{i}. {curso.nombre} (ID: {curso.id})")
    
    try:
        seleccion = int(input("Seleccione el número del curso: "))
        if seleccion < 1 or seleccion > len(cursos):
            print("Selección no válida")
            return
        
        curso = cursos[seleccion - 1]
        umbral = float(input("Umbral para promedios bajos (por defecto 60): ") or "60")
        
        reporte = plataforma.generar_reporte_promedios_bajos(curso.id, umbral)
        
        print(f"\n--- REPORTE DE ESTUDIANTES CON PROMEDIO BAJO EN {curso.nombre} ---")
        if not reporte:
            print(f"No hay estudiantes con promedio inferior a {umbral} en este curso.")
        else:
            for item in reporte:
                print(f"{item['estudiante'].nombre}: {item['promedio']:.2f}%")
    except ValueError:
        print("Error: Debe ingresar valores válidos")
    except Exception as e:
        print(f"Error: {e}")

# FUNCIÓN PRINCIPAL PARA EJECUTAR EL SISTEMA CON MENÚ
def ejecutar_sistema_con_menu():
    """Función principal que ejecuta el sistema con un menú interactivo"""
    plataforma = PlataformaCursos()
    
    # Menú principal
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            registrar_usuario_interactivo(plataforma)
        elif opcion == "2":
            crear_curso_interactivo(plataforma)
        elif opcion == "3":
            inscribir_estudiante_interactivo(plataforma)
        elif opcion == "4":
            crear_evaluacion_interactivo(plataforma)
        elif opcion == "5":
            registrar_calificacion_interactivo(plataforma)
        elif opcion == "6":
            consultar_informacion_interactivo(plataforma)
        elif opcion == "7":
            generar_reportes_interactivo(plataforma)
        elif opcion == "8":
            print("¡Gracias por usar la plataforma de gestión de cursos!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Punto de entrada del programa
ejecutar_sistema_con_menu()