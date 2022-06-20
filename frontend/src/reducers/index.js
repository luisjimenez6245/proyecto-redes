import { combineReducers } from "redux";
import UserReducer from 'reducers/UserReducer'
import UserTypeReducer from 'reducers/UserTypeReducer'
import DeviceReducer from 'reducers/DeviceReducer'
import ReportReducer from 'reducers/ReportReducer'

const reducers = {
    users: new UserReducer().reducer,
    user_types: new UserTypeReducer().reducer,
    devices: new DeviceReducer().reducer,
    reports: new ReportReducer().reducer,

};
export default combineReducers(reducers);