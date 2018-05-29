import sys
listaTranformaciones = {}
primeros = {}
siguientes = {}
predicciones = {}
prediccionesNoTerminales = {}

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
			#Si el ultimo valor de la transformacion es un no terminal con epsilon buscara el siguiente
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
	while linea != []:
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

noTerminales = primeros.keys( )
noTerminales.sort( )
with open( 'AnalizadorSintactico.py', 'w' ) as f:
	sys.stdout = f
	print "#Lenguajes de Programacion\n#Practica 2: Analizador Sintactico\n#Nicolas Leonardo Maldonado Garzon  2879709\n#Joan Sebastian Contreras Pena	  2879782"
	print "import sys\n"
	print "palabra = [ 'integer', 'single', 'long', 'double', 'string',\n            'dim', 'as', 'print', 'input',\n            'if', 'else', 'end', 'then', 'select', 'case',\n            'while', 'wend', 'do', 'loop', 'until', 'for',\n            'to', 'next', 'step', 'sub', 'shared', 'function',\n            'const', 'sub' ]" 
	t = "\t"
	print ""
	print "simbolos = {"
	print t +"#Operadores Relacionales"
	print t +"\"<\" : \"token_menor\","
	print t +"\">\" : \"token_mayor\","
	print t +"\"=\" : \"token_igual\","
	print t +"\"<=\" : \"token_menor_igual\","
	print t +"\">=\" : \"token_mayor_igual\", "
	print t +"\"<>\" : \"token_dif\","
	print t +"#Operadores Logicos"
	print t +"\"and\" : \"and\","
	print t +"\"or\" : \"or\","
	print t +"\"not\" : \"not\","
	print t +"\"xor\" : \"xor\","
	print t +"#Operadores Aritmeticos"
	print t +"\"+\" : \"token_mas\","
	print t +"\"-\" : \"token_menos\","
	print t +"\"*\" : \"token_mul\","
	print t +"\"/\" : \"token_div\","
	print t +"\"^\" : \"token_pot\","
	print t +"\"mod\" : \"mod\","
	print t +"#Signos de Puntuacion"
	print t +"\",\" : \"token_coma\","
	print t +"\";\" : \"token_pyc\","
	print t +"\"(\" : \"token_par_izq\","
	print t +"\")\" : \"token_par_der\","
	print t +"#Tipos de dato"
	print t +"\"%\" : \"token_porcentaje\","
	print t +"\"&\" : \"token_ampersand\","
	print t +"\"!\" : \"token_admiracion\","
	print t +"\"#\" : \"token_numeral\","
	print t +"\"$\" : \"token_pesos\","
	print "}\n"
	print "TOKENS = []"
	print "class TOKEN:"
	print "\tdef __init__( self ):"
	print t + "\tself.token = \"\""
	print t + "\tself.tipo = \"\""
	print t + "\tself.fila = 0"
	print t + "\tself.columna = 0\n"
	print "\tdef __init__( self, token , tipo , fila , columna ):"
	print t + "\tself.token = token"
	print t + "\tself.tipo = tipo"
	print t + "\tself.fila = fila"
	print t + "\tself.columna = columna"
	print "numeroLinea = 1"
	print "stopProcess = False"
	print "token = TOKEN( \"\", \"EOF\", 0, 0 )\n"

