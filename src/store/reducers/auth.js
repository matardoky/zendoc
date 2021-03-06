import { authType } from "../actions/actionTypes"
import { UpdateObject } from "./utils"

let initialState = {
    token:null,
    error:null,
    loading:false
}

const authStart = (state, action) => {
    return UpdateObject(state, {
        loading:true
    })
}

const authSuccess= (state, action) => {
    return UpdateObject(state, {
        loading:false,
        token:action.user.token, 
        first_name:action.user.first_name, 
        last_name:action.user.last_name,
        is_admin:action.user.is_admin,

    })
}

const authFail=(state, action) => {
    return UpdateObject(state,{
        loading:false,
        error:action.error
    })
}

const authLogout = (state, action) => {
    return UpdateObject(state, {
        token:null,
    })
}


export const authReducer= (state=initialState, action) => {
    switch(action.type){
        case authType.AUTH_START: return authStart(state, action)
        case authType.AUTH_SUCCESS: return authSuccess(state, action)
        case authType.AUTH_FAIL: return authFail(state, action)
        case authType.AUTH_LOGOUT: return authLogout(state, action)

        default: return state
    }
}