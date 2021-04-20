import React from 'react'
import { Switch, Redirect, Route} from 'react-router-dom'
import {ConfirmPasswordReset} from './components/Accounts/ConfirmPasswordReset';
import Login  from './components/Accounts/Login'
import PasswordChange from './components/Accounts/PasswordChange';
import { PasswordReset } from './components/Accounts/PasswordReset';


const PrivateRoute = ({component: Component, ...rest}) => {
    const isAuthenticated = localStorage.getItem("user") !==null;
    return (
        <Route
        {...rest}
        render={props =>
            isAuthenticated ===true ? (
                <Component {...props} />
            ):(
                <Redirect
                to={{
                    pathname:"/",
                    state: {from: props.location}
                }}
                />
            )
        }
        />
    )
}
export const BaseRouter = () => {

    return (
        <Switch>
            <Route exact path="/session/new" component ={Login}/>
            <Route exact path="/password/new" component={PasswordReset}/>
            <Route exact path="/rest-auth/password/reset/confirm/:uid/:token" component={ConfirmPasswordReset}/>
            <Route exact path="/password/change/new" component={PasswordChange}/>
            
        </Switch>
    )
    
}