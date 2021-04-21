import React, {useState, useEffect} from 'react'
import { connect} from "react-redux"
import { Layout } from 'antd'
import PropTypes from 'prop-types'
import { enquireScreen } from "enquire-js"
import { Header } from './contains/Hearder'
import DocumentTitle from 'react-document-title'
import { authLogout } from '../../store/actions/auth'

const { Content } = Layout


const BaseLayout = ({first_name, last_name, is_admin, logout, children}) => {
  const [isMobile, setIsMobile] = useState()

  useEffect(() => {
    enquireScreen( (b) => {
      setIsMobile(!!b)
    })
  }, []);

  return(
    <section id="session___home">
      <Layout>
        <Header 
        first_name={first_name} 
        last_name={last_name} 
        is_admin={is_admin}
        isMobile={isMobile}
        logout={logout}
        />
        <Content>
          {children}
        </Content>
        <DocumentTitle title="Optez pour le logiciel de gestion des consultations et des patients le plus complet"/>
      </Layout>
        
    </section>

  )
}

const mapStateToProps = ({auth: {first_name, last_name, is_admin}}) => {
  return {
    first_name: first_name, 
    last_name: last_name,
    is_admin: is_admin
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    logout: () => dispatch(authLogout())
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(BaseLayout)

BaseLayout.propTypes = {
  first_name:PropTypes.string,
  last_name:PropTypes.string,
  is_admin:PropTypes.bool,
  logout:PropTypes.func
}
