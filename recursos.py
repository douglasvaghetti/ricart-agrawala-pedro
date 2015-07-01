import middleware
import thread
from redefinePrint import cprint

numero_de_recursos = 10
TEM,QUER,LIVRE = range(3)
estadoRecursos = [LIVRE]*numero_de_recursos
tempoMeuPedido = [0]*numero_de_recursos
fila_pedidos_recursos = []
pode_pegar_recebidos = [0]*numero_de_recursos

for x in range(numero_de_recursos):
    fila_pedidos_recursos.append(list())

def trata_requisicao(recurso,timestamp_mensagem,peer_que_pediu):
    cprint("recebeu requisicao do peer",peer_que_pediu,"para acessar o recurso",recurso)
    if estadoRecursos[recurso]==LIVRE:
        cprint("recurso",recurso,"livre, mandando que pode pegar")
        middleware.mandaMensagem(str(middleware.getTimestamp())+":PODEPEGAR:"+str(recurso)+":by:"+str(middleware.portaRecebeMensagens), peer_que_pediu)
    elif estadoRecursos[recurso]==QUER:
        if timestamp_mensagem<tempoMeuPedido[recurso]:
            cprint("queria o recurso",recurso,"mas timestamp era posterior, mandando que pode pegar")
            middleware.mandaMensagem(str(middleware.getTimestamp())+":PODEPEGAR:"+str(recurso)+":by:"+str(middleware.portaRecebeMensagens), peer_que_pediu)
    else:
        cprint("ja tinha ou queria com timestamp menor, pedido do recurso",recurso,"fica na fila")
        fila_pedidos_recursos[recurso].append(peer_que_pediu)

def recebe_pode_pegar(recurso):
    pode_pegar_recebidos[recurso]+=1
    cprint("recebeu pode pegar do recurso",recurso)
    if pode_pegar_recebidos[recurso]==middleware.numero_de_peers:
        cprint("todos peers aprovam pegada do recurso",recurso)
        estadoRecursos[recurso] = TEM
        cprint("voce agora tem o recurso ",recurso)

def libera_recurso(recurso):
    if estadoRecursos[recurso] == TEM:
        estadoRecursos[recurso] = LIVRE
        for peer in fila_pedidos_recursos[recurso]:
            middleware.mandaMensagem(str(middleware.getTimestamp())+":PODEPEGAR:"+str(recurso)+":by:"+str(middleware.portaRecebeMensagens), peer)
        fila_pedidos_recursos[recurso] = list()
        cprint("recurso",recurso,"liberado")
    else:
        cprint("voce nao tem o recurso",recurso,"para liberar ele")

def adquire_recurso(recurso):
    if estadoRecursos[recurso] ==LIVRE:
        estadoRecursos[recurso] = QUER
        tempoMeuPedido[recurso] = middleware.getTimestamp()
        mensagem = str(middleware.getTimestamp())+":POSSOPEGAR:"+str(recurso)+":by:"+str(middleware.portaRecebeMensagens)
        cprint("pedindo recurso ",recurso,"a todos peers")
        middleware.broadcastMensagem(mensagem)
    else:
        cprint("voce ja tem ou ja requisitou esse recurso")
