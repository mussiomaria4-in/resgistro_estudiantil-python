import customtkinter as ctk
from tkinter import messagebox
import time # simula el tiempo de respuesta del servidor de la universidad


#  DATOS DE DEMOSTRACIÓN (MOCK DATA)
#    Añadimos el campo 'password' a todos los usuarios.
#  en este modulo se debe conectar con la base de datos de la universidad, simplemente estamos simulando los usuarios para entender su funcionamiento

MOCK_DATA = {
    'estudiantes': {
        '1001': {'nombre': 'Ana Perez', 'rol': 'estudiante', 'carrera': 'Informatica', 'materias_aprobadas': ['MAT101', 'FIS102'], 'notas': {'MAT101': 18, 'FIS102': 15}, 'password': '1001'},
        '1002': {'nombre': 'Juan Lopez', 'rol': 'estudiante', 'carrera': 'Informatica', 'materias_aprobadas': ['MAT101'], 'notas': {'MAT101': 14}, 'password': '1002'},
    },
    'profesores': {
        'P201': {'nombre': 'Dr. Raúl Silva', 'rol': 'profesor', 'materias_asignadas': ['ALG203'], 'password': 'P201'},
        'P202': {'nombre': 'Ing. Sofia Mena', 'rol': 'profesor', 'materias_asignadas': ['CAL304'], 'password': 'P202'},
    },
    'coordinadores': {
        'C300': {'nombre': 'Lic. Laura Diaz', 'rol': 'coordinador', 'password': 'C300'},
    },
    'materias': {
        'MAT101': {'nombre': 'Matemática I', 'creditos': 5, 'prerrequisitos': [], 'horario': 'LUN/MIE 8:00am', 'profesor_asignado': 'P201'},
        'FIS102': {'nombre': 'Física I', 'creditos': 5, 'prerrequisitos': ['MAT101'], 'horario': 'MAR/JUE 10:00am', 'profesor_asignado': 'P202'},
        'ALG203': {'nombre': 'Algoritmos', 'creditos': 6, 'prerrequisitos': ['MAT101'], 'horario': 'VIE 2:00pm', 'profesor_asignado': 'P201'},
        'CAL304': {'nombre': 'Cálculo Avanzado', 'creditos': 5, 'prerrequisitos': ['MAT101', 'FIS102'], 'horario': 'MAR/JUE 4:00pm', 'profesor_asignado': None},
        'QUI100': {'nombre': 'Química General', 'creditos': 4, 'prerrequisitos': [], 'horario': 'LUN/MIE 2:00pm', 'profesor_asignado': None},
    },
    'inscripciones_actuales': {
        '1001': ['CAL304', 'QUI100'],
        '1002': [],
    }
}

# Definición de colores Custom
BLUE_CIAN = "#00BFFF" 


# 1. CLASES DE ENTIDADES Y ROLES 
#    Añadimos 'password' a la clase Usuario


class Materia:
    def __init__(self, codigo, nombre, creditos, prerrequisitos, horario, profesor_id):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.prerrequisitos = prerrequisitos
        self.horario = horario
        self.profesor_id = profesor_id

class Usuario:
    def __init__(self, id, nombre, rol, password):
        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.password = password # Nuevo campo

class Estudiante(Usuario):
    def __init__(self, id, nombre, rol, password, carrera, materias_aprobadas, notas):
        super().__init__(id, nombre, rol, password)
        self.carrera = carrera
        self.materias_aprobadas = materias_aprobadas if materias_aprobadas is not None else []
        self.notas = notas if notas is not None else {}

class Profesor(Usuario):
    def __init__(self, id, nombre, rol, password, materias_asignadas):
        super().__init__(id, nombre, rol, password)
        self.materias_asignadas = materias_asignadas if materias_asignadas is not None else []

class Coordinador(Usuario):
    def __init__(self, id, nombre, rol, password):
        super().__init__(id, nombre, rol, password)


