import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

function Settings(setSSH) {

    const { handleSubmit, register, errors } = useForm();
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {

    }, [])

    let onSSH = (event) => {
        fetch('http://localhost:81/enable-ssh', {
            method: 'POST',
            mode: 'cors'
        })

    }

    let onSNMP = (event) => {
        fetch('http://localhost:81/network/set_snmp', {
            method: 'POST',
            mode: 'cors'
        })

    }

    let onProtocol = (event) => {
        fetch('http://localhost:81/network/set_topology?topology_type='+event.protocol, {
            method: 'POST',
            body:JSON.stringify({})
        })

    }

    return (
        <section className={`hero is-fullheight-with-navbar `}>
            <div className="hero-body">
                <div className="container">
                    <div className="columns is-centered">
                        <div className="column">
                            <div className="card">
                                <header class="card-header">
                                    <p className="card-header-title">
                                        Ajustes Iniciales
                                    </p>
                                </header>
                                <div className=" card-content ">
                                    <div class="columns is-centered">
                                        <div class="column">
                                            <form onSubmit={handleSubmit(onSSH)}>
                                                <div class="field">
                                                    <label class="label">Activar SSH</label>
                                                    <div class="control">
                                                        <input type="submit" class="button is-success" value="Activar" />
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                        <div class="column is-three-fifths">
                                            <form onSubmit={handleSubmit(onProtocol)}>
                                                <label class="label">Activar Protocolo de Enrutamiento</label>
                                                <div class="select">
                                                    <select class="is-focused" {...register("protocol", { required: true })}>
                                                        <option>Selecciona un protocolo</option>
                                                        <option>rip</option>
                                                        <option>ospf</option>
                                                        <option>eigrp</option>
                                                    </select>
                                                </div>
                                                <input type="submit" class="button is-link" value="Activar" />
                                                <br></br>
                                            </form>
                                        </div>
                                        <div class="column">
                                            <form onSubmit={handleSubmit(onSNMP)}>
                                                <div class="field">
                                                    <label class="label">Activar SNMP</label>
                                                    <div class="control">
                                                        <input type="submit" class="button is-warning" value="Activar" />
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Settings