"""
Este Programa Permite Comprimir Archivos De Música En Formato OPUS. 
El Usuario Puede Elegir La Carpeta De Origen Que Puede Contener 
Varias Carpetas Con Música En Diferentes Formatos ( MP3, AAC, WAV, 
OGG, M4A, Etc... ). El Programa Recorrerá Todas Las Carpetas De La 
Carpeta De Origen Y Creará La Misma Jerarquía En La Carpeta De 
Salida, Pero Con Los Archivos Ya Comprimidos En OPUS. Además, El Programa 
Detectará Los Cores De Tu CPU Y Los Usará Para Realizar La 
Compresión De Manera Más Rápida. Se Puede Configurar El Bitrate 
Máximo Y Mínimo Para La Compresión, Así Como La Opción De Activar 
O Desactivar El Variable Bit Rate ( VBR ). El Usuario También Puede 
Elegir Si Convertir El Audio A Estéreo O A Mono, Así Como Seleccionar 
La Frecuencia De Muestreo Deseada. Los Archivos Generados Incluirán 
Metatags Para Mejorar La Organización Y La Identificación De La 
Música Comprimida; " Para Mí ". Se Puede Elegir Si Incluirlos O No. 

Además... Se Puede Normalizar El Audio, Hacer Que Las Canciones Se 
Escuchen Al Revés, También Se Puede Añadir Eco A Las Canciones, Aumentar
Los Graves, Aumentar Los Agudos, Subir El Tono, Convertir El Audio A
Audio 8D Con O Sin Eco, Que Es El Audio 3D De Toda La Vida Y Aumentar
O Reducir La Velocidad De Reproducción...

Programador: MarcoS OchoA DieZ ( Alias: M8AX ) 
Fecha De Programación: 15 / OCTUBRE / 2024 - MARTES
Dispositivo Utilizado: MvIiIaX - Xiaomi MI 9 Lite - ( TERMUX Con PythoN )
Código Formateado Con: BlacK
"""

import os
import time
import random
import subprocess
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from tqdm import tqdm

ffmpeg_cmd_string = ""
mviiiax = multiprocessing.Value("i", 0)  # 'i' Significa Nº Entero

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
                "M8AX - ¿ Deseas Convertir El Audio A Mono O A Estéreo ? ( Escribe 'mono' O 'stereo', O Presiona Enter Para Mantener Los Canales Originales ): "
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
            print("M8AX - Error: Debes Escribir 'mono' O 'stereo'...")


# Función Para Solicitar Paneo Dinámico


