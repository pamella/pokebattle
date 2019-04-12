import { SET_DETAIL_BATTLE, SET_LIST_BATTLE } from '../constants';

const setDetailBattle = battle => ({
  type: SET_DETAIL_BATTLE,
  battle,
});

const setListBattle = listBattle => ({
  type: SET_LIST_BATTLE,
  listBattle,
});

export default {
  setDetailBattle,
  setListBattle,
};
