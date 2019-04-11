import {
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_DETAIL_BATTLE_ERROR,
  FETCH_LIST_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_ERROR,
} from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case FETCH_DETAIL_BATTLE_REQUEST:
      return {
        ...state,
        battle: action.battle,
      };
    case FETCH_DETAIL_BATTLE_ERROR:
      return {
        ...state,
        error: action.error,
      };
    case FETCH_LIST_BATTLE_REQUEST:
      return {
        ...state,
        listBattle: action.listBattle,
      };
    case FETCH_LIST_BATTLE_ERROR:
      return {
        ...state,
        error: action.error,
      };
    default:
      return state;
  }
};

export default battle;
