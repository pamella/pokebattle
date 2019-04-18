import {
  FETCH_DETAIL_BATTLE_REQUEST_SUCCESS,
  FETCH_DETAIL_BATTLE_ERROR,
  FETCH_LIST_BATTLE_REQUEST_SUCCESS,
  FETCH_LIST_BATTLE_ERROR,
  POST_CREATE_BATTLE_REQUEST_SUCCESS,
  POST_CREATE_BATTLE_ERROR,
} from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case FETCH_DETAIL_BATTLE_REQUEST_SUCCESS:
      return {
        ...state,
        payload: action.payload,
      };
    case FETCH_DETAIL_BATTLE_ERROR:
      return {
        ...state,
        payload: action.payload,
      };
    case FETCH_LIST_BATTLE_REQUEST_SUCCESS:
      return {
        ...state,
        payload: action.payload,
      };
    case FETCH_LIST_BATTLE_ERROR:
      return {
        ...state,
        payload: action.payload,
      };
    case POST_CREATE_BATTLE_REQUEST_SUCCESS:
      return {
        ...state,
        payload: action.payload,
      };
    case POST_CREATE_BATTLE_ERROR:
      return {
        ...state,
        payload: action.payload,
      };
    default:
      return state;
  }
};

export default battle;
