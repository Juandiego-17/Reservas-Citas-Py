import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital"
    )
    return  conn

admins = {}


def register():
    print("Por favor ingresa tus datos para registrarte:")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nombre, contraseña) VALUES (%s, %s)", (nombre, contraseña))
        conn.commit()
        print("Te has registrado exitosamente")
    except mysql.connector.IntegrityError:
        print("El nombre de usuario ya existe. Por favor elige otro nombre.")
    
    conn.close()

def registerAdmins():
    print("Por favor ingresa tus datos para registrarte:")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO admins (nombre, contraseña) VALUES (%s, %s)", (nombre, contraseña))
        conn.commit()
        print("Te has registrado exitosamente")
    except mysql.connector.IntegrityError:
        print("El nombre de usuario ya existe. Por favor elige otro nombre.")
    
    conn.close()

def login():
    print("Por favor ingresa tus datos para iniciar sesion:")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s", (nombre, contraseña))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        print("Has iniciado sesion con exito")
        return nombre
    else:
        print("Nombre de usuario o contraseña son incorrectos")
        return None

def loginAdmins():
    print("Por favor ingresa tus datos para iniciar sesion:")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admins WHERE nombre = %s AND contraseña = %s", (nombre, contraseña))
    admin = cursor.fetchone()

    conn.close()

    if admin:
        print("Has iniciado sesion con exito")
        return nombre
    else:
        print("Nombre de usuario o contraseña son incorrectos")
        return None

def reservaCitas(usuario):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (usuario,))
    usuario_id = cursor.fetchone()[0]

    print("\nPor favor ingresa el tipo de consulta que necesitas:")
    print("1. Medicina general")
    print("2. Odontologia")
    print("3. Alergologia")
    opcion = input("Selecciona una opcion: ")

    if opcion == "1":
        opcion = "Medicina general"
        print(f"Estos son los doctores de medicina general disponibles con sus fechas y horarios:\nAlejandro Garcia:\nDisponibilidad:\n10/05/2024: 08:00, 09:00, 10:00\n11/05/2024: 08:00, 09:00, 10:00, 11:00\n\nLorena Cañon:\nDisponibilidad:\n11/05/2024: 09:00, 10:00, 11:00\n12/05/2024: 09:00, 10:00, 11:00, 12:00\n\nValentina Gomez:\nDisponibilidad:\n12/05/2024: 10:00, 11:00, 12:00\n13/05/2024: 10:00, 11:00, 12:00, 13:00")
    elif opcion == "2":
        opcion = "Odontologia"
        print(f"Estos son los doctores de odontologia disponibles con sus fechas y horarios:\nJose Rodriguez:\nDisponibilidad:\n09/05/2024: 07:00, 08:00, 09:00\n11/05/2024: 09:00, 10:00, 11:00, 12:00\n\nJulieth Lopez:\nDisponibilidad:\n10/05/2024: 08:00, 09:00, 10:00\n12/05/2024: 09:00, 10:00, 11:00, 12:00\n\nTomas Chavarria:\nDisponibilidad:\n11/05/2024: 09:00, 10:00, 11:00\n13/05/2024: 10:00, 11:00, 12:00, 13:00")
    elif opcion == "3":
        opcion = "Alergologia"
        print(f"Estos son los doctores de alergologia disponibles con sus fechas y horarios:\nSebastian Guzman:\nDisponibilidad:\n24/06/2024: 09:00, 11:00, 13:00\n28/06/2024: 08:00, 10:00, 12:00, 14:00\n\nLuis Hernandez:\nDisponibilidad:\n05/06/2024: 10:00, 12:00, 14:00\n10/06/2024: 12:00, 14:00, 15:00\n\nEduardo Zapata:\nDisponibilidad:\n12/06/2024: 07:00, 11:00, 16:00\n15/06/2024: 08:00, 10:00, 13:00, 15:00")
    else:
        print("Opcion no valida.")
        conn.close()
        return

    print("Por favor ingresa los detalles para reservar una cita medica")
    fecha = input("Fecha (DD/MM/AAAA): ")
    hora = input("Hora (HH:MM): ")
    medico = input("Nombre del médico: ")

    cursor.execute("SELECT * FROM citas_medicas WHERE usuario_id = %s AND medico = %s AND fecha = %s AND hora = %s", (usuario_id, medico, fecha, hora))
    cita = cursor.fetchone()

    if cita:
        print("Ya hay una cita programada con el médico en esta fecha y hora. Por favor selecciona otra fecha.")
        conn.close()
        return

    motivo = input("Motivo de la cita: ")

    cursor.execute("INSERT INTO citas_medicas (usuario_id, medico, fecha, hora, motivo) VALUES (%s, %s, %s, %s, %s)", (usuario_id, medico, fecha, hora, motivo))
    conn.commit()
    conn.close()

    print("La cita medica se ha reservado exitosamente")

