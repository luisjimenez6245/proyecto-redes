import { connect } from "react-redux";
import { withRouter } from "react-router";

import User from 'actions/User'
import UserType from 'actions/UserType'
import Device from 'actions/Device'

import Defs from 'actions/helpers/Defs'

const user = new User();
const device = new Device();
const userType = new UserType();


const actions = [  
    {
        className: User,
        object: user
    },
    {
        className: UserType,
        object: userType
    },
    {
        className: Device,
        object: device
    },
    ...Defs
]


const stateToProps = (state, props) => {
    return {
        users: state.users.dataset,
    }
}

const dispToProps = (disp) => {
    let res = {};
    for (let action of actions) {
        let methods = Object.getOwnPropertyNames(action.className.prototype);
        for (let method of methods)
            if (method !== "constructor")
                res[method] = (...args) => disp(action.object[method](...args));
    }
    return res;
};


const mergeProps = (states, disps, props) =>
    Object.assign({}, states, disps, props);

const redux = (component) =>
    withRouter(connect(
        stateToProps,
        dispToProps,
        mergeProps
    )(component)
    );


export const reduxProperties = (component) =>
    withRouter(connect(

    )(component)
    );

export default redux;
