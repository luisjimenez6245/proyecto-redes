import netifaces as ni
from threading import Thread
import platform
import subprocess
from netmiko import ConnectHandler
import json
import time
import re


def check_str_ip_in_arr_dict(arr, ip):
    for i in arr:
        if ip in i.keys():
            return True
    return False


def verifica_conectividad(dict, arr_resp, dict_int):
    conexiones = []
    dict_conexiones = []
    for i, j in dict.items():
        for k, v in dict.items():
            if k != i:
                for a, b in v.items():
                    if b in j.values():
                        if (f"{i}-{k}:{b}" not in conexiones) and (f"{k}-{i}:{b}" not in conexiones):
                            r1 = a.split("-sub")[0]
                            r2 = ""
                            for c, d in j.items():
                                if d == b:
                                    r2 = c.split("-sub")[0]
                            ip_r1 = dict_int[i][r2].split("/")[0]
                            ip_r2 = dict_int[k][r1].split("/")[0]
                            if (check_str_ip_in_arr_dict(arr_resp, ip_r1) and check_str_ip_in_arr_dict(arr_resp, ip_r2)):
                                conexiones.append(f"{i}-{k}:{b}")
                                diccio = {"ip_1": ip_r2, "interface_1": r1, "host_1": k,
                                          "ip_2": ip_r1, "interface_2": r2, "host_2": i}
                                dict_conexiones.append(diccio)
    return [conexiones, dict_conexiones]


def create_masc_by_prefix(prefix):
    net = []
    for i in range(4):
        if (prefix-8) >= 0:
            net.append(255)
            prefix -= 8
    if prefix == 7:
        net.append(254)
    elif prefix == 6:
        net.append(252)
    elif prefix == 5:
        net.append(248)
    elif prefix == 4:
        net.append(240)
    elif prefix == 3:
        net.append(224)
    elif prefix == 2:
        net.append(192)
    elif prefix == 1:
        net.append(128)
    mis = 4-len(net)
    for i in range(mis):
        net.append(0)
    return net


def conectar(cisco, cmd):
    net_connect = ConnectHandler(**cisco)
    net_connect.enable()
    output = []
    for i in range(len(cmd)):
        output.append(net_connect.send_command(cmd[i]))
    return output


BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'


def arr_to_ip(ip):
    return f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"


def ping(host, result):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ["timeout", "1", 'ping' ,'-i', '0.2', param, '1', host]
    res = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.read().decode("utf-8")
    r = "100% packet loss" not in output
    msg = ""
    res.terminate()
    if r:
        msg = f"{GREEN} with answer [✓]{END}"
    else:
        msg = f"{RED} without answer [x]{END}"
    try:
        result.append(
        [r, f"{YELLOW} Send data to: {host.ljust(15)} {msg}", host, output.split("\n")[1]])
    except:
         result.append([False, ""])


def get_id_net(ip, net):
    idnet = []
    for i in range(4):
        idnet.append((ip[i] & net[i]))
    return idnet


def check_os_by_ttl(ttl):
    if ttl <= 64:
        return f"Unix-OS {64-ttl}"
    elif ttl > 64 and ttl <= 128:
        return f"MS-DOS_Windows-OS {128-ttl}"
    elif ttl > 128:
        return f"Cisco_Router_IOS {255-ttl}"


def get_broadcast_ip(idnet, net):
    ran = []
    for i in range(4):
        ran.append((idnet[i] | ((~net[i]) & 0xFF)))
    return ran


