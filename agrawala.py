import socket
import sys
import rede
import recursos
from redefinePrint import cprint, draw_print

if len(sys.argv) <= 2:
    cprint("modo de uso:\npython agrawala.py prioridade ip1 ip2 ip3 ... ")
else:
    prioridade = float(sys.argv[1])/10.0
    rede.timestamp = 1+prioridade
    lista_ips_peers = [socket.gethostname()]

if len(sys.argv) <= 1:
    rede.abre_thread_espera_conexoes()
    cprint("thread de espera de conexoes aberta")
print "aperte enter depois que todos clientes estiverem abertos"
_ = raw_input()
if len(sys.argv) > 1:
    rede.conecta_peers(lista_ips_peers)
    cprint("todos peers conectados")

cprint("existem atualmente", recursos.numeroDeRecursos)
while True:
    cprint('digite "o n" para obter o recurso n e "l n" para liberar o recurso n')
    draw_print()
    entrada = raw_input()
    comando, recurso = entrada.split(" ")
    recurso = int(recurso)
    if comando == "o":
        cprint("adquirindo o recurso", recurso)
        recursos.adquire_recurso(recurso)
        cprint("recurso obtido")
    elif comando == "l":
        cprint("liberando recurso", recurso)
        recursos.libera_recurso(recurso)
        cprint("recurso liberado")
    else:
        cprint("comando nao reconhecido:'"+comando+"'")
