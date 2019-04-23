import { FETCH_LIST_POKEMON_REQUEST_SUCCESS, FETCH_LIST_POKEMON_ERROR } from '../constants/pokemon';

const pokemon = (state = [], action) => {
  switch (action.type) {
    case FETCH_LIST_POKEMON_REQUEST_SUCCESS:
      return {
        ...state,
        payload: action.payload,
      };
    case FETCH_LIST_POKEMON_ERROR:
      return {
        ...state,
        payload: action.payload,
      };
    default:
      return state;
  }
};

export default pokemon;
