import { authType } from "../actions/actionTypes"
import { UpdateObject } from "./utils"

let initialState = {}

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


export const authReducer= (state=initialState, action) => {
    switch(action.type){
        case authType.AUTH_START: return authStart(state, action)
        case authType.AUTH_SUCCESS: return authSuccess(state, action)
        default: return state
    }
}