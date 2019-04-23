import { combineReducers } from 'redux';
import battleReducer from './battleReducer';
import userReducer from './userReducer';
import pokemonReducer from './pokemonReducer';

const pokebattleReducer = combineReducers({
  battle: battleReducer,
  user: userReducer,
  pokemon: pokemonReducer,
});

export default pokebattleReducer;
