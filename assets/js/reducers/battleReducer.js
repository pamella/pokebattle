import SET_DETAIL_BATTLE from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case SET_DETAIL_BATTLE:
      return {
        ...state,
        battle: action.battle,
      };
    default:
      return state;
  }
};

export default battle;
