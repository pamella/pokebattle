import { put, take, all } from 'redux-saga/effects';
import { SET_LIST_BATTLE } from '../constants';


function* loadListBattle() {
  try {
    yield take(SET_LIST_BATTLE);
  } catch (error) {
    yield put({
      type: 'FETCH_FAILED',
      error: error.message,
    });
  }
}

function* rootSaga() {
  yield console.log('testing saga');
  yield all([
    loadListBattle(),
  ]);
}

export default { rootSaga };
