import socket
import sys
import rede
import recursos

if  len(sys.argv) == 1:
	print "modo de uso:\npython agrawala.py ip1 ip2 ip3 ... "
else:
	lista_ips_peers = [socket.gethostname()]

if len(sys.argv)<=1:
	rede.abreThreadEsperaConexoes()
	print "thread de espera de conexoes aberta"
print "aperte enter depois que todos clientes estiverem abertos"
_ = raw_input()
if len(sys.argv)>1:
	rede.conectaPeers(lista_ips_peers)
	print "todos peers conectados"

print "existem atualmente",recursos.numeroDeRecursos
while True:
	print 'digite "o n" para obter o recurso n e "l n" para liberar o recurso n'
	entrada = raw_input()
	comando,recurso = entrada.split(" ")
	recurso = int(recurso)
	if comando == "o":
		print "adquirindo o recurso",recurso
		recursos.adquireRecurso(recurso)
		print "recurso obtido"
	elif comando =="l":
		print "liberando recurso",recurso
		recursos.liberaRecurso(recurso)
		print "recurso liberado"
	else:
		print "comando nao reconhecido:'"+comando+"'"
