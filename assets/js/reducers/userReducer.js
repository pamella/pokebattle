import { FETCH_LIST_USER_REQUEST_SUCCESS, FETCH_LIST_USER_ERROR } from '../constants/user';

const user = (state = [], action) => {
  switch (action.type) {
    case FETCH_LIST_USER_REQUEST_SUCCESS:
      return {
        ...state,
        payload: action.payload,
      };
    case FETCH_LIST_USER_ERROR:
      return {
        ...state,
        payload: action.payload,
      };
    default:
      return state;
  }
};

export default user;
