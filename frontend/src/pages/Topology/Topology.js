import React, { useCallback, useEffect, useState } from "react";
import Graph from "react-graph-vis";
import { reduxProperties } from "reducers/utils/Redux";

function Topology() {
  const info = [
    [
      {
        hostname: "R3",
        interfaces: [
          {
            name: "FastEthernet1/0",
            ip: "10.0.3.254",
            netmask: "255.255.255.0",
            idnet: "10.0.3.0/24",
          },
          {
            name: "FastEthernet1/1",
            ip: "10.0.1.254",
            netmask: "255.255.255.0",
            idnet: "10.0.1.0/24",
          },
          {
            name: "Ethernet2/0",
            ip: "10.0.7.254",
            netmask: "255.255.255.0",
            idnet: "10.0.7.0/24",
          },
        ],
      },
      {
        hostname: "R2",
        interfaces: [
          {
            name: "FastEthernet0/0",
            ip: "10.0.2.254",
            netmask: "255.255.255.0",
            idnet: "10.0.2.0/24",
          },
          {
            name: "FastEthernet1/0",
            ip: "10.0.3.253",
            netmask: "255.255.255.0",
            idnet: "10.0.3.0/24",
          },
          {
            name: "FastEthernet1/1",
            ip: "10.0.8.254",
            netmask: "255.255.255.0",
            idnet: "10.0.8.0/24",
          },
          {
            name: "Ethernet2/0",
            ip: "10.0.6.254",
            netmask: "255.255.255.0",
            idnet: "10.0.6.0/24",
          },
        ],
      },
      {
        hostname: "R1",
        interfaces: [
          {
            name: "FastEthernet0/0",
            ip: "10.0.2.253",
            netmask: "255.255.255.0",
            idnet: "10.0.2.0/24",
          },
          {
            name: "FastEthernet1/1",
            ip: "10.0.1.253",
            netmask: "255.255.255.0",
            idnet: "10.0.1.0/24",
          },
          {
            name: "Ethernet2/0",
            ip: "10.0.5.254",
            netmask: "255.255.255.0",
            idnet: "10.0.5.0/24",
          },
        ],
      },
      {
        hostname: "R4",
        interfaces: [
          {
            name: "FastEthernet1/1",
            ip: "10.0.8.253",
            netmask: "255.255.255.0",
            idnet: "10.0.8.0/24",
          },
        ],
      },
    ],
    ["R3-R2:10.0.3.0", "R3-R1:10.0.1.0", "R2-R1:10.0.2.0", "R2-R4:10.0.8.0"],
    {
      R3: {
        "FastEthernet1/0": "10.0.3.254/24",
        "FastEthernet1/1": "10.0.1.254/24",
        "Ethernet2/0": "10.0.7.254/24",
      },
      R2: {
        "FastEthernet0/0": "10.0.2.254/24",
        "FastEthernet1/0": "10.0.3.253/24",
        "FastEthernet1/1": "10.0.8.254/24",
        "Ethernet2/0": "10.0.6.254/24",
      },
      R1: {
        "FastEthernet0/0": "10.0.2.253/24",
        "FastEthernet1/1": "10.0.1.253/24",
        "Ethernet2/0": "10.0.5.254/24",
      },
      R4: {
        "FastEthernet1/1": "10.0.8.253/24",
      },
    },
    [
      {
        "10.0.7.10": "Unix-OS 0",
      },
      {
        "10.0.7.254": "Cisco_Router_IOS 0",
      },
      {
        "10.0.3.254": "Cisco_Router_IOS 0",
      },
      {
        "10.0.3.253": "Cisco_Router_IOS 1",
      },
      {
        "10.0.1.253": "Cisco_Router_IOS 1",
      },
      {
        "10.0.1.254": "Cisco_Router_IOS 0",
      },
      {
        "10.0.2.254": "Cisco_Router_IOS 1",
      },
      {
        "10.0.2.253": "Cisco_Router_IOS 1",
      },
      {
        "10.0.8.254": "Cisco_Router_IOS 1",
      },
      {
        "10.0.8.253": "Cisco_Router_IOS 2",
      },
      {
        "10.0.6.254": "Cisco_Router_IOS 1",
      },
      {
        "10.0.2.254": "Cisco_Router_IOS 1",
      },
      {
        "10.0.2.253": "Cisco_Router_IOS 1",
      },
      {
        "10.0.5.254": "Cisco_Router_IOS 1",
      },
    ],
    [
      {
        ip_1: "10.0.3.253",
        interface_1: "FastEthernet1/0",
        host_1: "R2",
        ip_2: "10.0.3.254",
        interface_2: "FastEthernet1/0",
        host_2: "R3",
      },
      {
        ip_1: "10.0.1.253",
        interface_1: "FastEthernet1/1",
        host_1: "R1",
        ip_2: "10.0.1.254",
        interface_2: "FastEthernet1/1",
        host_2: "R3",
      },
      {
        ip_1: "10.0.2.253",
        interface_1: "FastEthernet0/0",
        host_1: "R1",
        ip_2: "10.0.2.254",
        interface_2: "FastEthernet0/0",
        host_2: "R2",
      },
      {
        ip_1: "10.0.8.253",
        interface_1: "FastEthernet1/1",
        host_1: "R4",
        ip_2: "10.0.8.254",
        interface_2: "FastEthernet1/1",
        host_2: "R2",
      },
    ],
    "10.0.7.254",
  ];
  const nodesHost = info[0].map((host) => ({
    id: host.hostname,
    label: host.hostname,
  }));
  const edges = info[1].map((info) => {
    let infoSplit = info.split(":");
    return infoSplit[0];
  });
  const edgesHost = edges.map((edge) => {
    let edgeSplit = edge.split("-");
    return { from: edgeSplit[0], to: edgeSplit[1] };
  });

  const nDevice = info[3].map((node) => {
    return {
      id: Object.keys(node)[0],
      label: node[Object.keys(node)[0]],
    };
  });

  const nodesDevice = nDevice.filter(function (dato) {
    let idSplit = dato.id.split(".");
    return idSplit[3] != "254" && idSplit[3] != "253";
  });

  const device = nodesDevice.map((node) => {
    let idSplit = node.id.split(".");
    if (idSplit[3] != "254" && idSplit[3] != "253") {
      for (var key in info[2]) {
        let router_interfaces = info[2][key];
        let name = key;
        for (var key in router_interfaces) {
          if (node.id.slice(0, -3) == router_interfaces[key].slice(0, -7)) {
            return { from: node.id, to: name };
          }
        }
      }
    }
  });
  const edgesDevice = device.filter(function (dato) {
    return dato != undefined;
  });

  const graph = {
    nodes: [...nodesHost, ...nodesDevice],
    edges: [...edgesHost, ...edgesDevice],
  };

  const options = {
    layout: {
      hierarchical: false,
    },
    edges: {
      color: "#000000",
    },
    height: "500px",
  };

  const events = {
    select: function (event) {
      var { nodes, edges } = event;
    },
  };
  return <Graph graph={graph} options={options} events={events} />;
}

export default reduxProperties(Topology);
