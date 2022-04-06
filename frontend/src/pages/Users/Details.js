import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar } from 'finalsa-react-components'
import { ModalLayout } from "components/layout"
import { reduxProperties } from 'reducers/utils/Redux'
import Details from 'components/Users/Details'

function UserDetails(props) {

    const [data, setData] = useState(null)
    const { id } = props.match.params
    const { getUserDetails } = props

    let loadData = useCallback(() => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {

            }
        }
        getUserDetails(id, {}, callback)
    }, [getUserDetails, id])

    let reload = () => {
        setData(null)
        loadData()
    }

    useEffect(() => {
        loadData()
    }, [loadData])


    return (
        <>

            <ModalLayout
                title="Usuario"
                onReturn={props.onReturn}
                onReload={reload}
            >
                {
                    (!data) ?
                        (
                            <LoadingBar
                                isSmall={true}
                                reload={reload}
                            ></LoadingBar>
                        ) : (
                            <Details
                                data={data}
                            ></Details>
                        )
                }
            </ModalLayout>

        </>
    )
}

export default reduxProperties(UserDetails)