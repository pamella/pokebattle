import axios from 'axios';
import { normalize } from 'normalizr';
import { call, put } from 'redux-saga/effects';
import schemas from 'utils/schema';
import {
  FETCH_LIST_POKEMON_REQUEST_SUCCESS,
  FETCH_LIST_POKEMON_ERROR,
} from '../constants/pokemon';


function* loadListPokemon() {
  try {
    const url = 'api/pokemons';
    const listPokemons = yield call(axios.get, url);
    const normalizedListPokemons = normalize(listPokemons.data, schemas.listPokemons);
    yield put({
      type: FETCH_LIST_POKEMON_REQUEST_SUCCESS,
      payload: normalizedListPokemons,
    });
  } catch (error) {
    yield put({
      type: FETCH_LIST_POKEMON_ERROR,
      payload: error.message,
    });
  }
}

export default {
  loadListPokemon,
};
