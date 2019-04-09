/* eslint-disable react/prefer-stateless-function */
import React from 'react';
import BattleDetail from './DetailBattle';

class DetailBattle extends React.Component {
  render() {
    return (
      <div className="container">
        <BattleDetail />
      </div>
    );
  }
}

export default DetailBattle;
