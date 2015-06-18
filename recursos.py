import rede
import thread


numeroDeRecursos = 10
TENHO, QUERO, PODEPEGAR = range(3)
estadoRecursos = [PODEPEGAR]*numeroDeRecursos
ACKs_obtidos = [[False]*rede.numero_de_peers]*numeroDeRecursos
fila_pedidos_ack_armazenados = [[]]*numeroDeRecursos
from redefinePrint import cprint


def tem_recurso(n):
    return estadoRecursos[n] == TENHO


def quer_recurso(n):
    return estadoRecursos[n] == QUERO


def adquire_recurso(recurso):
    thread.start_new_thread(thread_adquire_recurso, (recurso,))


def thread_adquire_recurso(recurso):
    if estadoRecursos[recurso] != PODEPEGAR:
        cprint("voce ja tem ou ja quer este recurso")
        return
    estadoRecursos[recurso] = QUERO
    ACKs_obtidos[recurso] = [False]*rede.numero_de_peers
    rede.broadcast(str(recurso))
    while True:
        #baixar o mutex
        if ACKs_obtidos[recurso] == [True]*rede.numero_de_peers:
            #libera mutex
            break
        #libera mutex
    estadoRecursos[recurso] = TENHO


def libera_recurso(recurso):
    if not tem_recurso(recurso):
        cprint("voce nao pode liberar um recurso que voce nao tem")
        return
    estadoRecursos[recurso]=PODEPEGAR
    for pedido in fila_pedidos_ack_armazenados[recurso]:
        rede.manda_ack(pedido, recurso)


def trata_pedido_recurso(peer, recurso, timestamp_pedido):
    cprint("pedido do peer", peer, "para o recurso", recurso, "com timestamp", timestamp_pedido,)
    if estadoRecursos[recurso] == PODEPEGAR:
        rede.manda_ack(peer, recurso)
        cprint("concedido")
    elif estadoRecursos[recurso] == QUERO:
        if timestamp_pedido < rede.timestamp:
            rede.manda_ack(peer, recurso)
            cprint("concedido")
        else:
            fila_pedidos_ack_armazenados[recurso].append(peer)
            cprint("inserido na fila")
    elif estadoRecursos[recurso] == TENHO:
        fila_pedidos_ack_armazenados[recurso].append(peer)
        cprint("inserido na fila")


def trata_ack(peer, recurso):
    #baixa mutex
    ACKs_obtidos[recurso][peer] = True
    cprint("ack recebido do peer ", peer, "para recurso", recurso)
    #levanta mutex
