#  se importa el módulo ply.lex para el análisis léxico.
import ply.lex as lex    #ademas de que facilita la tarea de analizar y reconocer tokens en el código fuente de un programa
import ply.yacc as yacc  # se importa el módulo ply.yacc para el análisis sintáctico.

# Definición de los tokens
tokens = (
    'NUMERO',
    'SUMA',
    'MENOS',
    'MULTIPLICACION',
    'DIVISION',
    'LPAREN',
    'RPAREN',
    'EXPONENTE',
    'MAYORQUE',
    'MENORQUE',
)

# Expresiones regulares para los tokens
t_SUMA = r'\+'  # Token para la suma.
t_MENOS = r'\-'  # Token para la resta.
t_MULTIPLICACION = r'\*'  # Token para la multiplicación.
t_DIVISION = r'\/'  # Token para la división.
t_LPAREN = r'\('  # Token para el paréntesis izquierdo.
t_RPAREN = r'\)'  # Token para el paréntesis derecho.
t_EXPONENTE = r'\^'  # Token para el exponente.
t_MAYORQUE = r'>'  # Token para el mayor que.
t_MENORQUE = r'<'  # Token para el menor que.
t_NUMERO = r'\d+'  # Token para números.

# para ignorar espacios y saltos de línea
t_ignore = ' \n'  # Define que se deben ignorar espacios y saltos de línea.

# Función para manejar errores de tokens inválidos
def t_error(t):
    print(f"Token inválido: {t.value[0]}")
    t.lexer.skip(1)  # Ignora el token inválido y continúa el análisis.

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática
def p_expression(p):
    '''
    expression : expression SUMA expression
               | expression MENOS expression
               | expression MULTIPLICACION expression
               | expression DIVISION expression
               | expression EXPONENTE expression
               | expression MAYORQUE expression
               | expression MENORQUE expression
    '''
    # Esta es una regla de la gramática que describe cómo se deben combinar expresiones.
    # Puede ser una suma, resta, multiplicación, división, etc.
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    elif p[2] == '>':
        p[0] = int(p[1] > p[3])
    elif p[2] == '<':
        p[0] = int(p[1] < p[3])

def p_expression_number(p):
    'expression : NUMERO'
    p[0] = int(p[1])  # Esta regla maneja los números y asigna el valor numérico a p[0].

def p_expression_parentheses(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]  # Esta regla maneja expresiones dentro de paréntesis y toma el valor de la expresión.

def p_error(p):
    print("Error de sintaxis")  # Esta función maneja errores de sintaxis en la gramática.

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Función para clasificar tokens
def clasificar_tokens(expresion):
    lexer.input(expresion)
    tokens_clasificados = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens_clasificados.append((token.type, token.value))
    return tokens_clasificados  # Retorna una lista de tokens clasificados.

# Función para calcular el resultado
def calcular_resultado(expresion):
    try:
        # Clasificar los tokens
        tokens_clasificados = clasificar_tokens(expresion)

        if not tokens_clasificados:
            print("Error: La entrada está vacía o no hay tokens válidos")
            return None

        resultado = parser.parse(expresion)  # Analiza la expresión y calcula el resultado.

        # Imprimir tokens clasificados
        print("Tokens Clasificados:")
        for token in tokens_clasificados:
            print(f"Token: {token[0]}, Valor: {token[1]}")

        return resultado

    except Exception as e:
        print(f"Error de sintaxis: {e}")
        return None

# para solicitar entrada al usuario
expresion_a_evaluar = input("Ingrese una expresión: ")

# Calcular resultado y mostrar tokens
resultado_final = calcular_resultado(expresion_a_evaluar)

if resultado_final is not None:
    print(f"Resultado final: {resultado_final}")
