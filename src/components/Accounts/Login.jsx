import React from 'react'
import { Form, Input, Button, Checkbox, Spin, Typography } from 'antd';
import {UserOutlined, LockOutlined} from  '@ant-design/icons'
import { connect } from 'react-redux'
import { Redirect, Link } from "react-router-dom"
import { authLogin } from '../../store/actions/auth';

import PropTypes from 'prop-types'

const { Title, Paragraph } = Typography

const Login = ({loading, isAuthenticated, error, onAuth}) => {
  
  const onFinish = (values) => {
    onAuth(values.email, values.password)
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
  
  if(isAuthenticated){
    return <Redirect to="/session/home"/>
  }
  return (
    <section id="session__new">
      {
        loading ? (
          <Spin/>
        ):(
            <Form
            name="session__new"
            initialValues={{
              remember: true,
            }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            >  
              <Title level={2}>Identifiez-vous</Title>
              <Paragraph type="danger">{error}</Paragraph>
              <Form.Item
                label="Email"
                name="email"
                rules={[
                  {
                    required: true,
                    message: 'Please input your email!',
                  },
                ]}
              >
                <Input prefix={<UserOutlined />} placeholder="Adresse e-mail"/>
              </Form.Item>
          
              <Form.Item
                label="Password"
                name="password"
                rules={[
                  {
                    required: true,
                    message: 'Please input your password!',
                  },
                ]}
              >
                <Input.Password prefix={<LockOutlined />}/>
              </Form.Item>
          
              <Form.Item  name="remember" valuePropName="checked">
                <Checkbox>Se souvenir de mon identifiant</Checkbox>
              </Form.Item>
          
              <Form.Item >
                <Button type="primary" htmlType="submit">
                  connectez-vous
                </Button>
              </Form.Item>
              <Link to="/password/new"> mot de passe oublié ?</Link>
            </Form>
          )
      }
    
    </section>

        
      
  )
}

const mapStateToProps = ({auth:{token, loading, error}}) => {
  return {
    isAuthenticated: token !== null,
    loading: loading,
    error: error
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onAuth: (email, password)=> dispatch(authLogin(email, password))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);

Login.propTypes = {
  onAuth:PropTypes.func,
  isAuthenticated:PropTypes.bool,
  loading:PropTypes.bool,
  error: PropTypes.string
}