def ask_for_paneo():
    alehz = 0
    while True:
        choice = (
            input(
                "M8AX - ¿ Deseas Un Paneo Dinámico Para Todas Las Canciones ?, ale Implica Si, Pero La Duración Del Paneo Será Aleatoria En Cada Canción De 33s A 8s... ( Escribe 'si', 'no' O 'ale' ): "
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
            print("M8AX - Error: Debes Escribir 'si', 'no' O 'ale' ...")


# Función Para Solicitar Si Aumentamos El Tono


def ask_for_tono():
    while True:
        choice = (
            input("M8AX - ¿ Deseas Aumentar El Tono ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Eco En Paneo Dinámico


def ask_for_ecopane():
    while True:
        choice = (
            input("M8AX - ¿ Eco En Paneo Dinámico ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Añadimos MetaTags


def ask_for_meta():
    while True:
        choice = (
            input(
                "M8AX - ¿ Añadir MetaTags A Las Canciones ? si = Añade MetaTags no = Deja Como Están... ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Aumentamos Los Graves


def ask_for_graves():
    while True:
        choice = (
            input("M8AX - ¿ Deseas Aumentar Los Graves ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Aumentamos Los Agudos


def ask_for_agudos():
    while True:
        choice = (
            input("M8AX - ¿ Deseas Aumentar Los Agudos ? ( Escribe 'si' O 'no' ): ")
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Añadimos Eco A Las Canciones


def ask_for_eco():
    while True:
        choice = (
            input(
                "M8AX - ¿ Deseas Añadir Eco A Las Canciones ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Normalizamos Cada Canción


def ask_for_normal():
    while True:
        choice = (
            input(
                "M8AX - ¿ Deseas Que Las Canciones Sean Normalizadas ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar Si Queremos Que Las Canciones Se Escuchen Al Revés, ( REVERSE )


def ask_for_reverse():
    while True:
        choice = (
            input(
                "M8AX - ¿ Quieres Que Cada Canción Se Escuche Al Revés ? ( Escribe 'si' O 'no' ): "
            )
            .strip()
            .lower()
        )

        # Si La Opción Es Válida, Se Devuelve Esa Opción

        if choice in ["si", "no"]:
            return choice
        else:
            print("M8AX - Error: Debes Escribir 'si' O 'no'...")


# Función Para Solicitar La Frecuencia De Muestreo, 0 Para Dejar La Original


def ask_for_sample_rate(default_rate=0):
    sample_rates = ["0", "8000", "12000", "16000", "24000", "48000"]
    print(f"M8AX - Frecuencias De Muestreo Disponibles: {', '.join(sample_rates)} Hz")

    while True:
        user_input = input(
            "M8AX - Por Favor, Elige Una Frecuencia De Muestreo, ( 0 - Para Dejar La Original Del Fichero A Convertir ): "
        )
        if user_input in sample_rates:
            return user_input
        else:
            print("\nM8AX - Frecuencia No Válida, Inténtalo De Nuevo...\n")


# Función Para Solicitar La Velocidad


def ask_for_speed_rate(default_rate=1):
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

    print(f"M8AX - Velocidades Disponibles: {', '.join(atempo_values)} X")

    while True:
        user_input = input(
            "M8AX - Por Favor, Elige Una Velocidad, ( 1.0 - Para Dejar La Velocidad Original Del Fichero A Convertir ): "
        )
        if user_input in atempo_values:
            return user_input
        else:
            print("\nM8AX - Velocidad No Válida, Inténtalo De Nuevo...\n")


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

    # Comando Para Convertir A OPUS Con Metadatos

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
        ]
    ):

        ffmpeg_cmd += [
            "-filter:a",
            f"atempo={velocidad}",
        ]  # Velocidad

    # Agregar MetaTags

    if metetag == "si":
        ffmpeg_cmd += [
            "-metadata",
            f"episode_id=ORIGEN - {os.path.basename(file_path)} | DESTINO - {os.path.basename(output_file_path)}",  # ID Del Episodio
            "-metadata",
            r"copyright=-///📷\\\ --- MvIiIaX & M8AX 2025 - 2050 --- ///📷\\\-",  # Copyright
            "-metadata",
            r"genre=-///📷\\\ --- | ★ https://oncyber.io/@m8ax ★ | --- ///📷\\\-",  # Género
            "-metadata",
            r"MarcosOchoaDiez=@ - Programar No Es Solo Resolver Problemas, Es Transformar Ideas En Soluciones Que Cambian El Mundo... - @",  # MarcosOchoaDiez
            "-metadata",
            r"MvIiIaX=----- | ★ https://opensea.io/es/m8ax ★ | -----",  # NFTS
            "-metadata",
            r"BitcoinWallet=-/// ⚡LeD⚡ \\\ - Su Carencia De Fe, Resulta Molesta... - /// ⚡GeR⚡ \\\-",  # Wallet Bitcoin
            "-metadata",
            r"author=--- MarcoS OchoA DieZ -► ( ★ ********************* ★, ★ ********* ★ ) ---",  # Autor
            "-metadata",
            r"show=Mi Canal De YouTube - ((( ★ http://youtube.com/m8ax ★ )))",  # Show
            "-metadata",
            r"grouping=Mi Blog - ((( ★ http://mviiiaxm8ax.blogspot.com ★ )))",  # Agrupación Blog
            "-metadata",
            r"comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El Futuro... No Está Establecido, Solo Existe... El Que Nosotros Hacemos... 3 - El Miedo Es El Camino Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al Sufrimiento... 4 - Música Compilada En Honor A MDDD...",  # Comentario
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
            r"handler_name=--- MarcoS OchoA DieZ -► ( M8AX OR MvIiIaX ) ---",  # Nombre Del Compresor
            "-metadata",
            f"EHD_MDDD=.•♫•♬•🔥Ｍ𝚟ıııคx🔥•♬•♫•. X∀8ꟽ ⌘•⌘ ꧁☆❤️🅼8🅰🆇❤️☆꧂ ⌘•⌘",  # M8AX Programmer EHDMDDD
            "-metadata",
            r"ImoDTroN=Nunca Dejes Que Nadie Te Diga Que No Puedes Hacer Algo. Ni Siquiera Yo. Si Tienes Un Sueño, Tienes Que Protegerlo. Las Personas Que No Son Capaces De Hacer Algo Por Ellas Mismas, Te Dirán Que Tú Tampoco Puedes Hacerlo. ¿ Quieres Algo ? Ve Por Ello Y Punto...",  # Frasecilla
        ]

    # Agregar El Archivo De Salida Al Final Del Comando

    ffmpeg_cmd.append(output_file_path)  # Último Comando

    # Ejecutar El Comando FFmpeg Y Mostrar La Salida En Tiempo Real

    if mviiiax.value == 0:
        # Abro El Archivo En Modo Escritura

        with open("M8AX-Lista-FFmpeg.TxT", "w") as f:
            f.write(" ".join(ffmpeg_cmd))

    modificar_variable()

    result = subprocess.run(
        ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='latin-1'
    )

    # Mostrar La Salida De FFmpeg

    return result.stdout


# Función Para Obtener La Duración De Un Archivo De Audio


def get_audio_duration(file_path):
    result = subprocess.run(
        ["ffmpeg", "-i", file_path],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    for line in result.stderr.split("\n"):
        if "Duration" in line:
            duration_str = line.split("Duration: ")[1].split(",")[0]
            h, m, s = map(float, duration_str.split(":"))
            return h * 3600 + m * 60 + s  # Duración En Segundos
    return 0


# Función Para Obtener El Tamaño De Un Archivo En MB


def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)


# Función Para Solicitar Un Directorio Existente


def get_existing_directory(prompt):
    while True:
        directory = input(prompt).strip()
        if os.path.exists(directory):
            return directory
        else:
            print(
                f"M8AX - El Directorio '{directory}' No Existe. Por Favor, Verifica La Ruta..."
            )


# Solicitar Directorio De Entrada

clear_screen()

normalizar = "no"
hayreverse = "no"
hayeco = "no"
haygraves = "no"
hayagudos = "no"
haytono = "no"
haypaneo = "no"
velocidad = 1.0
hz_value = 0.1
alehz = 0

print(f"--------  M8AX - PROGRAMA PARA CONVERTIR MÚSICA A FORMATO OPUS - M8AX --------")
print(f"")
input_dir = get_existing_directory(
    "M8AX - Introduce El Directorio De Origen ( Donde Están Los Archivos A Convertir ): "
)

# Solicitar Directorio De Destino Y Crearlo Si No Existe

output_dir = input(
    "M8AX - Introduce El Directorio De Destino ( Donde Se Guardarán Los Archivos Convertidos ): "
).strip()
os.makedirs(output_dir, exist_ok=True)

# Solicitar Tasas De Bits Y VBR

min_bitrate = input(
    "M8AX - Introduce La Tasa De Bits Mínima En kbps ( Por Ejemplo, 5 ): "
).strip()
max_bitrate = input(
    "M8AX - Introduce La Tasa De Bits Máxima En kbps ( Por Ejemplo, 32 ): "
).strip()
vbr = (
    input(
        "M8AX - ¿ Habilitar VBR ? ( Escribe 'on' Para Habilitar O 'off' Para Deshabilitar ): "
    )
    .strip()
    .lower()
)

# Validar La Entrada Del Usuario

if vbr not in ["on", "off"]:
    print("M8AX - Error: Debes Escribir 'on' O 'off' Para VBR... on Si Error...")
    vbr='on'

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
    ]
):

    velocidad = ask_for_speed_rate()

# Solicitar Si Añadimos MetaTags

metetag = ask_for_meta()

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
    ".midi",
    ".ogm",
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
    f"--------------- Usando {num_cores} Núcleos Para La Conversión Al Codec OPUS ---------------\n"
)

# Medir El Tiempo Total Para La Conversión

start_time = time.time()

# Crear La Barra De Progreso Total

with tqdm(total=len(files_to_convert), desc="M8AX - Progreso Total", ncols=80) as pbar_total:

    # Usar Un Executor Para Convertir En Paralelo Con El Número De Núcleos Detectado

    with ProcessPoolExecutor(max_workers=num_cores) as executor:

        # Convertir Los Archivos Y Actualizar El Progreso

        for _ in executor.map(convert_to_opus, files_to_convert):
            pbar_total.update(1)

# Calcular El Tiempo Total De Conversión

end_time = time.time()
elapsed_time = end_time - start_time

# Convertir El Tiempo Total De Conversión A Días, Horas, Minutos Y Segundos

conversion_seconds = int(elapsed_time)
conv_days = conversion_seconds // (24 * 3600)
conv_hours = (conversion_seconds % (24 * 3600)) // 3600
conv_minutes = (conversion_seconds % 3600) // 60
conv_seconds = conversion_seconds % 60

# Convertir La Duración Total De Archivos A Días, Horas, Minutos Y Segundos

total_duration = sum(get_audio_duration(file_path) for file_path in files_to_convert)
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

# Calcular El Tamaño Total Después De La Conversión

final_total_size = 0
for root, _, files in os.walk(output_dir):
    for file in files:
        file_path = os.path.join(root, file)
        final_total_size += get_file_size_mb(file_path)

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
print(f"\nM8AX - Bitrate Mínimo: {min_bitrate} kbps")
print(f"\nM8AX - Bitrate Máximo: {max_bitrate} kbps")
print(
    f"\nM8AX - Variable Bit Rate (VBR): {'Habilitado' if vbr == 'on' else 'Deshabilitado'}"
)
if sample_rate == "0":
    print(
        "\nM8AX - Audio Convertido A: Configuración De Frecuencia De Muestreo Original, Mantenida."
    )
else:
    print(f"\nM8AX - Frecuencia De Muestreo Seleccionada: {sample_rate} Hz")
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
if metetag == "si":
    print("\nM8AX - MetaTags Añadidos Correctamente...")
else:
    print("\nM8AX - MetaTags Originales Mantenidos Correctamente...")
print(
    f"\nM8AX - Número Total De Archivos De Música Convertidos: {len(files_to_convert)} Archivos De Música..."
)
print(
    f"\nM8AX - Tiempo Total De Conversión A OPUS: {elapsed_time:.5f} Segundos. | {conv_days} Días, {conv_hours} Horas, {conv_minutes} Minutos Y {conv_seconds} Segundos"
)
print(
    f"\nM8AX - Duración Total De Todos Los Archivos De Música: {days} Días, {hours} Horas, {minutes} Minutos Y {seconds} Segundos"
)
print(
    f"\nM8AX - Duración Media De Cada Archivo De Música: {avg_days} Días, {avg_hours} Horas, {avg_minutes} Minutos Y {avg_seconds} Segundos"
)
print(f"\nM8AX - Archivos Convertidos Por Segundo: {files_per_second:.5f}")
print(f"\nM8AX - Tamaño Total Antes De La Conversión: {initial_total_size:.5f} MB")
print(f"\nM8AX - Tamaño Total Después De La Conversión: {final_total_size:.5f} MB")
print(f"\nM8AX - Porcentaje De Compresión Conseguido: {compression_percentage:.5f}%")
print(
    f"\nM8AX - MB Leídos Para Comprimir Por Segundo: {(initial_total_size/elapsed_time):.5f} MB/s"
)
print(f"\nM8AX - MB Grabados Por Segundo: {(final_total_size/elapsed_time):.5f} MB/s")
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
    f"--------  M8AX - CADENA DE FFMPEG UTILIZADA PARA LA CONVERSIÓN - M8AX --------\n"
)
with open("M8AX-Lista-FFmpeg.TxT", "r") as f:
    ffmpeg_cmd_string = f.read()  # Leo El Archivo

if os.path.exists("M8AX-Lista-FFmpeg.TxT"):
    os.remove("M8AX-Lista-FFmpeg.TxT")  # Borra El Archivo

print(ffmpeg_cmd_string)
print(
    f"\nM8AX - Número De Ficheros Procesados: {mviiiax.value}, El Cual Coincide Con Los Convertidos... ((( TODO OK )))"
)
print(f"\nBy MarcoS OchoA DieZ - http://youtube.com/m8ax\n")