# 2. CLASE PRINCIPAL DEL SISTEMA (Lógica de Negocio y Control)


class SistemaAcademico:
    def __init__(self, rawData):
        print("🔌 Placeholder de conexión simulada activo.")
        self.raw_data = rawData.copy()
        self.estudiantes = self._load_estudiantes()
        self.profesores = self._load_profesores()
        self.coordinadores = self._load_coordinadores()
        self.materias = self._load_materias()
        self.inscripciones_actuales = self.raw_data.get('inscripciones_actuales', {})

    # --- Métodos de Carga

    def _load_estudiantes(self):
        
        return {id: Estudiante(id, 
                               data['nombre'], 
                               data['rol'], 
                               data.get('password', id),  
                               data['carrera'], 
                               data.get('materias_aprobadas'), 
                               data.get('notas'))
                for id, data in self.raw_data.get('estudiantes', {}).items()}

    def _load_profesores(self):
       
        return {id: Profesor(id, 
                              data['nombre'], 
                              data['rol'], 
                              data.get('password', id), 
                              data.get('materias_asignadas'))
                for id, data in self.raw_data.get('profesores', {}).items()}

    def _load_coordinadores(self):
        return {id: Coordinador(id, 
                                 data['nombre'], 
                                 data['rol'], 
                                 data.get('password', id))
                for id, data in self.raw_data.get('coordinadores', {}).items()}

    def _load_materias(self):
        return {codigo: Materia(codigo, data['nombre'], data['creditos'], data['prerrequisitos'], data['horario'], data.get('profesor_asignado'))
                for codigo, data in self.raw_data.get('materias', {}).items()}

    # --- Lógica de Negocio ---

    def findUser(self, id):
        return self.estudiantes.get(id) or self.profesores.get(id) or self.coordinadores.get(id)
        
    def authenticate(self, id, password):
        user = self.findUser(id)
        if user and user.password == password:
            return user
        return None

    def aiRecomendarMaterias(self, estudianteId):
        # Lógica de recomendación... (sin cambios)
        estudiante = self.estudiantes.get(estudianteId)
        if not estudiante:
            return {'disponibles': [], 'pendientes': []}

        aprobadas = set(estudiante.materias_aprobadas)
        disponibles = []
        pendientes = []
        inscritas = set(self.inscripciones_actuales.get(estudianteId, []))

        for codigo, materia in self.materias.items():
            if codigo in aprobadas or codigo in inscritas:
                continue

            prerrequisitos = set(materia.prerrequisitos)
            faltantes = [p for p in prerrequisitos if p not in aprobadas]

            profesor_nombre = self.profesores.get(materia.profesor_id, {'nombre': 'Sin Asignar'}).get('nombre')
            materia_info = {
                'codigo': codigo,
                'nombre': materia.nombre,
                'creditos': materia.creditos,
                'horario': materia.horario,
                'profesor': profesor_nombre
            }

            if not faltantes:
                disponibles.append(materia_info)
            elif prerrequisitos:
                pendientes.append({
                    'codigo': codigo,
                    'nombre': materia.nombre,
                    'faltantes': faltantes
                })

        return {'disponibles': disponibles, 'pendientes': pendientes}

    def estudianteInscribirMateria(self, estudianteId, codigo):
        # Lógica de inscripción... 
        estudiante = self.estudiantes.get(estudianteId)
        materia = self.materias.get(codigo)

        if not estudiante or not materia:
            return {'success': False, 'message': "Estudiante o Materia no encontrado."}

        if codigo in self.inscripciones_actuales.get(estudianteId, []):
            return {'success': False, 'message': f"La materia {codigo} ya está inscrita."}
            
        faltantes = [p for p in materia.prerrequisitos if p not in estudiante.materias_aprobadas]
        if faltantes:
            return {'success': False, 'message': f"Faltan prerrequisitos: {', '.join(faltantes)}."}

        if estudianteId not in self.inscripciones_actuales:
            self.inscripciones_actuales[estudianteId] = []
        self.inscripciones_actuales[estudianteId].append(codigo)
        
        self.raw_data['inscripciones_actuales'][estudianteId] = self.inscripciones_actuales[estudianteId]
        
        return {'success': True, 'message': f"Materia {codigo} inscrita exitosamente."}

    def coordinadorAsignarProfesor(self, materiaCodigo, profesorId):
        # Lógica de asignación... 
        materia = self.materias.get(materiaCodigo)
        profesor = self.profesores.get(profesorId)

        if not materia or not profesor:
            return {'success': False, 'message': "Materia o Profesor no encontrado."}
        if materia.profesor_id is not None:
            return {'success': False, 'message': "La materia ya tiene un profesor asignado."}

        materia.profesor_id = profesorId
        profesor.materias_asignadas.append(materiaCodigo)
        
        self.raw_data['materias'][materiaCodigo]['profesor_asignado'] = profesorId
        self.raw_data['profesores'][profesorId]['materias_asignadas'] = profesor.materias_asignadas

        return {'success': True, 'message': f"Materia {materiaCodigo} asignada a {profesor.nombre} exitosamente."}
        
    def coordinadorRegistrarEstudiante(self, nombre, id, carrera):
        # Lógica de registro...
        if self.findUser(id):
            return {'success': False, 'message': "El ID de estudiante ya existe."}
        
        # Usamos el ID como contraseña por defecto
        password_default = id
        
        nuevo_estudiante_data = {
            'nombre': nombre, 
            'rol': 'estudiante', 
            'carrera': carrera, 
            'materias_aprobadas': [], 
            'notas': {},
            'password': password_default
        }
        self.raw_data['estudiantes'][id] = nuevo_estudiante_data
        
        # Recargar la lista de estudiantes
        self.estudiantes = self._load_estudiantes()
        self.inscripciones_actuales[id] = []
        
        return {'success': True, 'message': f"Estudiante {nombre} registrado con ID {id}. Contraseña inicial: {password_default}"}



