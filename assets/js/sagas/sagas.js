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


function* loadListBattle() {
  try {
    const url = 'api/my_battles';
    const listBattles = yield call(axios.get, url);
    yield put({
      type: FETCH_LIST_BATTLE_REQUEST_SUCCESS,
      payload: listBattles.data,
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
    yield put({
      type: FETCH_DETAIL_BATTLE_REQUEST_SUCCESS,
      payload: battle.data,
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
