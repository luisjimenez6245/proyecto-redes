import { useForm, Controller } from "react-hook-form";
import { Select } from "finalsa-react-components";

function UserForm(props) {
  const { handleSubmit, register, errors, control } = useForm();
  let onSubmit = (event) => {
    console.log(event);
    let callback = (res) => {
      if (res.ok) {
        props.onReturn();
      }
    };
    let data = {
      name: event.name,
      username: event.username,
      email: event.email,
      type: event.type,
      password: event.password,
    };
    console.log(data);
    props.saveUser(data, callback);
  };
  console.log(errors);
  return (
    <>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="columns is-multiline">
          <div className="column is-half">
            <div className="field">
              <label className="label">Nombre</label>
              <div className="control">
                <input
                  {...register("name", { required: true })}
                  type="text"
                  className="input"
                ></input>
              </div>
            </div>
          </div>
          <div className="column is-half">
            <div className="field">
              <label className="label">Nombre de Usuario</label>
              <div className="control">
                <input
                  {...register("username", { required: true })}
                  type="text"
                  className="input"
                ></input>
              </div>
            </div>
          </div>

          <div className="column is-half">
            <div className="field">
              <label className="label">Correo Electrónico</label>
              <div className="control">
                <input
                  {...register("email", { required: true })}
                  type="text"
                  className="input"
                ></input>
              </div>
            </div>
          </div>
          <div className="column is-half">
            <div className="field">
              <label className="label">Tipo de Usuario</label>
              <div className="control">
                <Controller
                  control={control}
                  name="type"
                  render={({ field: { onChange, onBlur, ref } }) => (
                    <Select
                      onSelect={(val) => onChange(val)}
                      ref={ref}
                      onBlur={onBlur}
                      placeholder="Selecciona el medio"
                      options={props.userTypes}
                      value="name"
                      label="name"
                    ></Select>
                  )}
                />
              </div>
            </div>
          </div>
          <div className="column is-half">
            <div className="field">
              <label className="label">Contraseña</label>
              <div className="control">
                <input
                  {...register("password", { required: true })}
                  type="password"
                  className="input"
                ></input>
              </div>
            </div>
          </div>
          <div className="column is-half">
            <div className="field">
              <label className="label">Confirma Contraseña</label>
              <div className="control">
                <input
                  {...register("conpassword", { required: true })}
                  type="password"
                  className="input"
                ></input>
              </div>
            </div>
          </div>
        </div>
        <div className="field">
          {errors
            ? errors.map((e) => {
                return <div></div>;
              })
            : null}
        </div>
        <div className="field mt-3 pt-3">
          <div className="buttons">
            <button
              className="button is-fullwidth is-link"
              value="submit"
              type="submit"
            >
              Guardar
            </button>
            <button
              className="button is-fullwidth is-danger"
              type="button"
              onClick={props.onReturn}
            >
              Cancelar
            </button>
          </div>
        </div>
      </form>
    </>
  );
}

export default UserForm;
