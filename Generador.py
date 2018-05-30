import sys
listaTranformaciones = {}
primeros = {}
siguientes = {}
predicciones = {}
prediccionesNoTerminales = {}

def primero( noTerminal ):
	#Crea la llave si no existe
	if noTerminal not in primeros:
		primeros[noTerminal] = []
	#Mira cada transformacion del noTerminal
	for transformacion in listaTranformaciones[noTerminal]:
		caracter = ord(transformacion[0][0])
		#Mira si el primer valor de la transformacion es un no terminal
		if caracter > 64 and caracter < 91:
			siguienteNoTerminal = primero(transformacion[0])
			for i in siguienteNoTerminal:
				if i not in primeros[noTerminal]:
					primeros[noTerminal].append(i)
			cont = 1
			#Mira si el ultimo valor de la transformacion es un no terminal con epsilon buscara el siguiente
			while 'epsilon' in siguienteNoTerminal and len(transformacion) > cont:
				primeros[noTerminal].remove('epsilon')
				caracter = ord(transformacion[cont][0])
				if caracter > 64 and caracter < 91:
					siguienteNoTerminal = primero(transformacion[cont])
					for i in siguienteNoTerminal:
						if i not in primeros[noTerminal]:
							primeros[noTerminal].append(i)
					cont += 1
				else:
					if transformacion[0] not in primeros[noTerminal]:
						primeros[noTerminal].append(transformacion[cont])
					break
		#Si es un terminal lo anade a la lista de primeros
		else:
			if transformacion[0] not in primeros[noTerminal]:
				primeros[noTerminal].append(transformacion[0])
	return primeros[noTerminal]

def siguiente(noTerminal):
	#Busca los no terminales dentro de las transformaciones del resto
	for llave in listaTranformaciones:
		for transformacion in listaTranformaciones[llave]:
			if noTerminal in transformacion:
				for i in range(len(transformacion)):
					if 	transformacion[i] == noTerminal:
						#Comprobaciones para siguientes
						cont = i
						while True:
							#noTerminal no es el ultimo simbolo en la transformacion
							if cont+1 < len(transformacion):
								caracter = ord(transformacion[cont+1][0])
								#Siguiente simbolo es un no termial
								if caracter > 64 and caracter < 91:
									prim = []
									prim += primeros[transformacion[cont+1]]
									#Si no tiene epsilon solo lo agrega
									if 'epsilon' not in prim:
										for i in prim:
											if i  not in siguientes[noTerminal]:
												siguientes[noTerminal].append(i)
										break
									#Busca en el siguiente simbolo del no termianl siguiente del noTerminal
									else:
										prim.remove('epsilon')
										for i in prim:
											if i not in siguientes[noTerminal]:
												siguientes[noTerminal].append(i)
										cont += 1
								#Siguiente termino es un terminal
								else:
									if transformacion[cont+1] not in siguientes[noTerminal]:
										siguientes[noTerminal].append(transformacion[cont+1])
									break 
							#Mirar caso de que sea el ultimo
							else:
								for i in siguientes[llave]:
									if i not in siguientes[noTerminal]:
										siguientes[noTerminal].append(i)
								break


def siguienteIterativo():
	cont = 0
	for noTerminal in listaTranformaciones:
		siguiente(noTerminal)
		cont += len(siguientes[noTerminal])
	return cont

cadena  = sys.stdin.readline().strip()
linea = cadena.split()
while linea != []:
	noTerminal = linea[0]
	predicciones[cadena] = []
	if noTerminal not in listaTranformaciones:
		listaTranformaciones[noTerminal] = []
	listaTranformaciones[noTerminal].append(linea[1:len(linea)])
	cadena = sys.stdin.readline().strip()
	linea = cadena.split()

# Carga los conjuntos de primeros y carga vacio en cada llave del conjunto de siguientes
for noTerminal in listaTranformaciones:
	primero(noTerminal)
	siguientes[noTerminal] = []
siguientes['S'].append('pesos')
nuevo = 0
tamano = 1

#Realiza la funcion para completar todos los conjuntos de siguientes tantas veces como sea necesario
while tamano != nuevo:
	tamano = nuevo
	nuevo = siguienteIterativo()

