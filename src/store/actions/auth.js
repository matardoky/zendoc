import axios from 'axios'
import { authUrls } from '../../constants'
import { authType } from './actionTypes'

const authStart = () => {
    return {
        type: authType.AUTH_START
    }
}

const authSuccess = (user) => {
    return {
        type: authType.AUTH_SUCCESS,
        user
    }
}

const authFail = (error) => {
    return {
        type:authType.AUTH_FAIL,
        error
    }
}

export const authLogout = ()=> {
    localStorage.removeItem('user')
    return {
        type:authType.AUTH_LOGOUT
    }
}

const chechAuthTimeout = (expirationDate) => {
    return dispatch => {
        setTimeout( ()=> {
            dispatch(authLogout())
        }, expirationDate*1000)
    }
}

export const chechAuthState = () => {
    return dispatch => {
        const user = JSON.parse(localStorage.getItem('user'))
        if(user===undefined || user===null){
            dispatch(authLogout())
        }else{
            const expirationDate = new Date(user.expirationDate)
            if(expirationDate <= new Date()){
                dispatch(authLogout())
            }else{
                dispatch(authSuccess(user))
                dispatch(chechAuthTimeout( (expirationDate.getTime()-new Date().getTime())/1000 ))
            }
        }
    }
}

export const authLogin = (email, password) => {
    return async dispatch => {
        dispatch(authStart())
        await axios.post(authUrls.LOGIN, {
            email,
            password
        })
        .then( ({data:{key, user_type}}) => {
            const user = {
                token: key,
                first_name: user_type.first_name,
                last_name: user_type.last_name,
                is_admin: user_type.is_admin,
                expirationDate: new Date(new Date().getTime()+3600*1000)
            }
            localStorage.setItem('user', JSON.stringify(user))
            dispatch(authSuccess(user))
            dispatch(chechAuthTimeout(3600))
        })
        .catch(error => {
            dispatch(authFail(error.response.data.non_field_errors[0]))
        })
    }
}