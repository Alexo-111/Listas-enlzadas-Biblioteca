class Nodo:
    """Nodo de una lista simplemente ligada: campos INFO y LIGA."""
    def __init__(self, info):
        self.info = info    # INFO
        self.liga = None    # LIGA (None equivale a NIL)


# ---------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------
def longitud(p):
    """Cuenta cuántos nodos tiene la lista."""
    cuenta = 0
    q = p
    while q is not None:
        cuenta += 1
        q = q.liga
    return cuenta


def iguales(a, b):
    """Compara dos textos sin distinguir mayúsculas ni espacios en los extremos."""
    return a.strip().lower() == b.strip().lower()


def obtener(p, pos):
    """Devuelve el nodo que está en la posición 'pos'."""
    q = p
    for _ in range(pos):
        q = q.liga
    return q


def recorre_iterativo(p):
    """Algoritmo 5.3: recorre e imprime la lista."""
    if p is None:
        print("  (la lista está vacía)")
        return
    q = p
    posicion = 0
    while q is not None:
        print(f"  [{posicion}] {q.info}")
        q = q.liga
        posicion += 1


def pedir_entero(mensaje, minimo, maximo):
    """Pide un entero entre minimo y maximo (ambos incluidos)."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Valor inválido. Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("Debe escribir un número entero.")


def pedir_si_no(mensaje):
    """Pregunta s/n y devuelve True si la respuesta es sí."""
    while True:
        r = input(mensaje + " (s/n): ").strip().lower()
        if r in ("s", "si", "sí"):
            return True
        if r in ("n", "no"):
            return False
        print("Responda 's' o 'n'.")


# ---------------------------------------------------------------
# Inserción y sobrescritura
# ---------------------------------------------------------------
def inserta_en_posicion(p, dato, pos):
    """Inserta 'dato' en la posición 'pos' (desde 0), desplazando los demás.
    Devuelve P, que cambia si se inserta al inicio."""
    nuevo = Nodo(dato)

    if pos == 0:                  # al inicio (también cubre la lista vacía)
        nuevo.liga = p
        return nuevo

    t = obtener(p, pos - 1)       # nodo anterior a la posición
    nuevo.liga = t.liga
    t.liga = nuevo
    return p


def sobrescribe_en_posicion(p, dato, pos):
    """Reemplaza la información del nodo en 'pos'. Devuelve el valor anterior."""
    nodo = obtener(p, pos)
    anterior = nodo.info
    nodo.info = dato
    return anterior


# ---------------------------------------------------------------
# Eliminación
# ---------------------------------------------------------------
def elimina_posicion(p, pos):
    """Elimina el nodo en la posición 'pos'.
    Devuelve (nuevo P, valor eliminado)."""
    if pos == 0:                  # Algoritmo 5.9: eliminar el primero
        eliminado = p.info
        return p.liga, eliminado

    t = obtener(p, pos - 1)       # nodo anterior
    q = t.liga                    # nodo a eliminar
    t.liga = q.liga               # se salta el nodo q
    return p, q.info


def elimina_valor(p, x):
    """Algoritmo 5.11 (Elimina_X): elimina la primera aparición de x.
    Devuelve (nuevo P, True/False según si se encontró)."""
    q = p
    t = None                      # t va un nodo detrás de q
    while q is not None and not iguales(q.info, x):
        t = q
        q = q.liga

    if q is None:                 # no se encontró
        return p, False

    if t is None:                 # es el primero
        p = q.liga
    else:                         # está en medio o al final
        t.liga = q.liga
    return p, True


# ---------------------------------------------------------------
# Búsqueda
# ---------------------------------------------------------------
def busca(p, x):
    """Algoritmo 5.13 (Búsqueda_desordenada), ampliado para devolver
    todas las posiciones donde aparece x."""
    posiciones = []
    q = p
    pos = 0
    while q is not None:
        if iguales(q.info, x):
            posiciones.append(pos)
        q = q.liga
        pos += 1
    return posiciones


# ---------------------------------------------------------------
# Opciones del menú
# ---------------------------------------------------------------
def opcion_agregar(p):
    dato = input("Valor a agregar: ")
    n = longitud(p)

    if n == 0:
        print("La lista está vacía, el dato se agregará en la posición 0.")
        return inserta_en_posicion(p, dato, 0)

    pos = pedir_entero(
        f"¿En qué posición desea agregarlo? (0 = inicio, {n} = final, otra = en medio): ",
        0, n)

    # Si la posición ya está ocupada, se pregunta si se sobrescribe
    if pos < n:
        actual = obtener(p, pos).info
        print(f"La posición {pos} ya contiene: '{actual}'")
        if pedir_si_no("¿Desea sobrescribir ese valor?"):
            sobrescribe_en_posicion(p, dato, pos)
            print(f"'{actual}' fue reemplazado por '{dato}' en la posición {pos}.")
            return p
        print("No se sobrescribe; el dato se insertará y los demás se desplazan.")

    p = inserta_en_posicion(p, dato, pos)
    print(f"'{dato}' agregado en la posición {pos}.")
    return p


def opcion_eliminar(p):
    n = longitud(p)
    if n == 0:
        print("La lista está vacía, no hay nada que eliminar.")
        return p

    print("\n  1. Eliminar por posición")
    print("  2. Eliminar por valor")
    modo = input("  Opción: ")

    if modo == "1":
        print("\nContenido actual:")
        recorre_iterativo(p)
        pos = pedir_entero(f"Posición a eliminar (0 a {n - 1}): ", 0, n - 1)
        p, eliminado = elimina_posicion(p, pos)
        print(f"'{eliminado}' fue eliminado de la posición {pos}.")
    elif modo == "2":
        x = input("Valor a eliminar: ")
        p, encontrado = elimina_valor(p, x)
        if encontrado:
            print(f"Se eliminó la primera aparición de '{x}'.")
        else:
            print(f"'{x}' no se encuentra en la lista.")
    else:
        print("Opción no válida.")
    return p


def opcion_buscar(p):
    if p is None:
        print("La lista está vacía.")
        return
    x = input("Valor a buscar: ")
    posiciones = busca(p, x)
    if posiciones:
        lista_pos = ", ".join(str(i) for i in posiciones)
        print(f"'{x}' sí se encuentra en la lista, en la(s) posición(es): {lista_pos}")
    else:
        print(f"'{x}' no se encuentra en la lista.")


def menu():
    p = None   # lista vacía: P = NIL

    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar un dato")
        print("2. Eliminar un dato")
        print("3. Buscar un dato")
        print("4. Mostrar la lista")
        print("5. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            p = opcion_agregar(p)
        elif opcion == "2":
            p = opcion_eliminar(p)
        elif opcion == "3":
            opcion_buscar(p)
        elif opcion == "4":
            print("\nContenido de la lista:")
            recorre_iterativo(p)
        elif opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()