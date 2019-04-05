/* eslint-disable react/prefer-stateless-function */
import React from 'react';
import BattleDetail from './DetailBattle';

class App extends React.Component {
  render() {
    return (
      <div className="container">
        <BattleDetail />
      </div>
    );
  }
}

export default App;
