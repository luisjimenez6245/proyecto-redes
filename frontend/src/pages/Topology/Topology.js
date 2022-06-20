import React, { useCallback, useEffect, useState } from "react";
import Graph from "react-graph-vis";
import  reduxProperties from "reducers/utils/Redux";

function Topology({get_topology}) {
  const [info, setInfo] = useState(null)
  
  useEffect(() => {
  
    let callback = (res) =>{
      if(res.ok){
        setInfo(res.body)
      }
    }
    get_topology(callback)
  }, [setInfo])

  
  if(!info){
    return (
      <></>
    )
  }
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
      color: "#FF0000",
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
