import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar } from 'finalsa-react-components'
import { ModalLayout } from "components/layout"
import { reduxProperties } from 'reducers/utils/Redux'
import Details from 'components/Devices/Details'

function DeviceDetails(props) {

    const [data, setData] = useState(null)
    const { id } = props.match.params
    const { getDeviceDetails, saveSnmp } = props

    let loadData = useCallback(() => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {

            }
        }
        getDeviceDetails(id, {}, callback)
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
                title="Dispositivo"
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
				saveChanges={saveSnmp}
                                data={data}
                            ></Details>
                        )
                }
            </ModalLayout>

        </>
    )
}

export default reduxProperties(DeviceDetails)
