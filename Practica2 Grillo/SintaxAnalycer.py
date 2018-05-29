import sys

Fila = 0
Columna = 0
Token = ""

def numero( linea , index ):
	tok = linea[ index ]
	index += 1
	punto = False
	while index < len( linea ) :
		if ord( linea[ index ] ) in range( 48 , 58 ):
			tok = tok + linea[ index ]
			index += 1
		elif ord( linea[ index ] ) == 46 and not punto:
			tok = tok + linea[ index ]
			punto = True
			index += 1
		else: 
			print("no es numero o punto en index " + str( index ))
			break
	return tok

def variable( linea , index ):
	tok = linea[ index ]
	index += 1
	simbolos = [ "$" , "%" , "&" , "!" , "#"]
	while index < len( linea ):
		if ( ord( linea[ index ] ) in range( 65, 90) ) or ( ord( linea[ index ] ) in range( 97, 123) ) or ord( linea[ index ] ) in range( 48 , 58 ) or ord( linea[ index ] ) == 95 :
			tok = tok + linea[ index ]
			index += 1
		elif linea[ index ] in simbolos:
			tok = tok + linea[ index ]
			index += 1
			break
		else:
			break
	return tok

def strin( linea , index ):
	tok = linea[ index ]
	index += 1
	while linea[ index ] != '"':
		tok = tok + linea[ index ]
		index += 1
	tok = tok + linea[ index ]
	index += 1
	return tok


def nextToken( linea ):
	global Token
	global Fila
	global Columna
	Token = ""
	#recorrer los espacios
	while linea[ Columna ] == " ":
		Columna+=1

	#es un numero
	if ord( linea[ Columna ] ) in range( 48 , 58 ):
		print("es un numero")
		Token = numero( linea , Columna)
		Columna = Columna + len( Token )

	#es una letra de palabra reservada o variable
	elif ( ord( linea[ Columna ] ) in range( 65, 90) ) or ( ord( linea[ Columna ] ) in range( 97, 123) ) :
		print("es letra de palabra reservada o variable")
		Token = variable( linea , Columna )
		Columna = Columna + len( Token )

	#comentario
	elif linea[ Columna ] == "'":
		print("es un comentario")
		Fila += 1
		Columna = 0
		linea = sys.stdin.readline().strip()
		if linea != "":
			Token = nextToken( linea )
			Columna = Columna + len( Token )

	#String 
	elif linea[ Columna ] == "\"":
		print("es un string")
		Token = strin( linea , Columna )
		Columna = Columna + len( Token )

	#otro simbolo
	else:
		print("es otro simbolo")
		Token = linea[ Columna ]
		Columna = Columna + len( Token )

	return Token

linea = sys.stdin.readline()

while linea != "":
	while Columna < len( linea ):
		Token = nextToken( linea )
		print("Fila: " + str( Fila ) + " Columna: " + str( Columna ) + " token: " + Token)
	linea = sys.stdin.readline()
	Fila += 1
	Columna = 0