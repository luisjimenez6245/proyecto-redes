import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

function RegistrationForm({
    history,
    saveUser
}){
    const { handleSubmit, register, errors } = useForm();
    const [errorMessage, setErrorMessage] = useState(null)

    let onRegister = (event) => {
        let email = event.email;
        let password = event.password;
        let name = event.name;
        let username = event.username;
        let data = {
            email: email,
            password: password,
            name: name,
            username: username,
            type: "permanent",
        }
        let callback = res => {
            console.log(res)
            if(res.ok){
                if(res.body.status){
                    setErrorMessage('Revisa tus credenciales')
                }
                history.replace('/login');
            }
            else{
                setErrorMessage('Ocurrió un error')
            }
        }
        saveUser(data, callback)
    }


    let onLogin = () => {
        history.replace('/login');
    }

    return(
        <>
            <section className="hero is-fullheight is-light">
                <div className="hero-body">
                    <div className="container">
                        <div className="columns is-centered">
                            <div className="column box px-6 is-4">
                                <form onSubmit={handleSubmit(onRegister)} className="px-4">
                                    <div className="title has-text-centered has-text-black">
                                        Registro
                                    </div>
                                    <div className="field">
                                        <label className="label">Nombre</label>
                                        <div className="control has-icons-left">
                                            <input type="text" placeholder="bobsmith@gmail.com"
                                                className="input" {...register("name", { required: true })} />
                                            <span className="icon is-small is-left">
                                                <i className="fa fa-envelope"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="field">
                                        <label className="label">Usuario</label>
                                        <div className="control has-icons-left">
                                            <input type="text" placeholder="bobsmith"
                                                className="input" {...register("username", { required: true })} />
                                            <span className="icon is-small is-left">
                                                <i className="fa fa-envelope"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="field">
                                        <label className="label">Correo</label>
                                        <div className="control has-icons-left">
                                            <input type="text" placeholder="bobsmith@gmail.com"
                                                className="input" {...register("email", { required: true })} />
                                            <span className="icon is-small is-left">
                                                <i className="fa fa-envelope"></i>
                                            </span>
                                        </div>
                                    </div>

                                    <div className="field">
                                        <label className="label">Password</label>
                                        <div className="control has-icons-left">
                                            <input type="password" placeholder="*******"
                                                className="input" {...register("password", { required: true })} />
                                            <span className="icon is-small is-left">
                                                <i className="fa fa-lock"></i>
                                            </span>
                                        </div>
                                    </div>

                                    <div className="field">
                                        {errors && errors.password && errors.password.type === "required" &&
                                            <p className="has-text-danger">Ingrese la contraseña</p>}
                                        {errorMessage ? <code className="has-text-red">{errorMessage}</code> : null}
                                    </div>
                                    <div className="field">
                                        <div className="field is-grouped is-grouped-centered">
                                            <p className="control">
                                                <button className='button is-small is-link is-inverted' type='button' onClick={onLogin}>
                                                     ¿Ya tienes cuenta? Ingresa
                                                </button>
                                            </p>
                                        </div>
                                    </div>
                                    <div className="field">
                                        <div className="field is-grouped is-grouped-centered">
                                            <p className="control">
                                                <input type="submit" value="Registrar" className="button is-fullwidth is-link" />
                                            </p>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
}
export default RegistrationForm;