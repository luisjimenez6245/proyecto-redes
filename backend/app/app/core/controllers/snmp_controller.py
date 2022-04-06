from pysnmp.hlapi import (
    getCmd,
    SnmpEngine,
    UsmUserData,
    usmHMACSHAAuthProtocol,
    usmDESPrivProtocol,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity
)

HOSTNAME_OID = "1.3.6.1.2.1.1.5.0"
DESCR_OID = "1.3.6.1.2.1.1.1.0"
CONTACT_OID = "1.3.6.1.2.1.1.4.0"
LOCATION_OID = "1.3.6.1.2.1.1.6.0"
INTERFACE_OID = "1.3.6.1.2.1.2.2.1"
INTNUMBER_OID = "1.3.6.1.2.1.2.1.0"

user = 'admin'
password = 'administrador_snmp'


def snmp_query(host: str, oid: str) -> str:
    error_indication, error_status, error_index, var_binds = next(
        getCmd(
            SnmpEngine(),
            UsmUserData(
                user, 
                password,
                password,
                authProtocol=usmHMACSHAAuthProtocol,        
                privProtocol=usmDESPrivProtocol
            ),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )
    if error_indication:
        raise Exception(f"Error  on snmp_query indicator {error_indication}")

    if error_status:
        raise Exception(
            f"{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1] or '?'}"
        )

    for name, val in var_binds:
        return str(val)


def get_router_data(host: str) -> dict:
    info = {
        "description": snmp_query(host, DESCR_OID),
        "contact": snmp_query(host, CONTACT_OID),
        "name": snmp_query(host, HOSTNAME_OID),
        "location": snmp_query(host, LOCATION_OID),
    }
    return info


def mac(raw_str):
    return ":".join("{:02x}".format(ord(c)) for c in raw_str)


def status(status):
    try:
        status = int(str(status))
        if status == 1:
            return "up"
        if status == 2:
            return "down"
        if status == 3:
            return "testing"
        return "unknown"
    except:
        return "unknown"


def get_if_info(ip:str , n: int ) -> dict:
    return {
        "descr":
            snmp_query(ip, f"{INTERFACE_OID}.2.{n}"),
        "mtu": snmp_query(ip, f"{INTERFACE_OID}.4.{n}"),
        "speed": snmp_query(ip, f"{INTERFACE_OID}.5.{n}"),
        "mac": mac(
            snmp_query(ip, f"{INTERFACE_OID}.6.{n}")
        ),
        "admin_statis": status(
            snmp_query(ip, f"{INTERFACE_OID}.7.{n}")
        ),
        "operataion_status": status(
            snmp_query(ip, f"{INTERFACE_OID}.8.{n}")
        ),
        "mib_index": n,
    }


def get_interfaces(ip):
    interfaces = []
    number = int(snmp_query(ip, INTNUMBER_OID)) + 1
    for i in range(number):
        interface = get_if_info(ip, i + 1)
        if interface["descr"] != "Null0" and interface["descr"] != "":
            interfaces.append(interface)
    return interfaces
