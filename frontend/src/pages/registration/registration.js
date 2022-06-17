import React, { useEffect, useState } from 'react'
import Form from 'components/Registration'
import redux from 'reducers/utils/Redux'
import { LoadingBar } from 'finalsa-react-components'

function Registration (props){
    const [isLoaded, setIsLoaded] = useState(false)
    console.log(props)
    useEffect(() => {
        let callbackValidate = (ok) => {
            if (ok) {
                props.history.replace('/home');
            } else {
                setIsLoaded(true)
            }
        }
        if (props) {
            props.validateSession(callbackValidate)
        }
    }, [props])

    if (!isLoaded) {
        return (
            <LoadingBar></LoadingBar>
        )
    }
    return(
        <>
         <Form
                history={props.history}
                login={props.login}
                saveUser={props.saveUser}
            ></Form>
        </>
    )
}

export default redux(Registration);