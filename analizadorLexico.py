# Importa el módulo ply.lex para el análisis léxico.
import ply.lex as lex    #ademas facilita la tarea de analizar y reconocer tokens en el código fuente de un programa
import ply.yacc as yacc  # Importa el módulo ply.yacc para el análisis sintáctico.
import tkinter as tk  # Importa el módulo tkinter para crear la interfaz gráfica.

# Definición de tokens
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

# Ignorar espacios y saltos de línea
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
    p[0] = int(p[1])  # Esta regla maneja números y asigna el valor numérico a p[0].

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

# Funciones para la interfaz gráfica
def calcular():
    expresion = entrada.get()  # Obtiene la expresión desde la entrada de texto.
    try:
        # Clasificar los tokens
        tokens_clasificados = clasificar_tokens(expresion)

        if not tokens_clasificados:
            resultado_label.config(text="Error: La entrada está vacía o no hay tokens válidos")
            return

        resultado = parser.parse(expresion)  # Analiza la expresión y calcula el resultado.

        resultado_label.config(text=f"Resultado: {resultado}")  # Muestra el resultado en la etiqueta de resultado.

        # Mostrar los tokens en el Text widget
        tokens_text.config(state=tk.NORMAL)  # Habilita la edición del Text widget.
        tokens_text.delete(1.0, tk.END)  # Borra el contenido anterior.
        tokens_text.insert(tk.END, "Tokens Clasificados:\n")
        for token in tokens_clasificados:
            token_text = f"Token: {token[0]}, Valor: {token[1]}\n"
            tokens_text.insert(tk.END, token_text)  # Muestra los tokens en el Text widget.
        tokens_text.config(state=tk.DISABLED)  # Deshabilita la edición del Text widget.

    except Exception as e:
        resultado_label.config(text="Error: Error de sintaxis")  # Muestra un mensaje de error de sintaxis.
        tokens_text.config(state=tk.NORMAL)  # Habilita la edición del Text widget.
        tokens_text.delete(1.0, tk.END)  # Borra el contenido anterior.
        tokens_text.insert(tk.END, f"Error de sintaxis: {e}\n")  # Muestra el error en el Text widget.
        tokens_text.config(state=tk.DISABLED)  # Deshabilita la edición del Text widget.

# Crear la ventana
ventana = tk.Tk()  # Crea una ventana de la interfaz gráfica.
ventana.title("Calculadora")  # Establece el título de la ventana.

# Crear y configurar los widgets
etiqueta = tk.Label(ventana, text="Ingrese una expresión:")  # Crea una etiqueta.
entrada = tk.Entry(ventana)  # Crea una entrada de texto.
calcular_boton = tk.Button(ventana, text="Calcular", command=calcular)  # Crea un botón de cálculo.
resultado_label = tk.Label(ventana, text="Resultado:")  # Crea una etiqueta para mostrar el resultado.
tokens_text = tk.Text(ventana, height=10, width=40)  # Crea un área de texto para mostrar tokens.
tokens_text.config(state=tk.DISABLED)  # Deshabilita la edición del Text widget.

# Colocar los widgets en la ventana
etiqueta.pack()  # Coloca la etiqueta en la ventana.
entrada.pack()  # Coloca la entrada de texto en la ventana.
calcular_boton.pack()  # Coloca el botón en la ventana.
resultado_label.pack()  # Coloca la etiqueta de resultado en la ventana.
tokens_text.pack()  # Coloca el área de texto en la ventana.

# Iniciar la interfaz gráfica
ventana.mainloop()  # Inicia el bucle principal de la interfaz gráfica.

