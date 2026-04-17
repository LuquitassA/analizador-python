import ply.lex as lex
import codecs #proporciona herramientas para trabajar con codificaciones de texto
import sys
import re


tokens = [
#SIGNOS DE PUNTUACION
'LLAVEDER', 'LLAVEIZQ', 'CORCHDER', 'CORCHIZQ', 'COMA',  'DOSPUNT', #'COMILLAS',


#NOMBRES DE OBJETOS Y LISTAS
'EQUIPOS_t', 'NOMBRE_EQUIPO_t', 'IDENTIDAD_EQUIPO_t', 'LINK_t', 'CARRERA_t', 'ASIGNATURA_t', 'UNIVERSIDAD_REGIONAL_t', 'ALIANZA_EQUIPO_t',
'DIRECCION_t', 'CALLE_t', 'CIUDAD_t', 'PAIS_t', 
'INTEGRANTES_t', 'PROYECTOS_t', 'TAREAS_t',
'NOMBRE_t', 'EDAD_t', 'CARGO_t', 'FOTO_t', 'EMAIL_t', 'HABILIDADES_t', 'SALARIO_t', 'ACTIVO_t',
'ESTADO_t', 'RESUMEN_t', 'FECHA_INICIO_t', 'FECHA_FIN_t', 'VIDEO_t', 'CONCLUSION_t',
'VERSION_t', 'FIRMA_DIGITAL_t',

#TERMINALES CON VALORES ESPECIFICOS
'STRING', 'FECHA', 'FECHA_INVALIDA', 'INTEGER', 'NULL_t', 'FLOAT', 'BOOL_t', 'TIPOC', 'ESTADOPROY', 'URL_t', 'CORREO_t',
]

t_ignore = ' \t\n'  # Ignorar espacios, tabs y saltos de línea

# Funciones ordenadas por prioridad

# FECHA debe ir antes que INTEGER también para evitar que se separe
# (19|20) indica que puede tomar alguno de los dos valores
# 0[1-9] si arranca con 0 puede tomar cualquier valor
# 1[0-2] forma los numeros 10, 11, 12
# [1-2][0-9] forma los numeros del 10 al 29
# 3[0-1] forma los numeros 30 y 31

#fecha
def t_FECHA(t):
    # Captura solo el formato básico YYYY-MM-DD entre comillas
    r'"(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"'
    t.value = t.value[1:-1]  # Elimina comillas
    return t

def t_FECHA_INVALIDA(t):
    # Captura cualquier otro formato que parezca fecha entre comillas
    r'"[0-9]{4}-[0-9]{2}-[0-9]{2}"'  # Formato YYYY-MM-DD
    print(f"Fecha con formato inválido: {t.value}")
    t.value = t.value[1:-1]  # Elimina comillas
    return t


def t_URL_t(t):
    r'"((http|https)://|www\.)[\w\-]+(\.[\w\-]+)+(:\d+)?(/[^\s"?#]*)?(\?[^\s"#]*)?(\#[^\s"]*)?"'
    t.value = t.value[1:-1]
    return t

# CORREO debe ir antes que STRING para tener prioridad
#primer termino (caracteres, digitos, _ , . , +, -,)
#segundo termino si o si @
#tercer termino alfanumerico o -
#cuarto termino si o si .
#quinto termino alfanumerico, giones, o puntos (.com.ar)
def t_CORREO_t(t):
    r'"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+){0,3}"' 
    t.value = t.value[1:-1]  # elimina comillas
    return t

def t_EQUIPOS_t(t):
    r'"equipos"'
    t.value = t.value[1:-1]
    return t

def t_DIRECCION_t(t):
    r'"direccion"' #tiene acento
    t.value = t.value[1:-1]     
    return t

def t_INTEGRANTES_t(t):
    r'"integrantes"'
    t.value = t.value[1:-1]
    return t

def t_PROYECTOS_t(t):
    r'"proyectos"'
    t.value = t.value[1:-1]
    return t

def t_TAREAS_t(t):
    r'"tareas"'
    t.value = t.value[1:-1]
    return t

def t_VERSION_t(t):
    r'"version"'
    t.value = t.value[1:-1]
    return t

def t_FIRMA_DIGITAL_t(t):
    r'"firma_digital"'
    t.value = t.value[1:-1]
    return t

