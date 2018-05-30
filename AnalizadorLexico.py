#Lenguajes de Programacion
#Diego Cruz
#Oscar Gomez
import sys

#Palabras Reservadas
reservadas = ['if','else','elseif','then','for','while','switch','case',
	'break','set','log','default','expr','continue','foreach','incr',
	'array','exists','size','proc','gets','stdin','return']

simbolos = {
	'{':'token_llave_izq',
	'}':'token_llave_der',
	'$':'token_dollar',
	';':'token_pyc',
	'[':'token_cor_izq',
	']':'token_cor_der',
	'(':'token_par_izq',
	')':'token_par_der',
	#Operadores Relacionales
	'>=':'token_mayor_igual',
	'<=':'token_menor_igual',
	'=':'token_igual_str',
	'ne':'token_diff_str',
	'==':'token_igual_num',
	'!=':'token_diff_num',
	'>':'token_mayor',
	'<':'token_menor',
	#Operadores Logicos
	'&&':'token_and',
	'||':'token_or',
	'!':'token_not',
	#Operadores Aritmeticos
	'+':'token_mas',
	'-':'token_menos',
	'*':'token_mul',
	'/':'token_div',
	'%':'token_mod',
	'**':'token_pot',
	}

class Token:
	def __init__( self ):
		self.tipo = ''
		self.token = ''
		self.fila = 0
		self.columna = 0

	def __init__( self, tipo , token , fila , columna ):
		self.tipo = tipo
		self.token = token
		self.fila = fila
		self.columna = columna
	def __str__(self):
		return '<%s,%s,%d,%d>' % (self.tipo, self.token, self.fila, self.columna)

	def __repr__(self):	
		return str(self)


Fila = 0
Columna = 0
auxToken = ''
TOKENS = []
token = Token( 'EOF', 'eof', 0, 0 )
stopProcess = False

def numero( linea , index , fila, columna ):
	auxToken = linea[ index ]
	index += 1
	punto = False
	tipo = 'token_integer'
	while index < len( linea ) :
		if ord( linea[ index ] ) in range( 48 , 58 ):
			auxToken = auxToken + linea[ index ]
			index += 1
		elif ord( linea[ index ] ) == 46 and not punto:
			auxToken = auxToken + linea[ index ]
			punto = True
			tipo = 'token_double'
			index += 1
		else:
			break
	return Token(tipo, auxToken, fila, columna)
	

def variable( linea , index , fila, columna ):
	auxToken = linea[ index ]
	index += 1
	tipo = 'id'
	while index < len( linea ):
		if ( ord( linea[ index ] ) in range( 65, 90) ) or ( ord( linea[ index ] ) in range( 97, 123) ) or ord( linea[ index ] ) in range( 48 , 58 ) or ord( linea[ index ] ) == 95 :
			auxToken = auxToken + linea[ index ]
			index += 1
		else:
			break
	return Token(tipo, auxToken, fila, columna)

def strin( linea , index , fila, columna ):
	auxToken = linea[ index ]
	index += 1
	tipo = 'token_string'
	while linea[ index ] != '"':
		auxToken = auxToken + linea[ index ]
		index += 1
	auxToken = auxToken + linea[ index ]
	index += 1
	return Token(tipo, auxToken, fila, columna)

def dos_simbolos( linea , index , fila , columna ):
	auxToken = linea[ index ]
	index += 1
	if index < len( linea ):
		if linea[ index ] == '=' and (auxToken == '!' or auxToken == '>' or auxToken == '<' or auxToken == '=' ):
			auxToken = auxToken + linea[ index ]
			tipo = simbolos[ auxToken ]
		elif linea[ index ] == '&' and auxToken == '&' :
			auxToken = auxToken + linea[ index ]
			tipo = simbolos[ auxToken ]
		elif linea[ index ] == '|' and auxToken == '|' :
			auxToken = auxToken + linea[ index ]
			tipo = simbolos[ auxToken ]
		else:
			tipo = simbolos[ auxToken ]
	else:
		tipo = simbolos[ auxToken ]
	return Token( tipo , auxToken , fila , columna )


def nextToken( linea ):
	global token
	global Fila
	global Columna
	token = Token('EOF', '', 0, 0 )
	#recorrer los espacios
	while linea[ Columna ] == ' ' or linea[ Columna ] == '\t':
		Columna+=1

	#es un numero
	if ord( linea[ Columna ] ) in range( 48 , 58 ):
		token = numero( linea , Columna , Fila , Columna )
		Columna = Columna + len( token.token )

	#es una letra de palabra reservada o variable
	elif ( ord( linea[ Columna ] ) in range( 65, 90) ) or ( ord( linea[ Columna ] ) in range( 97, 123) ) :
		token = variable( linea , Columna , Fila , Columna )
		Columna = Columna + len( token.token )

	#comentario
	elif linea[ Columna ] == '\n' or linea[ Columna ] == '#':
		token = Token('EOL', '', Fila, Columna )
	
	#String 
	elif linea[ Columna ] == '\"':
		token = strin( linea , Columna , Fila , Columna )
		Columna = Columna + len( token.token )

	#otro simbolo
	else:
		sim = linea[Columna]
		if sim == '>' or sim == '<' or sim == '!' or sim == '=' or sim == '&' or sim == '|':
			token = dos_simbolos( linea , Columna , Fila , Columna )
			Columna = Columna + len( token.token )
		elif sim in simbolos:
			token = Token( simbolos[sim] , sim , Fila , Columna )
			Columna = Columna + len( token.token )
		else:
			print('>>> Error lexico (linea: ' + str(Fila) + ', posicion: ' + str(Columna) + ')' )
			sys.exit(0)
	return token

linea = sys.stdin.readline()

while linea != '' :
	while Columna < len( linea ):
		token = nextToken( linea )
		if token.token in reservadas:
			token.tipo = token.token
			#print('<'+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		elif token.token in simbolos.keys(): 
			if token.token == 'ne' or token.token == '=':
				token.tipo = simbolos [ token.token ]
			#print('<'+token.tipo+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		elif token.tipo == 'token_string':
			#print('<'+token.tipo+','+token.token[1:-1]+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		elif token.tipo != 'EOF'  and token.tipo != 'EOL':
			#print('<'+token.tipo+','+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		else:
			break
	linea = sys.stdin.readline()
	Fila += 1
	Columna = 0
for i in TOKENS:
	print(i)
