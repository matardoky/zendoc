import React, {useState} from 'react'
import { Typography, Form, Input, Button, Row, Col, Alert} from 'antd'
import { useHistory, useParams } from 'react-router-dom'
import axios from 'axios'
import { authUrls } from '../../constants'


const { Title, Paragraph } = Typography

export const ConfirmPasswordReset = () => {
    const[success, setSuccess] = useState(false)
    const[fail, setFail] = useState(false)
    const[alert, setAlert] = useState("")

    let history = useHistory()
    let params = useParams()

    const confirm = (new_password1, new_password2) => {
      const {uid, token} = params
      
      const password = {
        new_password1,
        new_password2
      }

      const data = Object.assign(password, {uid, token})
      axios.post(authUrls.PASSWORD_RESET_CONFIRM, data
      )
      .then( ({data}) =>{
        setSuccess(true)
        setAlert(data.detail)
      })
      .catch( ({response:{data}}) =>{
        setFail(true)
        if(data.new_password2){
          setAlert(data.new_password2)
        }

        if(data.token){
          setAlert(data.token)
        }
      })

    }
    const onFinish = ({new_password1, new_password2}) => {
      confirm(new_password1, new_password2)
    }
    
    return (
      <section id="confirm__password">
        <Title level={4}>Créer votre nouveau mot de passe</Title>
        {
          success ? (
            <Alert message={alert} type="success" showIcon/>
 
          ):null
        }
        {
          fail ? (
            <Alert message={alert} type="error" showIcon/>
          ):null
        }
        <Paragraph>Choisissez un mot de passe sécurisé et ne le réutilisez pas pour d'autres comptes.</Paragraph>
        <Form
        hideRequiredMark
        colon={false}
        onFinish={onFinish}
        >
          <Form.Item
          name="new_password1"
          label="Nouveau mot de passe"
          style={{
            display:"block"
          }}
          rules ={[
            {
              required:true,
              message:"Entrer votre nouveau mot de passe"
            }
          ]}
          extra={`Niveau de sécurité du mot de passe: Utilisez au moins 8 caractères. Ne choisissez pas un mot de passe que vous utilisez déjà sur un autre site, ni un mot de passe trop évident, tel que le nom de votre animal de compagnie. `}
          >
            <Input.Password/>

          </Form.Item>
          <Form.Item
          name="new_password2"
          label="Confirmation du nouveau mot de passe"
          style={{
            display:"block"
          }}
          rules={[
            {
              required:true, 
              message:"Confirmer votre mot de passe"
            },
            ({getFieldValue}) => ({
              validator(rules, value){
                  if(!value || getFieldValue('new_password1')===value){
                    return Promise.resolve()
                  }
                  return Promise.reject("les deux mots de passe ne sont pas identiques")
              }
            })
          ]}
          dependencies={[
            "new_password1"
          ]}
          
          >
            <Input.Password/>

          </Form.Item>
          <Form.Item>
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <Button htmlType="submit" block > Valider </Button>
              </Col>
              <Col span={12}>
                <Button htmlType="submit" block onClick={()=> history.push("/")}>Annuler </Button>
              </Col>
            </Row>

          </Form.Item>

        </Form>
      </section>
    )
}