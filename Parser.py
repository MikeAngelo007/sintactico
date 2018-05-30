#Parser
#Lenguajes de Programacion
#
#
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
	'**':'token_pot'
	}

class Token:
	def __init__( self ):
		self.tipo = ''
		self.token = ''
		self.fila = 0
		self.columna = 0

	def __init__( self, tipo  , token , fila , columna ):
		self.token = token
		self.tipo = tipo
		self.fila = fila
		self.columna = columna

	def __str__(self):
		return '<%s,%s,%d,%d>' % (self.tipo, self.token, self.fila, self.columna)

	def __repr__(self):
		return str(self)

Columna = 0
Fila = 0
auxToken = ''
TOKENS = []
token = Token( 'EOF', 'eof', 0, 0 )
stopProcess = False

def numero( linea , index , fila, columna ):
	auxToken = linea[ index ]
	index += 1
	punto = False
	
	tipo = 'valor_entero'
	while index < len( linea ) :
		if ord( linea[ index ] ) in range( 48 , 58 ):
			auxToken = auxToken + linea[ index ]
			index += 1
		elif ord( linea[ index ] ) == 46 and not punto:
			auxToken = auxToken + linea[ index ]
			punto = True
			tipo = 'valor_double'
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
	tipo = 'valor_string'
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
	token = Token('EOF', 'eof', 0, 0 )
	#recorrer los espacios
	while linea[ Columna ] == ' '  or linea[ Columna ] == '\t':
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
	elif linea[ Columna ] == '#':
		while linea[ Columna ] != '\n':
			Columna+=1
		token = Token( 'EOL' , '' , Fila , Columna )
	elif linea[ Columna ] == '\n':
		token = Token( 'EOL' , '' , Fila , Columna )
	#String 
	elif linea[ Columna ] == '"':
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
			print('>>> Error lexico (linea: ' + str(Fila+1) + ', posicion: ' + str(Columna+1) + ')' )
			sys.exit(0)
	return token
