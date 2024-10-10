import csv
from datetime import datetime

def abrir_archivo():
    while True:
        try:
            with open("cheques_large.csv", "r") as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  

                dni = input("Ingresar el DNI: ")
                tipo_cheque = input("Ingresar 'E' si desea emitido o 'D' depositado: ").upper()
                while tipo_cheque not in ['E', 'D']:
                    tipo_cheque = input("Entrada inválida. Ingresar 'E' si desea emitido o 'D' depositado: ").upper()

                salida = input("Ingresar 'PANTALLA' para ver los resultados o 'CSV' para exportar: ").upper()
                estado_cheque = input("Ingresar el estado del cheque ('PENDIENTE', 'APROBADO', 'RECHAZADO') o dejar en blanco para omitir: ").upper()

                rango_fechas = input("Desea filtrar por rango de fechas? Ingrese 'S' para sí o 'N' para no: ").upper()

                fecha_inicio = None
                fecha_fin = None
                if rango_fechas == 'S':
                    fecha_inicio = input("Ingresar la fecha de inicio (YYYY-MM-DD): ")
                    fecha_fin = input("Ingresar la fecha de fin (YYYY-MM-DD): ")

                resultados = []

                for fila in lector_csv:
                    if len(fila) < 11: 
                        print(f"Fila incompleta ignorada: {fila}")
                        continue  

                    cheque_valido = False

                    if tipo_cheque == 'D' and fila[9] == dni and fila[10] == 'DEPOSITADO':
                        cheque_valido = True
                    elif tipo_cheque == 'E' and fila[9] == dni and fila[10] == 'EMITIDO':
                        cheque_valido = True

                    if estado_cheque and cheque_valido:
                        if fila[8] != estado_cheque:  
                            cheque_valido = False

                    if rango_fechas == 'S' and cheque_valido:
                        try:
                            fecha_cheque_str = fila[6]  
                            fecha_cheque = datetime.strptime(fecha_cheque_str, "%Y-%m-%d")
                            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
                            if not (fecha_inicio_dt <= fecha_cheque <= fecha_fin_dt):
                                cheque_valido = False
                        except ValueError as e:
                            print(f"Error al procesar la fecha '{fila[6]}': {e}")
                            cheque_valido = False  

                    if cheque_valido:
                        resultados.append(fila)

                if salida == 'PANTALLA':
                    if resultados:
                        for resultado in resultados:
                            print(" | ".join(resultado))  
                    else:
                        print("No se encontraron resultados.")
                elif salida == 'CSV':
                    with open("resultados_cheques.csv", "w") as archivo_salida:
                        escritor_csv = csv.writer(archivo_salida)
                        escritor_csv.writerows(resultados)
                    print("Resultados guardados en 'resultados_cheques.csv'.")
                else:
                    print("Opción de salida no válida.")

        except FileNotFoundError:
            print("No se pudo abrir el archivo. Verifique que el archivo 'cheques_large.csv' existe.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

        repetir = input("¿Desea realizar otra búsqueda? (S/N): ").upper()
        if repetir != 'S':
            print("Gracias por utilizar el sistema.")
            

abrir_archivo()
