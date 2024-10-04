
# Generar un archivo de texto para probar el programa
with open('archivo.txt', 'w') as file:
    file.write('44556677,1234,EMITIDO,1000\n')
    file.write('44556677,5678,RECIBIDO,2000\n')
    file.write('44556677,9101,EMITIDO,1500\n')
    file.write('11223344,1213,EMITIDO,3000\n')
    file.write('11223344,1415,RECIBIDO,4000\n')

# Leer el archivo de texto en modo lectura
with open('archivo.txt', 'r') as file:

    # Crear un diccionario vacio
    dicc = {}

    for line in file:
        #Separa los valores de la linea por coma
        valores = line.split(',')
        #Si no esta el DNI en el diccionario lo agrega junto con la transferencia
        if valores[0] not in dicc.keys():
            #DNI                  Codigo         datos de cada transferencia
            dicc[valores[0]] = [{'codigo': valores[1],  'estado': valores[2], 'monto': valores[3].replace('\n', '')}]
        else:
            #Si ya esta el DNI en el diccionario agrega la transferencia
            dicc[valores[0]].append({'codigo': valores[1],  'estado': valores[2], 'monto': valores[3].replace('\n', '')})




#Imprimir transferencias de un DNI en particular con sus datos
dni = '44556677'
for transferencias in dicc[dni]:
    print(f"Transferencia: {transferencias['codigo']}")
    print(f"Estado: {transferencias['estado']}")
    print(f"Monto: {transferencias['monto']}")
    print('-----------------')
        





             