def t_NOMBRE_EQUIPO_t(t):
    r'"nombre_equipo"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIDAD_EQUIPO_t(t):
    r'"identidad_equipo"' 
    t.value = t.value[1:-1]     
    return t

def t_LINK_t(t):
    r'"link"'
    t.value = t.value[1:-1]
    return t

def t_ASIGNATURA_t(t):
    r'"asignatura"'
    t.value = t.value[1:-1]
    return t

def t_CARRERA_t(t):
    r'"carrera"'
    t.value = t.value[1:-1]
    return t

def t_UNIVERSIDAD_REGIONAL_t(t):
    r'"universidad_regional"'
    t.value = t.value[1:-1]
    return t

def t_ALIANZA_EQUIPO_t(t):
    r'"alianza_equipo"'
    t.value = t.value[1:-1]
    return t

def t_CALLE_t(t):
    r'"calle"'
    t.value = t.value[1:-1]
    return t

def t_CIUDAD_t(t):
    r'"ciudad"'
    t.value = t.value[1:-1]
    return t

def t_PAIS_t(t):
    r'"pais"'   #tiene acento
    t.value = t.value[1:-1]         
    return t

def t_NOMBRE_t(t):
    r'"nombre"'
    t.value = t.value[1:-1]
    return t

def t_EDAD_t(t):
    r'"edad"'
    t.value = t.value[1:-1]
    return t

def t_CARGO_t(t):
    r'"cargo"'
    t.value = t.value[1:-1]
    return t

def t_FOTO_t(t):
    r'"foto"'
    t.value = t.value[1:-1]
    return t

def t_EMAIL_t(t):
    r'"email"'
    t.value = t.value[1:-1]
    return t

def t_HABILIDADES_t(t):
    r'"habilidades"'
    t.value = t.value[1:-1]
    return t

def t_SALARIO_t(t):
    r'"salario"'
    t.value = t.value[1:-1]
    return t

def t_ACTIVO_t(t):
    r'"activo"'
    t.value = t.value[1:-1]
    return t

def t_ESTADO_t(t):
    r'"estado"'
    t.value = t.value[1:-1]
    return t

def t_RESUMEN_t(t):
    r'"resumen"'
    t.value = t.value[1:-1]
    return t

def t_FECHA_INICIO_t(t):
    r'"fecha_inicio"'
    t.value = t.value[1:-1]
    return t

def t_FECHA_FIN_t(t):
    r'"fecha_fin"'
    t.value = t.value[1:-1]
    return t

def t_VIDEO_t(t):
    r'"video"'
    t.value = t.value[1:-1]
    return t

def t_CONCLUSION_t(t):
    r'"conclusion"' #acento
    t.value = t.value[1:-1]
    return t

# \b indica el limite entre el caracter inicial y final
# \s marca los espacios
'''def t_TIPOC(t):
    r'"(product analyst|project manager|ux designer|marketing|developer|devops|db admin)"'
    t.value = t.value[1:-1]
    return t

def t_ESTADOPROY(t):
    r'"(to ?do|in ?progress|canceled|done|on ?hold)"'
    t.value = t.value[1:-1]
    return t'''

def t_LLAVEIZQ(t): 
    r'\{'
    return t

def t_LLAVEDER(t):
    r'\}'
    return t

def t_CORCHIZQ(t):
    r'\['
    return t

def t_CORCHDER(t):
    r'\]'
    return t

#def t_COMILLAS(t):
#    r'\"'
#    return t

def t_DOSPUNT(t):
    r':'
    return t

def t_COMA(t):
    r','                  
    return t

def t_NULL_t(t):
    r'null'   #valor nulo/vacio
    return t

def t_BOOL_t(t):
    r'\btrue\b|\bfalse\b' #booleanos
    return t

def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'  # Cambiado para aceptar cualquier cantidad de decimales
    return t

def t_INTEGER(t): 
    r'[0-9]+'    #enteros
    return t

# STRING debe ir al final para que no interfiera con otros tokens
# ^ indica que lo que sigue coincidira con cualquier caracter menos lo indicado
def t_STRING(t):
    r'"([^\}^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    # Normaliza para comparar
    valor = t.value.strip().lower()
    tipoc_validos = [
        "product analyst", "project manager", "ux designer",
        "marketing", "developer", "devops", "db admin"
    ]
    estadoproy_validos = [
        "to do", "in progress", "canceled", "done", "on hold"
    ]
    if valor in tipoc_validos:
        t.type = 'TIPOC'
    elif valor in estadoproy_validos:
        t.type = 'ESTADOPROY'
    return t

