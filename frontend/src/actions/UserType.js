import Action from "actions/utils/Action";

class UserType extends Action {
  constructor() {
    super("USER", "user_types", (state) => state.userTypes);
  }

  getUserTypePagination(params = {}, pagination = true, callback) {
    if (pagination) params["pagination"] = 1;
    return this.getPagination("", params, callback);
  }

  getUserTypeList(params = {}, callback) {
    return this.getList("", params, callback);
  }

  getUserTypeDetails(userTypeId, params = {}, callback) {
    return this.getDetails(`/${userTypeId}`, params, callback);
  }

  saveUserType(userType, callback) {
    return this.postData("", userType, callback);
  }

  setUserType(userTypeId, userType, callback) {
    return this.putData("", userTypeId, userType, callback);
  }

  deleteUserType(userTypeId, callback) {
    return this.deleteData("", userTypeId, callback);
  }

  restartUserType() {
    return this.restartData();
  }
}
export default UserType;
