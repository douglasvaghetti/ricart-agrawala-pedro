import rede

numeroDeRecursos = 10
TENHO,QUERO,PODEPEGAR = range(3)
estadoRecursos = [PODEPEGAR]*numeroDeRecursos
ACKs_obtidos = [[False]*rede.numero_de_peers]*numeroDeRecursos
fila_pedidos_ack_armazenados = [[]]*numeroDeRecursos
filas_recursos_esperando_ack = [[]]*rede.numero_de_peers

def temRecurso(n):
	return estadoRecursos[n]==TENHO

def querRecurso(n):
	return estadoRecursos[n]==QUERO

def adquireRecurso(recurso):
	if estadoRecursos[recurso]!=PODEPEGAR:
		print "voce ja tem ou ja quer este recurso"
		return 
	estadoRecursos[recurso] = QUERO
	ACKs_obtidos[recurso] = [False]*rede.numero_de_peers
	for fila in filas_recursos_esperando_ack:
		fila.append(recurso)
	rede.broadcast(str(recurso))
	while True:
		#baixar o mutex
		if ACKs_obtidos[recurso]==[True]*rede.numero_de_peers:
			#libera mutex
			break
		#libera mutex
	estadoRecursos[recurso]=TENHO

def liberaRecurso(recurso):
	if not temRecurso(recurso):
		print "voce nao pode liberar um recurso que voce nao tem"
		return
	estadoRecursos[recurso]= PODEPEGAR
	for pedido in fila_pedidos_ack_armazenados[recurso]:
		rede.mandaACK(pedido)

def trataPedidoRecurso(peer,recurso,timestamp_pedido):
	print "pedido do peer",peer,"para o recurso",recurso,"com timestamp",timestamp_pedido,
	if estadoRecursos[recurso] == PODEPEGAR:
		rede.mandaACK(peer)
		print "concedido"
	elif estadoRecursos[recurso] == QUERO:
		if timestamp_pedido<rede.timestamp:
			rede.mandaACK(peer)
			print "concedido"
		else:
			fila_pedidos_ack_armazenados[recurso].append(peer)
			print "inserido na fila"
	elif estadoRecursos[recurso] == TENHO:
		fila_pedidos_ack_armazenados[recurso].append(peer)
		print "inserido na fila"

def trataACK(peer):
	print "ack recebido do peer ",peer
	#baixa mutex
	recurso_que_recebeu_ack = filas_recursos_esperando_ack[peer][0]
	ACKs_obtidos[recurso_que_recebeu_ack][peer] = True
	filas_recursos_esperando_ack[peer].pop(0)
	#levanta mutex
