import ply.yacc as yacc              #Importamos las librerias necesarias para el analizador 
from analizador_lexico import tokens #Importo tokens
import ply.lex as lex               #Importamos las librerias necesarias para el analizador
import analizador_lexico
import pathlib, codecs
import os
from sys import stdin
import re
import webbrowser

archivo_actual = None #Variable global para la ruta del archivo
okay = True
html_result = ""

#definimos si tiene prioridad por izquierda, derecha o no tiene (tokens)
precedence = (    
    ('nonassoc', 'STRING'),
    ('nonassoc', 'FECHA'),
    ('nonassoc', 'INTEGER'),
    ('nonassoc', 'NULL_t'),
    ('nonassoc', 'FLOAT'),
    ('nonassoc', 'BOOL_t'),
    ('left', 'ESTADOPROY'),
    ('left', 'TIPOC'),
    ('nonassoc', 'EQUIPOS_t'),
    ('nonassoc', 'NOMBRE_EQUIPO_t'),
    ('nonassoc', 'IDENTIDAD_EQUIPO_t'),
    ('nonassoc', 'LINK_t'),
    ('nonassoc', 'CARRERA_t'),
    ('nonassoc', 'ASIGNATURA_t'),
    ('nonassoc', 'UNIVERSIDAD_REGIONAL_t'),
    ('nonassoc', 'ALIANZA_EQUIPO_t'),
    ('nonassoc', 'DIRECCION_t'),
    ('nonassoc', 'CALLE_t'),
    ('nonassoc', 'CIUDAD_t'),
    ('nonassoc', 'PAIS_t'),
    ('nonassoc', 'INTEGRANTES_t'),
    ('nonassoc', 'PROYECTOS_t'),
    ('nonassoc', 'TAREAS_t'),
    ('nonassoc', 'NOMBRE_t'),
    ('nonassoc', 'EDAD_t'),
    ('nonassoc', 'CARGO_t'),
    ('nonassoc', 'FOTO_t'),
    ('nonassoc', 'EMAIL_t'),
    ('nonassoc', 'HABILIDADES_t'),
    ('nonassoc', 'SALARIO_t'),
    ('nonassoc', 'ACTIVO_t'),
    ('nonassoc', 'ESTADO_t'),
    ('nonassoc', 'RESUMEN_t'),
    ('nonassoc', 'FECHA_INICIO_t'),
    ('nonassoc', 'FECHA_FIN_t'),
    ('nonassoc', 'VIDEO_t'),
    ('nonassoc', 'CONCLUSION_t'),
    ('nonassoc', 'VERSION_t'),
    ('nonassoc', 'FIRMA_DIGITAL_t'),
    ('nonassoc', 'URL_t'),
    ('nonassoc', 'CORREO_t'),
    ('nonassoc', 'COMA'),
    ('nonassoc', 'DOSPUNT'),
    ('left', 'LLAVEIZQ'),
    ('left', 'LLAVEDER'),
    ('left', 'CORCHIZQ'),
    ('left', 'CORCHDER'),
)

#Analizamos producciones
def p_SIGMA(p):
    '''SIGMA : INICIO'''
    #abrimos y cerramos el html, para poder ir creando todo en p[0]
    p[0] = f'<html><body>{p[1]}</body></html>'
    global html_result
    html_result += p[0]

def p_INICIO(p):
    '''INICIO : LLAVEIZQ OJSON LLAVEDER'''
    p[0] = p[2]

#Todas las combinas de OJSON (equipos, version?, firma_digital?)

#todas las combinaciones de OJSON
def p_OJSON(p):
    '''OJSON : EQUIPOS COMA VERSION COMA FIRMA_DIGITAL
            | VERSION COMA EQUIPOS COMA FIRMA_DIGITAL
            | FIRMA_DIGITAL COMA VERSION COMA EQUIPOS
            | VERSION COMA FIRMA_DIGITAL COMA EQUIPOS
            | EQUIPOS COMA FIRMA_DIGITAL
            | EQUIPOS COMA VERSION
            | EQUIPOS
            | VERSION COMA EQUIPOS
            | FIRMA_DIGITAL COMA EQUIPOS'''
    #HTLM------------------------------------------------------
    html = ""
    for elem in p:
        if isinstance(elem, str):
            html += elem
    p[0] = html


