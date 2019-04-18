import axios from 'axios';
import { normalize } from 'normalizr';
import {
  call, put, takeLatest, all,
} from 'redux-saga/effects';
import schemas from 'utils/schema';
import apiPostWrapper from 'utils/api';
import {
  FETCH_LIST_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST_SUCCESS,
  FETCH_LIST_BATTLE_ERROR,
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_DETAIL_BATTLE_REQUEST_SUCCESS,
  FETCH_DETAIL_BATTLE_ERROR,
  POST_CREATE_BATTLE_REQUEST,
  POST_CREATE_BATTLE_REQUEST_SUCCESS,
  POST_CREATE_BATTLE_ERROR,
} from '../constants';


function* loadListBattle() {
  try {
    const url = 'api/my_battles';
    const listBattles = yield call(axios.get, url);
    const normalizedListBattles = normalize(listBattles.data, schemas.listBattles);
    yield put({
      type: FETCH_LIST_BATTLE_REQUEST_SUCCESS,
      payload: normalizedListBattles,
    });
  } catch (error) {
    yield put({
      type: FETCH_LIST_BATTLE_ERROR,
      payload: error.message,
    });
  }
}

function* loadDetailBattle(action) {
  try {
    const url = `/api/battle/${action.payload}`;
    const battle = yield call(axios.get, url);
    const normalizedBattle = normalize(battle.data, schemas.battle);
    yield put({
      type: FETCH_DETAIL_BATTLE_REQUEST_SUCCESS,
      payload: normalizedBattle,
    });
  } catch (error) {
    yield put({
      type: FETCH_DETAIL_BATTLE_ERROR,
      payload: error.message,
    });
  }
}

function* createBattle(action) {
  try {
    yield console.log('saga payload ', action.payload);
    const values = action.payload;
    const url = '/api/create_battle/';
    const battle = yield call(apiPostWrapper.post, url, values);
    yield console.log('post call', battle);
    yield put({
      type: POST_CREATE_BATTLE_REQUEST_SUCCESS,
      payload: battle,
    });
  } catch (error) {
    yield console.log('saga error ', error);
    yield put({
      type: POST_CREATE_BATTLE_ERROR,
      payload: error.message,
    });
  }
}

export default function* rootSaga() {
  yield all([
    takeLatest(FETCH_LIST_BATTLE_REQUEST, loadListBattle),
    takeLatest(FETCH_DETAIL_BATTLE_REQUEST, loadDetailBattle),
    takeLatest(POST_CREATE_BATTLE_REQUEST, createBattle),
  ]);
}
