import csv
import sys
from datetime import datetime

def cargar_datos_csv(nombre_archivo):
    cheques = []
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                cheques.append(fila)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {nombre_archivo}.")
        sys.exit(1)
    return cheques

def validar_filtros(cheques, dni, estado=None, fecha_rango=None):
    cheques_filtrados = [cheque for cheque in cheques if cheque['DNI'] == dni]

    if estado:
        cheques_filtrados = [cheque for cheque in cheques_filtrados if cheque['Estado'].lower() == estado.lower()]
    if fecha_rango:
        fecha_inicio, fecha_fin = map(lambda x: datetime.strptime(x, '%Y-%m-%d'), fecha_rango.split(':'))
        cheques_filtrados = [
            cheque for cheque in cheques_filtrados
            if fecha_inicio <= datetime.strptime(cheque['FechaPago'], '%Y-%m-%d %H:%M:%S') <= fecha_fin
        ]

    return cheques_filtrados

def mostrar_cheques_pantalla(cheques):
    print("NroCheque | CodigoBanco | CodigoSucursal | NumeroCuentaOrigen | NumeroCuentaDestino | Valor | FechaOrigen | FechaPago | DNI | Estado")
    for cheque in cheques:
        print(f"{cheque['NroCheque']} | {cheque['CodigoBanco']} | {cheque['CodigoSucursal']} | {cheque['NumeroCuentaOrigen']} | "
              f"{cheque['NumeroCuentaDestino']} | {cheque['Valor']} | {cheque['FechaOrigen']} | {cheque['FechaPago']} | {cheque['DNI']} | {cheque['Estado']}")

def exportar_cheques_csv(cheques, dni):
    nombre_archivo = f"{dni}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        campos = ['NroCheque', 'CodigoBanco', 'CodigoSucursal', 'NumeroCuentaOrigen', 'NumeroCuentaDestino',
                  'Valor', 'FechaOrigen', 'FechaPago', 'DNI', 'Estado']
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(cheques)
    print(f"Cheques exportados exitosamente a {nombre_archivo}")

def main():
    if len(sys.argv) < 5:
        print("Uso: python listado_cheques.py <archivo_csv> <DNI> <Salida> <TipoCheque> [<Estado>] [--fecha <YYYY-MM-DD:YYYY-MM-DD>]")
        sys.exit(1)

#esto imprimiria por pantalla
    archivo_csv = sys.argv[1]
    dni = sys.argv[2]
    salida = sys.argv[3].upper()  # PANTALLA o CSV
    tipo_cheque = sys.argv[4].upper()  # EMITIDO o DEPOSITADO
    estado = None
    fecha_rango = None

    # Validar estado y rango de fechas
    if len(sys.argv) > 5:
        estado = sys.argv[5]
    if '--fecha' in sys.argv:
        fecha_rango_index = sys.argv.index('--fecha') + 1
        if fecha_rango_index < len(sys.argv):
            fecha_rango = sys.argv[fecha_rango_index]

    # Cargar datos
    cheques = cargar_datos_csv(archivo_csv)

    # Filtrar los cheques 
    cheques_filtrados = validar_filtros(cheques, dni, estado, fecha_rango)
    if salida == 'PANTALLA':
        mostrar_cheques_pantalla(cheques_filtrados)
    elif salida == 'CSV':
        exportar_cheques_csv(cheques_filtrados, dni)
    else:
        print("Error: La salida debe ser 'PANTALLA' o 'CSV'.")

if __name__ == '__main__':
    main()
