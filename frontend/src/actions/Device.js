import Action from "actions/utils/Action";

class Device extends Action {
  constructor() {
    super("DEVICE", "devices", (state) => state.devices);
  }

  getDevicePagination(params = {}, pagination = true, callback) {
    if (pagination) params["pagination"] = 1;
    return this.getPagination("", params, callback);
  }

  getDeviceList(params = {}, callback) {
    return this.getList("", params, callback);
  }

  getDeviceDetails(deviceId, params = {}, callback) {
    return this.getDetails(`/${deviceId}`, params, callback);
  }

  saveDevice(device, callback) {
    return this.postData("", device, callback);
  }

  setDevice(deviceId, device, callback) {
    return this.putData("", deviceId, device, callback);
  }

  deleteDevice(deviceId, callback) {
    return this.deleteData("", deviceId, callback);
  }

  restartDevice() {
    return this.restartData();
  }
}
export default Device;
