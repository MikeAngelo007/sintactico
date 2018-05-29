#Lenguajes de Programacion
#Practica 2: Analizador Sintactico
#Nicolas Leonardo Maldonado Garzon  2879709
#Joan Sebastian Contreras Pena	  2879782
import sys

palabra = [ 'integer', 'single', 'long', 'double', 'string',
            'dim', 'as', 'print', 'input',
            'if', 'else', 'end', 'then', 'select', 'case',
            'while', 'wend', 'do', 'loop', 'until', 'for',
            'to', 'next', 'step', 'sub', 'shared', 'function',
            'const', 'sub' ]

simbolos = {
	#Operadores Relacionales
	"<" : "token_menor",
	">" : "token_mayor",
	"=" : "token_igual",
	"<=" : "token_menor_igual",
	">=" : "token_mayor_igual", 
	"<>" : "token_dif",
	#Operadores Logicos
	"and" : "and",
	"or" : "or",
	"not" : "not",
	"xor" : "xor",
	#Operadores Aritmeticos
	"+" : "token_mas",
	"-" : "token_menos",
	"*" : "token_mul",
	"/" : "token_div",
	"^" : "token_pot",
	"mod" : "mod",
	#Signos de Puntuacion
	"," : "token_coma",
	";" : "token_pyc",
	"(" : "token_par_izq",
	")" : "token_par_der",
	#Tipos de dato
	"%" : "token_porcentaje",
	"&" : "token_ampersand",
	"!" : "token_admiracion",
	"#" : "token_numeral",
	"$" : "token_pesos",
}

TOKENS = []
class TOKEN:
	def __init__( self ):
		self.token = ""
		self.tipo = ""
		self.fila = 0
		self.columna = 0

	def __init__( self, token , tipo , fila , columna ):
		self.token = token
		self.tipo = tipo
		self.fila = fila
		self.columna = columna
numeroLinea = 1
stopProcess = False
token = TOKEN( "", "EOF", 0, 0 )

def CONST( ):
	print "entro a CONST", token.token
	if token.token in ['identificador']  or token.tipo in ['identificador'] :
		emparejar( 'epsilon' )
	elif token.token in ['const']  or token.tipo in ['const'] :
		emparejar( 'const' )
	else:
		errorSintaxis( ['identificador', 'const']  )
	print "sale de CONST", token.token

def DECLA( ):
	print "entro a DECLA", token.token
	if token.token in ['identificador']  or token.tipo in ['identificador'] :
		emparejar( 'identificador' )
		SIMBOL1( );
		emparejar( '=' )
		EXPD( );
	else:
		errorSintaxis( ['identificador']  )
	print "sale de DECLA", token.token

def EXP( ):
	print "entro a EXP", token.token
	if token.token in ['-', 'not', 'identificador']  or token.tipo in ['-', 'not', 'identificador'] :
		UNID( );
		OP( );
	elif token.token in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long']  or token.tipo in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long'] :
		VA( );
		OP( );
	else:
		errorSintaxis( ['-', 'not', 'identificador', '-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long']  )
	print "sale de EXP", token.token

def EXPD( ):
	print "entro a EXPD", token.token
	if token.token in ['(']  or token.tipo in ['('] :
		emparejar( '(' )
		EXPD( );
		emparejar( ')' )
	elif token.token in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador']  or token.tipo in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador'] :
		EXP( );
	else:
		errorSintaxis( ['(', '-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador']  )
	print "sale de EXPD", token.token