def ARR():
	if token.token in  ['(']  or token.tipo in ['('] :
		emparejar('(')
		ARRIDX();
		emparejar(')')
	elif token.token in  ['valor_entero', 'valor_double', 'valor_string', '[', '$']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string', '[', '$'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['(', 'valor_entero', 'valor_double', 'valor_string', '[', '$'] )
def ARRIDX():
	if token.token in  ['[']  or token.tipo in ['['] :
		EXE();
	elif token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
	else:
		errorSintaxis( ['[', 'valor_entero', 'valor_double', 'valor_string'] )
def ARRLLA():
	if token.token in  ['size']  or token.tipo in ['size'] :
		emparejar('size')
		emparejar('id')
	elif token.token in  ['exists']  or token.tipo in ['exists'] :
		emparejar('exists')
		emparejar('id')
	else:
		errorSintaxis( ['size', 'exists'] )
def BINEXPR():
	if token.token in  ['+', '-', '*', '/', '**', '%', '||', '&&', '==', '!=', '<', '>', '<=', '>=', 'ne', '=']  or token.tipo in ['+', '-', '*', '/', '**', '%', '||', '&&', '==', '!=', '<', '>', '<=', '>=', 'ne', '='] :
		BINOP();
		EXPR();
	elif token.token in  [')', '}']  or token.tipo in [')', '}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['+', '-', '*', '/', '**', '%', '||', '&&', '==', '!=', '<', '>', '<=', '>=', 'ne', '=', ')', '}'] )
def BINOP():
	if token.token in  ['+']  or token.tipo in ['+'] :
		emparejar('+')
	elif token.token in  ['-']  or token.tipo in ['-'] :
		emparejar('-')
	elif token.token in  ['*']  or token.tipo in ['*'] :
		emparejar('*')
	elif token.token in  ['/']  or token.tipo in ['/'] :
		emparejar('/')
	elif token.token in  ['**']  or token.tipo in ['**'] :
		emparejar('**')
	elif token.token in  ['%']  or token.tipo in ['%'] :
		emparejar('%')
	elif token.token in  ['||']  or token.tipo in ['||'] :
		emparejar('||')
	elif token.token in  ['&&']  or token.tipo in ['&&'] :
		emparejar('&&')
	elif token.token in  ['==']  or token.tipo in ['=='] :
		emparejar('==')
	elif token.token in  ['!=']  or token.tipo in ['!='] :
		emparejar('!=')
	elif token.token in  ['<']  or token.tipo in ['<'] :
		emparejar('<')
	elif token.token in  ['>']  or token.tipo in ['>'] :
		emparejar('>')
	elif token.token in  ['<=']  or token.tipo in ['<='] :
		emparejar('<=')
	elif token.token in  ['>=']  or token.tipo in ['>='] :
		emparejar('>=')
	elif token.token in  ['ne']  or token.tipo in ['ne'] :
		emparejar('ne')
	elif token.token in  ['=']  or token.tipo in ['='] :
		emparejar('=')
	else:
		errorSintaxis( ['+', '-', '*', '/', '**', '%', '||', '&&', '==', '!=', '<', '>', '<=', '>=', 'ne', '='] )
def CB():
	if token.token in  ['case']  or token.tipo in ['case'] :
		CSB();
		CB();
	elif token.token in  ['default', '}']  or token.tipo in ['default', '}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['case', 'default', '}'] )
def CBS():
	if token.token in  ['case']  or token.tipo in ['case'] :
		CSBS();
		CBS();
	elif token.token in  ['default', '}']  or token.tipo in ['default', '}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['case', 'default', '}'] )
def CI():
	if token.token in  ['set']  or token.tipo in ['set'] :
		D();
		emparejar(';')
	elif token.token in  ['if']  or token.tipo in ['if'] :
		IFB();
	elif token.token in  ['while']  or token.tipo in ['while'] :
		WHILEB();
	elif token.token in  ['for']  or token.tipo in ['for'] :
		FORB();
	elif token.token in  ['switch']  or token.tipo in ['switch'] :
		SWICTHB();
	elif token.token in  ['gets']  or token.tipo in ['gets'] :
		IMPUT();
		emparejar(';')
	elif token.token in  ['log']  or token.tipo in ['log'] :
		OUTPUT();
		emparejar(';')
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
		emparejar(';')
	elif token.token in  ['break']  or token.tipo in ['break'] :
		emparejar('break')
		emparejar(';')
	elif token.token in  ['continue']  or token.tipo in ['continue'] :
		emparejar('continue')
		emparejar(';')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'break', 'continue'] )
def CIS():
	if token.token in  ['set']  or token.tipo in ['set'] :
		D();
		emparejar(';')
	elif token.token in  ['if']  or token.tipo in ['if'] :
		IFBS();
	elif token.token in  ['while']  or token.tipo in ['while'] :
		WHILEBS();
	elif token.token in  ['for']  or token.tipo in ['for'] :
		FORBS();
	elif token.token in  ['switch']  or token.tipo in ['switch'] :
		SWITCHBS();
	elif token.token in  ['gets']  or token.tipo in ['gets'] :
		IMPUT();
		emparejar(';')
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
		emparejar(';')
	elif token.token in  ['break']  or token.tipo in ['break'] :
		emparejar('break')
		emparejar(';')
	elif token.token in  ['continue']  or token.tipo in ['continue'] :
		emparejar('continue')
		emparejar(';')
	elif token.token in  ['return']  or token.tipo in ['return'] :
		RS();
		emparejar(';')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', '[', 'break', 'continue', 'return'] )
def CSB():
	if token.token in  ['case']  or token.tipo in ['case'] :
		emparejar('case')
		emparejar('valor_entero')
		emparejar('{')
		IBC();
		emparejar('}')
	else:
		errorSintaxis( ['case'] )
def CSBS():
	if token.token in  ['case']  or token.tipo in ['case'] :
		emparejar('case')
		emparejar('valor_entero')
		emparejar('{')
		IBSC();
		emparejar('}')
	else:
		errorSintaxis( ['case'] )
def D():
	if token.token in  ['set']  or token.tipo in ['set'] :
		emparejar('set')
		emparejar('id')
		ARR();
		VALASIG();
	else:
		errorSintaxis( ['set'] )
def DB():
	if token.token in  ['default']  or token.tipo in ['default'] :
		DSB();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['default', '}'] )
