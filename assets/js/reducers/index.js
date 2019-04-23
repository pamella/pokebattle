import { combineReducers } from 'redux';
import battleReducer from './battleReducer';
import userReducer from './userReducer';

const pokebattleReducer = combineReducers({
  battle: battleReducer,
  user: userReducer,
});

export default pokebattleReducer;