def scan_range(ips, broadcast):
    responde = []
    threads = []
    positivos = []
    i = 0
    b = 0
    while(True):
        if i % 35 == 0 and i > 0:
            for t in range(len(threads)):
                threads[t].join()
                # print(responde[t][1])
                if responde[t][0]:
                    ttl = responde[t][3].split("ttl=")[1]
                    ttl = int(ttl.split(" ")[0])
                    positivos.append({responde[t][2]: check_os_by_ttl(ttl)})
            threads = []
            responde = []
            b += 1

        thread = Thread(target=ping, args=(f"{ips[0]}.{ips[1]}.{ips[2]}.{ips[3]}", responde))
        threads.append(thread)
        thread.start()
        i += 1
        if ips[3]+1 == 256:
            ips[3] = 0
            if ips[2]+1 == 256:
                ips[2] = 0
                if ips[1]+1 == 256:
                    ips[1] = 0
                else:
                    ips[1] += 1
            else:
                ips[2] += 1
        else:
            ips[3] += 1
        if ips == broadcast:
            break
    
    for t in range(len(threads)):
        threads[t].join()
        if responde[t][0]:
            ttl = responde[t][3].split("ttl=")[1]
            ttl = int(ttl.split(" ")[0])
            positivos.append({responde[t][2]: check_os_by_ttl(ttl)})
    return positivos


def determinate_prefix(net):
    c = 0
    for i in range(4):
        if net[i] == 255:
            c += 8
        elif net[i] == 254:
            c += 7
        elif net[i] == 252:
            c += 6
        elif net[i] == 248:
            c += 5
        elif net[i] == 240:
            c += 4
        elif net[i] == 224:
            c += 3
        elif net[i] == 192:
            c += 2
        elif net[i] == 128:
            c += (1)
    return c


