import {
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST,
} from '../constants';


const fetchDetailBattle = battle => ({
  type: FETCH_DETAIL_BATTLE_REQUEST,
  battle,
});

const fetchListBattle = listBattle => ({
  type: FETCH_LIST_BATTLE_REQUEST,
  listBattle,
});

export default {
  fetchDetailBattle,
  fetchListBattle,
};
