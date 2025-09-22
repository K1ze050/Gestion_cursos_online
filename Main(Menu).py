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
            print("\n--- TODOS LOS CURSOS ---")
            if not cursos:
                print("No hay cursos registrados.")
            else:
                for i, curso in enumerate(cursos, 1):
                    in dfor = plataforma._usuarios.get(curso.instructor_id, None)
                    in dfor_nombre = instructor.nombre if instructor else "Desconocido"
                    pr df{i}. {curso.nombre} (ID: {curso.id}) - Instructor: {instructor_nombre}")
        
        elif opcion == df
            # Listar e dfntes
            estudiante dfataforma.obtener_usuarios_por_tipo("estudiante")
            print("\n- dfOS LOS ESTUDIANTES ---")
            if not est dfes:
                print( dfy estudiantes registrados.")
            else:
                for i, dfiante in enumerate(estudiantes, 1):
                    pr df{i}. {estudiante.nombre} ({estudiante.email}) - Cursos inscritos: {len(estudiante.cursos_inscritos)}")
        
        elif opcion == df
            # Listar i dftores
            instructor dflataforma.obtener_usuarios_por_tipo("instructor")
            print("\n- dfOS LOS INSTRUCTORES ---")
            if not ins dfres:
                print( dfy instructores registrados.")
            else:
                for i, dfuctor in enumerate(instructores, 1):
                    pr df{i}. {instructor.nombre} ({instructor.email}) - Especialidad: {instructor.especialidad}")
        
        elif opcion == df
            # Ver estu dfs de un curso
            cursos = p dfrma.obtener_todos_cursos()
            if not cur df
                print( dfy cursos registrados.")
                contin df
            
            print("Cur dfsponibles:")
            for i, cur dfenumerate(cursos, 1):
                print( df {curso.nombre} (ID: {curso.id})")
            
            try:
                selecc dfint(input("Seleccione el número del curso: "))
                if sel df < 1 or seleccion > len(cursos):
                    pr dfelección no válida")
                    co df
                
                curso  dfos[seleccion - 1]
                estudi df= plataforma.obtener_estudiantes_curso(curso.id)
                
                print( df- ESTUDIANTES INSCRITOS EN {curso.nombre} ---")
                if not dfiantes:
                    pr dfo hay estudiantes inscritos en este curso.")
                else:
                    fo dfstudiante in enumerate(estudiantes, 1):
                       dfedio = plataforma.obtener_promedio_estudiante(estudiante.id, curso.id)
                       dft(f"{i}. {estudiante.nombre} ({estudiante.email}) - Promedio: {promedio:.2f}")
            except Val dfr:
                print( df: Debe ingresar un número válido")
            except Exc df as e:
                print( dfr: {e}")
        
        elif opcion == df
            # Ver eval dfes de un curso
            cursos = p dfrma.obtener_todos_cursos()
            if not cur df
                print( dfy cursos registrados.")
                contin df
            
            print("Cur dfsponibles:")
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