def p_VERSION(p):
    '''VERSION : VERSION_t DOSPUNT STRING'''
    p[0] = f'<!-- Version: {p[3]} -->'

def p_FIRMA_DIGITAL(p):
    '''FIRMA_DIGITAL : FIRMA_DIGITAL_t DOSPUNT STRING'''
    p[0] = f'<!-- Firma Digital: {p[3]} -->'

def p_EQUIPOS(p):
    '''EQUIPOS : EQUIPOS_t DOSPUNT CORCHIZQ LISTA_EQ CORCHDER'''
    p[0] = p[4]


def p_LISTA_EQ1(p):
    '''LISTA_EQ : LLAVEIZQ OBJ_EQ LLAVEDER COMA LISTA_EQ '''
    p[0] = p[2] + p[5]

def p_LISTA_EQ2(p):
    ''' LISTA_EQ : LLAVEIZQ OBJ_EQ LLAVEDER'''
    p[0] = p[2]

def p_OBJ_EQ(p):
    ''' OBJ_EQ : NOMBRE_EQUIPO_t DOSPUNT STRING COMA IDENTIDAD_EQUIPO_t DOSPUNT URL_t COMA OPCIONAL_DIRECCION OPCIONAL_LINK CARRERA_t DOSPUNT STRING COMA ASIGNATURA_t DOSPUNT STRING COMA UNIVERSIDAD_REGIONAL_t DOSPUNT STRING COMA ALIANZA_EQUIPO_t DOSPUNT STRING COMA INTEGRANTES_t DOSPUNT CORCHIZQ LISTA_INTEGRANTES CORCHDER COMA PROYECTOS_t DOSPUNT CORCHIZQ LISTA_PROYECTOS CORCHDER'''
    #HTML------------------------------------------------------
    nombre = p[3]
    identidad = p[7]
    link_html = p[10]
    direccion = p[9]
    carrera = p[13]
    asignatura = p[17]
    universidad = p[21]
    alianza = p[25]
    integrantes = p[30]
    proyectos = p[36]

    html = f'''<div style="border:1px solid gray; padding:20px;">
    <h1>{nombre}</h1>
    <img src="{identidad}" alt="Logo del equipo" style="width:150px; border:1px solid #ccc;">
    {direccion}
    {link_html}
    <p><strong>Asignatura:</strong> {asignatura}</p>
    <p><strong>Carrera:</strong> {carrera}</p>
    <p><strong>Universidad:</strong> {universidad}</p>
    <p><strong>Alianza:</strong> {alianza}</p>
    <h2>Integrantes</h2>
    <ul>{integrantes}</ul>
    <h2>Proyectos</h2>
    {proyectos}
    </div>'''
    p[0] = html

def p_OPCIONAL_LINK(p):
    '''OPCIONAL_LINK : '''
    p[0] = ""

def p_OPCIONAL_LINK1(p):
    '''OPCIONAL_LINK : LINK_t DOSPUNT URL_t COMA'''
    p[0] = f'<p><strong>Link:</strong> <a target="_blank" href="{p[3]}">{p[3]}</a></p>'

def p_OPCIONAL_DIRECCION(p):
    '''OPCIONAL_DIRECCION : DIRECCION_t DOSPUNT LLAVEIZQ OBJ_DIR LLAVEDER COMA'''
    p[0] = f"<p><strong>Dirección:</strong> {p[4]}</p>"   

def p_OPCIONAL_DIRECCION1(p):
    '''OPCIONAL_DIRECCION : '''
    p[0] = ""

#CALLE, CIUDAD, PAIS
def p_OBJ_DIR(p):
    ''' OBJ_DIR : CALLE_t DOSPUNT STRING COMA CIUDAD_t DOSPUNT STRING COMA PAIS_t DOSPUNT STRING '''
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

#CALLE, PAIS, CIUDAD
def p_OBJ_DIR1(p):
    ''' OBJ_DIR : CALLE_t DOSPUNT STRING COMA PAIS_t DOSPUNT STRING COMA CIUDAD_t DOSPUNT STRING ''' 
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

