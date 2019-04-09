import { combineReducers } from 'redux';
import battleReducer from './battleReducer';

const pokebattleReducer = combineReducers({
  battle: battleReducer,
});

export default pokebattleReducer;
