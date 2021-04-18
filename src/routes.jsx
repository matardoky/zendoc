import React from 'react'
import { Switch, Redirect, Route} from 'react-router-dom'
import Login  from './components/Accounts/Login'


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
            <Route exact path="/login" component ={Login}/>
            
        </Switch>
    )
    
}