def t_error(t):
    if t.value[0].strip():  # Si el carácter no es espacio, tab o salto de línea
        print(f"⚠️ Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)


# Función para analizar desde archivo
"""
#---------------------------------------------------------------------------------------------------
def analizar_archivo(lexer, filename):
    try:
        with codecs.open(filename, "r", "utf-8") as fp:
            cadena = fp.read()
        
        lexer.input(cadena)
        print(f"\n--- Resultados del análisis léxico para {filename} ---")
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f'Token: {tok.type}, Valor: {tok.value}')
            
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo {filename}")
    except Exception as e:
        print(f"\nError al procesar el archivo: {str(e)}")

# Función para modo interactivo
def modo_interactivo(lexer):
    print("\nModo interactivo - Escribe texto JSON para analizar")
    print("Ingresa tu texto línea por línea. Escribe 'fin' en una nueva línea para terminar la entrada.")
    
    while True:
        try:
            # Leer entrada del usuario
            print("\nIngrese el texto a analizar (escribe 'fin' en una línea nueva para terminar):")
            lineas = []
            while True:
                linea = input("> ")
                if linea.lower() == 'fin':
                    break
                lineas.append(linea)
            
            texto = '\n'.join(lineas)
            if not texto.strip():
                print("No se ingresó texto para analizar.")
                continue
            
            # Analizar la entrada
            lexer.input(texto)
            print("\n--- Resultados del análisis ---")
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
                print(f'Token: {tok.type}, Valor: {tok.value}')
            
            if not tokens:
                print("No se encontraron tokens válidos.")
            
            # Menú de opciones después del análisis
            while True:
                print("\n¿Qué deseas hacer ahora?")
                print("1. Analizar otro texto")
                print("2. Cambiar a analizar un archivo")
                print("3. Salir del programa")
                
                opcion = input("Seleccione una opción (1-3): ").strip()
                
                if opcion == "1":
                    break  # Volver a pedir texto
                elif opcion == "2":
                    return "archivo"  # Salir para cambiar a modo archivo
                elif opcion == "3":
                    return "salir"  # Terminar el programa
                else:
                    print("Opción inválida. Por favor elija 1, 2 o 3.")
        
        except KeyboardInterrupt:
            print("\nInterrupción detectada. ¿Deseas salir?")
            respuesta = input("Presiona 's' para salir o cualquier otra tecla para continuar: ").lower()
            if respuesta == 's':
                return "salir"
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            continue

def main():
    # Crear el lexer
    analizador = lex.lex()
    
    # Menú principal
    while True:
        print("\n--- Menú Principal ---")
        print("1. Modo interactivo")
        print("2. Analizar archivo")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            resultado = modo_interactivo(analizador)
            if resultado == "archivo":
                opcion = "2"  # Cambiar a analizar archivo
            elif resultado == "salir":
                break
        if opcion == "2":
            filename = input("Ingrese la ruta del archivo .json: ").strip()
            if not filename.endswith('.json'):
                print("Error: El archivo debe tener extensión .json")
                continue
            analizar_archivo(analizador, filename)
            
            # Preguntar qué hacer después de analizar archivo
            while True:
                print("\n¿Qué deseas hacer ahora?")
                print("1. Analizar otro archivo")
                print("2. Cambiar a modo interactivo")
                print("3. Salir del programa")
                
                opcion = input("Seleccione una opción (1-3): ").strip()
                
                if opcion == "1":
                    filename = input("Ingrese la ruta del archivo .json: ").strip()
                    if not filename.endswith('.json'):
                        print("Error: El archivo debe tener extensión .json")
                        continue
                    analizar_archivo(analizador, filename)
                elif opcion == "2":
                    break  # Volverá al menú principal y podrá elegir modo interactivo
                elif opcion == "3":
                    print("\n¡Gracias por usar el analizador léxico!")
                    return
                else:
                    print("Opción inválida. Por favor elija 1, 2 o 3.")
                    
        elif opcion == "3":
            print("\n¡Gracias por usar el analizador léxico!")
            break
        else:
            print("Opción inválida. Por favor elija 1, 2 o 3.")
if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------
"""
# creas el lexer
analizador = lex.lex()