def EXPOP( ):
	print "entro a EXPOP", token.token
	if token.token in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long']  or token.tipo in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long'] :
		VA( );
		OP( );
	elif token.token in ['-', 'not', 'identificador']  or token.tipo in ['-', 'not', 'identificador'] :
		UNID( );
		OP( );
	else:
		errorSintaxis( ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', '-', 'not', 'identificador']  )
	print "sale de EXPOP", token.token

def ID( ):
	print "entro a ID", token.token
	if token.token in ['identificador']  or token.tipo in ['identificador'] :
		emparejar( 'identificador' )
		PARAM( );
		VARID( );
	else:
		errorSintaxis( ['identificador']  )
	print "sale de ID", token.token

def ID1( ):
	print "entro a ID1", token.token
	if token.token in ['identificador']  or token.tipo in ['identificador'] :
		emparejar( 'identificador' )
		PARAM( );
	else:
		errorSintaxis( ['identificador']  )
	print "sale de ID1", token.token

def OP( ):
	print "entro a OP", token.token
	if token.token in ['-']  or token.tipo in ['-'] :
		emparejar( '-' )
		EXPOP( );
	elif token.token in ['*']  or token.tipo in ['*'] :
		emparejar( '*' )
		EXPOP( );
	elif token.token in ['pesos', ',', ')']  or token.tipo in ['pesos', ',', ')'] :
		emparejar( 'epsilon' )
	elif token.token in ['>=']  or token.tipo in ['>='] :
		emparejar( '>=' )
		EXPOP( );
	elif token.token in ['<']  or token.tipo in ['<'] :
		emparejar( '<' )
		EXPOP( );
	elif token.token in ['xor']  or token.tipo in ['xor'] :
		emparejar( 'xor' )
		EXPOP( );
	elif token.token in ['/']  or token.tipo in ['/'] :
		emparejar( '/' )
		EXPOP( );
	elif token.token in ['<=']  or token.tipo in ['<='] :
		emparejar( '<=' )
		EXPOP( );
	elif token.token in ['+']  or token.tipo in ['+'] :
		emparejar( '+' )
		EXPOP( );
	elif token.token in ['mod']  or token.tipo in ['mod'] :
		emparejar( 'mod' )
		EXPOP( );
	elif token.token in ['or']  or token.tipo in ['or'] :
		emparejar( 'or' )
		EXPOP( );
	elif token.token in ['=']  or token.tipo in ['='] :
		emparejar( '=' )
		EXPOP( );
	elif token.token in ['and']  or token.tipo in ['and'] :
		emparejar( 'and' )
		EXPOP( );
	elif token.token in ['<>']  or token.tipo in ['<>'] :
		emparejar( '<>' )
		EXPOP( );
	elif token.token in ['>']  or token.tipo in ['>'] :
		emparejar( '>' )
		EXPOP( );
	else:
		errorSintaxis( ['-', '*', 'pesos', ',', ')', '>=', '<', 'xor', '/', '<=', '+', 'mod', 'or', '=', 'and', '<>', '>']  )
	print "sale de OP", token.token

def PARAM( ):
	print "entro a PARAM", token.token
	if token.token in ['(']  or token.tipo in ['('] :
		emparejar( '(' )
		EXPD( );
		VAREXP( );
		emparejar( ')' )
	elif token.token in [',', 'as', '+', '-', '*', '/', 'mod', 'xor', 'and', 'or', '<', '<=', '>=', '>', '=', '<>', 'pesos', ')']  or token.tipo in [',', 'as', '+', '-', '*', '/', 'mod', 'xor', 'and', 'or', '<', '<=', '>=', '>', '=', '<>', 'pesos', ')'] :
		emparejar( 'epsilon' )
	else:
		errorSintaxis( ['(', ',', 'as', '+', '-', '*', '/', 'mod', 'xor', 'and', 'or', '<', '<=', '>=', '>', '=', '<>', 'pesos', ')']  )
	print "sale de PARAM", token.token

def S( ):
	print "entro a S", token.token
	if token.token in ['dim']  or token.tipo in ['dim'] :
		emparejar( 'dim' )
		SHA( );
		ID( );
		emparejar( 'as' )
		TPD( );
	elif token.token in ['const', 'identificador']  or token.tipo in ['const', 'identificador'] :
		CONST( );
		DECLA( );
	else:
		errorSintaxis( ['dim', 'const', 'identificador']  )
	print "sale de S", token.token

def SHA( ):
	print "entro a SHA", token.token
	if token.token in ['identificador']  or token.tipo in ['identificador'] :
		emparejar( 'epsilon' )
	elif token.token in ['shared']  or token.tipo in ['shared'] :
		emparejar( 'shared' )
	else:
		errorSintaxis( ['identificador', 'shared']  )
	print "sale de SHA", token.token

def SIMBOL( ):
	print "entro a SIMBOL", token.token
	if token.token in ['#']  or token.tipo in ['#'] :
		emparejar( '#' )
	elif token.token in ['$']  or token.tipo in ['$'] :
		emparejar( '$' )
	elif token.token in ['%']  or token.tipo in ['%'] :
		emparejar( '%' )
	elif token.token in ['&']  or token.tipo in ['&'] :
		emparejar( '&' )
	elif token.token in ['!']  or token.tipo in ['!'] :
		emparejar( '!' )
	else:
		errorSintaxis( ['#', '$', '%', '&', '!']  )
	print "sale de SIMBOL", token.token

def SIMBOL1( ):
	print "entro a SIMBOL1", token.token
	if token.token in ['$', '%', '&', '!', '#']  or token.tipo in ['$', '%', '&', '!', '#'] :
		SIMBOL( );
	elif token.token in ['=']  or token.tipo in ['='] :
		emparejar( 'epsilon' )
	else:
		errorSintaxis( ['$', '%', '&', '!', '#', '=']  )
	print "sale de SIMBOL1", token.token

def TPD( ):
	print "entro a TPD", token.token
	if token.token in ['string']  or token.tipo in ['string'] :
		emparejar( 'string' )
	elif token.token in ['double']  or token.tipo in ['double'] :
		emparejar( 'double' )
	elif token.token in ['long']  or token.tipo in ['long'] :
		emparejar( 'long' )
	elif token.token in ['single']  or token.tipo in ['single'] :
		emparejar( 'single' )
	elif token.token in ['integer']  or token.tipo in ['integer'] :
		emparejar( 'integer' )
	else:
		errorSintaxis( ['string', 'double', 'long', 'single', 'integer']  )
	print "sale de TPD", token.token

def UN( ):
	print "entro a UN", token.token
	if token.token in ['-']  or token.tipo in ['-'] :
		emparejar( '-' )
	elif token.token in ['valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador']  or token.tipo in ['valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador'] :
		emparejar( 'epsilon' )
	elif token.token in ['not']  or token.tipo in ['not'] :
		emparejar( 'not' )
	else:
		errorSintaxis( ['-', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long', 'identificador', 'not']  )
	print "sale de UN", token.token

def UNID( ):
	print "entro a UNID", token.token
	if token.token in ['-', 'not', 'identificador']  or token.tipo in ['-', 'not', 'identificador'] :
		UN( );
		ID1( );
	else:
		errorSintaxis( ['-', 'not', 'identificador']  )
	print "sale de UNID", token.token

def VA( ):
	print "entro a VA", token.token
	if token.token in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long']  or token.tipo in ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long'] :
		UN( );
		VAL( );
	else:
		errorSintaxis( ['-', 'not', 'valor_integer', 'valor_single', 'valor_double', 'valor_string', 'valor_long']  )
	print "sale de VA", token.token

def VAL( ):
	print "entro a VAL", token.token
	if token.token in ['valor_integer']  or token.tipo in ['valor_integer'] :
		emparejar( 'valor_integer' )
	elif token.token in ['valor_double']  or token.tipo in ['valor_double'] :
		emparejar( 'valor_double' )
	elif token.token in ['valor_long']  or token.tipo in ['valor_long'] :
		emparejar( 'valor_long' )
	elif token.token in ['valor_string']  or token.tipo in ['valor_string'] :
		emparejar( 'valor_string' )
	elif token.token in ['valor_single']  or token.tipo in ['valor_single'] :
		emparejar( 'valor_single' )
	else:
		errorSintaxis( ['valor_integer', 'valor_double', 'valor_long', 'valor_string', 'valor_single']  )
	print "sale de VAL", token.token

def VAREXP( ):
	print "entro a VAREXP", token.token
	if token.token in [')']  or token.tipo in [')'] :
		emparejar( 'epsilon' )
	elif token.token in [',']  or token.tipo in [','] :
		emparejar( ',' )
		EXPD( );
	else:
		errorSintaxis( [')', ',']  )
	print "sale de VAREXP", token.token

def VARID( ):
	print "entro a VARID", token.token
	if token.token in ['as']  or token.tipo in ['as'] :
		emparejar( 'epsilon' )
	elif token.token in [',']  or token.tipo in [','] :
		emparejar( ',' )
		ID( );
	else:
		errorSintaxis( ['as', ',']  )
	print "sale de VARID", token.token


def errorSintaxis( lista ):
	global stopProcess
	if type( lista ) is list:
		lista.sort( )
	error = token.token
	if token.tipo == 'identificador':
		error = 'identificador'
	print '<' + str( token.fila ) + ':' + str( token.columna ) + "> Error sintactico: se encontro: '" + error + "'; se esperaba: '" + "', '".join( lista ) + "'."
	sys.exit(0)
	stopProcess = True

def emparejar( tokEsperado ):
	global token
	if tokEsperado != 'epsilon':
		if token.token in tokEsperado or token.tipo == tokEsperado:
			token = TOKENS.pop( 0 )
		else:
			errorSintaxis( tokEsperado )
def simb( subs ):
	caracter = ord( subs[ 0 ] )
	if caracter in range( 60 , 63):
		return "relacion"
	elif caracter in range( 33 , 39 ):
		return "tipo_de_dato"
	elif caracter == 40 or caracter == 41:
		return "parentesis"
	elif caracter == 44 or caracter == 59:
		return "puntuacion"
	else: return "operador"

#Clasificar entre palabras reservadas, variables, Strings y simbolos.
def busquedaDic( subs, ind ):
	if simbolos.get( subs.lower( ) ) != None:
		#print '<' + simbolos.get( subs.lower( ) ) + ',' + str( numeroLinea ) + ',' + str( ind + 1 ) + '>'
		simbol = subs.lower( )
		simbolType = simb( subs.lower( ) )
		tok = TOKEN( simbol , simbolType , str( numeroLinea ) , str ( ind + 1 ) )
		TOKENS.append( tok )
	elif subs.lower( ) in palabra:
		#print '<' + subs.lower( ) + ',' + str( numeroLinea ) + ',' + str( ind + 1 ) + '>'
		tok = TOKEN( subs.lower( ) , "palabra reservada" , str( numeroLinea ) , str( ind + 1 ) )
		TOKENS.append( tok )
	elif subs[ 0 ] != ' ' :
		if subs[ 0 ] == '"':
			#print '<token_string,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
			tok = TOKEN( 'valor_string', 'valor', str( numeroLinea ) , str ( ind + 1 ) )
			TOKENS.append( tok )
		else:
			#print '<id,' + subs.lower() + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
			tok = TOKEN( subs.lower(), "identificador" , str( numeroLinea ) , str ( ind + 1 ) )
			TOKENS.append( tok )

#Clasificar numeros enteros
def entero( subs, ind ):
	i = int( subs )
	#REVISAR HASTA QUE PUNTO ES INTEGER, SI HASTA 32767 O HASTA 32766
	if( i > 32767 ):
		#print '<token_long,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
		tok = TOKEN( 'valor_long', 'valor', str( numeroLinea ) , str( ind + 1 ) )
		TOKENS.append( tok )
	else:
		#print '<token_integer,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
		tok = TOKEN( 'valor_integer', 'valor', str( numeroLinea ) , str( ind + 1 ) )
		TOKENS.append( tok )

#Clasificar numeros decimales
def decimal( subs, ind ):
	for i in range( len( subs ) ):
		if subs[ i ] == '.':
			break
	if len( subs ) - i > 7:

		#print '<token_double,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
		tok = TOKEN( 'valor_double', 'valor', str( numeroLinea ) , str( ind + 1 ) )
		TOKENS.append( tok )
	else:
		#print '<token_single,' + subs + ',' + str( numeroLinea ) +',' + str( ind + 1 ) + '>'
		tok = TOKEN( 'valor_single', 'valor', str( numeroLinea ) , str( ind + 1 ) )
		TOKENS.append( tok )

#Numero antes de que se ingresara un punto sin tener otro numero despues y error.
def errorPunto( subs, ind ):
	for i in range( len( subs ) ):
		if subs[ i ] == '.':
			break;
	numero = subs[ : i ]
	entero( numero, ind )
	print ">>> Error lexico (linea: " + str( numeroLinea ) + ", posicion: " + str( ind + i + 1 ) + ")"

def automata( linea, ind ):
	index = ind
	estado = 0
	while True:
		estado = delta( estado, linea[ index ] )
		index += 1
		if not ( index < len( linea ) and estado < 10 and estado >= -1 ):
			break
	index -= 1
	if estado == 1:
		#Variable o palabra reservada
		subs = linea[ ind : index + 1 ]
		busquedaDic( subs, ind )
	elif estado == 2:
		#Numero entero
		subs = linea[ ind : index + 1 ]
		entero( subs, ind )
	elif estado == 3:
		#Decimal
		subs = linea[ ind : index + 1 ]
		decimal( subs, ind )
	elif estado == 4:
		#Simbolo reservado o dobles( <>, <= o >= )
		subs = linea[ ind : index + 1 ]
		busquedaDic( subs, ind )
	elif estado == 5:
		#Simbolo <
		subs = linea[ ind : index + 1 ]
		busquedaDic( subs, ind )
	elif estado == 6:
		#Simbolo >
		subs = linea[ ind : index + 1 ]
		busquedaDic( subs, ind )
	#Cadenas
	elif estado == 7:
		#String
		subs = linea[ind : index + 1 ]
		busquedaDic( subs, ind )
	elif estado == 9:
		#Espacio al punto
		subs = linea[ ind : index ]
		errorPunto( subs, ind )
	#Lexemas aceptados pero que no son fin de cadena
	elif estado == 11:
		#Strings, variables y simbolos.
		subs = linea[ ind : index ]
		busquedaDic( subs, ind )
	elif estado == 12:
		#Enteros
		subs = linea[ ind : index ]
		entero( subs, ind )
	elif estado == 13:
		#Decimales
		subs = linea[ ind : index ]
		decimal( subs, ind )
	#Errores Lexicos
	elif estado == -1:
		#String sin comillas de cierre
		print ">>> Error lexico (linea: " + str( numeroLinea ) + ", posicion: " + str( ind + 1 ) + ")" 
	elif estado == -2:
		#. y no viene de numeros
		subs = linea[ ind : index ]
		errorPunto( subs, ind )
	elif estado == -3:
		#Caracter no valido
		print ">>> Error lexico (linea: " + str( numeroLinea ) + ", posicion: " + str( ind + 1 ) + ")"
	return [ index , estado ]

def delta( estado , caracter ):
	caracter = ord( caracter )
	#Estado inicial
	if estado == 0:
		if( ( caracter > 64 and caracter < 91) or ( caracter > 96 and caracter < 123 ) ):
			return 1#Empieza por letra
		elif( caracter > 47 and caracter < 58 ):
			return 2#Empieza por numero
		elif( (caracter > 32 and caracter < 48 and caracter !=  34 and caracter != 39 and caracter != 46 ) or caracter == 59 or caracter == 61 or caracter == 94 ):
			return 4#Es un simbolos reservado de un caracter
		elif( caracter == 60 ):
			return 5#Empieza por <
		elif( caracter == 62 ):
			return 6#Empieza por >
		elif ( caracter == 32 ):
			return 8#Espacio
		elif( caracter == 39 ):
			return 10#Comentario
		elif( caracter == 34 ):
			return -1#Comilla de apertura
		elif( caracter == None or caracter == 10 ):
			return 0
		else:
			return -3#Caracter no permitido
		#Variables o palabras reservadas
	elif estado == 1:
		if ( ( caracter > 64 and caracter < 91 ) or ( caracter > 96 and caracter < 123 ) or ( caracter > 47 and caracter < 58 ) or caracter == 95 ):
			return 1#Siguen letras, numeros o '_'
		else:
			return 11#Si es otro valor
	#Numeros enteros y decimales
	elif estado == 2:
		if ( caracter > 47 and caracter < 58 ):
			return 2#Si es un numero
		elif ( caracter == 46 ):
			return 9#Si es un punto
		else:
			return 12#Si es otro valor
	#Numeros decimales
	elif estado == 3:
		if ( caracter > 47 and caracter < 58 ):
			return 3#Es un numero, parte decimal
		else:
			return 13#Sigue otro valor
	#Simbolos reservados
	elif estado == 4:
		return 11#Hay otro caracter diferente despues de los simbolos reservados
	#Simbolo <
	elif estado == 5:
		if ( caracter == 62 or caracter == 61 ):
			return 4#Es <= o <>
		else:
			return 11#Otro valor luego del <
	#Simbolo >
	elif estado == 6:
		if ( caracter == 61 ):
			return 4#Es >=
		else:
			return 11#Otro valor luego del >
	#String completo
	elif estado == 7:
		return 11#Otro valor luego de la comilla de cierre
	#Caracter ' '
	elif estado == 8:
		return 11#Hay un caracter despues de un espacio
	elif estado == 9:
		if ( caracter > 47 and caracter < 58 ):
			return 3#Si es un numero
		else:
			return -2#Error, caracter diferente despues de un punto
	#Caracter '
	elif estado == 10:
		return 10
	#String sin cerrar "
	elif estado == -1:
		if ( caracter == 34 ):
			return 7#Comilla de cierre
		else:
			return -1#No se cerro la comilla
	elif estado == -2:
		return -2
	#Caracter '.' despues de algun numero
	return 0

linea = sys.stdin.readline()
while linea != "" : 
	i = [ 0, 0 ]
	i = automata( linea , i[ 0 ] )
	while i[ 1 ] > 10:
		i = automata( linea , i[ 0 ] )
		if( i[ 1 ] < 0 or i[ 1 ] == 9 ):
			break
	numeroLinea += 1
	linea = sys.stdin.readline()
	token = TOKEN( "pesos", "pesos", 0, 0 )
	TOKENS.append( token )
token = TOKEN( "EOF", "EOF", 0, 0 )
TOKENS.append( token )
token = TOKENS.pop( 0 )
while not stopProcess:
	S()
	token = TOKENS.pop( 0 )
	if token.tipo == "EOF":
		print "El analisis sintactico se ha finalizado correctamente."
		break
