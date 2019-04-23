import axios from 'axios';
import { normalize } from 'normalizr';
import { call, put } from 'redux-saga/effects';
import schemas from 'utils/schema';
import {
  FETCH_LIST_USER_REQUEST_SUCCESS,
  FETCH_LIST_USER_ERROR,
} from '../constants/user';


function* loadListBattle() {
  try {
    const url = 'api/users';
    const listUsers = yield call(axios.get, url);
    const normalizedListUsers = normalize(listUsers.data, schemas.user);
    yield put({
      type: FETCH_LIST_USER_REQUEST_SUCCESS,
      payload: normalizedListUsers,
    });
  } catch (error) {
    yield put({
      type: FETCH_LIST_USER_ERROR,
      payload: error.message,
    });
  }
}

export default {
  loadListBattle,
};
