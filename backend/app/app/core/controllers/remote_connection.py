from operator import ne
import netmiko
from pexpect import TIMEOUT, pxssh
import pexpect
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetmikoBaseException, NetmikoTimeoutException


#device es la configuracion del dispositivo
#commands es la lista de comando a ejecutar
def telnetConexion(device, commands):
    result ={}
    #netmiko.read_timeout = 3000
    try:
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            for command in commands:
                output= telnet.send_command_timing(command)
                print(output)
                result[command] = output
        return result
    except(NetMikoAuthenticationException, NetmikoTimeoutException) as error:
        print("Error al conextar con router")


#Conexion por ssh, no requiere el dato secret
def sshConexion(device, commands):
    result ={}
    #netmiko.read_timeout = 3000
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output= ssh.send_command_timing(command)
                #print(output)
                result[command] = output
        return result
    except(NetMikoAuthenticationException, NetmikoTimeoutException) as error:
        print("Error al conextar con router")


def upSSh(device):
    #Se  conecta mediante una conexion telnet, y se pasa la lista de comandos para configurar ssh
    result = telnetConexion(device, [ "config t",  "ip domain-name redes.com.mx", "crypto key generate rsa usage-keys label sshkey modulus 1024", "ip ssh v 2", "ip ssh time-out 60", "line vty 0 15", "password "+device["password"] ,"login local","transport input ssh telnet","exit", "end"])
    #print(result)


def neighborsTel(user):
    respuesta= telnetConexion(user,["show cdp neighbors"])
    
    routers = respuesta["show cdp neighbors"]
    routers = routers.split()
    i = 35
    listRouters=[]
    while i < len(routers):
    	if ("R" in routers[i+4]):
            #print(routers[i])
            listRouters.append(routers[i])
            i = i + 8
    return listRouters

def neighborsSSH(user):
    respuesta= sshConexion(user,["show cdp neighbors"])
    
    routers = respuesta["show cdp neighbors"]
    routers = routers.split()
    i = 35
    listRouters=[]
    while i < len(routers):
    	if ("R" in routers[i+4]):
            #print(routers[i])
            listRouters.append(routers[i])
            i = i + 8
    return listRouters

def sshAllRouters(user):
    
    respuestaNeighbors=neighborsTel(user)
    upSSh(user)
    i=0
    
    for router in respuestaNeighbors:
        respuestaSsh=telnetConexion(user,["show cdp entry "+router])
        respuestaCdp = respuestaSsh["show cdp entry "+router]
        respuestaCdp = respuestaCdp.split()
        print("Respuesta de " + router)
        #print(respuestaCdp)
        print(respuestaCdp[3] + ": " + respuestaCdp[8])
        
        
        #for r in listRouter:
        print(telnetConexion(user, ["telnet "+respuestaCdp[8] ,user.get("username"),user.get("password"), "config t",  "ip domain-name redes.com.mx", "crypto key generate rsa usage-keys label sshkey modulus 1024", "ip ssh v 2", "ip ssh time-out 60", "line vty 0 15", "password "+user.get("password") ,"login local","transport input ssh telnet","exit", "end"]))

            
    

def commandAllRouters(user:dict ,commands, should_ignore = None):
    
    if should_ignore is None:
        should_ignore = []

    if user.get("host") in should_ignore:
        return 
    
    should_ignore.append(user.get("host"))
    
    respuestaNeighbors=neighborsSSH(user)
    
    print(sshConexion(user, commands))

    i=0
    listRouter=[]
    for router in respuestaNeighbors:
        respuestaSsh=sshConexion(user,["show cdp entry "+router])
        respuestaCdp = respuestaSsh["show cdp entry "+router]
        respuestaCdp = respuestaCdp.split()
        print("Respuesta de " + router)
        #print(respuestaCdp)
        
        listRouter.append([respuestaCdp[3],respuestaCdp[8]]) #[3] da el Id del router, [8] da la ip de la interfaz del router
        #for r in listRouter:

        commandsSend= ["ssh -l "+user.get("username")+" "+ respuestaCdp[8], user.get("password")]
        commandsSend.extend(commands)
        helper_user = user.copy()
        helper_user["host"] = respuestaCdp[8]   
        should_ignore.append(respuestaCdp[8])

        commandAllRouters(user, commandsSend, should_ignore)
        print(sshConexion(user, commandsSend) )

    return respuestaNeighbors


    