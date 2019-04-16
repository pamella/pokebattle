import { normalize } from 'normalizr';
import {
  call, put, takeLatest, all,
} from 'redux-saga/effects';
import axios from 'axios';
import {
  FETCH_LIST_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST_SUCCESS,
  FETCH_LIST_BATTLE_ERROR,
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_DETAIL_BATTLE_REQUEST_SUCCESS,
  FETCH_DETAIL_BATTLE_ERROR,
} from '../constants';
import schemas from '../utils/schema';


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


export default function* rootSaga() {
  yield all([
    takeLatest(FETCH_LIST_BATTLE_REQUEST, loadListBattle),
    takeLatest(FETCH_DETAIL_BATTLE_REQUEST, loadDetailBattle),
  ]);
}
