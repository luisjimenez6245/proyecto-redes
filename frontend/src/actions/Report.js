import Action from "actions/utils/Action";

class Report extends Action {
  constructor() {
    super("REPORT", "reports", (state) => state.reports);
  }

  getReportPagination(params = {}, pagination = true, callback) {
    if (pagination) params["pagination"] = 1;
    return this.getPagination("", params, callback);
  }

  getReportList(params = {}, callback) {
    return this.getList("", params, callback);
  }

  getReportDetails(reportId, params = {}, callback) {
    return this.getDetails(`/${reportId}`, params, callback);
  }

  saveReport(report, callback) {
    return this.postData("", report, callback);
  }

  setReport(reportId, report, callback) {
    return this.putData("", reportId, report, callback);
  }

  deleteReport(reportId, callback) {
    return this.deleteData("", reportId, callback);
  }

  restartReport() {
    return this.restartData();
  }
}
export default Report;
