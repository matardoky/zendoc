import React from 'react'
import { Form, Input, Button, Checkbox } from 'antd';
import { connect } from 'react-redux'
import { authLogin } from '../../store/actions/auth';

import PropTypes from 'prop-types'

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};
const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};

const Login = ({loading, isAuthenticated, error, onAuth}) => {
  const onFinish = (values) => {
    console.log(values.email, values.password)
    

    onAuth(values.email, values.password)

  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
  console.log(loading)
  return (
    
    <Form
      {...layout}
      name="basic"
      initialValues={{
        remember: true,
      }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
      <p>{error}</p>
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
        <Input />
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
        <Input.Password />
      </Form.Item>

      <Form.Item {...tailLayout} name="remember" valuePropName="checked">
        <Checkbox>Remember me</Checkbox>
      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};

const mapStateToProps = ({auth:{token, loading, error}}) => {
  return {
    isAuthenticated: token !==null,
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
  loading:PropTypes.bool

}