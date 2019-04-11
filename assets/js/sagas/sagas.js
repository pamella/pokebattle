import {
  call, put, takeLatest, all,
} from 'redux-saga/effects';
import axios from 'axios';
import {
  FETCH_LIST_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_ERROR,
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_DETAIL_BATTLE_ERROR,
} from '../constants';


function* loadListBattle() {
  try {
    const url = 'api/my_battles';
    const battles = yield call(axios.get, url);
    yield put({
      type: FETCH_LIST_BATTLE_REQUEST,
      listBattle: battles.data,
    });
  } catch (error) {
    yield put({
      type: FETCH_LIST_BATTLE_ERROR,
      error: error.message,
    });
  }
}

function* loadDetailBattle(action) {
  try {
    const url = `/api/battle/${action.id}`;
    const battle = yield call(axios.get, url);
    yield put({
      type: FETCH_DETAIL_BATTLE_REQUEST,
      battle: battle.data,
    });
  } catch (error) {
    yield put({
      type: FETCH_DETAIL_BATTLE_ERROR,
      error: error.message,
    });
  }
}


export default function* rootSaga() {
  yield all([
    takeLatest(FETCH_LIST_BATTLE_REQUEST, loadListBattle),
    takeLatest(FETCH_DETAIL_BATTLE_REQUEST, loadDetailBattle),
  ]);
}
