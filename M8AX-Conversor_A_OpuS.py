"""
Este Programa Permite Comprimir Archivos De Música En Formato OPUS. 
El Usuario Puede Elegir La Carpeta De Origen, Que Puede Contener 
Varias Carpetas Con Música En Diferentes Formatos ( MP3, AAC, WAV, 
OGG, M4A, Etc... ). El Programa Recorrerá Todas Las Carpetas De La 
Carpeta De Origen Y Creará La Misma Jerarquía En La Carpeta De 
Salida, Pero Con Los Archivos Ya Comprimidos En OPUS. Además, 
Detectará Los Núcleos De Tu CPU Y Te Preguntará Cuántos Usar Para 
Realizar La Compresión De Manera Más Rápida.

Se Puede Configurar El Bitrate Máximo Y Mínimo Para La Compresión, 
Así Como La Opción De Activar O Desactivar El Variable Bit Rate ( VBR ). 
El Usuario También Puede Elegir Convertir El Audio A Estéreo O A Mono, 
Así Como Seleccionar La Frecuencia De Muestreo Deseada. Los Archivos 
Generados Incluirán Metatags Para Mejorar La Organización Y La 
Identificación De La Música Comprimida ( "Para Mí" ). Se Puede Elegir 
Si Incluirlos O No. ( Incluye Portada Con Código QR Si Queremos )...

Además, Se Puede Normalizar El Audio, Hacer Que Las Canciones Se 
Escuchen Al Revés, Añadir Eco A Las Canciones, Aumentar Los Graves, 
Aumentar Los Agudos, Aumentar O Reducir El Volumen, Subir El Tono, 
Convertir El Audio A 8D Con O Sin Eco ( Que Es El Audio 3D De Toda 
La Vida ) Y Aumentar O Reducir La Velocidad De Reproducción.

También Se Puede Crear Un Espectrograma De Cada Canción En JPG, 
Si Así Lo Decidimos, Con Los Canales Izquierdo Y Derecho De Audio 
Separados. Además, Se Puede Crear Un JPG Con Los Canales Izquierdo 
Y Derecho De Cada Canción Con Su WaveForm Y Por Si Fuera Poco, Se
Pueden Crear Videos De Cada Canción, Con Cada Canción Incluida Y
Su WaveForm Animado Sin Filtros Y Codificado Con Codec H265 + OPUS
Que Claro Está, Va Al Ritmo De La Música...

Programador: MarcoS OchoA DieZ ( Alias: M8AX ) 
Fecha De Programación: 20 De Octubre De 2024 - Domingo - 00:00
Duración De Programación: 6.5h
Dispositivo Utilizado: MvIiIaX - Xiaomi MI 9 Lite ( TerMuX Con PyThoN ) 
Código Formateado Con: BlacK
"""

import os
import time
import re
import random
import subprocess
import qrcode
import shutil
import requests
import hashlib
import base64
import urllib.parse
import multiprocessing
from urllib.parse import urlparse
from concurrent.futures import ProcessPoolExecutor
from sympy import factorint
from mutagen.oggopus import OggOpus
from mutagen.flac import Picture
from mutagen import File
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from io import BytesIO

ffmpeg_cmd_string = ""
mviiiax = multiprocessing.Value("i", 0)  # 'i' Significa Nº Entero

# Comprobar Dirección Web Válida


def es_direccion_web_valida(direccion):
    resultado = urlparse(direccion)
    return all([resultado.scheme, resultado.netloc])


# Pedir Dirección URL Directa A Imágen


def solicitar_direccion_web():
    direccion_default = "https://yt3.googleusercontent.com/ytc/AIdro_kbQO4N_i3ddLrouqOb1lhgx72WQITlLn6t2D1WaSR29Q=s900-c-k-c0x00ffffff-no-rj"
    while True:
        direccion = input(
            "\nM8AX - Introduce Una Dirección Web, Que Apunte A Un Fichero Gráfico, jpg, bmp, png, webp, Etc... Para Añadir La Imágen Al Código QR. ( Deja Vacío Para Usar URL Con Tu Logo ): "
        )

        if not direccion:  # Si Está Vacío, Usar La Dirección Por Defecto
            return direccion_default

        if es_direccion_web_valida(direccion):
            return direccion
        else:
            print(
                "\nM8AX - La Dirección Web No Es Válida. Por Favor, Inténtalo De Nuevo."
            )


# Descargar Imágen Dada Una URL


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Lanza Un Error Si La Respuesta No Es 200
    img = Image.open(BytesIO(response.content))

    # Guardar La Imagen Como PNG

    img.save("m8ax.png", "PNG")


# Calcula El Hash SHA-256 De Un Archivo


def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Factoriza Número Aleatorio De 25 Cifras... Tontería Para Los Metadatos... ( Propia De Mí, Pero Me Identifica. )


def generar_y_factorizar():
    max_cifras = 25

    numero = random.randint(10 ** (max_cifras - 1), 10**max_cifras - 1)

    # Factorizar El Número

    factores = factorint(numero)

    # Construir La Cadena De Descomposición

    descomposicion = " * ".join(
        [f"{p}^{e}" if e > 1 else str(p) for p, e in factores.items()]
    )

    # Formatear La Salida

    resultado = f"M8AX - Número: 🔢 {numero} 🔢, Descompuesto En Factores Primos Es: ( ▶︎ {descomposicion} ◀︎ )."

    return resultado


# Fecha A Mi Gusto


def obtener_fecha_formateada():
    # Diccionarios Para Traducir Días Y Meses Al Español

    dias_semana = {
        0: "Lunesito",
        1: "Martesito",
        2: "Miércolesito",
        3: "Juevesito",
        4: "Viernesito",
        5: "Sábadocito",
        6: "Dominguito",
    }

    meses = {
        1: "Enerito",
        2: "Febrerito",
        3: "Marzito",
        4: "Abrilito",
        5: "Mayito",
        6: "Junito",
        7: "Julito",
        8: "Agostito",
        9: "Septiembrito",
        10: "Octubrito",
        11: "Noviembrito",
        12: "Diciembrito",
    }

    # Obtener La Fecha Y Hora Actual

    fecha_actual = datetime.now()

    # Obtener Los Componentes Traducidos De La Fecha

    dia_semana = dias_semana[
        fecha_actual.weekday()
    ]  # Obtener El Día De La Semana Como Índice (0=Lunes)
    mes = meses[fecha_actual.month]  # Obtener El Mes Usando El Número Del Mes

    # Formatear La Fecha En El Formato Requerido

    fecha_formateada = f"El {dia_semana}, {fecha_actual.day} De {mes} De {fecha_actual.year} A Las {fecha_actual.strftime('%H:%M:%S')}"

    return fecha_formateada


# Función Para Recibir Una Imágen Y Grabar Otra Con Modificaciones


