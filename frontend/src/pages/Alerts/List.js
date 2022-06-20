import React, { useCallback, useEffect, useState } from "react"
import { LoadingBar, TableModule } from 'finalsa-react-components'


function ReportList(props) {

    const [data, setData] = useState(null)
    const { getReportPagination, path } = props

    let loadData = useCallback((actualPage = 0) => {
        let callback = (res) => {
            if (res.ok) {
                setData(res.body)
            } else {
                console.log(res.body)
            }
        }
        getReportPagination({ page: actualPage }, true, callback)
    }, [getReportPagination])

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

    const cols = [
        {
            selector: 'id',
            name: "Identificador"
        },
        {
            selector: 'action',
            name: "Alerta"
        },
        {
            selector: 'created_date',
            name: "Fecha"
        }
    ]


    return (
        <>
            <div className="columns ml-0 pl-0 pt-0 mt-0 is-multiline ">
                <div className="column  ml-0 pl-0 pt-0 mt-0 is-full">
                    <div className="title ">
                        Alertas
                    </div>
                   
                </div>
                <div className="column is-full ml-0 pl-0 ">
                    <TableModule
                        cols={cols}
                        onSelectedRow={(row) => {
                            props.history.replace(`${path}/details/${row.id}`);
                        }}
                        title="Alertas"
                        data={data}
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

export default (ReportList)