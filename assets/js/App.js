import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import DetailBattle from './pages/detailBattlePage';
import ListBattle from './pages/listBattlePage';
import CreateBattle from './pages/createBattlePage';


function App() {
  return (
    <BrowserRouter forceRefresh>
      <div>
        <Navbar />
        <Switch>
          <Route path="/detail/:pk" component={DetailBattle} />
          <Route path="/my_battles" component={ListBattle} />
          <Route path="/create_battle" component={CreateBattle} />
          <Route render={() => <p>Page not found!</p>} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
