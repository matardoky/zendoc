import React from 'react'
import { Switch, Redirect, Route} from 'react-router-dom'


const PrivateRoute = ({component: Component, ...rest}) => {
    const isAuthenticated = localStorage.getItem("user") !==null
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
            
        </Switch>
    )
    

}