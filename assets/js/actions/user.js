import {
  FETCH_LIST_USER_REQUEST,
} from '../constants/user';


const fetchListUser = payload => ({
  type: FETCH_LIST_USER_REQUEST,
  payload,
});

export default {
  fetchListUser,
};
