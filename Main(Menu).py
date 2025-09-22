# main.py

from plataforma import PlataformaCursos
from excepciones import PlataformaError, UsuarioYaRegistradoError, CursoInexistenteError

def mostrar_menu_principal():
    """Muestra el menú principal de la plataforma"""
    print("\n" + "="*50)
    print("PLATAFORMA DE GESTIÓN DE CURSOS ONLINE")
    print("="*50)
    print("1. Registrar usuario")
    print("2. Crear curso")
    print("3. Inscribir estudiante en curso")
    print("4. Crear evaluación")
    print("5. Registrar calificación")
    print("6. Consultar información")
    print("7. Generar reportes")
    print("8. Salir")
    print("="*50)

def mostrar_menu_consultas():
    """Muestra el menú de consultas"""
    print("\n" + "="*50)
    print("CONSULTAS DE INFORMACIÓN")
    print("="*50)
    print("1. Listar todos los cursos")
    print("2. Listar estudiantes")
    print("3. Listar instructores")
    print("4. Ver estudiantes de un curso")
    print("5. Ver evaluaciones de un curso")
    print("6. Volver al menú principal")
    print("="*50)

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
    print("\n--- CREAR CURSO ---")
    
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
