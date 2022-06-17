import redux from "reducers/utils/Redux"
import { Route, Switch } from 'react-router-dom';
import { useEffect } from "react";
import Details from './Details'
import Form from './Form'
import List from './List'

function DevicesPage(props) {
    const { setActualPage, saveSnmp, getDevicePagination, getDeviceDetails, getDeviceList, saveDevice, deleteDevice, setDevice, } = props
    const { path } = props.match

    const devices = { saveSnmp, getDevicePagination, getDeviceDetails, getDeviceList, saveDevice, deleteDevice, setDevice, }
    let onReturn = () => {
        props.history.replace(`${path}`);
    }
    useEffect(() => {
        if (setActualPage) {
            setActualPage('devices')
        }
    }, [setActualPage])
    return (
        <>

            <Switch>
                <Route
                    path={`${path}/details/:id`}
                    exact
                >
                    <Details
                        onReturn={onReturn}
                        {...devices}
                    ></Details>
                </Route>
                <Route
                    path={`${path}/form`}
                    exact
                >
                    <Form
                        onReturn={onReturn}
                        {...devices}
                    ></Form>
                </Route>
                <Route
                    path={`${path}/edit/:id`}
                    exact
                >
                    <Form
                        onReturn={onReturn}
                        {...devices}
                    ></Form>
                </Route>
                <Route
                    path={`${path}`}
                    exact
                >
                    <List
                        path={path}
                        history={props.history}
                        {...devices}
                    ></List>
                </Route>
            </Switch>
        </>
    )
}

export default redux(DevicesPage)
