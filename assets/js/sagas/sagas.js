import {
  call, put, takeLatest, all,
} from 'redux-saga/effects';
import axios from 'axios';
import { FETCH_LIST_BATTLE } from '../constants';


function* loadListBattle() {
  try {
    const url = 'api/my_battles00';
    const battles = yield call(axios.get, url);
    yield put({
      type: FETCH_LIST_BATTLE,
      listBattle: battles,
    });
  } catch (error) {
    yield put({
      type: 'FETCH_FAILED',
      error: error.message,
    });
  }
}

// function* loadDetailBattle(action) {
//   console.log(action);
// }

// status, loading, done, error

export default function* rootSaga() {
  yield console.log('testing saga');
  yield all([
    takeLatest(FETCH_LIST_BATTLE, loadListBattle),
  ]);
}
