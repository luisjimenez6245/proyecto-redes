import React, { useEffect, useState, useCallback } from 'react'
import HomeLayout from 'components/Home'
import { LoadingBar } from 'finalsa-react-components'
import redux from 'reducers/utils/Redux'
import NotFound from 'pages/404'
import { Route, Switch } from 'react-router'

function Home(props) {

    const [selectedPath, setSelectedPath] = useState('')
    const { getUser, logout, getUserDetails, history } = props
    const { path } = props.match
    const logoutAction = useCallback(() => {
        history.replace('/login');
    }, [ history])

    const callback = useCallback((res) => {
        if (res.ok) {
            setUser(res.body)
        } else {
            logout(null, logoutAction)
        }
    }, [logout, logoutAction])

    const [user, setUser] = useState(null)

    useEffect(() => {
        console.log("render")
        getUser(callback, logoutAction, getUserDetails)

    }, [setUser, getUser, getUserDetails, callback, logoutAction,])

    if (!props) {
        return (
            <>
            </>
        )
    }

    if (!user) {
        return (
            <>
                <LoadingBar></LoadingBar>
            </>
        )
    }
    return (
        <>
            <HomeLayout path={selectedPath} user={user} logout={logout}>
                <Switch>
                
                    <Route>
                        <NotFound
                            setActualPage={setSelectedPath}
                        ></NotFound>
                    </Route>
                </Switch>
            </HomeLayout>
        </>
    )
}

export default redux(Home)