#Rellena el diccionario de predicciones
for regla in predicciones:
	#Separa el string leido como un arreglo de strings y toma  el no terminal  de la izquierda
	linea = regla.split()
	llave = linea.pop(0)
	while linea != "":
		noTerminal = linea.pop(0)
		caracter = ord(noTerminal[0])
		#Verifica  si el primero es terminal  y rellena con el mismo
		if not (caracter > 64 and caracter < 91) and noTerminal != 'epsilon':
			if noTerminal not in predicciones[regla]:
				predicciones[regla].append(noTerminal)
			break
		#Rellena  la prediccion  con el siguiente del terminal
		elif noTerminal == 'epsilon':
			for i  in siguientes[llave]:
				if i not in predicciones[regla]:
					predicciones[regla].append(i)
			break

		#Si el elemento era un terminal, guarda sus primeros en las predicciones
		prim = []
		prim += primeros[noTerminal]
		if 'epsilon' not in prim:
			for i in prim:
				if i not in predicciones[regla]:
					predicciones[regla].append(i)
			break
		#Si  contenia vacio, lo elimina  y mira  el siguiente
		else:
			prim.remove('epsilon')
			for i in prim:
				if i not in predicciones[regla]:
					predicciones[regla].append(i)
	#Si termina de iterar sobre  la regla y esta se acaba, rellena la prediccion con los siguientes	
	else:
		for i in siguientes[llave]:
			if i not in predicciones[regla]:
				predicciones[regla].append(i)