def DBS():
	if token.token in  ['default']  or token.tipo in ['default'] :
		DSBS();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['default', '}'] )
def DSB():
	if token.token in  ['default']  or token.tipo in ['default'] :
		emparejar('default')
		emparejar('{')
		IBC();
		emparejar('}')
	else:
		errorSintaxis( ['default'] )
def DSBS():
	if token.token in  ['default']  or token.tipo in ['default'] :
		emparejar('default')
		emparejar('{')
		IBSC();
		emparejar('}')
	else:
		errorSintaxis( ['default'] )
def ELSEB():
	if token.token in  ['else']  or token.tipo in ['else'] :
		ELSESB();
		ELSEB();
	elif token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue'] )
def ELSEBS():
	if token.token in  ['else']  or token.tipo in ['else'] :
		ELSESBS();
		ELSEBS();
	elif token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue'] )
def ELSEIF():
	if token.token in  ['elseif']  or token.tipo in ['elseif'] :
		emparejar('elseif')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('then')
		emparejar('{')
		IB();
		emparejar('}')
	else:
		errorSintaxis( ['elseif'] )
def ELSEIFB():
	if token.token in  ['elseif']  or token.tipo in ['elseif'] :
		ELSEIF();
		ELSEIFB();
	elif token.token in  ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue']  or token.tipo in ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['elseif', 'else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}', 'break', 'continue'] )
def ELSEIFBS():
	if token.token in  ['elseif']  or token.tipo in ['elseif'] :
		ELSEIFS();
		ELSEIFBS();
	elif token.token in  ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue']  or token.tipo in ['else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['elseif', 'else', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}', 'break', 'continue'] )
def ELSEIFS():
	if token.token in  ['elseif']  or token.tipo in ['elseif'] :
		emparejar('elseif')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('then')
		emparejar('{')
		IBS();
		emparejar('}')
	else:
		errorSintaxis( ['elseif'] )
def ELSESB():
	if token.token in  ['else']  or token.tipo in ['else'] :
		emparejar('else')
		emparejar('{')
		IB();
		emparejar('}')
	else:
		errorSintaxis( ['else'] )
def ELSESBS():
	if token.token in  ['else']  or token.tipo in ['else'] :
		emparejar('else')
		emparejar('{')
		IBS();
		emparejar('}')
	else:
		errorSintaxis( ['else'] )
def EXE():
	if token.token in  ['[']  or token.tipo in ['['] :
		emparejar('[')
		EXEB();
		emparejar(']')
	else:
		errorSintaxis( ['['] )
def EXEB():
	if token.token in  ['expr']  or token.tipo in ['expr'] :
		emparejar('expr')
		emparejar('{')
		EXPR();
		emparejar('}')
	elif token.token in  ['id']  or token.tipo in ['id'] :
		emparejar('id')
		SALL();
	elif token.token in  ['id']  or token.tipo in ['id'] :
		emparejar('id')
		emparejar('epsilon')
	elif token.token in  ['array']  or token.tipo in ['array'] :
		emparejar('array')
		ARRLLA();
	elif token.token in  ['gets']  or token.tipo in ['gets'] :
		IMPUT();
	else:
		errorSintaxis( ['expr', 'id', 'id', 'array', 'gets'] )
def EXPR():
	if token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
		BINEXPR();
	elif token.token in  ['!', '-']  or token.tipo in ['!', '-'] :
		UNEXPR();
	elif token.token in  ['(']  or token.tipo in ['('] :
		emparejar('(')
		EXPR();
		emparejar(')')
		BINEXPR();
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
		BINEXPR();
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
		BINEXPR();
	else:
		errorSintaxis( ['valor_entero', 'valor_double', 'valor_string', '!', '-', '(', '$', '['] )
