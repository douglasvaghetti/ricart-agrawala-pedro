import thread
import random
import recursos
import socket
from redefinePrint import cprint,draw_print

lista_peers = []
fila_mensagens = []
timestamp  = 0
numero_de_peers = 0
portaRecebeMensagens = 0

def init(listaPeers,porta_recebe_mensagens,porta_recebe_acks):
    global lista_peers
    global fila_mensagens
    global timestamp
    global numero_de_peers
    global portaRecebeMensagens
    portaRecebeMensagens = porta_recebe_mensagens
    lista_peers = listaPeers
    numero_de_peers = len(listaPeers)
    timestamp = random.random()
    listaPeers.sort()
    for peer in listaPeers:
        thread.start_new_thread(thread_recebe_mensagens,(peer,porta_recebe_mensagens,))
        thread.start_new_thread(thread_recebe_acks,(peer,porta_recebe_acks,))
    timestamp+=1

def thread_recebe_mensagens(peer,porta_recebe_mensagens):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.bind(('',porta_recebe_mensagens))
    while(True):

        dados = conexao.recv(1024)
        cprint("recebeu mensagem",dados,"do peer",peer)
        if not dados:
            cprint("TRETA")
        updateTimestamp(dados)
        fila_mensagens.append([dados,0,peer])
        fila_mensagens.sort()
        adiciona_ack(dados)
        broadcastACK(dados)
    conexao.close()


def thread_recebe_acks(peer,porta_recebe_acks):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.bind(('',porta_recebe_acks))
    while(True):
        dados,endereco = conexao.recvfrom(1024)
        cprint("recebeu ack",dados,"de",peer)
        updateTimestamp(dados)
        adiciona_ack(dados)

    conexao.close()

def adiciona_ack(mensagem):
    global fila_mensagens
    #cprint("fila mensagens = ",fila_mensagens)
    fila_mensagens[[x[0] for x in fila_mensagens].index(mensagem)][1]+=1
    if fila_mensagens[0][1]>= numero_de_peers:
        cprint("tudo ok com a mensagem ",mensagem,"subindo do middleware")

        if fila_mensagens[0][0].split(":")[1] == "POSSOPEGAR":
            if int(fila_mensagens[0][0].split(":")[4])!= portaRecebeMensagens:
                cprint("chamando trata requisicao")
                timestamp_mensagem= float(fila_mensagens[0][0].split(":")[0])
                recurso = int(fila_mensagens[0][0].split(":")[2])
                recursos.trata_requisicao(recurso, timestamp_mensagem, fila_mensagens[0][2])
        elif fila_mensagens[0][0].split(":")[1]=="PODEPEGAR":
            if int(fila_mensagens[0][0].split(":")[4])!= portaRecebeMensagens:
                recurso = int(fila_mensagens[0][0].split(":")[2])
                cprint("chamando recebe pode pegar")
                recursos.recebe_pode_pegar(recurso)
        else:
            cprint("ERRO, NINGUEM TRATA ESSA MENSAGEM")
        del fila_mensagens[0]


def updateTimestamp(mensagem):
    global timestamp
    timestamp_mensagem = float(mensagem.split(":")[0])
    timestamp = max (timestamp,timestamp_mensagem)

def getTimestamp():
    return timestamp

def mandaMensagem(mensagem,peer):
    cprint("mandando mensagem",mensagem,"para",peer)
    conexao =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fila_mensagens.append([mensagem,0,peer,True])
    conexao.sendto(mensagem,peer)
    conexao.close()


def broadcastMensagem(mensagem):
    cprint("fazendo broadcast da mensagem",mensagem)
    for peer in lista_peers:
        mandaMensagem(mensagem,peer)

def broadcastACK(mensagem):
    conexao =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cprint("fazendo broadcast de acks da mensagem",mensagem)
    for peer in lista_peers:
        cprint("mandando ack da mensagem",mensagem,"para",peer)
        conexao.sendto(mensagem,(peer[0],peer[1]+10))

    conexao.close()
