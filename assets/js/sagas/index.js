import { takeLatest, all } from 'redux-saga/effects';
import {
  FETCH_LIST_BATTLE_REQUEST,
  FETCH_DETAIL_BATTLE_REQUEST,
  POST_CREATE_BATTLE_REQUEST,
} from '../constants/battle';
import { FETCH_LIST_USER_REQUEST } from '../constants/user';
import { FETCH_LIST_POKEMON_REQUEST } from '../constants/pokemon';
import battleSagas from './battleSagas';
import userSagas from './userSagas';
import pokemonSagas from './pokemonSagas';


export default function* rootSaga() {
  yield all([
    takeLatest(FETCH_LIST_BATTLE_REQUEST, battleSagas.loadListBattle),
    takeLatest(FETCH_DETAIL_BATTLE_REQUEST, battleSagas.loadDetailBattle),
    takeLatest(POST_CREATE_BATTLE_REQUEST, battleSagas.createBattle),
    takeLatest(FETCH_LIST_USER_REQUEST, userSagas.loadListUser),
    takeLatest(FETCH_LIST_POKEMON_REQUEST, pokemonSagas.loadListPokemon),
  ]);
}
