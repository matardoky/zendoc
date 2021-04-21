import React, {useState} from 'react'
import { Col, Row, Menu, Popover} from 'antd'
import {MenuOutlined} from '@ant-design/icons'
import { Link } from 'react-router-dom'

const {SubMenu} = Menu

export const Header = ({isMobile, first_name, last_name, is_admin, logout}) => {
  const [menuVisible, setMenuVisible] = useState(false)
  const menuMode = isMobile ? "inline":"horizontal"

  const onMenuVisibleChange = (visible) => {
    setMenuVisible(visible)
  }

  const handleShowMenu = () => {
    setMenuVisible(true)
  }

  

  const menu = [
    <Menu mode={menuMode} defaultSelectedKeys={["home__1"]} id="nav" key="nav">
     
      <SubMenu title={`${first_name} ${last_name}`} key="submenu">
        {
          is_admin ? (
            <Menu.Item key="submenu__1">
              <Link to=""><span>Paramétres</span></Link>
            </Menu.Item>
              
          ):null
        }
        <Menu.Item key="submenu__2">
          <Link to=""><span>Profil bandoc</span></Link>
        </Menu.Item>

        <Menu.Item key="submenu__3">
          <Link to=""><span>Mon compte</span></Link>
        </Menu.Item>

        <Menu.Item key="submenu__4">
          <span onClick={()=>logout()}>Déconnexion</span>
        </Menu.Item>

      </SubMenu>

      <Menu.Item key="home__2">
       Icon
      </Menu.Item>
      <Menu.Item key="home__3">
        Icon
      </Menu.Item>

    </Menu>,
  ]
    return(
        <header id="header">
          {
            menuMode==="inline" ? (
              <Popover
              overlayClassName="popover-menu"
              placement="right"
              content={menu}
              trigger="click"
              arrowPointAtCenter
              visible={menuVisible}
              onVisibleChange={onMenuVisibleChange}
              >
                <MenuOutlined className="nav-phone-icon" onClick={handleShowMenu}/>

              </Popover>
 
            ):(
              null
            )
          }
          <Row>
            <Col lg={4} md={5} sm={24} xs={24}>
              <Link to="/session/home">
                <span>bandoc</span>
              </Link>
            </Col>
            <Col lg={20} md={19} sm={0} xs={0}>
              {
                menuMode ==="horizontal" ? menu : null
              }
            </Col>

          </Row>
            
        </header>

    )
}


