import {
  FETCH_DETAIL_BATTLE_REQUEST,
  FETCH_LIST_BATTLE_REQUEST,
  POST_CREATE_BATTLE_REQUEST,
} from '../constants/battle';


const fetchDetailBattle = payload => ({
  type: FETCH_DETAIL_BATTLE_REQUEST,
  payload,
});

const fetchListBattle = payload => ({
  type: FETCH_LIST_BATTLE_REQUEST,
  payload,
});

const postCreateBattle = payload => ({
  type: POST_CREATE_BATTLE_REQUEST,
  payload,
});

export default {
  fetchDetailBattle,
  fetchListBattle,
  postCreateBattle,
};