# 3. INTERFAZ GRÁFICA DE USUARIO (GUI - CustomTkinter)


class SICEU_App(ctk.CTk):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.current_user = None

        # Configuración de la Ventana Principal
        self.title("SICEU - Sistema de Gestión Académica")
        self.geometry("900x650") # Ventana ligeramente más grande
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue") # Podrías cambiarlo a "dark-blue" si quieres un tema más oscuro

        # Configuración de Layout (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # El contenedor principal ahora ocupa toda la ventana

        # Contenedor Principal
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Iniciar la aplicación con la vista de login
        self.show_login()

    # --- Métodos de Control de Vistas ---

    def show_message(self, message, is_success=True):
        messagebox.showinfo("Éxito" if is_success else "Error de Autenticación", message)

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
    def clear_dashboard_frames(self):
         for widget in self.menu_frame.winfo_children():
            widget.destroy()
         for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_main_container()
        self.current_user = None

        # 1. Marco para el Fondo (Simulación de un fondo grande)
        # Aquí usamos un color de fondo para la ventana y un marco.
        # en la aplicacion real usamos la imagen representativa de la unefa
        
        # Frame del Login (La 'Tarjeta' blanca/transparente de la imagen)
        login_card = ctk.CTkFrame(self.main_container, width=350, height=450, 
                                  fg_color=("white", "gray15"), # Blanco en modo claro, oscuro en modo oscuro
                                  corner_radius=15)
        login_card.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        login_card.grid_columnconfigure(0, weight=1)
        
        # Logo/Título de la Tarjeta
        ctk.CTkLabel(login_card, text="UNEFA SICEU", 
                     font=ctk.CTkFont(size=22, weight="bold"), 
                     text_color=BLUE_CIAN).grid(row=0, column=0, padx=40, pady=(30, 10))
        
        # Tipo Documento (Simulando el Dropdown)
        ctk.CTkLabel(login_card, text="Tipo Documento", 
                     font=ctk.CTkFont(size=13, weight="normal")).grid(row=1, column=0, padx=40, pady=(15, 0), sticky="w")
        self.doc_type_combo = ctk.CTkComboBox(login_card, values=["Cédula (V)", "Pasaporte (P)", "RIF (J)"], 
                                              width=270, height=35, dropdown_hover_color=BLUE_CIAN)
        self.doc_type_combo.grid(row=2, column=0, padx=40, pady=5)
        self.doc_type_combo.set("Cédula (V)")
        
        # Cédula/ID
        ctk.CTkLabel(login_card, text="👤 Cédula:", 
                     font=ctk.CTkFont(size=13, weight="normal")).grid(row=3, column=0, padx=40, pady=(15, 0), sticky="w")
        self.id_entry = ctk.CTkEntry(login_card, placeholder_text="Ingrese ID o Cédula (Ej: 1001)", width=270, height=35)
        self.id_entry.grid(row=4, column=0, padx=40, pady=5)
        
        # Contraseña
        ctk.CTkLabel(login_card, text="🔒 Contraseña:", 
                     font=ctk.CTkFont(size=13, weight="normal")).grid(row=5, column=0, padx=40, pady=(15, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(login_card, placeholder_text="Contraseña", show='*', width=270, height=35)
        self.password_entry.grid(row=6, column=0, padx=40, pady=5)
        
        # Botón INGRESAR 
        self.login_button = ctk.CTkButton(login_card, text="INGRESAR", command=self.attempt_login, 
                                          width=270, height=45, fg_color=BLUE_CIAN, hover_color="#00AEEF",
                                          font=ctk.CTkFont(size=15, weight="bold"))
        self.login_button.grid(row=7, column=0, padx=40, pady=(30, 10))
        
        # Enlace 
        ctk.CTkLabel(login_card, text="¿Ha olvidado su contraseña, o primera vez?", 
                     font=ctk.CTkFont(size=10), text_color="gray").grid(row=8, column=0, padx=40, pady=(5, 20))
        
        # Binding de Enter
        self.id_entry.bind("<Return>", lambda event=None: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event=None: self.attempt_login())


    def attempt_login(self):
        user_id = self.id_entry.get().upper()
        password = self.password_entry.get()

        if not user_id or not password:
            self.show_message("Por favor, ingrese Cédula/ID y Contraseña.", False)
            return

        # Desactivar botón y mostrar 'Cargando...'
        self.login_button.configure(text="Cargando...", state="disabled")
        self.update() 
        
        # Simular retardo de red
        time.sleep(0.5) 
        
        user = self.system.authenticate(user_id, password)

        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            self.show_message("Cédula/ID o Contraseña incorrecta. Intente de nuevo.", False)
            self.login_button.configure(text="INGRESAR", state="normal") # Restaurar botón

    def show_dashboard(self):
        self.clear_main_container()
        
        # 1. Cabecera (Header)
        self.header_frame = ctk.CTkFrame(self.main_container, height=50, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=1) # Para centrar el título

        self.title_label = ctk.CTkLabel(self.header_frame, text="SICEU - Dashboard", 
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.user_info_label = ctk.CTkLabel(self.header_frame, 
                                            text=f"{self.current_user.nombre} ({self.current_user.rol.capitalize()})", 
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.user_info_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        self.logout_button = ctk.CTkButton(self.header_frame, text="Salir", command=self.show_login, 
                                          width=80, fg_color="red", hover_color="#CC0000")
        self.logout_button.grid(row=0, column=2, padx=(0, 20), pady=10, sticky="e")
        
        # 2. Contenido Principal (Menu + Content)
        self.content_container = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=0) # Menu fijo
        self.content_container.grid_columnconfigure(1, weight=1) # Contenido expandible
        self.main_container.grid_rowconfigure(1, weight=1) # El contenedor de contenido se expande

        # Frame del menú de navegación (izquierda)
        self.menu_frame = ctk.CTkFrame(self.content_container, width=180, fg_color=("gray85", "gray20"))
        self.menu_frame.grid(row=0, column=0, sticky="ns", padx=(0, 15), pady=0)
        self.menu_frame.grid_columnconfigure(0, weight=1)
        
        # Frame de contenido (derecha)
        self.content_frame = ctk.CTkFrame(self.content_container)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Renderizar el menú y la vista inicial
        self.render_menu()
        self.show_initial_view()

    def render_menu(self):
        # Limpiar menú anterior
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.menu_frame, text="MENÚ PRINCIPAL", 
                     font=ctk.CTkFont(size=15, weight="bold"), 
                     text_color=BLUE_CIAN).grid(row=0, column=0, padx=20, pady=(20, 10))

        if self.current_user.rol == 'estudiante':
            menu_items = [
                ("Inscripción (AI)", self.show_estudiante_inscripcion),
                ("Ver Horario", self.show_estudiante_horario),
                ("Récord Académico", self.show_estudiante_record),
                ("Constancia", self.show_estudiante_constancia),
            ]
        elif self.current_user.rol == 'profesor':
            menu_items = [
                ("Materias Asignadas", self.show_profesor_materias),
                ("Cargar Notas (Demo)", self.show_profesor_cargar_notas),
            ]
        elif self.current_user.rol == 'coordinador':
            menu_items = [
                ("Asignar Profesor", self.show_coordinador_asignar),
                ("Registrar Estudiante", self.show_coordinador_registrar),
            ]
        else:
            menu_items = []
            
        for i, (text, command) in enumerate(menu_items):
            button = ctk.CTkButton(self.menu_frame, text=text, command=command, anchor="w", 
                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                   hover_color=("gray70", "gray30"))
            button.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
            
        ctk.CTkLabel(self.menu_frame, text="SICEU 2024", text_color="gray", 
                     font=ctk.CTkFont(size=10)).grid(row=len(menu_items) + 2, column=0, pady=(30, 10))


    def show_initial_view(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text=f"Bienvenido/a al Sistema, {self.current_user.nombre}.",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=BLUE_CIAN).grid(row=0, column=0, padx=20, pady=20, sticky="n")
        ctk.CTkLabel(self.content_frame, text=f"Su rol de acceso es: {self.current_user.rol.capitalize()}.",
                     font=ctk.CTkFont(size=16)).grid(row=1, column=0, padx=20, pady=5, sticky="n")
        ctk.CTkLabel(self.content_frame, text="Utilice el menú de la izquierda para navegar por las funcionalidades disponibles.",
                     font=ctk.CTkFont(size=14), text_color="gray").grid(row=2, column=0, padx=20, pady=20, sticky="n")


    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.content_frame.grid_rowconfigure(0, weight=0) # Reset weight

    # 4. VISTAS ESPECÍFICAS POR ROL 


    # --- Estudiante ---

    def show_estudiante_inscripcion(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Inscripción de Materias (AI Recomendada)", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.content_frame.grid_rowconfigure(2, weight=1)

        results = self.system.aiRecomendarMaterias(self.current_user.id)
        disponibles = results['disponibles']
        pendientes = results['pendientes']
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Recomendaciones para Inscripción")
        scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)

        # 1. Materias Disponibles
        ctk.CTkLabel(scroll_frame, text="✅ Materias Disponibles", font=ctk.CTkFont(size=15, weight="bold"), text_color="green").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        if not disponibles:
            ctk.CTkLabel(scroll_frame, text="No hay materias disponibles actualmente.").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        else:
            for i, m in enumerate(disponibles):
                item_frame = ctk.CTkFrame(scroll_frame)
                item_frame.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
                item_frame.grid_columnconfigure(0, weight=1)
                
                info_text = f"{m['codigo']} - {m['nombre']} (Créditos: {m['creditos']}, Profesor: {m['profesor']})"
                ctk.CTkLabel(item_frame, text=info_text, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                btn = ctk.CTkButton(item_frame, text="Inscribir", width=80, fg_color=BLUE_CIAN, hover_color="#00AEEF",
                                    command=lambda code=m['codigo']: self._inscribir_materia_callback(code))
                btn.grid(row=0, column=1, padx=10, pady=5)
        
        # 2. Materias Pendientes
        row_offset = len(disponibles) + 2
        ctk.CTkLabel(scroll_frame, text="❌ Materias Pendientes (Faltan Prerrequisitos)", font=ctk.CTkFont(size=15, weight="bold"), text_color="red").grid(row=row_offset, column=0, padx=10, pady=(10, 5), sticky="w")
        
        if not pendientes:
            ctk.CTkLabel(scroll_frame, text="No tienes prerrequisitos pendientes.", text_color="gray").grid(row=row_offset + 1, column=0, padx=10, pady=5, sticky="w")
        else:
            for i, m in enumerate(pendientes):
                info_text = f"{m['codigo']} - {m['nombre']} | Faltantes: {', '.join(m['faltantes'])}"
                ctk.CTkLabel(scroll_frame, text=info_text, anchor="w", text_color="red").grid(row=row_offset + i + 1, column=0, padx=10, pady=5, sticky="w")

    def _inscribir_materia_callback(self, codigo):
        result = self.system.estudianteInscribirMateria(self.current_user.id, codigo)
        self.show_message(result['message'], result['success'])
        if result['success']:
            self.show_estudiante_inscripcion()
            
    def show_estudiante_horario(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Horario de Clases Actual", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        inscritas_codigos = self.system.inscripciones_actuales.get(self.current_user.id, [])
        
        if not inscritas_codigos:
            ctk.CTkLabel(self.content_frame, text="No tienes materias inscritas para el periodo actual.").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            return

        header_frame = ctk.CTkFrame(self.content_frame)
        header_frame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=2)
        header_frame.grid_columnconfigure(1, weight=3)
        header_frame.grid_columnconfigure(2, weight=2)
        header_frame.grid_columnconfigure(3, weight=3)
        
        ctk.CTkLabel(header_frame, text="Código", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(header_frame, text="Materia", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(header_frame, text="Horario", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkLabel(header_frame, text="Profesor", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5)

        table_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Clases Inscritas")
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=2)
        table_frame.grid_columnconfigure(1, weight=3)
        table_frame.grid_columnconfigure(2, weight=2)
        table_frame.grid_columnconfigure(3, weight=3)
        self.content_frame.grid_rowconfigure(2, weight=1)

        for i, codigo in enumerate(inscritas_codigos):
            materia = self.system.materias.get(codigo)
            if materia:
                profesor_nombre = self.system.profesores.get(materia.profesor_id, {}).get('nombre', 'Sin Asignar')

                ctk.CTkLabel(table_frame, text=codigo, anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=materia.nombre, anchor="w").grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=materia.horario, anchor="w").grid(row=i, column=2, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=profesor_nombre, anchor="w").grid(row=i, column=3, padx=5, pady=5, sticky="ew")

    def show_estudiante_record(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Récord Académico", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        notas = self.current_user.notas
        
        if not notas:
            ctk.CTkLabel(self.content_frame, text="No hay notas registradas históricamente.").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            return

        header_frame = ctk.CTkFrame(self.content_frame)
        header_frame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=5)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(header_frame, text="Materia", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Nota Final", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(header_frame, text="Estado", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        table_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Notas Históricas")
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=5)
        table_frame.grid_columnconfigure(1, weight=1)
        table_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        for i, (codigo, nota) in enumerate(notas.items()):
            materia_nombre = self.system.materias.get(codigo, {}).get('nombre', 'Materia Desconocida')
            estado = "APROBADO" if nota >= 10 else "REPROBADO"
            color = "green" if nota >= 10 else "red"

            ctk.CTkLabel(table_frame, text=f"{materia_nombre} ({codigo})", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(table_frame, text=str(nota), anchor="center").grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(table_frame, text=estado, text_color=color, anchor="center").grid(row=i, column=2, padx=5, pady=5, sticky="ew")
            
    def show_estudiante_constancia(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Constancia de Inscripción", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        constancia_frame = ctk.CTkFrame(self.content_frame, border_width=2, fg_color=("white", "gray10"), border_color=BLUE_CIAN)
        constancia_frame.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        constancia_frame.grid_columnconfigure(0, weight=1)
        
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(constancia_frame, text="UNIVERSIDAD SICEU", 
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=BLUE_CIAN).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="n")
        ctk.CTkLabel(constancia_frame, text="CONSTANCIA DE INSCRIPCIÓN", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")

        data_frame = ctk.CTkFrame(constancia_frame, fg_color="transparent")
        data_frame.grid(row=2, column=0, padx=30, pady=10, sticky="ew")
        data_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(data_frame, text="Estudiante:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text=self.current_user.nombre, anchor="w").grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text="Cédula/ID:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text=self.current_user.id, anchor="w").grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text="Carrera:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text=self.current_user.carrera, anchor="w").grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text="Período:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(data_frame, text="2024-II (Simulado)", anchor="w").grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(constancia_frame, text="Materias Inscritas:", 
                     font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, padx=30, pady=(20, 5), sticky="w")
                     
        inscritas_codigos = self.system.inscripciones_actuales.get(self.current_user.id, [])
        materias_list_frame = ctk.CTkFrame(constancia_frame, fg_color="transparent")
        materias_list_frame.grid(row=4, column=0, padx=40, pady=(0, 20), sticky="ew")
        materias_list_frame.grid_columnconfigure(0, weight=1)
        
        if not inscritas_codigos:
            ctk.CTkLabel(materias_list_frame, text="(Ninguna materia inscrita en el periodo actual)").grid(row=0, column=0, sticky="w")
        else:
            for i, codigo in enumerate(inscritas_codigos):
                nombre = self.system.materias.get(codigo, {}).get('nombre', 'Materia Desconocida')
                ctk.CTkLabel(materias_list_frame, text=f"• {codigo} - {nombre}", anchor="w").grid(row=i, column=0, sticky="ew")


    # --- Profesor ---

    def show_profesor_materias(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Materias Asignadas", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        asignadas_codigos = self.current_user.materias_asignadas
        
        if not asignadas_codigos:
            ctk.CTkLabel(self.content_frame, text="No tiene materias asignadas actualmente.").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            return

        table_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Materias que Imparte")
        table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        for i, codigo in enumerate(asignadas_codigos):
            materia = self.system.materias.get(codigo)
            if materia:
                inscritos = sum(1 for inscritas in self.system.inscripciones_actuales.values() if codigo in inscritas)
                
                info_frame = ctk.CTkFrame(table_frame)
                info_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
                info_frame.grid_columnconfigure(0, weight=1)
                
                ctk.CTkLabel(info_frame, text=f"📘 {materia.nombre} ({codigo})", font=ctk.CTkFont(weight="bold"), anchor="w").grid(row=0, column=0, padx=10, pady=(5, 0), sticky="ew")
                ctk.CTkLabel(info_frame, text=f"Horario: {materia.horario} | Créditos: {materia.creditos}", text_color="gray", anchor="w").grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
                ctk.CTkLabel(info_frame, text=f"👥 Estudiantes Inscritos: {inscritos}", text_color=BLUE_CIAN, anchor="w").grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

    def show_profesor_cargar_notas(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Cargar Notas (Funcionalidad de Demo)", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        ctk.CTkLabel(self.content_frame, text="Esta funcionalidad requiere interacción compleja con la base de datos.", 
                     text_color="gray").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.content_frame, text="En una aplicación real, aquí se listaría cada estudiante inscrito\nyse permitiría al profesor ingresar o modificar la nota final.", 
                     text_color="gray").grid(row=2, column=0, padx=20, pady=5, sticky="w")


    # --- Coordinador ---

    def show_coordinador_asignar(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Asignar Profesor a Materia", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        materias_sin_profesor = [m for m in self.system.materias.values() if m.profesor_id is None]
        profesores_list = list(self.system.profesores.values())
        
        materia_options = [f"{m.nombre} ({m.codigo})" for m in materias_sin_profesor]
        profesor_options = [f"{p.nombre} ({p.id})" for p in profesores_list]
        
        if not materias_sin_profesor:
            ctk.CTkLabel(self.content_frame, text="Todas las materias tienen un profesor asignado.", 
                         text_color="green").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            return
            
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Materia sin Asignar:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.materia_var = ctk.StringVar(value=materia_options[0] if materia_options else "")
        self.materia_select = ctk.CTkComboBox(form_frame, values=materia_options, variable=self.materia_var, width=350, dropdown_hover_color=BLUE_CIAN)
        self.materia_select.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Profesor a Asignar:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.profesor_var = ctk.StringVar(value=profesor_options[0] if profesor_options else "")
        self.profesor_select = ctk.CTkComboBox(form_frame, values=profesor_options, variable=self.profesor_var, width=350, dropdown_hover_color=BLUE_CIAN)
        self.profesor_select.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkButton(self.content_frame, text="Confirmar Asignación", command=self._asignar_profesor_callback, 
                      fg_color=BLUE_CIAN, hover_color="#00AEEF").grid(row=2, column=0, padx=20, pady=20, sticky="w")

    def _asignar_profesor_callback(self):
        materia_display = self.materia_var.get()
        profesor_display = self.profesor_var.get()
        
        if not materia_display or not profesor_display:
            self.show_message("Debe seleccionar una materia y un profesor.", False)
            return

        materia_codigo = materia_display.split('(')[-1].strip(')')
        profesor_id = profesor_display.split('(')[-1].strip(')')
        
        result = self.system.coordinadorAsignarProfesor(materia_codigo, profesor_id)
        self.show_message(result['message'], result['success'])
        
        if result['success']:
            self.show_coordinador_asignar()

    def show_coordinador_registrar(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Registrar Nuevo Estudiante", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="w")
                     
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Nombre Completo:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.reg_nombre_entry = ctk.CTkEntry(form_frame, width=250)
        self.reg_nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="ID/Cédula (Ej: 1003):", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.reg_id_entry = ctk.CTkEntry(form_frame, width=250)
        self.reg_id_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Carrera:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.reg_carrera_entry = ctk.CTkEntry(form_frame, width=250)
        self.reg_carrera_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(self.content_frame, text="Registrar Estudiante", command=self._registrar_estudiante_callback, 
                      fg_color=BLUE_CIAN, hover_color="#00AEEF").grid(row=2, column=0, padx=20, pady=20, sticky="w")
        
    def _registrar_estudiante_callback(self):
        nombre = self.reg_nombre_entry.get()
        id = self.reg_id_entry.get().upper()
        carrera = self.reg_carrera_entry.get()

        if not nombre or not id or not carrera:
            self.show_message("Todos los campos son obligatorios.", False)
            return
            
        result = self.system.coordinadorRegistrarEstudiante(nombre, id, carrera)
        self.show_message(result['message'], result['success'])

        if result['success']:
            self.reg_nombre_entry.delete(0, ctk.END)
            self.reg_id_entry.delete(0, ctk.END)
            self.reg_carrera_entry.delete(0, ctk.END)


if __name__ == "__main__":
    # Inicializar el sistema de gestión
    sistema = SistemaAcademico(MOCK_DATA)
    
    # Inicializar y correr la aplicación GUI
    app = SICEU_App(sistema)
    app.mainloop()