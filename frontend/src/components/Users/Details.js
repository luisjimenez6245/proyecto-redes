function UserDetails(props) {
    const { data } = props
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
                            Usuario
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.username}
                            >
                            </input>
                        </div>
                    </div>
                </div>
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Correo
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.email}
                            >
                            </input>
                        </div>
                    </div>
                </div>
                <div className="column is-half">
                    <div className="field">
                        <label className="label">
                            Tipo
                        </label>
                        <div className="control">
                            <input type="text"
                                className="input"
                                value={data.type.name}
                            >
                            </input>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}
export default UserDetails