#CIUDAD, CALLE, PAIS
def p_OBJ_DIR2(p):
    ''' OBJ_DIR : CIUDAD_t DOSPUNT STRING COMA CALLE_t DOSPUNT STRING COMA PAIS_t DOSPUNT STRING '''
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

#CIUDAD, PAIS, CALLE
def p_OBJ_DIR3(p):
    ''' OBJ_DIR : CIUDAD_t DOSPUNT STRING COMA PAIS_t DOSPUNT STRING COMA CALLE_t DOSPUNT STRING '''
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

#PAIS, CALLE, CIUDAD
def p_OBJ_DIR4(p):
    ''' OBJ_DIR : PAIS_t DOSPUNT STRING COMA CALLE_t DOSPUNT STRING COMA CIUDAD_t DOSPUNT STRING '''
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

#PAIS, CIUDAD, CALLE
def p_OBJ_DIR5(p):
    ''' OBJ_DIR : PAIS_t DOSPUNT STRING COMA CIUDAD_t DOSPUNT STRING COMA CALLE_t DOSPUNT STRING ''' 
    p[0] = f"{p[3]}, {p[7]}, {p[11]}"

def p_LISTA_INTEGRANTES(p):
    '''LISTA_INTEGRANTES : LLAVEIZQ OBJ_INT LLAVEDER COMA LISTA_INTEGRANTES'''
    p[0] = p[2] + p[5] 

def p_LISTA_INTEGRANTES1(p):
    '''LISTA_INTEGRANTES : LLAVEIZQ OBJ_INT LLAVEDER'''
    p[0] = p[2]  

def p_OBJ_INT(p):
    '''OBJ_INT : NOMBRE_t DOSPUNT STRING COMA OPCIONAL_EDAD CARGO_t DOSPUNT TIPOC COMA FOTO_t DOSPUNT URL_t COMA EMAIL_t DOSPUNT CORREO_t COMA HABILIDADES_t DOSPUNT STRING COMA SALARIO_t DOSPUNT FLOAT COMA ACTIVO_t DOSPUNT BOOL_t'''
    #HTML------------------------------------------------------
    nombre = p[3]
    edad = p[5]
    cargo = p[8]
    foto = p[12]
    email = p[16]
    habilidades = p[20]
    salario = p[24]
    activo = p[28]

    p[0] = f'''<li><strong>{nombre}</strong> - {edad} - {cargo} - {email} - {habilidades} - {salario} - {activo}<br><img src="{foto}" alt="Foto de {nombre}" style="width:100px; height:auto;"><br></li>'''
    
def p_OPCIONAL_EDAD_CON(p):
    '''OPCIONAL_EDAD : EDAD_t DOSPUNT INTEGER COMA'''
    p[0] = f"Edad: {p[3]}"

def p_OPCIONAL_EDAD_SIN(p):
    '''OPCIONAL_EDAD : '''
    p[0] = ""

def p_LISTA_PROYECTOS(p):
    '''LISTA_PROYECTOS : LLAVEIZQ OBJ_PRO LLAVEDER COMA LISTA_PROYECTOS'''
    p[0] = p[2] + p[5] 

def p_LISTA_PROYECTOS1(p):
    '''LISTA_PROYECTOS : LLAVEIZQ OBJ_PRO LLAVEDER'''
    p[0] = p[2]               

