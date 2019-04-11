import {
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST,
} from '../constants';


const fetchDetailBattle = (id, battle) => ({
  type: FETCH_DETAIL_BATTLE_REQUEST,
  id,
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
