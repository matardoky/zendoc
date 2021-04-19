import React, {useState} from 'react'
import axios from 'axios'

import { Typography, Row, Col, Badge, Form, Input, Button, Alert} from "antd"
import { authUrls } from '../../constants'
const { Title, Paragraph } = Typography

export const PasswordReset = () => {
  const [alert, setAlert] = useState("")
  const [send, setSend] = useState(false)
  
  const reset = async (email) => {
      await axios.post(authUrls.PASSWORD_RESET, {
        email
      })
      .then( async ({data}) => {
        setSend(true)
        setAlert( await data.detail)

      })
      .catch(err => {
        console.log(err)
      })
  }
  
  const onFinish = (values) => {
    reset(values.email)
  }
  
    return(
        <section id="password__reset">
          <Title level={2}>Réinitialiser le mot de passe de votre compte bandoc</Title>
          {
            send ? (
              <Alert message={alert} type="success" showIcon/>
            ): null

          }
          <Row gutter={[16,16]}>
            <Col span={1}>
              <Badge count={1}  style={{ backgroundColor: '#001529' }} />
            </Col>
            <Col span={12} >
              <Paragraph>Entrez votre adresse mail ci-dessous.</Paragraph> 
            </Col>
          </Row>
          
          <Row gutter={[16,16]}>
            <Col span={1}>
              <Badge count={2}  style={{ backgroundColor: '#001529' }} />
            </Col>
            <Col span={12} >
              <Paragraph>Vous recevrez un mail.</Paragraph> 
            </Col>
          </Row>

          <Row gutter={[16,16]}>
            <Col span={1}>
              <Badge count={3}  style={{ backgroundColor: '#001529' }} />
            </Col>
            <Col span={12} >
              <Paragraph>Cliquez sur le lien dans le mail, vous pourrez choisir votre nouveau mot de passe.</Paragraph> 
            </Col>
          </Row>

          <Row gutter={[16,16]}>
            <Col span={1}>
              <Badge count={4}  style={{ backgroundColor: '#001529' }} />
            </Col>
            <Col span={12} >
              <Paragraph>Après la validation de votre nouveau mot de passe, vous pouvez vous connecter !</Paragraph> 
            </Col>
          </Row>

          <Form
          name="session__new"
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
          >
            <Form.Item
            name="email"
            rules = {[
              {
                required:true,
                message:"Enter votre addresse e-mail de votre compte bandoc"
              }
            ]}
            >
              <Input placeholder="Adresse e-mail de votre compte bandoc"/>

            </Form.Item>

            <Form.Item>
              <Button htmlType="submit" block>Envoyer</Button>
            </Form.Item>

          </Form>

          <Title level={3}>Je n’ai pas reçu de mail, pourquoi ?</Title>
          <Paragraph>La réception du mail peut se faire dans les minutes qui suivent, pensez également à vérifier vos spams. Si le problème persiste, merci de consulter notre FAQ.</Paragraph>
            
        </section>
    )
}