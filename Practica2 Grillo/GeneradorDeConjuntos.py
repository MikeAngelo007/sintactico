import sys

listaTranformaciones = {}
primeros = {}
siguientes = {}
predicciones = {}

def primero( noTerminal ):
	#Crea la llave si no existe
	if noTerminal not in primeros:
		primeros[ noTerminal ] = []
	#Mira cada transformacion del noTerminal
	for transformacion in listaTranformaciones[ noTerminal ]:
		caracter = ord( transformacion[ 0 ][ 0 ] )
		#Mira si el primer valor de la transformacion es un no terminal.
		if caracter > 64 and caracter < 91:
			siguienteNoTerminal = primero( transformacion[ 0 ] )
			for i in siguienteNoTerminal:
				if i not in primeros[ noTerminal ]:
					primeros[ noTerminal ].append( i )
			cont = 1
			#Si el ultimo valor de la transformacion es un no terminal, con epsilon buscara el siguiente
			while 'epsilon' in siguienteNoTerminal and len( transformacion ) > cont:
				primeros[ noTerminal ].remove( 'epsilon' )
				caracter = ord( transformacion[ cont ][ 0 ] )
				if caracter > 64 and caracter < 91:
					siguienteNoTerminal = primero( transformacion[ cont ] )
					for i in siguienteNoTerminal:
						if i not in primeros[ noTerminal ]:
							primeros[ noTerminal ].append( i )
					cont += 1
				else:
					if transformacion[ 0 ] not in primeros[ noTerminal ]:
						primeros[ noTerminal ].append( transformacion[ cont ] )
					break
		#Si es un terminal lo anade a la lista de primeros
		else:
			if transformacion[ 0 ] not in primeros[ noTerminal ]:
				primeros[ noTerminal ].append( transformacion[ 0 ] )
	return primeros[ noTerminal ]

def siguiente( noTerminal ):
	#Busca los no terminales dentro de las transformaciones del resto
	for llave in listaTranformaciones:
		for transformacion in listaTranformaciones[ llave ]:
			if noTerminal in transformacion:
				for i in range( len( transformacion ) ):
					if transformacion[ i ] == noTerminal:
						#comprobaciones para siguientes
						cont = i
						while( True ):
							#noTerminal no es el ultimo simbolo en la transformacion
							if cont + 1 < len( transformacion ):
								caracter = ord( transformacion[ cont + 1 ][ 0 ] )
								#siguiente simbolo es un no terminal
								if caracter > 64 and caracter < 91:
									prim = []
									prim += primeros[ transformacion[ cont + 1 ] ]
									#Si no contiene epsilon solo lo agrega
									if 'epsilon' not in prim:
										for i in prim:
											if i not in siguientes[ noTerminal ]:
												siguientes[ noTerminal ].append( i )
										break
									#Busca en el siguiente simbolo del no terminal siguiente del noTerminal
									else:
										prim.remove( 'epsilon' )
										for i in prim:
											if i not in siguientes[ noTerminal ]:
												siguientes[ noTerminal ].append( i )
										cont += 1
								#siguiente simbolo es un terminal
								else:
									if transformacion[ cont + 1 ] not in siguientes[ noTerminal ]:
										siguientes[ noTerminal ].append( transformacion[ cont + 1 ] )
									break
							#Mirar caso de que sea el ultimo
							else:
								for i in siguientes[ llave ]:
									if i not in siguientes[ noTerminal ]:
										siguientes[ noTerminal ].append( i )
								break


def siguienteIterativo():
	cont = 0
	for noTerminal in listaTranformaciones:
		siguiente( noTerminal )
		cont += len( siguientes[ noTerminal ] )
	return cont

cadena = sys.stdin.readline().strip()
linea = cadena.split()
while linea != []:
	noTerminal = linea[ 0 ]
	predicciones[ cadena ] = []
	if noTerminal not in listaTranformaciones:
		listaTranformaciones[ noTerminal ] = []
	listaTranformaciones[ noTerminal ].append( linea[ 1 : len( linea ) ] )
	cadena = sys.stdin.readline().strip()
	linea = cadena.split()

#Carga los conjuntos de primeros y carga vacio en cada llave del conjunto de siguientes
for noTerminal in listaTranformaciones:
	primero( noTerminal )
	siguientes[ noTerminal ] = []
siguientes[ 'S' ].append( 'pesos' )
nuevo = 0
tamano = 1

#Realiza la funcion para complementear todos los conjuntos de siguientes tantas veces como sea necesario
while tamano != nuevo:
	tamano = nuevo
	nuevo = siguienteIterativo()

#Rellena el diccionario de predicciones
for regla in predicciones:
	#Separa el string leido como un arreglo de strings y toma el no terminal de la izquierda
	linea = regla.split()
	llave = linea.pop( 0 )
	while linea != "":
		noTerminal = linea.pop( 0 )
		caracter = ord( noTerminal[ 0 ] )
		#verifica si el primero es terminal y rellena con el mismo.
		if not ( caracter > 64 and caracter < 91 ) and noTerminal != 'epsilon':
			if noTerminal not in predicciones[ regla ]:
				predicciones[ regla ].append( noTerminal )
			break
		#rellena la prediccion con el siguiente del terminal
		elif noTerminal == 'epsilon':
			for i in siguientes[ llave ]:
				if i not in predicciones[ regla ]:
					predicciones[ regla ].append( i )
			break

		#Si el elemento era un terminal, guarda sus primeros en las predicciones
		prim = []
		prim += primeros[ noTerminal ]
		if 'epsilon' not in prim:
			for i in prim:
				if i not in predicciones[ regla ]:
					predicciones[ regla ].append( i )
			break
		#Si contenia vacio, lo elimina y mira el siguiente
		else:
			prim.remove( 'epsilon' )
			for i in prim:
				if i not in predicciones[ regla ]:
					predicciones[ regla ].append( i )
	#Si termina de iterar sobre la regla y esta se acaba, rellena la prediccion con los siguientes
	else:
		for i in siguientes[ llave ]:
			if i not in predicciones[ regla ]:
				predicciones[ regla ].append( i )


print("Primeros")
for i in primeros:
	print(i,primeros[i])
print("\nSiguientes")
for i in siguientes:
	print(i,siguientes[i])
print("\nPredicciones")
for i in predicciones:
	print(i,predicciones[i])