def scan_by_interface(interface_name="enp0s3", user="admin", password="admin", secret="1234"):
    # Prototipo de conexión a router cisco
    cisco = {
        "device_type": "cisco",
        "ip": "",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "secret": "cisco"
    }
    # Obtienen el disccionario de los datos de la red
    dic_data = ni.ifaddresses(interface_name)
    if 2 not in dic_data:
        print("No hay una dirección IPv4 en la interfaz")
        return [-1, -1]
    dic_data = dic_data[2][0]
    print(f"\n---------About---------\n{interface_name}:{dic_data}")
    addr = list(map(int, dic_data["addr"].split(".")))
    net = list(map(int, dic_data["netmask"].split(".")))

    c = determinate_prefix(net)
    # Se obtiene el identificador de la subred
    idnet = get_id_net(addr, net)
    # Se obtiene la dirección de broadcast
    range_net = get_broadcast_ip(idnet, net)

    print(
        f"-------Scan Network:-------\n\tID: {arr_to_ip(idnet)}/{c}\n\tNetmask: {arr_to_ip(net)}\n\tBroadcast: {arr_to_ip(range_net)}")

    # Se prepara para hacer is_host_up
    ips = [idnet[0], idnet[1], idnet[2], idnet[3]+1]
    responde = scan_range(ips, range_net)

    # Se filtra por primera vez que solo los elementos que sean Cisco

    ciscos = []
    gateway = ""
    for i in range(len(responde)):
        for k, v in responde[i].items():
            if "Cisco_Router_IOS" in v:
                gateway = k
                ciscos.append(responde[i])
    print(f"Solo routers cisco: {ciscos}")

    # Despues de todo lo que hace el modulo hay que conectarse por ssh o telnet
    #   a los dispositivos cisco
    cmd = ["sh ip int | i Internet address",
           "sh ip int br | include up", "sh run | include hostname"]
    c = 0
    red = {}
    red_id = {}
    net_router = {}
    for i in ciscos:
        flag = False
        # Los datos del router (Interfaces)
        for k, v in i.items():

            print(f"-------Enviando comandos a router con ip: {k}-------")
            cisco["ip"] = k
            start = time.time()
            output = conectar(cisco, cmd)
            end = time.time()
            print(f"Tiempo de conexión: {end-start}")

            dir = re.split("\n|  Internet address is | ", output[0])
            inte = re.split(
                "\n|YES NVRAM  up                    up|YES manual up                    up| ", output[1])
            host_cmd = output[2].split("hostname ")[1]
            direcciones = []
            interf = []
            for j in dir:
                if j != "":
                    direcciones.append(j)
            for j in inte:
                if j != "":
                    interf.append(j)
            if host_cmd in red.keys():
                flag = False
            else:
                flag = True
            if flag:
                iter = {}
                iter_s = {}
                try:
                    for j in range(len(direcciones)):
                        iter[interf[(j*2)]] = direcciones[j]
                        sub = direcciones[j].split("/")
                        print("Dirreciones: ", sub)
                        pr = sub[1]  # En el original es 1 OJO
                        sub = list(map(int, sub[0].split(".")))
                        sub = arr_to_ip(get_id_net(
                            sub, create_masc_by_prefix(int(pr))))
                        iter_s[f"{interf[(j*2)]}-sub"] = sub
                except:
                    print("Error")
                red[host_cmd] = iter
                red_id[host_cmd] = iter_s
            dir.clear()
            inte.clear()
            direcciones.clear()
        # Scan de subredes del router
        if flag:
            start = time.time()
            for k, v in red.items():
                if 0 not in v.values():
                    for j, l in v.items():
                        red_e = l.split("/")
                        if red_e[0] in i.keys():
                            print(
                                f"-------Exists the network scanning {red_e[0]}-------")
                        else:
                            net = create_masc_by_prefix(int(red_e[1]))
                            id = get_id_net(
                                list(map(int, red_e[0].split("."))), net)
                            br = get_broadcast_ip(id, net)
                            if arr_to_ip(br) != arr_to_ip(id):
                                ip = [id[0], id[1], id[2], id[3]+1]
                                print(
                                    f"-------Scan Network:-------\n\tID: {arr_to_ip(id)}\n\tNetmask: {arr_to_ip(net)}\n\tBroadcast: {arr_to_ip(br)}")
                                resp_r = scan_range(ip, br)
                                responde = responde + resp_r
                                # aca filtrar Equipos cisco
                                for a in range(len(resp_r)):
                                    for b, d in resp_r[a].items():
                                        if "Cisco_Router_IOS" in d:
                                            ciscos.append(resp_r[a])
                    net_router[k] = v
                red[k] = {0: 0}
            end = time.time()
            print(f"Tiempo de for: {end-start}")
    json_respond = json.dumps(responde, sort_keys=True, indent=4)
    json_routers = json.dumps(net_router, sort_keys=True, indent=4)
    json_id = json.dumps(red_id, sort_keys=True, indent=4)
    arr_conexiones = verifica_conectividad(red_id, responde, net_router)
    print(f"Host con respuesta:\n{json_respond}\n"
          f"Diccionario de routers:\n{json_routers}\n"
          f"Identificadores de red de cada interfaz:\n{json_id}\n"
          f"Interconexiones:\n{json.dumps(arr_conexiones[1],indent=4)}")

    conexiones_r = []
    for k, v in net_router.items():
        host_n = {"hostname": k, "interfaces": []}
        inter = []
        for w, x in v.items():
            b = red_id[k][f"{w}-sub"]
            net = arr_to_ip(create_masc_by_prefix(int(x.split("/")[1])))
            prefix = int(x.split("/")[1])
            b = f"{b}/{prefix}"
            a = {"name": w,
                 "ip": x.split("/")[0],
                 "netmask": net,
                 "idnet": b}
            inter.append(a)
        host_n["interfaces"] = inter
        conexiones_r.append(host_n)
    json_conexiones = json.dumps(conexiones_r, sort_keys=True, indent=4)
    print(f"Información general:\n{json_conexiones}")
    # Posición 0 devuelve el json de todas las interfaces acomadado
    # Posición 1 devuelve el arreglo de interconexiones que hay entre routers
    # Posicion 2 devuelve todos los host que responsidieron al ping
    return [conexiones_r, arr_conexiones[0], net_router, responde, arr_conexiones[1], gateway]
    # return [json_conexiones,arr_conexiones,json_respond]




#'snmpwalk -v3 -l authPriv -u admin -a SHA -A administrador_snmp -x des -X administrador_snmp 10.0.8.253 1.3.6.1.2.1.1'