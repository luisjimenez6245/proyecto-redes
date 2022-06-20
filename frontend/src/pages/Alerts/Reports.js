import redux from "reducers/utils/Redux"
import { Route, Switch } from 'react-router-dom';
import { useEffect } from "react";
import List from './List'

function ReportsPage(props) {
    const { setActualPage, getReportPagination, getReportDetails, getReportList, saveReport, deleteReport, setReport} = props
    const { path } = props.match

    const reports = { getReportPagination, getReportDetails, getReportList, saveReport, deleteReport, setReport }
    useEffect(() => {
        if (setActualPage) {
            setActualPage('reports')
        }
    }, [setActualPage])
    return (
        <>

            <Switch>
                <Route>
                    <List
                        path={path}
                        history={props.history}
                        {...reports}
                    ></List>
                </Route>
            </Switch>
        </>
    )
}

export default redux(ReportsPage)