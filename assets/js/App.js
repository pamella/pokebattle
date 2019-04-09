import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import DetailBattle from './pages/detailBattlePage';


function App() {
  return (
    <BrowserRouter forceRefresh>
      <div>
        <Navbar />
        <Switch>
          <Route path="/detail/:pk" component={DetailBattle} />
          <Route render={() => <p>Page not found!</p>} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
