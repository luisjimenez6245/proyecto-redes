from datetime import datetime as dt
import pathlib
import subprocess
import napalm
fa0_0_in_oct = '1.3.6.1.2.1.2.2.1.10.1'
fa0_0_in_uPackets = '1.3.6.1.2.1.2.2.1.11.1'
fa1_0_in_oct = '1.3.6.1.2.1.2.2.1.10.2'
fa1_0_in_uPackets = '1.3.6.1.2.1.2.2.1.11.2'
fa2_0_in_oct = '1.3.6.1.2.1.2.2.1.10.3'
fa2_0_in_uPackets = '1.3.6.1.2.1.2.2.1.11.3'
communityName = "public"
port = 2400
tiempo_muestreo = 5.0


class SNMP:

    def prepareDevice(self, ip: str, user="cisco", password="cisco"):
        driver = napalm.get_network_driver('ios')
        optional_args = {}
        optional_args['dest_file_system'] = 'nvram:'
        optional_args['fast_cli'] = False
        try:
            device = driver(hostname=ip, username=user,
                            password=password, optional_args=optional_args)
        except:
            print("No SSH Supported trying with telnet...")

        optional_args['transport'] = 'telnet'
        try:
            device = driver(hostname=ip, username=user,
                            password=password, optional_args=optional_args)
        except:
            print("No SSH and no telnet support...")
        device.open()
        print("Opening %s..." % ip)
        return device

    def getInterfacesCounters(self, ip: str, interface: str, ip2: str, interface2: str):
        try:
            device = self.prepareDevice(ip)
            device2 = self.prepareDevice(ip2)
            interfaceData = device.get_interfaces_counters()[
                'FastEthernet' + interface]
            interfaceData2 = device2.get_interfaces_counters()[
                'FastEthernet' + interface2]
            lostPackages1 = int(
                interfaceData2['tx_unicast_packets']) - int(interfaceData['rx_unicast_packets'])
            lostPackages2 = int(
                interfaceData['tx_unicast_packets']) - int(interfaceData2['rx_unicast_packets'])
            return True, {
                'input1': interfaceData['rx_unicast_packets'],
                'output1': interfaceData['tx_unicast_packets'],
                'broken1': interfaceData['rx_errors'],
                'lost1': lostPackages1,
                'input2': interfaceData2['rx_unicast_packets'],
                'output2': interfaceData2['tx_unicast_packets'],
                'broken2': interfaceData2['rx_errors'],
                'lost2': lostPackages2,
            }
        except Exception as e:
            return False, {"response": "%s" % e}


def reset_files():
    if_f00_file = open(
        f"{pathlib.Path().resolve()}/static/files/interface_f00.json", "w")
    if_f20_file = open(
        f"{pathlib.Path().resolve()}/static/files/interface_f20.json", "w")
    traps_file = open(
        f"{pathlib.Path().resolve()}/static/files/traps.txt", "w")
    if_f00_file.write("[]")
    if_f20_file.write("[]")
    if_f00_file.close()
    if_f20_file.close()
    traps_file.close()


def print_results(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    print('Nueva trap entrando...')
    traps_file = open(
        f'{pathlib.Path().resolve()}/static/files/traps.txt', "a")
    time = dt.now().strftime("%H:%M:%S")
    for name, val in varBinds:
        if "1.3.6.1.2.1.2.2.1.2" in name.prettyPrint():
            traps_file.write(name.prettyPrint()+"," + val.prettyPrint()+"\n")
        if "1.3.6.1.4.1.9.2.2.1.1.20" in name.prettyPrint():
            traps_file.write(f"{name.prettyPrint()},{val.prettyPrint()},")
            traps_file.write(f"{time}\n")
    traps_file.close()


def get_info(ip):
    command = [
        "snmpwalk",
        "-v3",
        "-l",
        "authPriv",
        "-u",
        "admin",
        "-a",
        "SHA",
        "-A",
        'administrador_snmp',
        "-x",
        "des",
        "-X",
        "administrador_snmp",
        ip,
        "1.3.6.1.2.1.1"
    ]
    res = subprocess.check_output(command).decode("utf-8")
    header = "Compiled Wed 22-Aug-12 11:45 by prod_rel_team"
    i = res.rfind(header)
    res = res[i + len(header):]
    res = res.split("\n")
    keys = {

    }
    for d in res:
        if 'iso' in d:
            k = d.split("=")
            keys[k[0].replace(" ", "")] = k[1]
    result = {
        "location": keys["iso.3.6.1.2.1.1.6.0"],
        "contact": keys["iso.3.6.1.2.1.1.4.0"],
        "hostname": keys["iso.3.6.1.2.1.1.5.0"]
    }
    return result



