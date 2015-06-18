import socket
import thread
from redefinePrint import cprint, draw_print


PORTARECEBECONEXOES = 50001
conexoes = []
numero_de_peers = 1
prioridade = 0
timestamp = 1
import recursos


def conecta_peers(lista_ips_peers):
    cprint("conectando peers")
    for ip in lista_ips_peers:

        cprint("conectando com", ip)
        conexao = socket.create_connection((ip, PORTARECEBECONEXOES))
        conexoes.append(conexao)
        thread.start_new_thread(thread_trata_mensagens, (conexao, len(conexoes)-1,))


def thread_trata_mensagens(conexao, id_peer):
    while True:
        time_stamp_mensagem, mensagem = conexao.recv(1024).split(":")
        time_stamp_mensagem = int(time_stamp_mensagem)
        cprint("recebeu mensagem", mensagem, "timestamp da msg = ", time_stamp_mensagem)
        if mensagem[:3] == "ACK":
            recurso = int(mensagem[3:])
            recursos.trata_ack(id_peer, recurso)
        else:
            recursos.trata_pedido_recurso(id_peer, int(mensagem), time_stamp_mensagem)
        draw_print()


def thread_espera_conexoes():

    import socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), PORTARECEBECONEXOES))
    serversocket.listen(5)
    while True:

        conexao, endereco = serversocket.accept()
        conexoes.append(conexao)
        cprint("recebeu novo pedido de conexao de", endereco)
        thread.start_new_thread(thread_trata_mensagens, (conexao, len(conexoes)-1,))


def abre_thread_espera_conexoes():
    thread.start_new_thread(thread_espera_conexoes, ())


def broadcast(mensagem):
    for conexao in conexoes:
        cprint("mandando mensagem'"+str(timestamp)+":"+mensagem+"'")
        conexao.send(str(timestamp)+":"+mensagem)


def manda_ack(peer, recurso):
    conexoes[peer].send(str(timestamp)+":"+"ACK"+str(recurso))