def FORB():
	if token.token in  ['for']  or token.tipo in ['for'] :
		emparejar('for')
		emparejar('{')
		emparejar('set')
		emparejar('id')
		FORSETA();
		emparejar('}')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('{')
		emparejar('incr')
		emparejar('id')
		INCRA();
		emparejar('}')
		emparejar('{')
		IBC();
		emparejar('}')
	else:
		errorSintaxis( ['for'] )
def FORBS():
	if token.token in  ['for']  or token.tipo in ['for'] :
		emparejar('for')
		emparejar('{')
		emparejar('set')
		emparejar('id')
		FORSETAS();
		emparejar('}')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('{')
		emparejar('incr')
		emparejar('id')
		INCRAS();
		emparejar('}')
		emparejar('{')
		IBSC();
		emparejar('}')
	else:
		errorSintaxis( ['for'] )
def FORSETA():
	if token.token in  ['valor_entero']  or token.tipo in ['valor_entero'] :
		emparejar('valor_entero')
	elif token.token in  ['expr']  or token.tipo in ['expr'] :
		emparejar('expr')
		emparejar('{')
		EXPR();
		emparejar('}')
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	else:
		errorSintaxis( ['valor_entero', 'expr', '$'] )
def FORSETAS():
	if token.token in  ['valor_entero']  or token.tipo in ['valor_entero'] :
		emparejar('valor_entero')
	elif token.token in  ['expr']  or token.tipo in ['expr'] :
		emparejar('expr')
		emparejar('{')
		EXPR();
		emparejar('}')
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	else:
		errorSintaxis( ['valor_entero', 'expr', '$'] )
def I():
	if token.token in  ['set']  or token.tipo in ['set'] :
		D();
		emparejar(';')
	elif token.token in  ['if']  or token.tipo in ['if'] :
		IFB();
	elif token.token in  ['while']  or token.tipo in ['while'] :
		WHILEB();
	elif token.token in  ['for']  or token.tipo in ['for'] :
		FORB();
	elif token.token in  ['switch']  or token.tipo in ['switch'] :
		SWICTHB();
	elif token.token in  ['gets']  or token.tipo in ['gets'] :
		IMPUT();
		emparejar(';')
	elif token.token in  ['log']  or token.tipo in ['log'] :
		OUTPUT();
		emparejar(';')
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
		emparejar(';')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '['] )
def IB():
	if token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '['] :
		I();
		IB();
	elif token.token in  ['eof', '}']  or token.tipo in ['eof', '}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof', '}'] )
def IBC():
	if token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'break', 'continue']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'break', 'continue'] :
		CI();
		IBC();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'break', 'continue', '}'] )
def IBS():
	if token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return'] :
		SI();
		IBS();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return', '}'] )
def IBSC():
	if token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', '[', 'break', 'continue', 'return']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', '[', 'break', 'continue', 'return'] :
		CIS();
		IBSC();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', '[', 'break', 'continue', 'return', '}'] )
def ID():
	if token.token in  ['$']  or token.tipo in ['$'] :
		emparejar('$')
		emparejar('id')
		ARR;();
	else:
		errorSintaxis( ['$'] )
def IFB():
	if token.token in  ['if']  or token.tipo in ['if'] :
		emparejar('if')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('then')
		emparejar('{')
		IB();
		emparejar('}')
		ELSEIFB();
		ELSEB();
	else:
		errorSintaxis( ['if'] )
def IFBS():
	if token.token in  ['if']  or token.tipo in ['if'] :
		emparejar('if')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('then')
		emparejar('{')
		IBS();
		emparejar('}')
		ELSEIFBS();
		ELSEBS();
	else:
		errorSintaxis( ['if'] )
def IMPUT():
	if token.token in  ['gets']  or token.tipo in ['gets'] :
		emparejar('gets')
		emparejar('stdin')
	else:
		errorSintaxis( ['gets'] )