def p_OBJ_PROVN(p):
    ''' OBJ_PRO : NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[3]
    estado = p[7]
    resumen = p[11]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_OBJ_PROVN1(p):
    ''' OBJ_PRO : NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[3]
    estado = p[11]
    resumen = p[7]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_OBJ_PROVE(p):
    ''' OBJ_PRO : ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[7]
    estado = p[3]
    resumen = p[11]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_OBJ_PROVE1(p):
    ''' OBJ_PRO : ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[11]
    estado = p[3]
    resumen = p[7]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_OBJ_PROVR(p):
    ''' OBJ_PRO : RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[7]
    estado = p[11]
    resumen = p[3]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_OBJ_PROVR1(p):
    ''' OBJ_PRO : RESUMEN_t DOSPUNT STRING COMA  ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING COMA TAREAS_t DOSPUNT CORCHIZQ LISTA_TAREAS CORCHDER COMA FECHA_INICIO_t DOSPUNT FECHA COMA FECHA_FIN_t DOSPUNT FECHA COMA VIDEO_t DOSPUNT URL_t COMA CONCLUSION_t DOSPUNT STRING'''
    #HTML-------------------------------------------------------
    nombre = p[11]
    estado = p[7]
    resumen = p[3]
    tareas = p[16]
    fecha_inicio = p[21]
    fecha_fin = p[25]
    video = p[29]
    conclusion = p[33]

    p[0] = f"<h3>{nombre}</h3><p><strong>Estado:</strong>{estado}</p><p><strong>Resumen:</strong>{resumen}</p><p><strong>Tareas:</strong>{tareas}</p><p><strong>Fecha Inicio:</strong>{fecha_inicio}</p><p><strong>Fecha Fin:</strong>{fecha_fin}</p><p><strong>Video:</strong><a href='{video}'>{video}</a></p><p><strong>Conslusión:</strong>{conclusion}</p>"

def p_LISTA_TAREAS(p):
    '''LISTA_TAREAS : LLAVEIZQ OBJ_TARE LLAVEDER COMA LISTA_TAREAS'''
    p[0] = p[2] + p[5] 

def p_LISTA_TAREAS1(p):
    '''LISTA_TAREAS : LLAVEIZQ OBJ_TARE LLAVEDER'''
    p[0] = p[2] 

#NOMBRE_TARE, ESTADO_TARE, RESUMEN_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVN(p):
    '''OBJ_TARE : NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[3]}</td><td>{p[7]}</td><td>{p[11]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''

#NOMBRE_TARE, ESTADO_TARE, RESUMEN_TARE, FECHA_INICIO,
def p_OBJ_TAREVN1(p):
    '''OBJ_TARE : NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[3]}</td><td>{p[7]}</td><td>{p[11]}</td><td>{p[12]}</td></tr></table>'''

#NOMBRE_TARE, RESUMEN_TARE, ESTADO_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVN2(p):
    '''OBJ_TARE : NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[3]}</td><td>{p[11]}</td><td>{p[7]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''

#NOMBRE_TARE, RESUMEN_TARE, ESTADO_TARE, FECHA_INICIO,
def p_OBJ_TAREVN3(p):
    '''OBJ_TARE : NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[3]}</td><td>{p[11]}</td><td>{p[7]}</td><td>{p[12]}</td></tr></table>'''

#RESUMEN_TARE, NOMBRE_TARE, ESTADO_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVR(p):
    '''OBJ_TARE : RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[7]}</td><td>{p[11]}</td><td>{p[3]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''
#RESUMEN_TARE, NOMBRE_TARE, ESTADO_TARE, FECHA_INICIO
def p_OBJ_TAREVR1(p):
    '''OBJ_TARE : RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[7]}</td><td>{p[11]}</td><td>{p[3]}</td><td>{p[12]}</td></tr></table>'''

#RESUMEN_TARE, ESTADO_TARE, NOMBRE_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVR2(p):
    '''OBJ_TARE : RESUMEN_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[11]}</td><td>{p[7]}</td><td>{p[3]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''

#RESUMEN_TARE, ESTADO_TARE, NOMBRE_TARE, FECHA_INICIO, 
def p_OBJ_TAREVR3(p):
    '''OBJ_TARE : RESUMEN_t DOSPUNT STRING COMA ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[11]}</td><td>{p[7]}</td><td>{p[3]}</td><td>{p[12]}</td></tr></table>'''


# ESTADO_TARE, RESUMEN_TARE, NOMBRE_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVE(p):
    '''OBJ_TARE : ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[11]}</td><td>{p[3]}</td><td>{p[7]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''

# ESTADO_TARE, RESUMEN_TARE, NOMBRE_TARE, FECHA_INICIO|
def p_OBJ_TAREVE1(p):
    '''OBJ_TARE : ESTADO_t DOSPUNT ESTADOPROY COMA RESUMEN_t DOSPUNT STRING COMA NOMBRE_t DOSPUNT STRING OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[11]}</td><td>{p[3]}</td><td>{p[7]}</td><td>{p[12]}</td></tr></table>'''


# ESTADO_TARE, NOMBRE_TARE, RESUMEN_TARE, FECHA_INICIO, FECHA_FIN|
def p_OBJ_TAREVE2(p):
    '''OBJ_TARE : ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING OPCIONAL_FECHA_INICIO OPCIONAL_FECHA_FIN'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[7]}</td><td>{p[3]}</td><td>{p[11]}</td><td>{p[12]}</td><td>{p[13]}</td></tr></table>'''

# ESTADO_TARE, NOMBRE_TARE, RESUMEN_TARE, FECHA_INICIO
def p_OBJ_TAREVE3(p):
    '''OBJ_TARE : ESTADO_t DOSPUNT ESTADOPROY COMA NOMBRE_t DOSPUNT STRING COMA RESUMEN_t DOSPUNT STRING OPCIONAL_FECHA_INICIO'''
    #HTML------------------------------------------------------
    p[0] = f'''<table border="1"><tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Inicio</th><th>Fin</th></tr>
    <tr><td>{p[7]}</td><td>{p[3]}</td><td>{p[11]}</td><td>{p[12]}</td></tr></table>'''



def p_OPCIONAL_FECHA_FIN_CON(p):
    '''OPCIONAL_FECHA_FIN : COMA FECHA_FIN_t DOSPUNT FECHA '''
    p[0] = p[4]

def p_OPCIONAL_FECHA_FIN_SIN(p):
    '''OPCIONAL_FECHA_FIN : COMA FECHA_FIN_t DOSPUNT NULL_t'''
    p[0] = "" 

def p_OPCIONAL_FECHA_FIN_VACIO(p):
    '''OPCIONAL_FECHA_FIN : COMA FECHA_FIN_t DOSPUNT
                          | COMA FECHA_FIN_t DOSPUNT STRING'''
    # Si el string está vacío, lo toma como null
    if len(p) == 4 or (len(p) == 5 and p[4].strip() == ""):
        p[0] = ""
    else:
        p[0] = p[4]
    
def p_OPCIONAL_FECHA_INICIO_CON(p):
    '''OPCIONAL_FECHA_INICIO : COMA FECHA_INICIO_t DOSPUNT FECHA '''
    p[0] = p[4] 

def p_OPCIONAL_FECHA_INICIO_SIN(p):
    '''OPCIONAL_FECHA_INICIO : COMA FECHA_INICIO_t DOSPUNT NULL_t'''
    p[0] = ""

def p_OPCIONAL_FECHA_INICIO_VACIO(p):
    '''OPCIONAL_FECHA_INICIO : COMA FECHA_INICIO_t DOSPUNT
                             | COMA FECHA_INICIO_t DOSPUNT STRING'''
    if len(p) == 4 or (len(p) == 5 and p[4].strip() == ""):
        p[0] = ""
    else:
        p[0] = p[4]


#Control de errores
def obtener_linea_con_error(posicion, archivo=None, contenido=None):
    if archivo is not None:
        with open(archivo, 'r', encoding='utf-8') as file:
            suma_caracteres = 0
            for linea in file:
                suma_caracteres += len(linea) + 1  # acumula en suma_caracteres, +1 para contar el caracter de nueva linea
                if suma_caracteres >= posicion:
                    pos_error = posicion - (suma_caracteres - len(linea) - 1)
                    return linea, pos_error
        return None, -1
    elif contenido is not None:
        suma_caracteres = 0
        for linea in contenido.splitlines(True):
            suma_caracteres += len(linea)
            if suma_caracteres >= posicion:
                pos_error = posicion - (suma_caracteres - len(linea))
                return linea, pos_error
        return None, -1
    else:
        return None, -1

def encontrar_linea(posicion, archivo=None, contenido=None):
    if archivo is not None:
        with open(archivo, 'r', encoding='utf-8') as file:
            suma_caracteres = 0
            linea_num = 0
            for linea in file:
                linea_num += 1
                suma_caracteres += len(linea) + 1
                if suma_caracteres >= posicion:
                    return linea_num
        return -1
    elif contenido is not None:
        suma_caracteres = 0
        linea_num = 0
        for linea in contenido.splitlines(True):
            linea_num += 1
            suma_caracteres += len(linea)
            if suma_caracteres >= posicion:
                return linea_num
        return -1
    else:
        return -1

def get_expected_tokens(parser):
    state = parser.statestack[-1]   # lo pone en la ultima posicion que parseo
    expected_tokens = []            # lo pone en vacio, almacenará los tokens que el analizador sintáctico usara
    for token, action in parser.action[state].items():
        if isinstance(action, int) and action > 0:  
            expected_tokens.append(token)             # el token si es aceptado se agrega a la lista 
    return expected_tokens          #devuelve la lista, que contiene todos los tokens que el analizador espera en el estado actual.


# Lista global para acumular errores
errores_sintacticos = []

def p_error(p):
    global archivo_actual, okay, _contenido_memoria, errores_sintacticos
    if p:
        if archivo_actual is not None:
            linea = encontrar_linea(p.lexpos, archivo_actual)
            linea_contenido, pos_error = obtener_linea_con_error(p.lexpos, archivo_actual)
        else:
            linea = encontrar_linea(p.lexpos, contenido=_contenido_memoria)
            linea_contenido, pos_error = obtener_linea_con_error(p.lexpos, contenido=_contenido_memoria)
        expected_tokens = get_expected_tokens(parser)
        expected_tokens_str = ', '.join(expected_tokens) if expected_tokens else "Desconocidos"
        error_msg = (
            f"Error de sintaxis por token no esperado '{p.type}', valor '{p.value}' en la línea {linea}, posición {p.lexpos}.\n"
            f"Se esperaban los tokens: {expected_tokens_str}\n"
            f"{linea_contenido.rstrip()}\n"
            f"{' ' * pos_error}^")
        errores_sintacticos.append(error_msg)
        print(error_msg)  # Ahora también imprime el error en la salida estándar
        okay = False
        parser.errok()
    else:
        if not okay:
            error_msg = "Error de sintaxis: Fin del archivo inesperado."
            errores_sintacticos.append(error_msg)
            print(error_msg)  # También imprime este error

            
# PARSER Y FLUJO PRINCIPAL
import ply.yacc as yacc
import logging

log = logging.getLogger()
hdlr = logging.FileHandler("parser_warnings.log")
log.addHandler(hdlr)

parser = yacc.yacc(errorlog=log)

lexer  = lex.lex(module=analizador_lexico)


# ---------- función auxiliar ----------
def procesar_archivo(ruta_archivo: str) -> None:
    """Lee, parsea y genera el .html a partir de `ruta_archivo`.
    Acepta rutas absolutas o relativas (a la carpeta del script)."""
    global archivo_actual, html_result, okay, xd
    ruta = pathlib.Path(ruta_archivo.strip('"')).expanduser()
    if not ruta.is_absolute():
        ruta = pathlib.Path(__file__).parent / ruta  # relativa al script
    
    archivo_actual = ruta

    try:
        with codecs.open(ruta, "r", "utf-8") as fp:
            contenido = fp.read()
    except FileNotFoundError:
        print(f"❌ No se ha encontrado el archivo: {ruta}")
        return
    okay = True
    html_result = ""
    resultado = parser.parse(contenido, lexer=lexer) # parsea el contenido del archivo
    html_code = resultado or html_result            # usa lo que realmente devuelva tu gramática
    salida_html = ruta.with_suffix(".html")
    import tkinter.messagebox as messagebox

    if okay:
        with open(salida_html, "w", encoding="utf-8") as f:
            f.write(html_code)    
        messagebox.showinfo("Éxito", f"HTML generado: {salida_html}")
        if messagebox.askyesno("Abrir HTML", "¿Desea abrir el archivo HTML generado?"):
                webbrowser.open_new(salida_html.as_uri())
    else:
        messagebox.showwarning("Error", f"⚠️  HTML NO generado por errores de sintaxis.\nRevisa los errores en la consola.")



# ---------- MAIN ----------
'''def main() -> None:
    # 1) ¿Vino argumento en la línea de comandos?
    if len(sys.argv) > 1:
        procesar_archivo(sys.argv[1])
        return
    # 2) Modo interactivo (opcional)
    while True:
        print("Seleccione una opción:")
        print("1) Ingresar la RUTA del documento (.json o .txt)")
        print("2) Salir")
        opcion = input("Opción: ").strip()
        if opcion == "2":
            break
        if opcion != "1":
            print("⚠️  Opción no válida\n")
            continue
        ruta = input("Ruta del documento: ")
        procesar_archivo(ruta)

if __name__ == "__main__":
    #ain()'''
