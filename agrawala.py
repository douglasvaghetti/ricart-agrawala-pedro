import sys
import random
from redefinePrint import cprint, draw_print
import middleware
import recursos

if len(sys.argv) <= 1:
    cprint("modo de uso:\npython agrawala.py minhaPorta ip1 ip2 ip3 porta1 porta2 porta3")
else:
    lista_ips_peers = sys.argv[2:(len(sys.argv)-2)/2+2]
    print "minha porta: ",sys.argv[1]
    porta_recebe_conexoes = int(sys.argv[1])
    print "lista de ips = ",lista_ips_peers
    lista_portas_peers = sys.argv[(len(sys.argv))/2+1:]
    print "lista portas peers = ",lista_portas_peers
    middleware.numero_de_peers = len(lista_ips_peers)
    print "setou o numero de peers para",middleware.numero_de_peers


middleware.init(zip(lista_ips_peers,[int(x) for x in lista_portas_peers]),porta_recebe_conexoes,porta_recebe_conexoes+10)
cprint("thread recebedora de mensagens aberta")


cprint("aperte enter depois que todos clientes estiverem abertos")
draw_print()

cprint("existem atualmente", recursos.numero_de_recursos,"recursos")

while True:
    draw_print()
    entrada = raw_input()
    try:
        comando, recurso = entrada.split(" ")
        recurso = int(recurso)
    except:
        cprint("erro na entrada")
        continue
    if comando == "o":
        cprint("adquirindo o recurso", recurso)
        recursos.adquire_recurso(recurso)
    elif comando == "l":
        cprint("liberando recurso", recurso)
        recursos.libera_recurso(recurso)
    else:
        cprint("comando nao reconhecido:'"+comando+"'")
