import React from 'react';
import { NavLink } from 'react-router-dom';
import styled from 'styled-components';
import Urls from '../utils/urls';
import '../../css/normalize.css';
import '../../css/base.css';
import logo from '../../images/icons/logo.png';

const HeaderContainerStyled = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: center;
  height: 60px;
  background-color: #004d99;
`;

const HeaderLogoStyled = styled.img`
  width: 2.5rem;
  margin-right: 5px;
`;

const HeaderTitleStyled = styled.a`
  color: white;
    font-size: 1.5rem;
    font-weight: 500;
    text-decoration: none;
`;

const MenuContainerStyled = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-around;
  height: 50px;
  background-color: white;
  box-shadow: 1px 1px 1px lightgray;
`;

const MenuLinkStyled = styled(NavLink)`
  text-decoration: none;
  color:  #004d99;

  :hover {
    color: #479cf1;
  }
`;

function Navbar() {
  return (
    <nav>
      <HeaderContainerStyled>
        <HeaderLogoStyled src={logo} alt="pokebattle's logo" />
        <HeaderTitleStyled href={Urls.home()}>PokeBattle</HeaderTitleStyled>
      </HeaderContainerStyled>

      <MenuContainerStyled>
        <MenuLinkStyled to={Urls['battles:create_battle']()}>
          Create a Battle!
        </MenuLinkStyled>
        <MenuLinkStyled to={Urls['battles:list_battle']()}>
          My Battles
        </MenuLinkStyled>
        <MenuLinkStyled to={Urls['battles:invite_friend']()}>
          Invite a friend
        </MenuLinkStyled>
        <MenuLinkStyled to={Urls['users:logout']()}>
          Logout
        </MenuLinkStyled>
      </MenuContainerStyled>
    </nav>
  );
}

export default Navbar;
