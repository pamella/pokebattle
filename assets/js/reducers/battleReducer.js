import { SET_DETAIL_BATTLE, SET_LIST_BATTLE } from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case SET_DETAIL_BATTLE:
      return {
        ...state,
        battle: action.battle,
      };
    case SET_LIST_BATTLE:
      return {
        ...state,
        listBattle: action.listBattle,
      };
    default:
      return state;
  }
};

export default battle;
