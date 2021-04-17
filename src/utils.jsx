import axios from 'axios'
import { APIEndpoint } from './constants'

export const authAxios = axios.create({
    baseURL: APIEndpoint,
    headers:{
        'Content-Type': 'application/json',
        Authorization:{
            toString(){
                return `Token ${JSON.parse(localStorage.getItem('user')).token}`
            }
        }
    }
})