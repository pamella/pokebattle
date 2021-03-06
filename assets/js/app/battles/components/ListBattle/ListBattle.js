/* eslint-disable camelcase */
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { isEmpty } from 'lodash';
import actions from 'actions';
import Urls from 'utils/urls';


const BattleWrapperStyled = styled.div`
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
`;

const BattleItemStyled = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 300px;
  height: 300px;
  margin-bottom: 30px;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid lightgray;
  box-shadow: 1px 1px 4px lightgray;
`;

const WinnerBattleStyled = styled.span`
  color: #009999;
`;

const HrStyled = styled.hr`
  width: 100%;
`;

const PStyled = styled.p`
  word-wrap: break-word;
`;

const OrangePStyled = styled.p`
  color: #ff6600;
`;

const DetailLinkStyled = styled(Link)`
  text-decoration: none;
  color: #ff6600;

  :hover {
    color: #ffb84d;
  }
`;

function OngoingBattleBox(battle) {
  const {
    id, is_trainer_creator, trainer_opponent_email, trainer_creator_email, rounds,
  } = battle.battle;
  const opponent = is_trainer_creator
    ? trainer_opponent_email
    : trainer_creator_email;

  return (
    <BattleItemStyled>
      {is_trainer_creator
        ? (
          <div>
            <OrangePStyled>Waiting trainer to challenge back.</OrangePStyled>
            <HrStyled />
            <PStyled>
              <b>Opponent:</b>
              &nbsp;
              {opponent}
            </PStyled>
            <div>
              <b>My team:</b>
              <ul>
                { rounds.map(pokemon => <li>{pokemon.creator_pokemon.name}</li>) }
              </ul>
            </div>
          </div>
        )
        : (
          <div>
            <PStyled>
              Trainer&nbsp;
              <b>{trainer_creator_email}</b>
              &nbsp;challenge you.
            </PStyled>
            <DetailLinkStyled to={Urls['battles:select_team']().concat(`?id=${id}`)}>
              Select your team to challenge back!
            </DetailLinkStyled>
          </div>
        )
}
    </BattleItemStyled>
  );
}

function SettledBattleBox(battle) {
  const {
    id, is_trainer_creator, trainer_opponent_email, trainer_creator_email,
    trainer_winner_email, rounds,
  } = battle.battle;
  const opponent = is_trainer_creator
    ? trainer_opponent_email
    : trainer_creator_email;

  return (
    <BattleItemStyled>
      <WinnerBattleStyled>
        <b>Winner:</b>
        &nbsp;
        {trainer_winner_email}
      </WinnerBattleStyled>

      <HrStyled />

      <PStyled>
        <b>Opponent:</b>
        &nbsp;
        {opponent}
      </PStyled>
      <div>
        <b>My team:</b>
        <ul>
          {is_trainer_creator
            ? rounds.map(pokemon => <li>{pokemon.creator_pokemon.name}</li>)
            : rounds.map(pokemon => <li>{pokemon.opponent_pokemon.name}</li>)
          }
        </ul>
      </div>
      <DetailLinkStyled to={Urls['battles:detail_battle'](id)}>
        Click to see this battle details.
      </DetailLinkStyled>
    </BattleItemStyled>
  );
}

function OngoingBattles(battles) {
  if (isEmpty(battles)) return null;
  const listItem = battles.battles.map(battle => <OngoingBattleBox battle={battle} />);
  return (
    <div>
      <h2>On Going Battles</h2>
      <BattleWrapperStyled>
        {listItem}
      </BattleWrapperStyled>
    </div>
  );
}

function SettledBattles(battles) {
  if (isEmpty(battles)) return null;
  const listItem = battles.battles.map(battle => <SettledBattleBox battle={battle} />);
  return (
    <div>
      <h2>Settled Battles</h2>
      <BattleWrapperStyled>
        {listItem}
      </BattleWrapperStyled>
    </div>
  );
}

class BattleList extends React.Component {
  componentDidMount() {
    const { fetchListBattle } = this.props;
    fetchListBattle();
  }

  render() {
    const { battles } = this.props;
    if (isEmpty(battles)) return null;

    const ongoing = battles.filter(battle => battle.status === 'ON_GOING');
    const settled = battles.filter(battle => battle.status === 'SETTLED');
    return (
      <div>
        <OngoingBattles battles={ongoing} />
        <SettledBattles battles={settled} />
      </div>
    );
  }
}

BattleList.propTypes = {
  battles: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  fetchListBattle: PropTypes.func.isRequired,
};

const mapStateToProps = state => ({
  battles: state.battle.payload,
});

const mapDispatchToProps = dispatch => ({
  fetchListBattle: () => dispatch(actions.fetchListBattle()),
});


export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