def mostrarCitasMedicas():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM citas_medicas")
    citas = cursor.fetchall()

    conn.close()

    if citas:
        print("\nCitas Médicas Programadas:")
        for cita in citas:
            print(f"Usuario: {cita[1]} | Médico: {cita[2]} | Fecha: {cita[3]} | Hora: {cita[4]} | Motivo: {cita[5]}")
    else:
        print("No hay citas médicas programadas.")


def agregarHistorialPaciente():
    print("Agregar Historial del Paciente:")
    nombre_paciente = input("Nombre del paciente: ")
    medico = input("Nombre del medico: ")
    fecha = input("Fecha de la cita médica (DD/MM/AAAA): ")
    hora = input("Hora de la cita médica (HH:MM): ")
    motivo = input("Motivo de la cita: ")
    descripcion = input("Descripción del tratamiento o diagnóstico: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO historial_paciente (nombre_paciente, medico, fecha, hora, motivo, descripcion) VALUES (%s, %s, %s, %s, %s, %s)", (nombre_paciente, medico, fecha, hora, motivo, descripcion))
    conn.commit()
    conn.close()

    print("Historial del paciente agregado exitosamente")

def verificarHistorialdelPaciente():
    nombre_paciente = input("Ingrese el nombre del paciente: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM historial_paciente WHERE nombre_paciente = %s", (nombre_paciente,))
    historial = cursor.fetchall()

    conn.close()

    if historial:
        print("\nHistorial del Paciente:")
        for entrada in historial:
            print("Nombre del paciente:", nombre_paciente)
            print("Historial:")
            print(f"Medico: {entrada[2]}")
            print(f"Fecha: {entrada[3]}")
            print(f"Hora: {entrada[4]}")
            print(f"Motivo: {entrada[5]}")
            print(f"Descripción: {entrada[6]}")
            print("----------")
    else:
        print("No se encontró historial para el paciente.")


def verHistorialPaciente():
    nombre_paciente = input("Ingrese el nombre del paciente: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM historial_paciente WHERE nombre_paciente = %s", (nombre_paciente,))
    historial = cursor.fetchall()

    conn.close()

    if historial:
        for entrada in historial:
            print(f"\nMedico: {entrada[2]}")
            print(f"Fecha: {entrada[3]}")
            print(f"Hora: {entrada[4]}")
            print(f"Motivo: {entrada[5]}")
            print(f"Descripcion: {entrada[6]}")
    else:
        print("No se encontró historial para el paciente.")

def menuAdmin(admins):
    print(f"\nBienvenido {admins}")
    print("1. Añadir historial de pacientes")
    print("2. Verificar historial de pacientes")
    print("3. Ver citas médicas")
    print("4. Cerrar Sesion")

def menuDelUsuario(usuario):
    print(f"\nBienvenido {usuario}")   
    print("1. Reservar cita medica")
    print("2. Ver historia clinica")
    print("3. Ver citas médicas")
    print("4. Cerrar sesion")


def main():
    usuario_actual = None
    admin_actual = None

    while True:
        if usuario_actual is None and admin_actual is None:
            print("\nBienvenido al sistema hospitalario de Ibague")
            print("1. Registrar pacientes")
            print("2. Iniciar sesión para pacientes")
            print("3. Iniciar sesión para administradores")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                register()
            elif opcion == "2":
                usuario_actual = login()
            elif opcion == "3":
                admin_actual = loginAdmins()
            elif opcion == "4":
                print("Hasta luego")
                break
            else:
                print("Por favor selecciona una opción válida")

        elif admin_actual:
            menuAdmin(admin_actual)
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                agregarHistorialPaciente()
            elif opcion == "2":
                nombre_paciente = input("Nombre del paciente: ")
                verificarHistorialdelPaciente(nombre_paciente)
            elif opcion == "3":
                mostrarCitasMedicas()
            elif opcion == "4":
                print(f"Hasta luego {admin_actual}")
                admin_actual = None
            else:
                print("Por favor selecciona una opción válida")


        elif usuario_actual:
            menuDelUsuario(usuario_actual)
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                reservaCitas(usuario_actual)
            elif opcion == "2":
                verHistorialPaciente()
            elif opcion == "3":
                mostrarCitasMedicas()
            elif opcion == "4":
                print(f"Hasta luego {usuario_actual}")
                usuario_actual = None
            else:
                print("Por favor selecciona una opción válida")

if __name__ == "__main__":
    main()