def INCRA():
	if token.token in  ['valor_entero']  or token.tipo in ['valor_entero'] :
		emparejar('valor_entero')
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['valor_entero', '}'] )
def INCRAS():
	if token.token in  ['valor_entero']  or token.tipo in ['valor_entero'] :
		emparejar('valor_entero')
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['valor_entero', '}'] )
def OUTA():
	if token.token in  ['[']  or token.tipo in ['['] :
		EXE();
	elif token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	else:
		errorSintaxis( ['[', 'valor_entero', 'valor_double', 'valor_string', '$'] )
def OUTPUT():
	if token.token in  ['log']  or token.tipo in ['log'] :
		emparejar('log')
		OUTA();
	else:
		errorSintaxis( ['log'] )
def RA():
	if token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
	elif token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
	elif token.token in  [';']  or token.tipo in [';'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['$', '[', 'valor_entero', 'valor_double', 'valor_string', ';'] )
def RS():
	if token.token in  ['return']  or token.tipo in ['return'] :
		emparejar('return')
		RA();
	else:
		errorSintaxis( ['return'] )
def S():
	if token.token in  ['proc', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof']  or token.tipo in ['proc', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof'] :
		SRB();
		IB();
		emparejar('eof')
	else:
		errorSintaxis( ['proc', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof'] )
def SAD():
	if token.token in  ['{']  or token.tipo in ['{'] :
		emparejar('{')
		emparejar('id')
		emparejar('}')
	else:
		errorSintaxis( ['{'] )
def SAF():
	if token.token in  ['[']  or token.tipo in ['['] :
		EXE();
	elif token.token in  ['expr']  or token.tipo in ['expr'] :
		emparejar('expr')
		emparejar('{')
		EXPR();
		emparejar('}')
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	elif token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
	else:
		errorSintaxis( ['[', 'expr', '$', 'valor_entero', 'valor_double', 'valor_string'] )
def SALL():
	if token.token in  ['{']  or token.tipo in ['{'] :
		emparejar('{')
		SAF();
		emparejar('}')
	else:
		errorSintaxis( ['{'] )
def SI():
	if token.token in  ['set']  or token.tipo in ['set'] :
		D();
		emparejar(';')
	elif token.token in  ['if']  or token.tipo in ['if'] :
		IFBS();
	elif token.token in  ['while']  or token.tipo in ['while'] :
		WHILEBS();
	elif token.token in  ['for']  or token.tipo in ['for'] :
		FORBS();
	elif token.token in  ['switch']  or token.tipo in ['switch'] :
		SWITCHBS();
	elif token.token in  ['gets']  or token.tipo in ['gets'] :
		IMPUT();
		emparejar(';')
	elif token.token in  ['log']  or token.tipo in ['log'] :
		OUTPUT();
		emparejar(';')
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
		emparejar(';')
	elif token.token in  ['return']  or token.tipo in ['return'] :
		RS();
		emparejar(';')
	else:
		errorSintaxis( ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'return'] )
def SLAD():
	if token.token in  ['{']  or token.tipo in ['{'] :
		SAD();
		SLAD();
	elif token.token in  ['}']  or token.tipo in ['}'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['{', '}'] )
def SLALL():
	if token.token in  ['{']  or token.tipo in ['{'] :
		SALL();
		SLALL();
	elif token.token in  []  or token.tipo in [] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['{'] )
def SRB():
	if token.token in  ['proc']  or token.tipo in ['proc'] :
		SRD();
		SRB();
	elif token.token in  ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof']  or token.tipo in ['set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof'] :
		emparejar('epsilon')
	else:
		errorSintaxis( ['proc', 'set', 'if', 'while', 'for', 'switch', 'gets', 'log', '[', 'eof'] )
def SRD():
	if token.token in  ['proc']  or token.tipo in ['proc'] :
		emparejar('proc')
		emparejar('id')
		emparejar('{')
		SLAD();
		emparejar('}')
		emparejar('{')
		IBS();
		emparejar('}')
	else:
		errorSintaxis( ['proc'] )
