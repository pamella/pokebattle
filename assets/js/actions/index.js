import {
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST,
} from '../constants';


const fetchDetailBattle = payload => ({
  type: FETCH_DETAIL_BATTLE_REQUEST,
  payload,
});

const fetchListBattle = payload => ({
  type: FETCH_LIST_BATTLE_REQUEST,
  payload,
});

export default {
  fetchDetailBattle,
  fetchListBattle,
};