#creador de las funciones
	for noTerminal in noTerminales:
		prediccionesNoTerminales[ noTerminal ] = []
		t = "\t"
		print "def " + noTerminal + "( ):"
		print t + "print \"entro a " + noTerminal + "\", token.token"
		cont = 0
		for i in predicciones:
			trans = i.split( )
			if noTerminal == trans[ 0 ]:
				if cont != 0:
					t += "el"
				print t + "if token.token in", predicciones[i], " or token.tipo in", predicciones[ i ], ":"
				prediccionesNoTerminales[ noTerminal ] += predicciones[i]
				if cont != 0:
					t = t[ : 1 ]
				t += "\t"
				for token in trans[ 1: len( trans ) ]:
					caracter = ord( token[ 0 ] )
					if caracter > 64 and caracter < 91:
						print t + token + "( );"
					else:
						print t + "emparejar( '" + token + "' )"
				t = t[ 1 : ]
				cont += 1
		print t + "else:"
		t += "\t"
		print t + "errorSintaxis(", prediccionesNoTerminales[ noTerminal ], " )"
		print "\tprint \"sale de " + noTerminal + "\", token.token\n"
	print ""
	print "def errorSintaxis( lista ):"
	t = "\t"
	print t + "global stopProcess"
	print t + "if type( lista ) is list:"
	print t + "\tlista.sort( )"
	print t + "error = token.token"
	print t + "if token.tipo == 'identificador':"
	print t + "\terror = 'identificador'"
	print t + "print '<' + str( token.fila ) + ':' + str( token.columna ) + \"> Error sintactico: se encontro: '\" + error + \"'; se esperaba: '\" + \"', '\".join( lista ) + \"'.\""
	print t + "stopProcess = True"
	print t + "sys.exit(0)"

	t = t[ 1 : ]

	print ""
	print "def emparejar( tokEsperado ):"
	t = "\t"
	print t + "global token"
	print t + "if tokEsperado != 'epsilon':"
	t += "\t"
	print t + "if token.token in tokEsperado or token.tipo == tokEsperado:"
	t += "\t"
	print t + "token = TOKENS.pop( 0 )"
	t = t[ 1: ]
	print t + "else:"
	t += "\t"
	print t + "errorSintaxis( tokEsperado )"

	t = "\t"
	print "def simb( subs ):"
	print t + "caracter = ord( subs[ 0 ] )"
	print t + "if caracter in range( 60 , 63):"
	print t + "\treturn \"relacion\""
	print t + "elif caracter in range( 33 , 39 ):"
	print t + "\treturn \"tipo_de_dato\""
	print t + "elif caracter == 40 or caracter == 41:"
	print t + "\treturn \"parentesis\""
	print t + "elif caracter == 44 or caracter == 59:"
	print t + "\treturn \"puntuacion\""
	print t + "else: return \"operador\""

	print ""
	print "#Clasificar entre palabras reservadas, variables, Strings y simbolos."
	print "def busquedaDic( subs, ind ):"
	t = "\t"
	print t + "if simbolos.get( subs.lower( ) ) != None:"
	t += "\t"
	print t + "#print '<' + simbolos.get( subs.lower( ) ) + ',' + str( numeroLinea ) + ',' + str( ind + 1 ) + '>'"
	print t + "simbol = subs.lower( )"
	print t + "simbolType = simb( subs.lower( ) )" 
	print t + "tok = TOKEN( simbol , simbolType , str( numeroLinea ) , str ( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = "\t"
	print t + "elif subs.lower( ) in palabra:"
	t += "\t"
	print t + "#print '<' + subs.lower( ) + ',' + str( numeroLinea ) + ',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( subs.lower( ) , \"palabra reservada\" , str( numeroLinea ) , str( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = "\t"
	print t + "elif subs[ 0 ] != ' ' :"
	t += "\t"
	print t + "if subs[ 0 ] == '\"':"
	t += "\t"
	print t + "#print '<token_string,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( 'valor_string', 'valor', str( numeroLinea ) , str ( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = t[ 1 : ]
	print t + "else:"
	t += "\t"
	print t + "#print '<id,' + subs.lower() + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( subs.lower(), \"identificador\" , str( numeroLinea ) , str ( ind + 1 ) )"
	print t + "TOKENS.append( tok )"

	print ""
	print "#Clasificar numeros enteros"
	print "def entero( subs, ind ):"
	t = "\t"
	print t + "i = int( subs )"
	print t + "#REVISAR HASTA QUE PUNTO ES INTEGER, SI HASTA 32767 O HASTA 32766"
	print t + "if( i > 32767 ):"
	t += "\t"
	print t + "#print '<token_long,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( 'valor_long', 'valor', str( numeroLinea ) , str( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = "\t"
	print t + "else:"
	t += "\t"
	print t + "#print '<token_integer,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( 'valor_integer', 'valor', str( numeroLinea ) , str( ind + 1 ) )"
	print t + "TOKENS.append( tok )"

	print ""
	print "#Clasificar numeros decimales"
	print "def decimal( subs, ind ):"
	t = "\t"
	print t + "for i in range( len( subs ) ):"
	t += "\t"
	print t + "if subs[ i ] == '.':"
	t += "\t"
	print t + "break"
	t = "\t"
	print t + "if len( subs ) - i > 7:"
	t += "\t"

	print ""
	print t + "#print '<token_double,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( 'valor_double', 'valor', str( numeroLinea ) , str( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = "\t"
	print t + "else:"
	t += "\t"
	print t + "#print '<token_single,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'"
	print t + "tok = TOKEN( 'valor_single', 'valor', str( numeroLinea ) , str( ind + 1 ) )"
	print t + "TOKENS.append( tok )"
	t = "\t"

	print ""
	print "#Numero antes de que se ingresara un punto sin tener otro numero despues y error."
	print "def errorPunto( subs, ind ):"
	print t +"for i in range( len( subs ) ):"
	t += "\t"
	print t +"if subs[ i ] == '.':"
	t += "\t"
	print t +"break;"
	t = "\t"
	print t +"numero = subs[ : i ]"
	print t +"entero( numero, ind )"
	print t +"print \">>> Error lexico (linea: \" + str( numeroLinea ) + \", posicion: \" + str( ind + i + 1 ) + \")\""

	print ""
	print "def automata( linea, ind ):"
	t = "\t"
	print t + "index = ind"
	print t + "estado = 0"
	print t + "while True:"
	t += "\t"
	print t + "estado = delta( estado, linea[ index ] )"
	print t + "index += 1"
	print t + "if not ( index < len( linea ) and estado < 10 and estado >= -1 ):"
	t += "\t"
	print t + "break"
	t = "\t"
	print t + "index -= 1"
	print t + "if estado == 1:"
	print t + "\t#Variable o palabra reservada"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "elif estado == 2:"
	print t + "\t#Numero entero"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tentero( subs, ind )"
	print t + "elif estado == 3:"
	print t + "\t#Decimal"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tdecimal( subs, ind )"
	print t + "elif estado == 4:"
	print t + "\t#Simbolo reservado o dobles( <>, <= o >= )"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "elif estado == 5:"
	print t + "\t#Simbolo <"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "elif estado == 6:"
	print t + "\t#Simbolo >"
	print t + "\tsubs = linea[ ind : index + 1 ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "#Cadenas"
	print t + "elif estado == 7:"
	print t + "\t#String"
	print t + "\tsubs = linea[ind : index + 1 ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "elif estado == 9:"
	print t + "\t#Espacio al punto"
	print t + "\tsubs = linea[ ind : index ]"
	print t + "\terrorPunto( subs, ind )"
	print t + "#Lexemas aceptados pero que no son fin de cadena"
	print t + "elif estado == 11:"
	print t + "\t#Strings, variables y simbolos."
	print t + "\tsubs = linea[ ind : index ]"
	print t + "\tbusquedaDic( subs, ind )"
	print t + "elif estado == 12:"
	print t + "\t#Enteros"
	print t + "\tsubs = linea[ ind : index ]"
	print t + "\tentero( subs, ind )"
	print t + "elif estado == 13:"
	print t + "\t#Decimales"
	print t + "\tsubs = linea[ ind : index ]"
	print t + "\tdecimal( subs, ind )"
	print t + "#Errores Lexicos"
	print t + "elif estado == -1:"
	print t + "\t#String sin comillas de cierre"
	print t + "\tprint \">>> Error lexico (linea: \" + str( numeroLinea ) + \", posicion: \" + str( ind + 1 ) + \")\" "
	print t + "elif estado == -2:"
	print t + "\t#. y no viene de numeros"
	print t + "\tsubs = linea[ ind : index ]"
	print t + "\terrorPunto( subs, ind )"
	print t + "elif estado == -3:"
	print t + "\t#Caracter no valido"
	print t + "\tprint \">>> Error lexico (linea: \" + str( numeroLinea ) + \", posicion: \" + str( ind + 1 ) + \")\""
	print t + "return [ index , estado ]"

	print ""
	print "def delta( estado , caracter ):"
	print t + "caracter = ord( caracter )"
	print t + "#Estado inicial"
	print t + "if estado == 0:"
	t += "\t"
	print t +"if( ( caracter > 64 and caracter < 91) or ( caracter > 96 and caracter < 123 ) ):"
	print t +"\treturn 1#Empieza por letra"
	print t +"elif( caracter > 47 and caracter < 58 ):"
	print t +"\treturn 2#Empieza por numero"
	print t +"elif( (caracter > 32 and caracter < 48 and caracter !=  34 and caracter != 39 and caracter != 46 ) or caracter == 59 or caracter == 61 or caracter == 94 ):"
	print t +"\treturn 4#Es un simbolos reservado de un caracter"
	print t +"elif( caracter == 60 ):"
	print t +"\treturn 5#Empieza por <"
	print t +"elif( caracter == 62 ):"
	print t +"\treturn 6#Empieza por >"
	print t +"elif ( caracter == 32 ):"
	print t +"\treturn 8#Espacio"
	print t +"elif( caracter == 39 ):"
	print t +"\treturn 10#Comentario"
	print t +"elif( caracter == 34 ):"
	print t +"\treturn -1#Comilla de apertura"
	print t +"elif( caracter == None or caracter == 10 ):"
	print t +"\treturn 0"
	print t +"else:"
	print t +"\treturn -3#Caracter no permitido"
	print t +"#Variables o palabras reservadas"
	t = t[ 1 : ]
	print t +"elif estado == 1:"
	t += "\t"
	print t +"if ( ( caracter > 64 and caracter < 91 ) or ( caracter > 96 and caracter < 123 ) or ( caracter > 47 and caracter < 58 ) or caracter == 95 ):"
	print t +"\treturn 1#Siguen letras, numeros o '_'"
	print t +"else:"
	print t +"\treturn 11#Si es otro valor"
	t = t[ 1 : ]
	print t +"#Numeros enteros y decimales"
	print t +"elif estado == 2:"
	t += "\t"
	print t +"if ( caracter > 47 and caracter < 58 ):"
	print t +"\treturn 2#Si es un numero"
	print t +"elif ( caracter == 46 ):"
	print t +"\treturn 9#Si es un punto"
	print t +"else:"
	print t +"\treturn 12#Si es otro valor"
	t = t[ 1 : ]
	print t +"#Numeros decimales"
	print t +"elif estado == 3:"
	print t +"\tif ( caracter > 47 and caracter < 58 ):"
	print t +"\t\treturn 3#Es un numero, parte decimal"
	print t +"\telse:"
	print t +"\t\treturn 13#Sigue otro valor"
	print t +"#Simbolos reservados"
	print t +"elif estado == 4:"
	print t +"\treturn 11#Hay otro caracter diferente despues de los simbolos reservados"
	print t +"#Simbolo <"
	print t +"elif estado == 5:"
	print t +"\tif ( caracter == 62 or caracter == 61 ):"
	print t +"\t\treturn 4#Es <= o <>"
	print t +"\telse:"
	print t +"\t\treturn 11#Otro valor luego del <"
	print t +"#Simbolo >"
	print t +"elif estado == 6:"
	print t +"\tif ( caracter == 61 ):"
	print t +"\t\treturn 4#Es >="
	print t +"\telse:"
	print t +"\t\treturn 11#Otro valor luego del >"
	print t +"#String completo"
	print t +"elif estado == 7:"
	print t +"\treturn 11#Otro valor luego de la comilla de cierre"
	print t +"#Caracter ' '"
	print t +"elif estado == 8:"
	print t +"\treturn 11#Hay un caracter despues de un espacio"
	print t +"elif estado == 9:"
	print t +"\tif ( caracter > 47 and caracter < 58 ):"
	print t +"\t\treturn 3#Si es un numero"
	print t +"\telse:"
	print t +"\t\treturn -2#Error, caracter diferente despues de un punto"
	print t +"#Caracter '"
	print t +"elif estado == 10:"
	print t +"\treturn 10"
	print t +"#String sin cerrar \""
	print t +"elif estado == -1:"
	print t +"\tif ( caracter == 34 ):"
	print t +"\t\treturn 7#Comilla de cierre"
	print t +"\telse:"
	print t +"\t\treturn -1#No se cerro la comilla"
	print t +"elif estado == -2:"
	print t +"\treturn -2"
	print t +"#Caracter '.' despues de algun numero"
	print t +"return 0"

	print ""
	print "linea = sys.stdin.readline()"
	print "while linea != \"\" : "
	t = "\t"
	print t + "i = [ 0, 0 ]"
	print t + "i = automata( linea , i[ 0 ] )"
	print t + "while i[ 1 ] > 10:"
	t += "\t"
	print t + "i = automata( linea , i[ 0 ] )"
	print t + "if( i[ 1 ] < 0 or i[ 1 ] == 9 ):"
	t += "\t"
	print t + "break"
	t = "\t"
	print t + "numeroLinea += 1"
	print t + "linea = sys.stdin.readline()"
	print t + "token = TOKEN( \"pesos\", \"pesos\", 0, 0 )"
	print t + "TOKENS.append( token )"
	print "token = TOKEN( \"EOF\", \"EOF\", 0, 0 )"
	print "TOKENS.append( token )"
	print "token = TOKENS.pop( 0 )"
	print "while not stopProcess:"
	print t + "S()"
	print t + "token = TOKENS.pop( 0 )"
	print t +"if token.tipo == \"EOF\":"
	t += "\t"
	print t + "print \"El analisis sintactico se ha finalizado correctamente.\""
	print t + "break"
f.close( )