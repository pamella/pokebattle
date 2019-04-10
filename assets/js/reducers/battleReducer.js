import { FETCH_DETAIL_BATTLE, FETCH_LIST_BATTLE } from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case FETCH_DETAIL_BATTLE:
      return {
        ...state,
        battle: action.battle,
      };
    case FETCH_LIST_BATTLE:
      return {
        ...state,
        listBattle: action.listBattle,
      };
    default:
      return state;
  }
};

export default battle;
