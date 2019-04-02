import React from 'react';
import { NavLink } from 'react-router-dom';
import Urls from '../utils/urls';
import '../../css/normalize.css';
import '../../css/base.css';
import '../../css/navbar.css';
import logo from '../../images/icons/logo.png';


function Navbar() {
  return (
    <nav className="navbar">
      <div className="header__container">
        <img className="header__logo" src={logo} alt="pokebattle's logo" />
        <a className="header__title" href={Urls.home()}>PokeBattle</a>
      </div>

      <div className="menu">
        <NavLink className="menu__link" to={Urls['battles:create_battle']()}>
          Create a Battle!
        </NavLink>
        <NavLink className="menu__link" to={Urls['battles:list_battle']()}>
          My Battles
        </NavLink>
        <NavLink className="menu__link" to={Urls['battles:invite_friend']()}>
          Invite a friend
        </NavLink>
        <NavLink className="menu__link" to={Urls['users:logout']()}>
          Logout
        </NavLink>
      </div>
    </nav>
  );
}

export default Navbar;
