import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar, TableModule } from 'finalsa-react-components'


function DeviceList(props) {

    const [data, setData] = useState(null)
    const { getDevicePagination, deleteDevice, path } = props

    let loadData = useCallback((actualPage = 0) => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {
                console.log(res.body)
            }
        }
        getDevicePagination({ page: actualPage }, true, callback)
    }, [getDevicePagination])

    let reload = () => {
        setData(null)
        loadData()
    }

    useEffect(() => {
        loadData()
    }, [loadData])
    console.log(data)
    if (!data) {
        return (
            <LoadingBar
                reload={reload}
            ></LoadingBar>
        )
    }
    let deleteAction = (row) => {
        let callback = (res) => {
            if (res.ok) {
                reload()
            }
            else {

            }
        }
        deleteDevice(row.id, callback)
    }

    const cols = [
        {
            selector: 'devicename',
            name: "Usuario"
        },
        {
            selector: 'name',
            name: "Nombre"
        },
        {
            selector: 'email',
            name: "Correo"
        },
        {
            selector: 'type.name',
            name: "Rol"
        },
    ]


    return (
        <>
            <div className="columns ml-0 pl-0 pt-0 mt-0 is-multiline ">
                <div className="column  ml-0 pl-0 pt-0 mt-0 is-full">
                    <div className="title ">
                        Dispositvos
                    </div>
                </div>
                <div className="column is-full ml-0 pl-0 ">
                    <TableModule
                        cols={cols}
                        onSelectedRow={(row) => {
                            props.history.replace(`${path}/details/${row.id}`);
                        }}
                        title="Dispositvos"
                        data={data}
                        onAdd={() => {
                            props.history.replace(`${path}/form`);
                        }}
                        onReload={reload}
                        totalPages={data.total_pages}
                        automatic={false}
                        handleChangePage={loadData}
                        count={data.actualPage}
                    ></TableModule>
                </div>
            </div>
        </>
    )
}

export default (DeviceList)