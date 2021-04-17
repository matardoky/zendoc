import { authType } from "../actions/actionTypes"
import { UpdateObject } from "./utils"

let initialState = {
    
}

const authStart = (state, action) => {
    return UpdateObject(state, {
        loading:true
    })
}

const authSuccess= (state, action) => {
    return UpdateObject(state, {
        loading:false
    })
}

const authFail=(state, action) => {
    return UpdateObject(state,{

    })
}

const authLogout = (state, action) => {
    return UpdateObject(state, {

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