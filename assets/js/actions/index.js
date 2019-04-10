import {
  FETCH_DETAIL_BATTLE,
  FETCH_LIST_BATTLE,
} from '../constants';


const fetchDetailBattle = battle => ({
  type: FETCH_DETAIL_BATTLE,
  battle,
});

const fetchListBattle = listBattle => ({
  type: FETCH_LIST_BATTLE,
  listBattle,
});

export default {
  fetchDetailBattle,
  fetchListBattle,
};
