import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar } from 'finalsa-react-components'
import { ModalLayout } from "components/layout"
import { reduxProperties } from 'reducers/utils/Redux'
import Form from 'components/Users/Form'

function UserForm(props) {

    const [data, setData] = useState(null)
    const [userTypes, setUserTypes] = useState([])
    const [formData, setFormData] = useState(null)
    const { id } = props.match.params
    const { getUserDetails, getUserTypeList } = props

    let loadData = useCallback(() => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {

            }
        }
        let getUserTypesCallback = (res) => {
            if (res.ok) {
                setUserTypes(res.body)
            } else {

            }
        }
        if (id) {
            getUserDetails(id, {}, callback)
        }
        getUserTypeList({}, getUserTypesCallback)
        setFormData({})
    }, [getUserDetails, id, getUserTypeList])

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
                title="Nuevo Usuario"
                onReturn={props.onReturn}
                onReload={reload}
            >
                {
                    (!formData) ?
                        (
                            <LoadingBar
                                isSmall={true}
                                reload={reload}
                            ></LoadingBar>
                        ) : (
                            <Form
                                data={data}
                                onReturn={props.onReturn}
                                saveUser={props.saveUser}
                                userTypes={userTypes}
                            ></Form>
                        )
                }
            </ModalLayout>

        </>
    )
}

export default reduxProperties(UserForm)