import socket
import thread


PORTARECEBECONEXOES= 50000
conexoes = []
numero_de_peers = 1
timestamp = 1
import recursos

def conectaPeers(lista_ips_peers):
	print "conectando peers"
	for ip in lista_ips_peers:
		print "conectando com",ip
		conexao = socket.create_connection((ip,PORTARECEBECONEXOES))
		conexoes.append(conexao)
		thread.start_new_thread(threadTrataMensagens,(conexao,len(conexoes)-1,))


def threadTrataMensagens(socket,id_peer):
	while True:
		time_stamp_mensagem,mensagem = socket.recv(1024).split(":")
		time_stamp_mensagem = int(time_stamp_mensagem)
		print "recebeu mensagem",mensagem,"timestamp da msg = ",time_stamp_mensagem
		if mensagem == "ACK":
			print "recebeu ack do peer",id_peer
			recursos.trataACK(id_peer)
		else:
			recursos.trataPedidoRecurso(id_peer,int(mensagem),time_stamp_mensagem)


def threadEsperaConexoes():
	import socket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), PORTARECEBECONEXOES))
	serversocket.listen(5)
	while True:
		socket,endereco = serversocket.accept()
		conexoes.append(socket)
		print "recebeu novo pedido de conexao de",endereco
		thread.start_new_thread(threadTrataMensagens,(socket,len(conexoes)-1,))

def abreThreadEsperaConexoes():
	thread.start_new_thread(threadEsperaConexoes,())

def broadcast(mensagem):
	for conexao in conexoes:
		print "mandando mensagem'"+str(timestamp)+":"+mensagem+"'"
		conexao.send(str(timestamp)+":"+mensagem)

def mandaACK(peer):
	conexoes[peer].send(str(timestamp)+":"+"ACK")

def get_num_peers():
	return numero_de_peers
