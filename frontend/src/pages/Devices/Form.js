import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar } from 'finalsa-react-components'
import { ModalLayout } from "components/layout"
import { reduxProperties } from 'reducers/utils/Redux'
import Form from 'components/Devices/Form'

function DeviceForm(props) {

    const [data, setData] = useState(null)
    const [formData, setFormData] = useState(null)
    const { id } = props.match.params
    const { getDeviceDetails } = props

    let loadData = useCallback(() => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {

            }
        }
        if (id) {
            getDeviceDetails(id, {}, callback)
        }
        setFormData({})
    }, [getDeviceDetails, id])

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
                title="Nuevo Dispositivo"
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
                                saveDevice={props.saveDevice}
                            ></Form>
                        )
                }
            </ModalLayout>

        </>
    )
}

export default reduxProperties(DeviceForm)