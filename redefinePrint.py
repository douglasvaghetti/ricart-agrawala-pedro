import os
buffersaida = []


def cprint(*entradas):
    global buffersaida
    buffersaida.append(" ".join([str(x) for x in entradas]))

    buffersaida = buffersaida[-15:]


def draw_print():
    os.system("clear")
    for linha in buffersaida:
        print linha
    import recursos
    nomes = ["T", "Q", "L"]

    print map(lambda i: nomes[i], recursos.estadoRecursos)

    print "\n>",
