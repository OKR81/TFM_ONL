# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 17:23:00 2024

@author: Óscar Núñez López
"""

import tkinter as tk
from tkinter import filedialog
import random

# Tabla de propiedades según Kyte-Doolittle y cargas
tabla_kyte_doolittle = {
    'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5,
    'CYS': 2.5, 'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4,
    'HIS': -3.2, 'ILE': 4.5, 'LEU': 3.8, 'LYS': -3.9,
    'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6, 'SER': -0.8,
    'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2
}

tabla_cargas = {
    'ALA': 0, 'ARG': 1, 'ASN': 0, 'ASP': -1,
    'CYS': 0, 'GLN': 0, 'GLU': -1, 'GLY': 0,
    'HIS': 1, 'ILE': 0, 'LEU': 0, 'LYS': 1,
    'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
    'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0
}

hidrofobicos = ['ALA', 'ILE', 'LEU', 'MET', 'PHE', 'TRP', 'VAL', 'CYS', 'GLY', 'PRO']
hidrofilicos_positivos = ['ARG', 'LYS', 'HIS']
hidrofilicos_negativos = ['ASP', 'GLU']
hidrofilicos_neutros = ['ASN', 'GLN', 'SER', 'THR', 'TYR']

# Función para abrir el archivo y leer sus contenidos
def abrir_archivo():
    try:
        root = tk.Tk()
        root.withdraw()
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona el archivo de texto del pocket",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        root.destroy()
        if not ruta_archivo:
            print("No se seleccionó ningún archivo.")
            return None
        with open(ruta_archivo, 'r') as archivo:
            datos = archivo.readlines()
        return datos
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return None

# Función para extraer los datos del archivo
def extraer_datos(datos):
    try:
        carga_objetivo = int([line.split(":")[1].strip() for line in datos if "Carga total del pocket" in line][0])
        hidrofobicidad_objetivo = float([line.split(":")[1].strip() for line in datos if "Hidrofobicidad total del pocket" in line][0])
        secuencia_molde = [line.split(":")[1].strip() for line in datos if "Secuencia de aminoácidos del pocket" in line][0].split()
        return carga_objetivo, hidrofobicidad_objetivo, secuencia_molde
    except IndexError:
        print("Error: Formato del archivo incorrecto.")
        return None, None, None

# Función para generar una secuencia compatible
def generar_secuencia(secuencia_molde, carga_objetivo):
    secuencia_nueva = []
    suma_carga = 0
    carga_complementaria = -carga_objetivo

    for aa in secuencia_molde:
        if aa in hidrofobicos:
            compatible = random.choice(hidrofobicos)
        elif aa in hidrofilicos_positivos:
            compatible = random.choice(hidrofilicos_negativos)
        elif aa in hidrofilicos_negativos:
            compatible = random.choice(hidrofilicos_positivos)
        elif aa in hidrofilicos_neutros:
            compatible = random.choice(hidrofilicos_neutros)
        else:
            compatible = aa  # Si no pertenece a ninguna categoría conocida
        secuencia_nueva.append(compatible)
        suma_carga += tabla_cargas[compatible]

    return secuencia_nueva

# Programa principal
def main():
    while True:
        print("Seleccione un archivo para comenzar.")
        datos = abrir_archivo()
        if not datos:
            print("No se seleccionó ningún archivo. Terminando el programa.")
            break

        carga_objetivo, hidrofobicidad_objetivo, secuencia_molde = extraer_datos(datos)
        if not secuencia_molde:
            print("Error al procesar el archivo. Verifica el formato.")
            continue

        print("Generando secuencias compatibles...")
        secuencias = []
        for _ in range(10):  # Generar 10 secuencias
            secuencia = generar_secuencia(secuencia_molde, carga_objetivo)
            carga_total = sum(tabla_cargas[aa] for aa in secuencia)
            hidrofobicidad_total = sum(tabla_kyte_doolittle[aa] for aa in secuencia)
            secuencias.append((secuencia, carga_total, hidrofobicidad_total))

        # Ordenar secuencias de mayor a menor hidrofobicidad
        secuencias.sort(key=lambda x: abs(x[2] - hidrofobicidad_objetivo))

        salida = []
        for secuencia, carga_total, hidrofobicidad_total in secuencias:
            etiqueta = " (Más cercana a la hidrofobicidad objetivo)" if abs(hidrofobicidad_total - hidrofobicidad_objetivo) == min(
                abs(h[2] - hidrofobicidad_objetivo) for h in secuencias
            ) else ""
            linea = f"Secuencia: {' '.join(secuencia)} | Carga: {carga_total} | Hidrofobicidad: {hidrofobicidad_total:.2f}{etiqueta}"
            print(linea)
            salida.append(linea)

        guardar = input("¿Desea guardar la salida en un archivo? (s/n): ").strip().lower()
        if guardar == 's':
            with open(filedialog.asksaveasfilename(defaultextension=".txt"), 'w') as archivo:
                archivo.write("\n".join(salida))
                print("Archivo guardado.")

        repetir = input("¿Desea procesar otro archivo? (s/n): ").strip().lower()
        if repetir != 's':
            break

if __name__ == "__main__":
    main()
