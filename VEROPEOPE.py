import os
import csv


def process_text_file(input_file, output_csv):
    try:
        # Intentar decodificar con UTF-8
        encodings = ['utf-8', 'latin-1']

        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                break
            except UnicodeDecodeError:
                continue

        rows = []

        current_row = []

        for line in lines:
            # Asegurarse de que la línea no esté vacía
            if line.strip():
                # Verificar si la línea comienza una nueva estructura
                if line.startswith("    "):  # Líneas de datos
                    current_row.append(line.rstrip('\n'))  # Mantener el salto de línea al final
                else:
                    # Si hay datos acumulados en current_row, procesarlos como una estructura
                    if current_row:
                        process_row(current_row, rows)
                        current_row = []  # Reiniciar current_row para la próxima estructura

        # Procesar la última estructura si quedó pendiente
        if current_row:
            process_row(current_row, rows)

        # Obtener el nombre del archivo de salida basado en el nombre del archivo de entrada
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_csv = os.path.join(output_csv, f"{file_name}.csv")

        with open(output_csv, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')  # Cambiar el delimitador a punto y coma
            writer.writerow(["CTA", "descr", "fe", "impte", "indenti", "real"])
            for row in rows:
                writer.writerow(row)  # Escribir cada estructura como una línea en el archivo CSV

        print(f"Archivo CSV creado exitosamente en: {output_csv}")

    except Exception as e:
        print(f"Error al procesar el archivo {input_file}: {str(e)}")


def process_row(current_row, rows):
    # Combinar líneas de datos en una sola línea para la estructura
    combined_line = ''.join(current_row)

    # Dividir la línea combinada en campos según el formato esperado
    while combined_line:
        CTA = combined_line[0:6].strip().ljust(6)
        descr = combined_line[6:36].strip().ljust(30)
        fe = combined_line[36:38].strip().ljust(2)
        impte = combined_line[38:54].strip().ljust(16)
        indenti = combined_line[54:55].strip().ljust(1)
        real = combined_line[55:64].strip().ljust(9)

        rows.append([CTA, descr, fe, impte, indenti, real])

        # Avanzar a la siguiente línea dentro de la estructura
        combined_line = combined_line[64:]


def process_text_files(input_folder, output_folder):
    try:
        # Listar todos los archivos en la carpeta de entrada
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Procesar cada archivo de texto en la carpeta de entrada
        for file_name in files:
            input_file = os.path.join(input_folder, file_name)

            # Llamar a process_text_file con el nombre de archivo de salida personalizado
            process_text_file(input_file, output_folder)

    except Exception as e:
        print(f"Error al procesar archivos en la carpeta {input_folder}: {str(e)}")


# Rutas de entrada y salida
input_folder = r'C:\Users\david.albino\Desktop\sopa'
output_folder = r'C:\Users\david.albino\Desktop\CSVs'

# Procesar archivos de texto y convertirlos a CSV
process_text_files(input_folder, output_folder)
