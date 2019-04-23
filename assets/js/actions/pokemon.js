import {
  FETCH_LIST_POKEMON_REQUEST,
} from '../constants/pokemon';


const fetchListPokemon = payload => ({
  type: FETCH_LIST_POKEMON_REQUEST,
  payload,
});

export default {
  fetchListPokemon,
};