def SWICTHB():
	if token.token in  ['switch']  or token.tipo in ['switch'] :
		emparejar('switch')
		emparejar('$')
		emparejar('id')
		emparejar('{')
		CB();
		DB();
		emparejar('}')
	else:
		errorSintaxis( ['switch'] )
def SWITCHBS():
	if token.token in  ['switch']  or token.tipo in ['switch'] :
		emparejar('switch')
		emparejar('$')
		emparejar('id')
		emparejar('{')
		CBS();
		DBS();
		emparejar('}')
	else:
		errorSintaxis( ['switch'] )
def UNEXPR():
	if token.token in  ['!', '-']  or token.tipo in ['!', '-'] :
		UNOP();
		EXPR();
	else:
		errorSintaxis( ['!', '-'] )
def UNOP():
	if token.token in  ['!']  or token.tipo in ['!'] :
		emparejar('!')
	elif token.token in  ['-']  or token.tipo in ['-'] :
		emparejar('-')
	else:
		errorSintaxis( ['!', '-'] )
def VAL():
	if token.token in  ['valor_entero']  or token.tipo in ['valor_entero'] :
		emparejar('valor_entero')
	elif token.token in  ['valor_double']  or token.tipo in ['valor_double'] :
		emparejar('valor_double')
	elif token.token in  ['valor_string']  or token.tipo in ['valor_string'] :
		emparejar('valor_string')
	else:
		errorSintaxis( ['valor_entero', 'valor_double', 'valor_string'] )
def VALASIG():
	if token.token in  ['valor_entero', 'valor_double', 'valor_string']  or token.tipo in ['valor_entero', 'valor_double', 'valor_string'] :
		VAL();
	elif token.token in  ['[']  or token.tipo in ['['] :
		EXE();
	elif token.token in  ['$']  or token.tipo in ['$'] :
		ID();
	else:
		errorSintaxis( ['valor_entero', 'valor_double', 'valor_string', '[', '$'] )
def WHILEB():
	if token.token in  ['while']  or token.tipo in ['while'] :
		emparejar('while')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('{')
		IBC();
		emparejar('}')
	else:
		errorSintaxis( ['while'] )
def WHILEBS():
	if token.token in  ['while']  or token.tipo in ['while'] :
		emparejar('while')
		emparejar('{')
		EXPR();
		emparejar('}')
		emparejar('{')
		IBSC();
		emparejar('}')
	else:
		errorSintaxis( ['while'] )

def errorSintaxis(lista):
	global stopProcess
	if type( lista ) is list:
		sorted(lista)
	error = token.token
	if token.tipo == 'identificador':
		error = 'identificador'
	print('<' + str( token.fila + 1 ) + ':' + str( token.columna  + 1 ) + "> Error sintactico: se encontro: '" + error + "'; se esperaba: '" + "', '".join( lista ) + "'.")
	sys.exit(0)
	stopProcess = True

def emparejar( tokEsperado ):
	global token
	if tokEsperado != 'epsilon':
		if token.token in tokEsperado or token.tipo == tokEsperado:
			token = TOKENS.pop( 0 )
		else:
			errorSintaxis( tokEsperado )

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
		elif token.tipo == 'valor_string':
			token.token = token.token[1:-1]
			#print('<'+token.tipo+','+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		elif token.tipo != 'EOF'  and token.tipo != 'EOL':
			#print('<'+token.tipo+','+token.token+','+str(token.fila+1)+','+str(token.columna+1)+'>' )
			TOKENS.append(token)
		else:
			break
	linea = sys.stdin.readline()
	Fila += 1
	Columna = 0
	#token = Token( "pesos", "pesos", 0, 0 )
	#TOKENS.append( token )
token = Token( "EOF", "eof", 0, 0 )
TOKENS.append( token )
token = TOKENS.pop( 0 )
#for i in TOKENS:
	#print(i)
while not stopProcess:
	S()
	token = TOKENS.pop( 0 )
	if token.tipo == "EOF":
		print("El analisis sintactico se ha finalizado correctamente.")
		break
