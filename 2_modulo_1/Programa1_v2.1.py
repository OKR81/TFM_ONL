# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:55:00 2024

@author: Óscar Núñez López
"""

# -*- coding: utf-8 -*-
"""
Programa para analizar secuencias de aminoácidos en pockets.

"""

import tkinter as tk
from tkinter import filedialog

# Diccionario de hidrofobicidad de cada aminoácido basado en valores de Kyte-Doolittle
hidrofobicidad = {
    'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
    'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8,
    'TRP': -0.9, 'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLU': -3.5,
    'GLN': -3.5, 'ASP': -3.5, 'ASN': -3.5, 'LYS': -3.9, 'ARG': -4.5
}

# Diccionario que asigna la carga eléctrica a cada aminoácido
carga = {
    'ARG': 1, 'LYS': 1, 'ASP': -1, 'GLU': -1,
    'ILE': 0, 'VAL': 0, 'LEU': 0, 'PHE': 0, 'CYS': 0, 'MET': 0,
    'ALA': 0, 'GLY': 0, 'THR': 0, 'SER': 0, 'TRP': 0, 'TYR': 0,
    'PRO': 0, 'HIS': 1, 'GLN': 0, 'ASN': 0
}

def seleccionar_archivo():
    """Abre un cuadro de diálogo para seleccionar un archivo."""
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

def guardar_archivo_como(texto):
    """Abre un cuadro de diálogo para guardar un archivo."""
    root = tk.Tk()
    root.withdraw()
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if ruta_guardado:
        try:
            with open(ruta_guardado, 'w') as archivo:
                archivo.write(texto)
            print(f"Resultados guardados exitosamente en {ruta_guardado}")
        except Exception as e:
            print(f"Error al guardar los resultados: {e}")

def leer_archivo_y_contar_aminoacidos(ruta_archivo):
    """
    Lee un archivo y cuenta los aminoácidos de cada pocket mientras
    mantiene el orden en que aparecen en el archivo.
    """
    conteo_aminoacidos = {}  # Diccionario para conteo de aminoácidos
    secuencia_pockets = {}   # Diccionario para secuencia ordenada de aminoácidos
    try:
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                partes = linea.split()
                if len(partes) > 11:  # Validar formato esperado
                    aminoacido = partes[3]
                    pocket = partes[11]
                    if pocket.isdigit():
                        # Crear la lista si el pocket no existe aún
                        if pocket not in secuencia_pockets:
                            secuencia_pockets[pocket] = []
                        # Añadir el aminoácido en orden
                        secuencia_pockets[pocket].append(aminoacido)

                        # Actualizar el conteo de aminoácidos por pocket
                        if pocket not in conteo_aminoacidos:
                            conteo_aminoacidos[pocket] = {}
                        if aminoacido in conteo_aminoacidos[pocket]:
                            conteo_aminoacidos[pocket][aminoacido] += 1
                        else:
                            conteo_aminoacidos[pocket][aminoacido] = 1
    except FileNotFoundError:
        print("El archivo no fue encontrado. Por favor, verifica la ruta proporcionada.")
        return {}, {}
    return conteo_aminoacidos, secuencia_pockets

def mostrar_pockets_disponibles(conteo_aminoacidos):
    """Muestra los pockets disponibles y el total de aminoácidos en cada uno."""
    print("Pockets disponibles y total de aminoácidos en cada uno:")
    for pocket in sorted(conteo_aminoacidos.keys(), key=int):
        total_aminoacidos = sum(conteo_aminoacidos[pocket].values())
        print(f"Pocket {pocket}: {total_aminoacidos} aminoácidos total")

def mostrar_detalle_pocket(conteo_aminoacidos, secuencia_pockets, pocket_elegido):
    """
    Muestra detalles de un pocket específico, asegurando que la secuencia
    esté en el orden correcto.
    """
    resultado = ""
    if pocket_elegido in conteo_aminoacidos:
        resultado += f"Detalles para el Pocket {pocket_elegido}:\n"
        carga_total = 0
        hidrofobicidad_total = 0
        total_aminoacidos = sum(conteo_aminoacidos[pocket_elegido].values())

        # Analizar cada aminoácido en el pocket
        for aminoacido, conteo in conteo_aminoacidos[pocket_elegido].items():
            porcentaje = (conteo / total_aminoacidos) * 100
            resultado += f"  {aminoacido}: {conteo} veces ({porcentaje:.2f}%)\n"
            carga_total += carga.get(aminoacido, 0) * conteo
            hidrofobicidad_total += hidrofobicidad.get(aminoacido, 0) * conteo

        # Agregar los resultados finales
        resultado += f"Carga total del pocket: {round(carga_total, 3)}\n"
        resultado += f"Hidrofobicidad total del pocket: {round(hidrofobicidad_total, 3)}\n"
        # Mantener el orden de la secuencia
        secuencia_aminoacidos = " ".join(secuencia_pockets[pocket_elegido])
        resultado += f"Secuencia de aminoácidos del pocket: {secuencia_aminoacidos.strip()}\n"
    else:
        resultado += "No se encontraron datos para el pocket seleccionado.\n"
    return resultado

def procesar_archivo():
    """
    Gestiona el flujo principal del programa: selecciona archivo,
    muestra detalles de pockets y permite guardar resultados.
    """
    ruta_archivo = seleccionar_archivo()
    if ruta_archivo:
        conteo_aminoacidos, secuencia_pockets = leer_archivo_y_contar_aminoacidos(ruta_archivo)
        if conteo_aminoacidos:
            print(f"Procesando archivo: {ruta_archivo}")
            mostrar_pockets_disponibles(conteo_aminoacidos)
            pocket_elegido = input("Por favor, introduce el número de pocket que deseas analizar: ")
            resultados = mostrar_detalle_pocket(conteo_aminoacidos, secuencia_pockets, pocket_elegido)
            print(resultados)
            if input("¿Deseas guardar los resultados? (s/n): ").lower() == 's':
                guardar_archivo_como(resultados)
        else:
            print("No se encontraron datos en el archivo proporcionado.")
    else:
        print("No se seleccionó ningún archivo.")

def main():
    """Ejecuta el programa en un bucle hasta que el usuario decida salir."""
    while True:
        procesar_archivo()
        if input("¿Deseas analizar otro archivo? (s/n): ").lower() != 's':
            break

if __name__ == "__main__":
    main()
