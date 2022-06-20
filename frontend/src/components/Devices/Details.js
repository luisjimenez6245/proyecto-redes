import React,  { useState } from "react"


function DeviceDetails(props) {

   const { data } = props

    const [ inputData, setInputData ] = useState({
	type  : "contact",
	value : "",
	id : data.id,
    })

   let selectOnChange = (e) => {
        let newData = {
      ...inputData
}
        newData.type = e.target.value
      setInputData(newData)
  }


  let textOnChange = (e) => {
        let newData = { 
      ...inputData
}       
        newData.value = e.target.value
      setInputData(newData)
}

        let buttonOnClick = () => {
        console.log(inputData)
        props.saveChanges(inputData)        
}

   if(!inputData)
        return (<></>)
    return (
        <>
            <div className="columns is-multiline">
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Nombre
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.name}
                            >
                            </input>
                        </div>
                    </div>
                </div>
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            HostName
                       </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.hostname}
                            >
                            </input>
                        </div>
                    </div>
                </div>
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Ubicacion
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.location}
                            >
                            </input>
                        </div>
                    </div>
                </div>
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Contacto
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.contact}
                            >
                            </input>
                        </div>
                    </div>
                </div>
            </div>
	   <div className="columns is-multiline">
		<div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Valor a cambiar
                        </label>
                        <div className="control">
                            <select name="type" id="type" value={inputData.type} onChange={(e) => { selectOnChange(e) }}>
  				<option value="contact">contacto</option>
  				<option value="hostname">hostname</option>
  				<option value="location">ubicacion</option>
			    </select>
                        </div>
                    </div>
                </div>
		<div className="column is-half">
                    <div className="field">
                        <br></br>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={inputData.value}
                                onChange={ (e)  => { textOnChange(e)}}
                            >
                            </input>
                        </div>
                    </div>
                </div>
		<div className="column is-half">
                    <div className="field">
                        <div className="control">
                            <input type="button" onClick={ (e) => {buttonOnClick(e)}}  value ="Actualizar" />
                        </div>
                    </div>
                </div>
	   </div>
        </>
    )
}
export default DeviceDetails
