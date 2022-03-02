import sys
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculadora')
        self.setFixedSize(260, 320)

        self.componente_general = QWidget(self)
        self.setCentralWidget(self.componente_general)

        self.layout_principal = QVBoxLayout()
        self.componente_general.setLayout(self.layout_principal)

        # Métodos para la parte visual de la calculadora:
        self._crear_area_display()
        self._crear_botones()

        # Señales:
        self._conectar_botones()

    def _crear_area_display(self):
        self.linea_entrada = QLineEdit()
        # Propiedades de entrada
        self.linea_entrada.setFixedHeight(35)
        self.linea_entrada.setAlignment(Qt.AlignRight)
        self.linea_entrada.setReadOnly(True)
        # Publicar linea de entrada en layout:
        self.layout_principal.addWidget(self.linea_entrada)

    def _crear_botones(self):
        layout_botones = QGridLayout()
        self.botones = {}  # nombre boton | posición (renglón, columna)
        self.botones = {'AC': (0, 0),
                        '÷': (0, 3),
                        '7': (1, 0),
                        '8': (1, 1),
                        '9': (1, 2),
                        'x': (1, 3),
                        '4': (2, 0),
                        '5': (2, 1),
                        '6': (2, 2),
                        '-': (2, 3),
                        '1': (3, 0),
                        '2': (3, 1),
                        '3': (3, 2),
                        '+': (3, 3),
                        '0': (4, 0),
                        '.': (4, 2),
                        '=': (4, 3)}

        # Crear botones y agregarlos al QGridLayoutout
        for texto_boton, posicion in self.botones.items():
            if texto_boton not in {'AC', '0'}:
                self.botones[texto_boton] = QPushButton(texto_boton)
                self.botones[texto_boton].setFixedSize(50, 50)
                # Publicar el boton en el QGridLayout:
                layout_botones.addWidget(self.botones[texto_boton], posicion[0], posicion[1])

        self.botones['AC'] = QPushButton('AC')
        self.botones['AC'].setFixedSize(175, 50)
        layout_botones.addWidget(self.botones['AC'], 0, 0, 1, 3)
        self.botones['0'] = QPushButton('0')
        self.botones['0'].setFixedSize(115, 50)
        layout_botones.addWidget(self.botones['0'], 4, 0, 1, 2)

        # Agregar layout botones a layout principal:
        self.layout_principal.addLayout(layout_botones)

    def _conectar_botones(self):
        # Recorrer botones en el diccionario:
        for texto_boton, posicion_boton in self.botones.items():
            if texto_boton not in {'AC', '='}:  # filtrar Casos especiales
                posicion_boton.clicked.connect(partial(self._construir_expresion, texto_boton))

            # Conectar botones AC e =:
            self.botones['AC'].clicked.connect(self._limpiar_linea_entrada)
            self.botones['='].clicked.connect(self._calcular_resultado)
            self.linea_entrada.returnPressed.connect(self._calcular_resultado)

    def _construir_expresion(self, texto_boton):
        texto_display = self.obtener_texto_display()
        if texto_display == 'Syntax ERROR':
            self._limpiar_linea_entrada()

        expresion = self.obtener_texto_display() + texto_boton
        # Actiualizar la línea de entrada:
        self.actualizar_texto_display(expresion)

    def obtener_texto_display(self):
        return self.linea_entrada.text()

    def actualizar_texto_display(self, texto):
        self.linea_entrada.setText(texto)
        self.linea_entrada.setFocus()

    def _limpiar_linea_entrada(self):
        self.actualizar_texto_display('')

    # Filtrar y reemplazar los símbolos ÷ y x por:
    def filtro_simbolos(self, texto_boton):
        texto_boton = texto_boton.replace('÷', '/')
        texto_boton = texto_boton.replace('x', '*')
        return texto_boton

    def _calcular_resultado(self):
        resultado = self._evaluar_expresion(self.obtener_texto_display())
        self.actualizar_texto_display(resultado)

    def _evaluar_expresion(self, expresion):
        expresion = self.filtro_simbolos(expresion)
        try:
            # Función eval para evaluar expresiones:
            resultado = str(eval(expresion))
        except Exception as e:
            resultado = 'Syntax ERROR'
        return resultado


if __name__ == '__main__':
    app = QApplication([])
    calculadora = Calculadora()
    calculadora.show()
    sys.exit(app.exec())