def add_text_to_image(input_image_path, output_image_path, text):
    # Abrir La Imágen

    with Image.open(input_image_path) as img:
        # Obtener Las Dimensiones De La Imágen Original

        width, height = img.size

        # Crear Una Nueva Imágen Con Espacio Adicional Para El Texto

        new_height = height + 80  # Aumentar La Altura En 80 Píxeles
        new_img = Image.new("RGB", (width, new_height), color="black")

        # Pegar La Imágen Original En La Nueva Imágen

        new_img.paste(img, (0, 0))

        # Crear Un Objeto Para Dibujar

        draw = ImageDraw.Draw(new_img)

        # Usar Una Fuente Por Defecto

        font_size = 20
        font = ImageFont.load_default()

        # Dibujar El Texto Centrado

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((width - text_width) // 2, height + (80 - text_height) // 2)

        # Dibujar El Texto

        draw.text(text_position, text, font=font, fill="white")

        # Guardar La Imágen Resultante

        new_img.save(output_image_path)


# Función Para Limpiar La Pantalla


def clear_screen():
    if os.name == "nt":  # Para Windows
        subprocess.run("cls", shell=True)
    else:  # Para Unix/Linux/Mac
        subprocess.run("clear")


# Función Para Solicitar Si Convertir A Mono O A Estéreo, Sin Cambiar Si Se Deja Vacío


def ask_for_audio_channels():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Convertir El Audio A Mono O A Estéreo ? ( Escribe 'mono' O 'stereo', O Presiona Enter Para Mantener Los Canales Originales ): "
            )
            .strip()
            .lower()
        )

        # Si El usuario No Ingresa Nada, No Cambia Los Canales

        if not choice:
            return None  # Indica Que Se Debe Mantener La Configuración Original

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["mono", "stereo"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'mono' O 'stereo'...")


# Función Para Solicitar Paneo Dinámico


def ask_for_paneo():
    alehz = 0
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Un Paneo Dinámico Para Todas Las Canciones ?, ale Implica Si, Pero La Duración Del Paneo Será Aleatoria En Cada Canción De 33s A 8s... ( Escribe 'si', 'no' O 'ale' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no", "ale"]:
            if choice == "ale":
                alehz = 1
            else:
                alehz = 0
            return choice, alehz
        else:
            print("\nM8AX - Error: Debes Escribir 'si', 'no' O 'ale' ...")


# Función Para Solicitar Si Aumentamos El Tono


def ask_for_tono():
    while True:
        choice = (
            input("\nM8AX - ¿ Deseas Aumentar El Tono ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Creamos Espectrograma


def ask_for_espec():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Que Se Creen Espectrogramas De Cada Canción, Con 2 Gráficas En Cada JPG, Una Para El Canal Izquierdo Y Otra Para El Derecho ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Creamos WaveForms


def ask_for_ondas():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Que Se Creen WaveForms De Cada Canción, Con 2 Gráficas En Cada JPG, Una Para El Canal Izquierdo Y Otra Para El Derecho ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Creamos Videos Con WaveForms Animados


def ask_for_video():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Que Se Creen Videos Con WaveForms Animados De Cada Canción Con Título Y Audio Incluido ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Eco En Paneo Dinámico


def ask_for_ecopane():
    while True:
        choice = (
            input("\nM8AX - ¿ Eco En Paneo Dinámico ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Añadimos MetaTags


def ask_for_meta():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Añadir MetaTags A Las Canciones ? si = Añade MetaTags no = Deja Como Están... ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Añadimos Código QR A Metadata Como Portada


def ask_for_qr():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Añadir Código QR Como Portada De Las Canciones ? si = Añade QRCODE no = No Lo Añade... ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Aumentamos Los Graves


def ask_for_graves():
    while True:
        choice = (
            input("\nM8AX - ¿ Deseas Aumentar Los Graves ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Aumentamos Los Agudos


def ask_for_agudos():
    while True:
        choice = (
            input("\nM8AX - ¿ Deseas Aumentar Los Agudos ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Añadimos Eco A Las Canciones


def ask_for_eco():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Añadir Eco A Las Canciones ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Normalizamos Cada Canción


def ask_for_normal():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Deseas Que Las Canciones Sean Normalizadas ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Queremos Que Las Canciones Se Escuchen Al Revés, ( REVERSE )


def ask_for_reverse():
    while True:
        choice = (
            input(
                "\nM8AX - ¿ Quieres Que Cada Canción Se Escuche Al Revés ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("\nM8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar La Frecuencia De Muestreo, 0 Para Dejar La Original


def ask_for_sample_rate(default_rate=0):
    sample_rates = ["0", "8000", "12000", "16000", "24000", "48000"]
    print(f"\nM8AX - Frecuencias De Muestreo Disponibles: {', '.join(sample_rates)} Hz")

    while True:
        user_input = input(
            "\nM8AX - Por Favor, Elige Una Frecuencia De Muestreo, ( 0 - Para Dejar La Original Del Fichero A Convertir ): "
        )
        if user_input in sample_rates:
            return user_input
        else:
            print("\nM8AX - Frecuencia No Válida, Inténtalo De Nuevo...")


# Función Para Solicitar Aumento O Reducción De Volumen


def ask_for_volume():
    while True:
        entrada = input(
            "\nM8AX - Por Favor, Introduce Un Aumento O Reducción De Volumen.\n\n"
            "Silencio (0): Un Valor De 0 Significa Que El Audio Se Silenciará Completamente.\n\n"
            "Volumen Original (1): Un Valor De 1 Representa El Volumen Original Sin Cambios.\n\n"
            "Aumento: Los Valores Mayores Que 1 Aumentan El Volumen. Por Ejemplo, Un Valor De 2 Duplica El Volumen.\n\n"
            "Reducción: Los Valores Entre 0 Y 1 Reducen El Volumen. Por Ejemplo, 0.5 Reduce El Volumen A La Mitad.\n\n"
            "M8AX - Introduce Un Número, Puede Tener Decimales: "
        )

        try:
            numero = float(entrada)
            jox = 0
            if numero >= 0:
                jox = "si"
                return numero, jox
            else:
                print("\nM8AX - Debes Introducir Un Número Mayor O Igual A 0...")
        except ValueError:
            print(
                "\nM8AX - Entrada No Válida. Asegúrate De Introducir Un Número Válido..."
            )


# Función Para Preguntar El Número De Núcleos A Usar En La Compresión De Audio


def ask_for_cores():
    while True:
        entrada = input(
            "\nM8AX- Introduce El Número De Núcleos A Usar En La Compresión A OPUS... Cuantos Más Núcleos Tenga Tu CPU, Más Rápido Terminará El Proceso, A Cada Core Se Le Asignará A Comprimir Una Canción. ¿ Cuántos Núcleos Usamos ?: "
        )

        try:
            xnum_coress = int(entrada)
            if xnum_coress >= 1:
                return xnum_coress
            else:
                print("M8AX - Debes Introducir Un Número Mayor O Igual A 1...")
        except ValueError:
            print(
                "M8AX - Entrada No Válida. Asegúrate De Introducir Un Número Válido..."
            )


# Función Para Solicitar La Velocidad


def ask_for_speed_rate(default_rate=float(1)):
    atempo_values = [
        "0.5",
        "0.55",
        "0.6",
        "0.65",
        "0.7",
        "0.75",
        "0.8",
        "0.85",
        "0.9",
        "0.95",
        "1.0",
        "1.05",
        "1.1",
        "1.15",
        "1.2",
        "1.25",
        "1.3",
        "1.35",
        "1.4",
        "1.45",
        "1.5",
        "1.55",
        "1.6",
        "1.65",
        "1.7",
        "1.75",
        "1.8",
        "1.85",
        "1.9",
        "1.95",
        "2.0",
    ]

    print(f"\nM8AX - Velocidades Disponibles: {', '.join(atempo_values)} X")

    while True:
        user_input = input(
            "\nM8AX - Por Favor, Elige Una Velocidad, ( 1.0 - Para Dejar La Velocidad Original Del Fichero A Convertir ): "
        )
        if user_input in atempo_values:
            return float(user_input)
        else:
            print("\nM8AX - Velocidad No Válida, Inténtalo De Nuevo...")


# Aumentar Variable mviiiax En 1


def modificar_variable():
    # Modificar La Variable Compartida

    with mviiiax.get_lock():  # Aseguramos Que Solo Un Proceso Acceda A La Variable A La Vez
        mviiiax.value += 1


# Función Para Convertir Archivos A OPUS Usando FFmpeg


def convert_to_opus(file_path):
    relative_path = os.path.relpath(file_path, input_dir)
    output_file_path = os.path.join(
        output_dir, relative_path.rsplit(".", 1)[0] + ".opus"
    )
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Calcular HASH SHA-256 Del Fichero De Audio Original M8AXHash256AudioOriginalM8AX

    hash_value = calculate_hash(file_path)

    # Comando Para Convertir A OPUS Con Metadatos

    current_time = obtener_fecha_formateada() + " ⌚ "
    current_time += datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        file_path,
        "-ar",
        sample_rate,  # Frecuencia De Muestreo Elegida
        "-c:a",
        "libopus",
        "-b:a",
        f"{max_bitrate}k",  # Tasa De Bits Máxima
        "-minrate",
        f"{min_bitrate}k",  # Tasa De Bits Mínima
        "-vbr",
        vbr,
        "-compression_level",
        "10",
    ]

    # Agregar Configuración De Canales Solo Si Se Especifica

    if audio_channels == "mono":
        ffmpeg_cmd += [
            "-ac",
            "1",
        ]  # Conversión A Mono
    elif audio_channels == "stereo":
        ffmpeg_cmd += [
            "-ac",
            "2",
        ]  # Conversión A Estéreo

    # Hacer Que Las Canciones Se Escuchen Al Revés

    if hayreverse == "si":
        ffmpeg_cmd += [
            "-af",
            "areverse",
        ]  # Hacemos Que Se Escuche Al Revés

    # Normalizar Cada Canción Al Pasarla A OPUS

    if normalizar == "si":
        ffmpeg_cmd += [
            "-af",
            "loudnorm",
        ]  # Normalizar

    # Agregar Eco Al Pasar A OPUS

    if hayeco == "si":
        ffmpeg_cmd += [
            "-af",
            "aecho=0.8:0.88:60:0.4",
        ]  # Agregar Eco

    # Aumentar Los Graves

    if haygraves == "si":
        ffmpeg_cmd += [
            "-af",
            "equalizer=f=100:t=q:w=1:g=7",
        ]  # Aumentar Graves

    # Aumentar Los Agudos

    if hayagudos == "si":
        ffmpeg_cmd += [
            "-af",
            "equalizer=f=10000:t=q:w=1:g=7",
        ]  # Aumentar Agudos

    # Aumentar El Tono

    if haytono == "si":
        ffmpeg_cmd += [
            "-af",
            "asetrate=44100*1.5",
        ]  # Aumentar Tono

    # Paneo Dinámico

    if alehz == 1:
        hz_value = random.uniform(0.03, 0.15)
    else:
        hz_value = 0.1

    if haypaneo == "si" or haypaneo == "ale":
        if paneco == "si":
            ffmpeg_cmd += [
                "-af",
                f"apulsator=mode=sine:hz={hz_value:.2f}:amount=0.90, aecho=0.8:0.4:150:0.4",
            ]  # Paneo Dinámico Con Eco
        else:
            ffmpeg_cmd += [
                "-af",
                f"apulsator=mode=sine:hz={hz_value:.2f}:amount=0.90",
            ]  # Paneo Dinámico Sin Eco

    # Aumentar O Reducir La Velocidad De La Canción

    if all(
        [
            normalizar == "no",
            hayreverse == "no",
            hayeco == "no",
            haygraves == "no",
            hayagudos == "no",
            haytono == "no",
            haypaneo == "no",
            jox == "no",
            velocidad != float(1),
        ]
    ):

        ffmpeg_cmd += [
            "-filter:a",
            f"atempo={velocidad}",  # Velocidad
        ]

    # Subir O Bajar Volumen

    if jox == "si" and volumencillo != 1:
        ffmpeg_cmd += [
            "-filter:a",
            f"volume={volumencillo}",  # Ajuste De Volumen
        ]

    # Agregar MetaTags

    if metetag == "si":
        ffmpeg_cmd += [
            "-metadata",
            f"episode_id=ORIGEN - {os.path.basename(file_path)} | DESTINO - {os.path.basename(output_file_path)}",  # ID Del Episodio
            "-metadata",
            r"copyright=-///📷\\\ --- MvIiIaX & M8AX 2025 - 2050 --- ///📷\\\-",  # Copyright
            "-metadata",
            r"artist=-///🎹\\\ --- ░M░A░R░C░O░S░ --- ///🎹\\\-",  # Artist
            "-metadata",
            r"album=-///🎸\\\ --- ＊*•̩̩͙✩•̩̩͙*˚ᛖ𝐯ᎥᎥᎥⱥx*•̩̩͙✩•̩̩͙*˚＊ --- ///🎸\\\-",  # Album
            "-metadata",
            r"genre=-///₿\\\ --- | ★ https://oncyber.io/@m8ax ★ | --- ///₿\\\-",  # Género
            "-metadata",
            r"MarcosOchoaDiez=🧑‍💻 🢂 @-📱-@ Programar No Es Solo Resolver Problemas, Es Transformar Ideas En Soluciones Que Cambian El Mundo... @-📱-@ 🢀 💻🧑‍",  # MarcosOchoaDiez
            "-metadata",
            r"MvIiIaX=----- | ★ https://opensea.io/es/m8ax ★ | -----",  # NFTS
            "-metadata",
            f"M8AXCompressionDate={current_time}",
            "-metadata",
            r"BitcoinWallet=-/// ⚡LeD⚡ \\\ - XXXXX - /// ⚡GeR⚡ \\\-",  # Wallet Bitcoin
            "-metadata",
            r"author=--- MarcoS OchoA DieZ -► ( ★ XXXXX ★, ★ XXXXX ★ ) ---",  # Autor
            "-metadata",
            r"show=Mi Canal De YouTube - ((( ★ http://youtube.com/m8ax ★ )))",  # Show
            "-metadata",
            r"grouping=Mi Blog - ((( ★ http://mviiiaxm8ax.blogspot.com ★ )))",  # Agrupación Blog
            "-metadata",
            r"comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El Futuro... No Está Establecido, No Hay Destino, Sólo Existe El Que Nosotros Hacemos... 3 - El Miedo Es El Camino Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al Sufrimiento... 4 - Música Compilada En Honor A MDDD...",  # Comentario
            "-metadata",
            r"M8AX=Yo He Visto Cosas Que Vosotros No Creeríais. Atacar Naves En Llamas Más Alla De Orión. He Visto Rayos-C Brillar En La Oscuridad Cerca De La Puerta De Tannhäuser. Todos Esos Momentos Se Perderán En El Tiempo, Como Lágrimas En La Lluvia. Es Hora De Morir...",  # Frase M8AX
            "-metadata",
            f"title={os.path.basename(output_file_path)}",  # Título
            "-metadata",
            f"ImoD=----- The Algorithm Man -► ( AND NOT OR ) ( E=MC^2 ) ( Ax=b ) -----",  # M8AX Programmer
            "-metadata",
            f"MvIiIaX_M8AX=Mi CPU Procesa En Red Neural, Es De Aprendizaje... Pero Skynet Solo Lee, Cuando Nos Envían Solos A Una Misión...",  # Frasecilla
            "-metadata",
            f"M8AX_MvIiIaX=No Soy Una Máquina, Ni Un Hombre. Soy Más...",  # Frasecilla
            "-metadata",
            r"handler_name=--- -🇪🇸- MarcoS OchoA DieZ -► ( M8AX ◀️👨‍💻▶️ MvIiIaX ) -🇪🇸- ---",  # Nombre Del Compresor
            "-metadata",
            f"EHD_MDDD=.•♫•♬•🔥Ｍ𝚟ıııคx🔥•♬•♫•. X∀8ꟽ ⌘•⌘ ꧁☆❤️🅼8🅰🆇❤️☆꧂ ⌘•⌘",  # M8AX Programmer EHDMDDD
            "-metadata",
            f"fingerprint=1003197777913001",  # M8AX FingerPrint
            "-metadata",
            f"M8AXHash256AudioOriginalM8AX={hash_value}",  # M8AX HASH SHA-256 Del Fichero De Audio Original
            "-metadata",
            f"GualoMajanDuchi=M2O-MAR-POR",  # RISAS
            "-metadata",
            r"ImoDTroN=Nunca Dejes Que Nadie Te Diga Que No Puedes Hacer Algo. Ni Siquiera Yo. Si Tienes Un Sueño, Tienes Que Protegerlo. Las Personas Que No Son Capaces De Hacer Algo Por Ellas Mismas, Te Dirán Que Tú Tampoco Puedes Hacerlo. ¿ Quieres Algo ? Ve Por Ello Y Punto...",  # Frasecilla
        ]

    # Agregar Espectrograma En Formato JPG, Título De La Cancion Incluido .opus.JpG

    if espec == "si":
        ffplay_cmd = [
            "ffmpeg",
            "-i",
            file_path,  # Archivo De Audio De Entrada
            "-lavfi",
            "showspectrumpic=s=800x400:scale=log:mode=separate",  # Filtro Para Generar El Espectrograma
            f"{output_file_path}.Espectrograma.JpG",  # Guardar El Espectrograma Como Imágen
        ]

    # Agregar WaveForms En Formato JPG, Título De La Cancion Incluido .opus.JpG

    if ondas == "si":
        ffplayo_cmd = [
            "ffmpeg",
            "-i",
            file_path,  # Archivo De Audio De Entrada
            "-lavfi",
            "showwavespic=split_channels=1:s=800x400",  # Filtro Para Generar La Forma De Onda Combinada
            f"{output_file_path}.Forma-De-Onda.JpG",  # Guardar La Forma De Onda Como Imágen
        ]

    # Hacer Video Con WaveForm Animada Al Ritmo De La Música Con Título De La Cancion + Audio .opus.Mp4

    cleaned_text = os.path.basename(output_file_path)
    cleaned_text = clean_text_for_drawtext(cleaned_text)

    if hacerv == "si":
        HacerVideo = [
            "ffmpeg",
            "-i",
            file_path,  # Archivo De Audio De Entrada
            "-ar",
            sample_rate,
            "-filter_complex",
            f"showwaves=s=1152x576:mode=cline[v];[0:a]anull[a];[v]drawtext=text='M8AX - {cleaned_text} - M8AX':fontcolor=white:fontsize=18:x=(w-text_w)/2:y=10[v]",  # Filtro Para Generar El Video De Ondas Y Añadir Texto
            "-map",
            "[v]",  # Mapea El Video Generado
            "-map",
            "[a]",  # Mapea El Audio
            "-c:v",
            "libx265",  # Codec De Video
            "-preset",
            "medium",
            "-b:v",
            "512k",
            "-maxrate",
            "1003k",
            "-bufsize",
            "2006k",
            "-pix_fmt",
            "yuv420p",  # Formato De Píxeles
            "-c:a",
            "libopus",  # Codec De Audio
            "-b:a",
            f"{max_bitrate}k",  # Tasa De Bits Para El Audio
            "-minrate",
            f"{min_bitrate}k",  # Tasa De Bits Mínima
            "-vbr",
            vbr,
            "-compression_level",
            "10",
        ]

    if hacerv == "si" and metetag == "si":
        HacerVideo += [
            "-metadata",
            f"episode_id=ORIGEN - {os.path.basename(file_path)} | DESTINO - {os.path.basename(output_file_path)}",  # ID Del Episodio
            "-metadata",
            r"copyright=-///📷\\\ --- MvIiIaX & M8AX 2025 - 2050 --- ///📷\\\-",  # Copyright
            "-metadata",
            r"artist=-///🎹\\\ --- ░M░A░R░C░O░S░ --- ///🎹\\\-",  # Artist
            "-metadata",
            r"album=-///🎸\\\ --- ＊*•̩̩͙✩•̩̩͙*˚ᛖ𝐯ᎥᎥᎥⱥx*•̩̩͙✩•̩̩͙*˚＊ --- ///🎸\\\-",  # Album
            "-metadata",
            r"genre=-///₿\\\ --- | ★ https://oncyber.io/@m8ax ★ | --- ///₿\\\-",  # Género
            "-metadata",
            r"MarcosOchoaDiez=🧑‍💻 🢂 @-📱-@ Programar No Es Solo Resolver Problemas, Es Transformar Ideas En Soluciones Que Cambian El Mundo... @-📱-@ 🢀 💻🧑‍",  # MarcosOchoaDiez
            "-metadata",
            r"MvIiIaX=----- | ★ https://opensea.io/es/m8ax ★ | -----",  # NFTS
            "-metadata",
            f"M8AXCompressionDate={current_time}",
            "-metadata",
            r"BitcoinWallet=-/// ⚡LeD⚡ \\\ - XXXXX - /// ⚡GeR⚡ \\\-",  # Wallet Bitcoin
            "-metadata",
            r"author=--- MarcoS OchoA DieZ -► ( ★ XXXXX ★, ★ XXXXX ★ ) ---",  # Autor
            "-metadata",
            r"show=Mi Canal De YouTube - ((( ★ http://youtube.com/m8ax ★ )))",  # Show
            "-metadata",
            r"grouping=Mi Blog - ((( ★ http://mviiiaxm8ax.blogspot.com ★ )))",  # Agrupación Blog
            "-metadata",
            r"comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El Futuro... No Está Establecido, No Hay Destino, Sólo Existe El Que Nosotros Hacemos... 3 - El Miedo Es El Camino Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al Sufrimiento... 4 - Video Compilado En Honor A MDDD...",  # Comentario
            "-metadata",
            r"M8AX=Yo He Visto Cosas Que Vosotros No Creeríais. Atacar Naves En Llamas Más Alla De Orión. He Visto Rayos-C Brillar En La Oscuridad Cerca De La Puerta De Tannhäuser. Todos Esos Momentos Se Perderán En El Tiempo, Como Lágrimas En La Lluvia. Es Hora De Morir...",  # Frase M8AX
            "-metadata",
            f"title={os.path.basename(output_file_path)}",  # Título
            "-metadata",
            f"ImoD=----- The Algorithm Man -► ( AND NOT OR ) ( E=MC^2 ) ( Ax=b ) -----",  # M8AX Programmer
            "-metadata",
            f"MvIiIaX_M8AX=Mi CPU Procesa En Red Neural, Es De Aprendizaje... Pero Skynet Solo Lee, Cuando Nos Envían Solos A Una Misión...",  # Frasecilla
            "-metadata",
            f"M8AX_MvIiIaX=No Soy Una Máquina, Ni Un Hombre. Soy Más...",  # Frasecilla
            "-metadata",
            r"handler_name=--- -🇪🇸- MarcoS OchoA DieZ -► ( M8AX ◀️👨‍💻▶️ MvIiIaX ) -🇪🇸- ---",  # Nombre Del Compresor
            "-metadata",
            f"EHD_MDDD=.•♫•♬•🔥Ｍ𝚟ıııคx🔥•♬•♫•. X∀8ꟽ ⌘•⌘ ꧁☆❤️🅼8🅰🆇❤️☆꧂ ⌘•⌘",  # M8AX Programmer EHDMDDD
            "-metadata",
            f"fingerprint=1003197777913001",  # M8AX FingerPrint
            "-metadata",
            f"M8AXHash256AudioOriginalM8AX={hash_value}",  # M8AX HASH SHA-256 Del Fichero De Audio Original
            "-metadata",
            f"GualoMajanDuchi=M2O-MAR-POR",  # RISAS
            "-metadata",
            r"ImoDTroN=Nunca Dejes Que Nadie Te Diga Que No Puedes Hacer Algo. Ni Siquiera Yo. Si Tienes Un Sueño, Tienes Que Protegerlo. Las Personas Que No Son Capaces De Hacer Algo Por Ellas Mismas, Te Dirán Que Tú Tampoco Puedes Hacerlo. ¿ Quieres Algo ? Ve Por Ello Y Punto...",  # Frasecilla
        ]

    if hacerv == "si":
        HacerVideo += [
            f"{output_file_path}.Mp4",  # Archivo De Salida
        ]

    # Agregar El Archivo De Salida Al Final Del Comando

    ffmpeg_cmd.append(output_file_path)  # Último Comando

    if mviiiax.value == 0:
        # Abro El Archivo En Modo Escritura

        with open("M8AX-Lista-FFmpeg.TxT", "w") as f:
            f.write(" ".join(ffmpeg_cmd))
            if espec == "si":
                f.write(
                    "\n\n-- M8AX - CADENA DE FFMPEG UTILIZADA PARA LA CREACIÓN DE ESPECTROGRAMAS - M8AX --\n\n"
                    + " ".join(ffplay_cmd)
                )
            if ondas == "si":
                f.write(
                    "\n\n---- M8AX - CADENA DE FFMPEG UTILIZADA PARA LA CREACIÓN DE WAVEFORMS - M8AX ----\n\n"
                    + " ".join(ffplayo_cmd)
                )
            if hacerv == "si":
                f.write(
                    "\n\n--- M8AX - CADENA DE FFMPEG UTILIZADA PARA LA CREACIÓN DE LOS VIDEOS - M8AX ---\n\n"
                    + " ".join(HacerVideo)
                )

    modificar_variable()

    # Ejecutar El Comando FFmpeg Para Crear Videos Con WaveForms Animados

    if hacerv == "si":
        result_videoo = subprocess.run(
            HacerVideo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="latin-1",
        )

    # Ejecutar El Comando FFmpeg Para Crear Espectrograma

    if espec == "si":
        result_ffplay = subprocess.run(
            ffplay_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="latin-1",
        )

    # Ejecutar El Comando FFmpeg Para Crear WaveForms

    if ondas == "si":
        result_ffplayo = subprocess.run(
            ffplayo_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="latin-1",
        )

    # Ejecutar El Comando FFmpeg Y Mostrar La Salida En Tiempo Real

    result = subprocess.run(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="latin-1",
    )

    # Mostrar La Salida De FFmpeg Y Beep De Fichero Procesado

    os.system("play -n synth 0.0050 sin 100 > /dev/null 2>&1")

    return result.stdout


# Función Para Obtener La Duración De Un Archivo De Audio


def get_audio_duration(file_path):
    audio = File(file_path)
    return audio.info.length  # Devuelve La Duración En Segundos


# Función Para Obtener El Tamaño De Un Archivo En MB


def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)


# Función Para Limpiar Cadena De Caracteres Extraños...


def clean_text_for_drawtext(text):
    # Eliminar Caracteres Que No Son Letras, Números O Espacios

    # Aquí Se Pueden Incluir Otros Caracteres Permitidos Según Sea Necesario

    return re.sub(r"[<>:\"/\\|?*[\]{}();%&$#@!^~`+=\-']", "", text)


# Función Para Solicitar Un Directorio Existente


def get_existing_directory(prompt):
    while True:
        directory = input(prompt).strip()
        if os.path.exists(directory):
            return directory
        else:
            print(
                f"\nM8AX - El Directorio '{directory}' No Existe. Por Favor, Verifica La Ruta...\n"
            )


# Comenzando

clear_screen()

normalizar = "no"
hayreverse = "no"
hayeco = "no"
haygraves = "no"
hayagudos = "no"
haytono = "no"
haypaneo = "no"
jox = "no"
volumencillo = 1
total_duration = 0
sumando = 0
velocidad = float(1)
hz_value = 0.1
alehz = 0
markitosfac = "No Se Ha Factorizado Nada, Ha Habido Errores Para Bajar Una Imágen De Internet Y Adornar El Código QR... Todo Lo Demás, Correcto."

print(f"--------  M8AX - PROGRAMA PARA CONVERTIR MÚSICA A FORMATO OPUS - M8AX --------")
print(f"")
os.system("play -n synth 0.0150 sin 7000 > /dev/null 2>&1")
input_dir = get_existing_directory(
    "M8AX - Introduce El Directorio De Origen ( Donde Están Los Archivos A Convertir ): "
)

# Solicitar Directorio De Destino Y Crearlo Si No Existe

output_dir = input(
    "\nM8AX - Introduce El Directorio De Destino ( Donde Se Guardarán Los Archivos Convertidos ): "
).strip()
os.makedirs(output_dir, exist_ok=True)

# Solicitar Tasas De Bits Y VBR

min_bitrate = input(
    "\nM8AX - Introduce La Tasa De Bits Mínima En kbps ( Por Ejemplo, 5 ): "
).strip()

# Si No Se Introduce Nada, Se Establece En 5

if not min_bitrate:
    min_bitrate = 5
else:
    min_bitrate = int(min_bitrate)  # Convertir A Entero Si Se Introduce Un Valor

max_bitrate = input(
    "\nM8AX - Introduce La Tasa De Bits Máxima En kbps ( Por Ejemplo, 32 ): "
).strip()

# Si No Se Introduce Nada, Se Establece En 32

if not max_bitrate:
    max_bitrate = 32
else:
    max_bitrate = int(max_bitrate)  # Convertir A Entero Si Se Introduce Un Valor

# Pedimos VBR Activado O Desactivado

vbr = (
    input(
        "\nM8AX - ¿ Habilitar VBR ? ( Escribe 'on' Para Habilitar O 'off' Para Deshabilitar ): "
    )
    .strip()
    .lower()
)

if vbr not in ["on", "off"]:
    print("\nM8AX - Error: Debes Escribir 'on' O 'off' Para VBR... on Si Error...")
    vbr = "on"

# Solicitar Si Convertir A Mono O A Estéreo

audio_channels = ask_for_audio_channels()

# Solicitar La Frecuencia De Muestreo

sample_rate = ask_for_sample_rate()

# Solicitar Normalización De Audio Si/No

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    normalizar = ask_for_normal()

# Solicitar Hacer Reverse A Las Canciones

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    hayreverse = ask_for_reverse()

# Solicitar Si Añadir Eco

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    hayeco = ask_for_eco()

# Solicitar Aumento De Graves

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    haygraves = ask_for_graves()

# Solicitar Aumento De Agudos

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    hayagudos = ask_for_agudos()

# Solicitar Aumento De Tono

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    haytono = ask_for_tono()

# Solicitar Paneo Dinámico

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    haypaneo, alehz = ask_for_paneo()
    if haypaneo == "si" or haypaneo == "ale":
        paneco = ask_for_ecopane()

# Solicitar Velocidad

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):

    velocidad = ask_for_speed_rate()

# Solicitar Subir O Bajar Volumen

if all(
    [
        normalizar == "no",
        hayreverse == "no",
        hayeco == "no",
        haygraves == "no",
        hayagudos == "no",
        haytono == "no",
        haypaneo == "no",
        jox == "no",
    ]
):
    if velocidad == float(1):
        volumencillo, jox = ask_for_volume()

# Solicitar Si Añadimos MetaTags

metetag = ask_for_meta()

# Solicitar Si Añadimos QRCODE

aqrcode = ask_for_qr()

if aqrcode == "si":
    # Solicitar Dirección Web Directa A Una Imágen

    direimagenqr = solicitar_direccion_web()

# Solicitar Si Creamos Espectrograma

espec = ask_for_espec()

# Solicitar Si Creamos WaveForms

ondas = ask_for_ondas()

# Solicitar Si Creamos Videos Con WaveForms Animados

hacerv = ask_for_video()

# Preguntar Número De Núcleos A Usar

xnum_cores = ask_for_cores()

os.system("play -n synth 0.0150 sin 7000 > /dev/null 2>&1")

# Lista De Extensiones De Audio A Convertir

audio_extensions = (
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".m4a",
    ".wma",
    ".opus",
    ".aiff",
    ".alac",
    ".dts",
    ".ac3",
    ".mid",
    ".midi",
    ".ogm",
    ".amr",
    ".speex",
)

# Limpiar La Pantalla Al Comienzo Del Programa

clear_screen()

# Crear Una Lista De Archivos Para Convertir

files_to_convert = []
initial_total_size = 0
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith(audio_extensions):
            file_path = os.path.join(root, file)
            files_to_convert.append(file_path)
            initial_total_size += get_file_size_mb(file_path)

# Detectar El Número De Núcleos De La CPU

num_cores = multiprocessing.cpu_count()
print(
    f"------------ Usando {xnum_cores} De {num_cores} Núcleos Para La Conversión Al Codec OPUS ------------\n"
)

# Medir El Tiempo Total Para La Conversión

start_time = time.time()

antes = obtener_fecha_formateada()

# Crear La Barra De Progreso Total

fill_color = ["blue", "cyan", "green", "magenta", "red", "yellow", "white"]

fill_color = random.choice(fill_color)

with tqdm(
    total=len(files_to_convert), desc="M8AX - Paso 1/2 - ", ncols=80, colour=fill_color
) as pbar_total:

    # Usar Un Executor Para Convertir En Paralelo, Con El Número De Núcleos Que Hemos Elegido
    with ProcessPoolExecutor(max_workers=xnum_cores) as executor:

        # Convertir Los Archivos Y Actualizar El Progreso

        for _ in executor.map(convert_to_opus, files_to_convert):
            pbar_total.update(1)


# Calcular El Tamaño Total Después De La Conversión Y Alguna Cosilla Más

final_total_size = 0
final_total_size_jpgespec = 0
final_total_size_jpgondas = 0
final_total_size_jpg = 0
final_total_size_mp4 = 0

# Recorre El Directorio Para Contar Archivos

total_files = sum(len(files) for _, _, files in os.walk(output_dir))

print("\n")

fill_color = ["blue", "cyan", "green", "magenta", "red", "yellow", "white"]

fill_color = random.choice(fill_color)

# Barra De Progreso Para Procesos Finales Del Cálculo Y Añadir QRCODE A MetaTags Si Así Lo Queremos...

with tqdm(total=total_files, desc="M8AX - Paso 2/2 - ", colour=fill_color) as pbar:
    for root, _, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".opus"):
                # Sumar Duración De Los Ficheros De Música

                total_duration += get_audio_duration(file_path)

                sumando += 1

                # Crear Un Objeto QRCode

                if aqrcode == "si":
                    if not os.path.isfile("m8ax.png"):
                        try:
                            continua = 1
                            download_image(direimagenqr)
                            os.system("play -n synth 0.150 sin 1000 > /dev/null 2>&1")
                        except Exception:
                            continua = 0
                            pass  # Ignora El Error Y Continúa Sin Hacer Nada
                    else:
                        continua = 1
                    if continua == 1:
                        markitosfac = generar_y_factorizar()
                        nombrefi = os.path.basename(file_path)
                        titulo_codificado = urllib.parse.quote(nombrefi)
                        link_busqueda = (
                            f"https://www.google.com/search?q={titulo_codificado}"
                        )

                        colors = [
                            "cyan",
                            "red",
                            "white",
                            "#3B5998",
                            "brown",
                            "orange",
                            "magenta",
                            "#FF5733",
                            "#ECC420",
                            "#9DB8EC",
                            "#F38F6D",
                            "#999594",
                            "#90D6C4",
                            "#D69097",
                            "#06FB25",
                        ]

                        fill_colo = random.choice(colors)
                        qr = qrcode.QRCode(
                            version=2,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=8,
                            border=2,
                        )

                        qr.add_data(
                            f"Título: {nombrefi}\n\nLink: {link_busqueda}\n\nWeb 1: https://youtube.com/m8ax\nWeb 2: https://opensea.io/es/m8ax\nMail: XXXXX\nTlf: XXXXX\n\nPor Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás...\n\n{markitosfac}\n"
                            + "\n.•♫•♬•🔥Ｍ𝚟ıııคx🔥•♬•♫•.\nX∀8ꟽ\n⌘•⌘ ꧁☆❤️🅼8🅰🆇❤️☆꧂ ⌘•⌘"
                        )

                        qr.make(fit=True)
                        img = qr.make_image(fill_color=fill_colo, back_color="black")
                        img.save("mddd-cover.jpg")

                        # Abre Las Imágenes De Fondo Y Superposición

                        background = Image.open("mddd-cover.jpg")
                        overlay = Image.open("m8ax.png")

                        # Asegúrate De Que Las Imágenes Tengan El mismo Tamaño, Si No, Redimensiona La De Superposición

                        overlay = overlay.resize(background.size)

                        # Aplica La Opacidad A La Imagen De Superposición ( 0 Es Completamente Transparente, 255 Es Opaco )

                        opacity = 65  # 65% De Opacidad
                        overlay = overlay.convert("RGBA")
                        alpha = overlay.split()[3]  # Extrae El Canal Alfa
                        alpha = alpha.point(
                            lambda p: p * (opacity / 255)
                        )  # Ajusta El Canal Alfa Según La Opacidad
                        overlay.putalpha(
                            alpha
                        )  # Aplica El Nuevo Canal Alfa A La Imágen De Superposición

                        # Superpone La Imágen Con Opacidad Sobre La De Fondo

                        combined = Image.alpha_composite(
                            background.convert("RGBA"), overlay
                        )

                        # Guarda El Resultado

                        combined.save("mviiiax-cover.png")
                        input_image = "mviiiax-cover.png"
                        output_image = "g8alax-cover.png"

                        text_to_add = f"{nombrefi}\nMvIiIaX - The Algorithm Man - MvIiIaX\nEl Futuro... No Esta Establecido, No Hay Destino, Solo Existe El Que Nosotros Hacemos...\nhttp://youtube.com/m8ax\n--- En Honor De M8AX-MDDD ---"

                        add_text_to_image(input_image, output_image, text_to_add)
                        main_image = Image.open("g8alax-cover.png")
                        small_image = Image.open("m8ax.png")
                        small_image = small_image.resize((75, 75))
                        width, height = main_image.size
                        main_image.paste(small_image, (0, height - 75))  # (X, Y)
                        main_image.paste(
                            small_image, (width - 75, height - 75)
                        )  # (X, Y)

                        main_image.save(
                            "m8ax-cover.webp", format="WEBP", optimize=True, quality=75
                        )

                        audio_file = file_path
                        cover_file = "m8ax-cover.webp"
                        audio = OggOpus(audio_file)

                        # Leer La Imágen De Portada

                        with open(cover_file, "rb") as f:
                            cover_data = f.read()

                        # Crear Un Objeto Picture

                        picture = Picture()
                        picture.data = cover_data
                        picture.type = 3  # 3 Significa Portada Frontal
                        picture.mime = "image/webp"
                        picture.desc = "Cover"

                        # Codificar La Imágen En Base64

                        picture_data = base64.b64encode(picture.write())

                        # Añadir La Imágen Codificada Como Un Nuevo Campo De Metadatos

                        audio["metadata_block_picture"] = [picture_data.decode("ascii")]
                        audio["comment"] = (
                            f"🎶 ----- {nombrefi} ----- 🎶 ----- M8AX . Portada Con Con Código QR Incorporada . M8AX ----- 💻 ----- {markitosfac} ----- 💻"
                        )

                        # Guardar Los Cambios

                        audio.save()

                        # Borrar Temporales, El QR Ya Está Metido En El Fichero OPUS

                        os.remove("m8ax-cover.webp")
                        os.remove("mviiiax-cover.png")
                        os.remove("g8alax-cover.png")
                        os.remove("mddd-cover.jpg")

                final_total_size += get_file_size_mb(file_path)

            if file.endswith(".Mp4"):
                final_total_size_mp4 += get_file_size_mb(file_path)

            elif file.lower().endswith(".jpg"):
                final_total_size_jpg += get_file_size_mb(file_path)

                if file.endswith(".opus.Espectrograma.JpG"):
                    final_total_size_jpgespec += get_file_size_mb(file_path)
                elif file.endswith(".opus.Forma-De-Onda.JpG"):
                    final_total_size_jpgondas += get_file_size_mb(file_path)

            # Actualiza La Barra De Progreso

            if sumando % 50 == 0:
                os.system("play -n synth 0.0050 sin 100 > /dev/null 2>&1")

            pbar.update(1)

# Calcular El Tiempo Total De Conversión

end_time = time.time()
elapsed_time = end_time - start_time

# Borrar Imágen Descargada De URL

if os.path.isfile("m8ax.png"):
    os.remove("m8ax.png")

despues = obtener_fecha_formateada()

# Convertir El Tiempo Total De Conversión A Días, Horas, Minutos Y Segundos

conversion_seconds = int(elapsed_time)
conv_days = conversion_seconds // (24 * 3600)
conv_hours = (conversion_seconds % (24 * 3600)) // 3600
conv_minutes = (conversion_seconds % 3600) // 60
conv_seconds = conversion_seconds % 60

# Convertir La Duración Total De Archivos A Días, Horas, Minutos Y Segundos

total_seconds = int(total_duration)
days = total_seconds // (24 * 3600)
hours = (total_seconds % (24 * 3600)) // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

# Calcular La Duración Media Por Archivo

average_duration = total_duration / len(files_to_convert) if files_to_convert else 0
avg_seconds = int(average_duration)
avg_days = avg_seconds // (24 * 3600)
avg_hours = (avg_seconds % (24 * 3600)) // 3600
avg_minutes = (avg_seconds % 3600) // 60
avg_seconds = avg_seconds % 60

# Calcular El Porcentaje De Compresión

compression_percentage = (
    (1 - (final_total_size / initial_total_size)) * 100 if initial_total_size > 0 else 0
)

# Calcular Archivos Convertidos Por Segundo

files_per_second = len(files_to_convert) / elapsed_time if elapsed_time > 0 else 0

# Mostrar Resultados Finales

clear_screen()

print(
    f"-----  M8AX - PROGRAMA FINALIZADO CON ÉXITO ( -- TODO CORRECTO -- ) - M8AX -----"
)
print(f"\nM8AX - Directorio De Entrada: {input_dir}")
print(f"\nM8AX - Directorio De Salida: {output_dir}")
if espec == "si":
    print(
        f"\nM8AX - Se Han Creado {mviiiax.value} Espectrogramas De Las Canciones Y Ocupan {final_total_size_jpgespec:.5f} MB."
    )
if ondas == "si":
    print(
        f"\nM8AX - Se Han Creado {mviiiax.value} WaveForms De Las Canciones Y Ocupan {final_total_size_jpgondas:.5f} MB."
    )
if ondas == "si" and espec == "si":
    print(
        f"\nM8AX - Se Han Creado {mviiiax.value*2} Imágenes De Las Canciones, Entre Espectrogramas Y WaveForms Y Ocupan {final_total_size_jpg:.5f} MB."
    )
if hacerv == "si":
    print(
        f"\nM8AX - Se Han Creado {mviiiax.value} Videos Animados Con WaveForms De Las Canciones Y Ocupan {final_total_size_mp4:.5f} MB."
    )
print(f"\nM8AX - Bitrate Mínimo: {min_bitrate} kbps.")
print(f"\nM8AX - Bitrate Máximo: {max_bitrate} kbps.")
print(
    f"\nM8AX - Variable Bit Rate (VBR): {'Habilitado.' if vbr == 'on' else 'Deshabilitado.'}"
)
if sample_rate == "0":
    print(
        "\nM8AX - Audio Convertido A: Configuración De Frecuencia De Muestreo Original, Mantenida."
    )
else:
    print(f"\nM8AX - Frecuencia De Muestreo Seleccionada: {sample_rate} Hz.")
if audio_channels is None:
    print(
        "\nM8AX - Audio Convertido A: Configuración De Canales Mono/Estéreo Original, Mantenida."
    )
else:
    print(
        f"\nM8AX - Audio Convertido A: {'Mono.' if audio_channels == 'mono' else 'Estéreo.'}"
    )
if normalizar == "si":
    print(
        "\nM8AX - Volumen De Las Canciones Normalizado, Para Asegurar Que Todas Tengan Un Nivel De Sonoridad Adecuado."
    )
if hayreverse == "si":
    print("\nM8AX - Las Canciones Se Escucharán Al Revés...")
if hayeco == "si":
    print("\nM8AX - Eco Añadido A Las Canciones...")
if haygraves == "si":
    print("\nM8AX - Graves Aumentados...")
if hayagudos == "si":
    print("\nM8AX - Agudos Aumentados...")
if haytono == "si":
    print("\nM8AX - Tono Aumentado...")
if haypaneo == "si":
    print("\nM8AX - Paneo Dinámico Aplicado A 0.1 Hz...")
    if paneco == "si":
        print("\nM8AX - Paneo Dinámico Aplicado Con Eco...")
    if paneco == "no":
        print("\nM8AX - Paneo Dinámico Aplicado Sin Eco...")
if haypaneo == "ale":
    print("\nM8AX - Paneo Dinámico Aplicado Aleatoriamente A Cada Canción...")
    if paneco == "si":
        print("\nM8AX - Paneo Dinámico Aplicado Con Eco...")
    if paneco == "no":
        print("\nM8AX - Paneo Dinámico Aplicado Sin Eco...")
if velocidad:
    print(f"\nM8AX - Velocidad De Las Canciones A: {velocidad}X.")
if volumencillo >= 0 and volumencillo < 1:
    print(f"\nM8AX - El Volumen Se Ha Reducido A: {volumencillo:.5f}.")
if volumencillo > 1:
    print(f"\nM8AX - El Volumen Se Ha Aumentado En: {volumencillo:.5f}.")
if volumencillo == 1:
    print(f"\nM8AX - El Volumen Se Ha Mantenido Igual: {volumencillo:.5f}.")
if metetag == "si":
    print("\nM8AX - MetaTags Añadidos Correctamente...")
else:
    print("\nM8AX - MetaTags Originales Mantenidos Correctamente...")
if aqrcode == "si":
    print(
        f"\nM8AX - Código QRCODE Añadido Correctamente, Como Portada De Cada Fichero De Audio... Adornado Con La Imágen De Este Link - {direimagenqr}."
    )
else:
    print("\nM8AX - No Se Ha Añadido QRCODE Como Portada, En Los Ficheros De Audio...")
print(
    f"\nM8AX - Número Total De Archivos De Música Convertidos: {len(files_to_convert)} Archivos De Música..."
)
print(
    f"\nM8AX - Tiempo Total De Conversión A OPUS: {elapsed_time:.5f} Segundos. | {conv_days} Días, {conv_hours} Horas, {conv_minutes} Minutos Y {conv_seconds} Segundos."
)
print(
    f"\nM8AX - Duración Total De Todos Los Archivos De Música: {days} Días, {hours} Horas, {minutes} Minutos Y {seconds} Segundos."
)
print(
    f"\nM8AX - Duración Media De Cada Archivo De Música: {avg_days} Días, {avg_hours} Horas, {avg_minutes} Minutos Y {avg_seconds} Segundos."
)
print(
    f"\nM8AX - He Usado {xnum_cores} De Los {num_cores} Núcleos De La CPU, Que Podría Usar..."
)
print(f"\nM8AX - Archivos Convertidos Por Segundo: {files_per_second:.5f} Arch/s.")
print(f"\nM8AX - Archivos Convertidos Por Minuto: {(files_per_second)*60:.5f} Arch/m.")
print(f"\nM8AX - Archivos Convertidos Por Hora: {(files_per_second)*3600:.5f} Arch/h.")
print(f"\nM8AX - Archivos Convertidos Por Día: {(files_per_second)*86400:.5f} Arch/d.")
print(
    f"\nM8AX - Archivos Convertidos Por Semana: {(files_per_second)*604800:.5f} Arch/sem."
)
print(
    f"\nM8AX - Archivos Convertidos Por Mes: {(files_per_second)*2592000:.5f} Arch/mes."
)
print(
    f"\nM8AX - Archivos Convertidos Por Año: {(files_per_second)*31536000:.5f} Arch/año."
)
print(f"\nM8AX - Tamaño Total Antes De La Conversión: {initial_total_size:.5f} MB.")
print(f"\nM8AX - Tamaño Total Después De La Conversión: {final_total_size:.5f} MB.")
print(f"\nM8AX - Porcentaje De Compresión Conseguido: {compression_percentage:.5f} %.")
print(
    f"\nM8AX - Segundos De Música Por Segundo Procesados: {total_duration/elapsed_time:.5f} TimeMus(s)/s..."
)
print(
    f"\nM8AX - Minutos De Música Por Segundo Procesados: {(total_duration/elapsed_time)/60:.5f} TimeMus(m)/s..."
)
print(
    f"\nM8AX - Horas De Música Por Segundo Procesadas: {(total_duration/elapsed_time)/3600:.5f} TimeMus(h)/s..."
)
print(
    f"\nM8AX - Horas De Música Por Hora Procesadas: {((total_duration/elapsed_time)*3600)/3600:.5f} TimeMus(h)/h..."
)
print(
    f"\nM8AX - MB Leídos Para Comprimir Por Segundo: {(initial_total_size/elapsed_time):.5f} MB/s."
)
print(f"\nM8AX - MB Grabados Por Segundo: {(final_total_size/elapsed_time):.5f} MB/s.")
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Linea Recta, Con Tamaño De Letra Normal, Ocuparían Sin Comprimir A OPUS: {(initial_total_size*1000000*0.0025):.5f} Metros | {((initial_total_size*1000000*0.0025)/1000):.5f} KM..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Linea Recta, Con Tamaño De Letra Normal, Ocuparían Comprimidos A OPUS: {(final_total_size*1000000*0.0025):.5f} Metros | {((final_total_size*1000000*0.0025)/1000):.5f} KM..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Linea Recta, Con Tamaño De Letra Normal, Leeríamos Para Comprimir A OPUS A: {((initial_total_size*1000000*0.0025)/elapsed_time):.5f} Metros Por Segundo... | {(((initial_total_size*1000000*0.0025)/elapsed_time)/1000):.5f} Kilómetros Por Segundo..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Linea Recta, Con Tamaño De Letra Normal, Grabaríamos A OPUS A: {((final_total_size*1000000*0.0025)/elapsed_time):.5f} Metros Por Segundo... | {(((final_total_size*1000000*0.0025)/elapsed_time)/1000):.5f} Kilómetros Por Segundo..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, Escrito En Páginas A5 De Un Libro, Con Tamaño De Letra Normal, Ocuparían Sin Comprimir A OPUS: {((initial_total_size*1000000)/2500):.5f} Páginas | {(((initial_total_size*1000000)/2500)/300):.5f} Libros De 300 Páginas, Que Es Creo Yo... La Media De Páginas Mundial, Que Contienen Los Libros Escritos Por El Hombre..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, Escrito En Páginas A5 De Un Libro, Con Tamaño De Letra Normal, Ocuparían Comprimidos A OPUS: {((final_total_size*1000000)/2500):.5f} Páginas | {(((final_total_size*1000000)/2500)/300):.5f} Libros De 300 Páginas, Que Es Creo Yo... La Media De Páginas Mundial, Que Contienen Los Libros Escritos Por El Hombre..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Formato Libro, Leeríamos Para Comprimir A OPUS A: {(((initial_total_size*1000000)/2500)/elapsed_time):.5f} Páginas Por Segundo... | {((((initial_total_size*1000000)/2500)/300)/elapsed_time):.5f} Libros Por Segundo..."
)
print(
    f"\nM8AX - Si Los MB Fueran De Texto, En Formato Libro, Escribiríamos A OPUS A: {(((final_total_size*1000000)/2500)/elapsed_time):.5f} Páginas Por Segundo... | {((((final_total_size*1000000)/2500)/300)/elapsed_time):.5f} Libros Por Segundo..."
)
print(
    f"\nM8AX - En Un Año 24/7, Tu Dispositivo Sería Capaz De Comprimir A OPUS: {((31536000*len(files_to_convert))/elapsed_time):.5f} Ficheros De Música, Que A Una Media De {(average_duration):.5f} Segundos Por Fichero, Nos Darían {((((31536000*len(files_to_convert))/elapsed_time)*average_duration)/86400):.5f} Días De Reproducción Continua O Lo Que Es Lo Mismo {(((((31536000*len(files_to_convert))/elapsed_time)*average_duration)/86400)/365):.5f} Años... Una Locura...\n"
)
print(
    f"---------- M8AX - CADENA DE FFMPEG UTILIZADA PARA LA CONVERSIÓN - M8AX ----------\n"
)

with open("M8AX-Lista-FFmpeg.TxT", "r") as f:
    ffmpeg_cmd_string = f.read()  # Leo El Archivo

if os.path.exists("M8AX-Lista-FFmpeg.TxT"):
    os.remove("M8AX-Lista-FFmpeg.TxT")  # Borra El Archivo

print(ffmpeg_cmd_string)
if aqrcode == "si":
    print(
        f"\nM8AX - Último Número Factorizado Metido En MetaData Si Portada QR ON: {markitosfac}"
    )
print(f"\nM8AX - El Trabajo Comenzó {antes} Y Terminó {despues}.")
print(
    f"\nM8AX - Número De Ficheros Procesados: {mviiiax.value}, El Cual Coincide Con Los Convertidos... ((( TODO OK )))."
)
print(f"\nBy MarcoS OchoA DieZ - http://youtube.com/m8ax\n")

os.system("play -n synth 0.0150 sin 7000 > /dev/null 2>&1")

subprocess.run(
    [
        "espeak",
        "¡Todo Correcto, Marcos!. Gran Labor En La Conversión De Los Archivos De Música Al Formato Opus. Tu Atención Al Detalle Y Precisión En El Proceso Son Notables. ¡Un Saludo Y Sigue Optimizando!",
    ]
)

# Ruta Del Directorio Que Contiene Los Archivos De Música

directorio_musica = output_dir

# Lista Todos Los Archivos En El Directorio

for archivo in os.listdir(directorio_musica):
    # Verifica Si El Archivo Tiene Una Extensión De Música

    if archivo.endswith(
        (
            ".mp3",
            ".wav",
            ".flac",
            ".aac",
            ".ogg",
            ".m4a",
            ".wma",
            ".opus",
            ".aiff",
            ".alac",
            ".dts",
            ".ac3",
            ".mid",
            ".midi",
            ".ogm",
            ".amr",
            ".speex",
        )
    ):  # Agrega Más Extensiones Si Es Necesario
        ruta_archivo = os.path.join(directorio_musica, archivo)
        print(
            f"🎹 M8AX 🎹 - Ctrl+Z Para Abortar. Reproduciendo: ((( ▶︎ {ruta_archivo} ◀︎ ))) - 🎹 M8AX 🎹"
        )
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", ruta_archivo],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )