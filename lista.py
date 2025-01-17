import os
import random

palabraAdivinada = []
letrasEscritas = []
intentos = 6
palabraSecretaAjustes = "1"
nombreArchivoGrupos = "grupos.txt"


def prepararPalabra(original):
    global palabraAdivinada
    original = original.lower()
    palabraAdivinada = []
    for letra in original:
        palabraAdivinada.append({
            "letra": letra,
            "adivinada": False,
        })


def imprimirPalabra():
    for letraCompuesta in palabraAdivinada:
        if letraCompuesta["adivinada"]:
            print(letraCompuesta["letra"], end="")
        else:
            print("-", end="")
    print("")


def imprimirPalabraOriginal():
    for letraCompuesta in palabraAdivinada:
        print(letraCompuesta["letra"], end="")


def descubrirLetra(letraDeUsuario):
    global palabraAdivinada
    global letrasEscritas
    global intentos
    letraDeUsuario = letraDeUsuario.lower()
    if letraDeUsuario in letrasEscritas:
        return
    else:
        letrasEscritas.append(letraDeUsuario)
    if not letraEstaEnPalabra(letraDeUsuario):
        intentos -= 1
    else:
        for letraCompuesta in palabraAdivinada:
            if letraCompuesta["letra"] == letraDeUsuario:
                letraCompuesta["adivinada"] = True


def letraEstaEnPalabra(letra):
    global palabraAdivinada
    for letraCompuesta in palabraAdivinada:
        if letraCompuesta["letra"] == letra:
            return True
    return False


def imprimirAhorcado():
    if intentos == 1:
        print("""
                       ___
                      |   |
                     _O/  |
                      |   |
                     / \  |
                    ______|
        """)
    elif intentos == 2:
        print("""
                       ___
                      |   |
                     _O/  |
                      |   |
                       \  |
                    ______|
        """)
    elif intentos == 3:
        print("""
                       ___
                      |   |
                     _O/  |
                      |   |
                          |
                    ______|
        """)
    elif intentos == 4:
        print("""
                       ___
                      |   |
                     _O/  |
                          |
                          |
                    ______|
        """)
    elif intentos == 5:
        print("""
                       ___
                      |   |
                      O/  |
                          |
                          |
                    ______|
        """)
    elif intentos == 6:
        print("""
                       ___
                      |   |
                      O   |
                          |
                          |
                    ______|
        """)


def dibujarIntentos():
    print("Intentos restantes: " + str(intentos))


def haGanado():
    global palabraAdivinada
    for letra in palabraAdivinada:
        if not letra["adivinada"]:
            return False
    return True

#3
def instrucciones():
    print("""
INSTRUCCIONES
El objetivo de este juego es descubrir una palabra adivinando las letras que la componen.
1. Debes seleccionar de qué conjunto de palabras quisieras jugar
2. Inicias con """ + str(intentos) + " vidas" +
          """
          3. Ingresa una letra que creas vaya en la palabra a adivinar
          Suerte con el juego
          """)

#4
def obtenerPalabra():
    print("Jugar con: ")
    grupos = obtenerGrupos()
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupo = grupos[indice]
    palabras = obtenerPalabrasDeGrupo(grupo)
    return random.choice(palabras)


def jugar():
    global letrasEscritas
    global intentos
    intentos = 6
    letrasEscritas = []
    palabra = obtenerPalabra()
    prepararPalabra(palabra)
    while True:
        imprimirAhorcado()
        dibujarIntentos()
        imprimirPalabra()
        descubrirLetra(input("Ingresa la letra: "))
        if intentos <= 0:
            print("Perdiste. La palabra era: ")
            imprimirPalabraOriginal()
            return
        if haGanado():
            print("Ganaste")
            return

#5
def ajustes():
    if input("Ingrese la contraseña: ") != palabraSecretaAjustes:
        print("Contraseña incorrecta")
        return
    menu = """
1. Eliminar grupo de palabras
2. Crear grupo de palabras
3. Modificar grupo de palabras
"""
    grupos = obtenerGrupos()

    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion > 3:
        print("No válido")
        return
    if eleccion == 1:
        eliminarGrupoDePalabras(grupos)
    elif eleccion == 2:
        crearGrupoDePalabras(grupos)
    elif eleccion == 3:
        modificarGrupoDePalabras(grupos)


def eliminarGrupoDePalabras(grupos):
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupoEliminado = grupos[indice]
    del grupos[indice]
    os.unlink(grupoEliminado + ".txt")
    escribirGrupos(grupos)


def imprimirGruposYSolicitarIndice(grupos):
    for i, grupo in enumerate(grupos):
        print(f"{i + 1}. {grupo}")
    return int(input("Seleccione el grupo: ")) - 1


def crearGrupoDePalabras(grupos):
    grupo = input("Ingrese el nombre del grupo: ")
    palabras = solicitarPalabrasParaNuevoGrupo()
    escribirPalabrasDeGrupo(palabras, grupo)
    grupos.append(grupo)
    escribirGrupos(grupos)
    print("Grupo creado correctamente")


def escribirGrupos(grupos):
    with open(nombreArchivoGrupos, "w") as archivo:
        for grupo in grupos:
            archivo.write(grupo + "\n")


def escribirPalabrasDeGrupo(palabras, grupo):
    with open(grupo + ".txt", "w") as archivo:
        for palabra in palabras:
            archivo.write(palabra + "\n")


def solicitarPalabrasParaNuevoGrupo():
    palabras = []
    while True:
        palabra = input("Ingrese la palabra. Deje la cadena vacía si quiere terminar: ")
        if palabra == "":
            return palabras
        palabras.append(palabra)


def modificarGrupoDePalabras(grupos):
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupoQueSeCambia = grupos[indice]
    palabras = obtenerPalabrasDeGrupo(grupoQueSeCambia)
    menu = """
1. Cambiar una palabra
2. Agregar una palabra
3. Eliminar una palabra
Seleccione: """
    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion > 3:
        print("No válido")
        return
    if eleccion == 1:
        cambiarUnaPalabra(grupoQueSeCambia, palabras)
    elif eleccion == 2:
        agregarUnaPalabra(grupoQueSeCambia, palabras)
    elif eleccion == 3:
        eliminarUnaPalabra(grupoQueSeCambia, palabras)


def cambiarUnaPalabra(grupo, palabras):
    indice = imprimirPalabrasYSolicitarIndice(palabras)
    palabraCambiada = palabras[indice]
    print("Se cambia la palabra " + palabraCambiada)
    nuevaPalabra = input("Ingrese la nueva palabra: ")
    palabras[indice] = nuevaPalabra
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra cambiada correctamente")


def agregarUnaPalabra(grupo, palabras):
    palabra = input("Ingrese la palabra que se agrega: ")
    palabras.append(palabra)
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra agregada correctamente")


def eliminarUnaPalabra(grupo, palabras):
    indice = imprimirPalabrasYSolicitarIndice(palabras)
    del palabras[indice]
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra eliminada correctamente")


def imprimirPalabrasYSolicitarIndice(palabras):
    for i, palabra in enumerate(palabras):
        print(f"{i + 1}. {palabra}")
    return int(input("Seleccione la palabra: ")) - 1


def obtenerGrupos():
    grupos = []
    with open(nombreArchivoGrupos) as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            grupos.append(linea)
    return grupos


def obtenerPalabrasDeGrupo(grupo):
    palabras = []
    with open(grupo + ".txt") as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            palabras.append(linea)
    return palabras


def prepararArchivo():
    if not os.path.isfile(nombreArchivoGrupos):
        with open(nombreArchivoGrupos, "w") as archivo:
            archivo.write("")

#5
def menu_principal():
    menu = """
1. Jugar
2. Instrucciones
3. Ajustes
4. Salir
Seleccione: """
    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion >= 4:
        exit()
    if eleccion == 1:
        jugar()
    elif eleccion == 2:
        instrucciones()
    elif eleccion == 3:
        ajustes()


def main():
    prepararArchivo()
    while True:
        menu_principal()


main()