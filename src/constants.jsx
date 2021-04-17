let DEBUG = true
let host = "http://127.0.0.1:8000"

if(DEBUG===false){
    host = "";
}

export const APIEndpoint = `${host}`

export const authUrls = {
    LOGIN: `${APIEndpoint}/rest-auth/login/`, 
    REGISTRATION: `${APIEndpoint}/rest-auth/registration/`, 
    PASSWORD_CHANGE: `${APIEndpoint}/rest-auth/password/change/`, 
    PASSWORD_RESET: `${APIEndpoint}/rest-auth/password/reset/`, 
    PASSWORD_RESET_CONFIRM: `${APIEndpoint}/rest-auth/password/reset/confirm/`, 
    USER_ACTIVATION: `${APIEndpoint}/rest-auth/registration/verify-email`, 
    USER_PROFILE: `${APIEndpoint}/rest-auth/user/`, 
}