noTerminales = sorted(primeros.keys())
with open( 'Parser.py', 'w' ) as f:
	sys.stdout = f
	print("#Lenguajes de Programacion")
	print("import sys\n")
	print("#Palabras Reservadas")
	print("reservadas = ['if','else','elseif','then','for','while','switch','case',\n\t'break','set','puts','default','expr','continue','foreach','incr',\n\t'array','exists','size','proc','gets','stdin','return']")
	t = "\t"
	print("\nsimbolos = {")
	print(t+"'{':'token_llave_izq',")
	print(t+"'}':'token_llave_der',")
	print(t+"'$':'token_dollar',")
	print(t+"';':'token_pyc',")
	print(t+"'[':'token_cor_izq',")
	print(t+"']':'token_cor_der',")
	print(t+"'(':'token_par_izq',")
	print(t+"')':'token_par_der',")
	print(t+"#Operadores Relacionales")
	print(t+"'>=':'token_mayor_igual',")
	print(t+"'<=':'token_menor_igual',")
	print(t+"'eq':'token_igual_str',")
	print(t+"'ne':'token_diff_str',")
	print(t+"'==':'token_igual_num',")
	print(t+"'!=':'token_diff_num',")
	print(t+"'>':'token_mayor',")
	print(t+"'<':'token_menor',")
	print(t+"#Operadores Logicos")
	print(t+"'&&':'token_and',")
	print(t+"'||':'token_or',")
	print(t+"'!':'token_not',")
	print(t+"#Operadores Aritmeticos")
	print(t+"'+':'token_mas',")
	print(t+"'-':'token_menos',")
	print(t+"'*':'token_mul',")
	print(t+"'/':'token_div',")
	print(t+"'%':'token_mod',")
	print(t+"'**':'token_pot'")
	print(t+"}\n")
	print("class Token:")
	print(t+"def __init__( self ):")
	t += "\t"
	print(t+"self.tipo = ''")
	print(t+"self.token = ''")
	print(t+"self.fila = 0")
	print(t+"self.columna = 0\n")
	t = t[1:]
	print(t+"def __init__( self, tipo  , token , fila , columna ):")
	t += "\t"
	print(t+"self.token = token")
	print(t+"self.tipo = tipo")
	print(t+"self.fila = fila")
	print(t+"self.columna = columna\n")
	t = t[1:]
	print(t+"def __str__(self):")
	t += "\t"
	print(t+"return '<%s,%s,%d,%d>' % (self.tipo, self.token, self.fila, self.columna)\n")
	t = t[1:]
	print(t+"def __repr__(self):")
	t += "\t"
	print(t+"return str(self)\n")
	print("Columna = 0")
	print("Fila = 0")
	print("auxToken = ''")
	print("TOKENS = []")
	print("token = Token( 'EOF', 'eof', 0, 0 )")
	print("stopProcess = False\n")
	t = t[1:]
	print("def numero( linea , index , fila, columna ):")
	print(t+"auxToken = linea[ index ]")
	print(t+"index += 1")
	print(t+"punto = False")
	print(t+"")
	print(t+"tipo = 'valor_entero'")
	print(t+"while index < len( linea ) :")
	t += "\t"
	print(t+"if ord( linea[ index ] ) in range( 48 , 58 ):")
	t += "\t"
	print(t+"auxToken = auxToken + linea[ index ]")
	print(t+"index += 1")
	t = t[1:]
	print(t+"elif ord( linea[ index ] ) == 46 and not punto:")
	t += "\t"
	print(t+"auxToken = auxToken + linea[ index ]")
	print(t+"punto = True")
	print(t+"tipo = 'valor_double'")
	print(t+"index += 1")
	t = t[1:]
	print(t+"else:")
	print(t+"\tbreak")
	t = t[1:]
	print(t+"return Token(tipo, auxToken, fila, columna)")
	print("def variable( linea , index , fila, columna ):")
	t = "\t"
	print(t+"auxToken = linea[ index ]")
	print(t+"index += 1")
	print(t+"tipo = 'id'")
	print(t+"while index < len( linea ):")
	t += "\t"
	print(t+"if ( ord( linea[ index ] ) in range( 65, 90) ) or ( ord( linea[ index ] ) in range( 97, 123) ) or ord( linea[ index ] ) in range( 48 , 58 ) or ord( linea[ index ] ) == 95 :")
	print(t+"\tauxToken = auxToken + linea[ index ]")
	print(t+"\tindex += 1")
	print(t+"else:")
	print(t+"\tbreak")
	t = t[1:]
	print(t+"return Token(tipo, auxToken, fila, columna)")
	print("def strin( linea , index , fila, columna ):")
	t = "\t"
	print(t+"auxToken = linea[ index ]")
	print(t+"index += 1")
	print(t+"tipo = 'valor_string'")
	print(t+"while linea[ index ] != '\"':")
	print(t+"\tauxToken = auxToken + linea[ index ]")
	print(t+"\tindex += 1")
	print(t+"auxToken = auxToken + linea[ index ]")
	print(t+"index += 1")
	print(t+"return Token(tipo, auxToken, fila, columna)")
	print("def dos_simbolos( linea , index , fila , columna ):")
	print(t+"auxToken = linea[ index ]")
	print(t+"index += 1")
	print(t+"if index < len( linea ):")
	t += "\t"
	print(t+"if linea[ index ] == '=' and (auxToken == '!' or auxToken == '>' or auxToken == '<' or auxToken == '=' ):")
	print(t+"\tauxToken = auxToken + linea[ index ]")
	print(t+"\ttipo = simbolos[ auxToken ]")
	print(t+"elif linea[ index ] == '&' and auxToken == '&' :")
	print(t+"\tauxToken = auxToken + linea[ index ]")
	print(t+"\ttipo = simbolos[ auxToken ]")
	print(t+"elif linea[ index ] == '|' and auxToken == '|' :")
	print(t+"\tauxToken = auxToken + linea[ index ]")
	print(t+"\ttipo = simbolos[ auxToken ]")
	print(t+"else:")
	print(t+"\ttipo = simbolos[ auxToken ]")
	t = t[1:]
	print(t+"else:")
	print(t+"\ttipo = simbolos[ auxToken ]")
	print(t+"return Token( tipo , auxToken , fila , columna )")
	print("def nextToken( linea ):")
	t = "\t"
	print(t+"global token")
	print(t+"global Fila")
	print(t+"global Columna")
	print(t+"token = Token('EOF', 'eof', 0, 0 )")
	print(t+"#recorrer los espacios")
	print(t+"while linea[ Columna ] == ' '  or linea[ Columna ] == '\\t':")
	print(t+"\tColumna+=1")
	print(t+"#es un numero")
	print(t+"if ord( linea[ Columna ] ) in range( 48 , 58 ):")
	print(t+"\ttoken = numero( linea , Columna , Fila , Columna )")
	print(t+"\tColumna = Columna + len( token.token )")
	print(t+"#es una letra de palabra reservada o variable")
	print(t+"elif ( ord( linea[ Columna ] ) in range( 65, 90) ) or ( ord( linea[ Columna ] ) in range( 97, 123) ) :")
	print(t+"\ttoken = variable( linea , Columna , Fila , Columna )")
	print(t+"\tColumna = Columna + len( token.token )")
	print(t+"#comentario")
	print(t+"elif linea[ Columna ] == '#':")
	print(t+"\twhile linea[ Columna ] != '\\n':")
	print(t+"\t\tColumna+=1")
	print(t+"\ttoken = Token( 'EOL' , '' , Fila , Columna )")
	print(t+"elif linea[ Columna ] == '\\n':")
	print(t+"\ttoken = Token( 'EOL' , '' , Fila , Columna )")
	print(t+"#String ")
	print(t+"elif linea[ Columna ] == '\"':")
	print(t+"\ttoken = strin( linea , Columna , Fila , Columna )")
	print(t+"\tColumna = Columna + len( token.token )")
	print(t+"#otro simbolo")
	print(t+"else:")
	t += "\t"
	print(t+"sim = linea[Columna]")
	print(t+"if sim == '>' or sim == '<' or sim == '!' or sim == '=' or sim == '&' or sim == '|':")
	print(t+"\ttoken = dos_simbolos( linea , Columna , Fila , Columna )")
	print(t+"\tColumna = Columna + len( token.token )")
	print(t+"elif sim in simbolos:")
	print(t+"\ttoken = Token( simbolos[sim] , sim , Fila , Columna )")
	print(t+"\tColumna = Columna + len( token.token )")
	print(t+"else:")
	print(t+"\tprint('>>> Error lexico (linea: ' + str(Fila+1) + ', posicion: ' + str(Columna+1) + ')' )")
	print(t+"\tsys.exit(0)")
	t = t[1:]
	print(t+"return token")

	#Creador de las funciones
	for noTerminal in noTerminales:
		prediccionesNoTerminales[noTerminal] = []
		t = "\t"
		print("def "+noTerminal+"():")
		cont = 0
		for i in predicciones:
			trans = i.split()
			if noTerminal == trans[0]:
				if cont != 0:
					t += "el"
				print(t+"if token.token in ",predicciones[i]," or token.tipo in", predicciones[i],":")
				prediccionesNoTerminales[noTerminal] += predicciones[i]
				if cont != 0:
					t = t[:1]
				t += "\t"
				for token in trans[1:len(trans)]:
					caracter = ord(token[0])
					if caracter < 90 and caracter > 64:
						print(t+token+"();")
					else:
						print(t+"emparejar('"+token+"')")
				t = t[1:]
				cont += 1
		print(t+"else:")
		t += "\t"
		print(t+"errorSintaxis(",prediccionesNoTerminales[noTerminal],")")
	print("")
	print("def errorSintaxis(lista):")
	t = "\t"
	print(t+"global stopProcess")
	print(t+"if type( lista ) is list:")
	print(t+"\tsorted(lista)")
	print(t+"error = token.token")
	print(t+"if token.tipo == 'identificador':")
	print(t+"\terror = 'identificador'")
	print(t+"print('<' + str( token.fila + 1 ) + ':' + str( token.columna  + 1 ) + \"> Error sintactico: se encontro: '\" + error + \"'; se esperaba: '\" + \"', '\".join( lista ) + \"'.\")")
	print(t+"sys.exit(0)")
	print(t+"stopProcess = True")
	t = t[ 1 : ]
	print("")
	print("def emparejar( tokEsperado ):")
	t = "\t"
	print(t+"global token")
	print(t+"if tokEsperado != 'epsilon':")
	t += "\t"
	print(t+"if token.token in tokEsperado or token.tipo == tokEsperado:")
	t += "\t"
	print(t+"token = TOKENS.pop( 0 )")
	t = t[ 1: ]
	print(t+"else:")
	t += "\t"
	print(t+"errorSintaxis( tokEsperado )\n")
	print("linea = sys.stdin.readline()")
	print("while linea != '' :")
	t = "\t"
	print(t+"while Columna < len( linea ):")
	t += "\t"
	print(t+"token = nextToken( linea )")
	print(t+"if token.token in reservadas:")
	print(t+"\ttoken.tipo = token.token")
	print(t+"\t#print('<'+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' ) ")
	print(t+"\tTOKENS.append(token)")
	print(t+"elif token.token in simbolos.keys(): ")
	print(t+"\tif token.token == 'ne' or token.token == 'eq':")
	print(t+"\t\ttoken.tipo = simbolos [ token.token ]")
	print(t+"\t#print('<'+token.tipo+','+str(token.fila+1)+','+str(token.columna+1)+'>' )")
	print(t+"\tTOKENS.append(token)")
	print(t+"elif token.tipo == 'valor_string':")
	print(t+"\ttoken.token = token.token[1:-1]")
	print(t+"\t#print('<'+token.tipo+','+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )")
	print(t+"\tTOKENS.append(token)")
	print(t+"elif token.tipo != 'EOF'  and token.tipo != 'EOL':")
	print(t+"\t#print('<'+token.tipo+','+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )")
	print(t+"\tTOKENS.append(token)")
	print(t+"else:")
	print(t+"\tbreak")
	t = t[ 1: ]
	print(t+"linea = sys.stdin.readline()")
	print(t+"Fila += 1")
	print(t+"Columna = 0")
	t = "\t"
	print(t+"#token = Token( \"pesos\", \"pesos\", 0, 0 )")
	print(t+"#TOKENS.append( token )")
	print("token = Token( \"EOF\", \"eof\", 0, 0 )")
	print("TOKENS.append( token )")
	print("token = TOKENS.pop( 0 )")
	print("#for i in TOKENS:")
	print("\t#print(i)")
	print("while not stopProcess:")
	print(t+"S()")
	print(t+"token = TOKENS.pop( 0 )")
	print(t+"if token.tipo == \"EOF\":")
	t += "\t"
	print(t+"print(\"El analisis sintactico se ha finalizado correctamente.\")")
	print(t+"break")
f.close( )	