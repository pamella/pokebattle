import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';
import pokebattleReducer from './reducers';
import rootSaga from './sagas';
import App from './App';


const sagaMiddleware = createSagaMiddleware();
const store = createStore(
  pokebattleReducer,
  applyMiddleware(sagaMiddleware),
);

sagaMiddleware.run(rootSaga);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('react-app'),
);
