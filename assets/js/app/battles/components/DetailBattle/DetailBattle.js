/* eslint-disable camelcase */
import React from 'react';
import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { isEmpty } from 'lodash';
import { denormalize } from 'normalizr';
import schemas from 'utils/schema';
import actions from 'actions/battle';
import fist from '../../../../../images/icons/fist.png';
import player from '../../../../../images/icons/player.png';
import fight from '../../../../../images/icons/fight.png';


const StyledItem = styled.div`
  padding: 30px 0 40px 0;
  box-sizing: border-box;
`;

const StyledTrainerCreator = styled.span`
  color: #008ae6;
`;

const StyledTrainerOpponent = styled.span`
  color: #da0000;
`;

const StyledRoundItem = styled.div`
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
`;

const StyledRoundPokemonsItem = styled.div`
  display: flex;
  justify-content: space-between;
  width: 300px;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid lightgray;
  box-shadow: 1px 1px 4px lightgray;
`;

const StyledPokemonItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const StyledPokemonImg = styled.img`
  height: 96px;
`;

function Subtitle(props) {
  const { name, img } = props;
  return (
    <h2>
      <img src={img} alt="" />
      {' '}
      {name}
    </h2>
  );
}

function TrainerWinner(props) {
  const { creator, opponent, winner } = props;
  const isCreatorWinner = winner === creator;
  return (
    <div>
      { isCreatorWinner
        ? <StyledTrainerCreator>{creator}</StyledTrainerCreator>
        : <StyledTrainerOpponent>{opponent}</StyledTrainerOpponent>
      }
    </div>
  );
}

function Trainers(props) {
  const { creator, opponent } = props;
  return (
    <div>
      <StyledTrainerCreator>{creator}</StyledTrainerCreator>
      {' '}
      VS
      {' '}
      <StyledTrainerOpponent>{opponent}</StyledTrainerOpponent>
    </div>
  );
}

function RoundHeader(props) {
  const { index } = props;
  return (
    <h4>
    Round
      {' '}
      {index + 1}
    </h4>
  );
}

function Pokemon(props) {
  const { trainerteam } = props;
  return (
    <StyledPokemonItem>
      <StyledPokemonImg src={trainerteam.sprite} alt="" />
      <ul>
        <li>{trainerteam.name}</li>
        <li>
          A:
          {' '}
          {trainerteam.attack}
        </li>
        <li>
          D:
          {' '}
          {trainerteam.defense}
        </li>
        <li>
          HP:
          {' '}
          {trainerteam.hitpoints}
        </li>
      </ul>
    </StyledPokemonItem>
  );
}

function Round(props) {
  const { round, index } = props;
  const creator_pokemon = round[0];
  const opponent_pokemon = round[1];
  return (
    <div>
      <RoundHeader index={index} />

      <StyledRoundPokemonsItem>
        <StyledTrainerCreator>
          <Pokemon trainerteam={creator_pokemon} />
        </StyledTrainerCreator>
        <StyledTrainerOpponent>
          <Pokemon trainerteam={opponent_pokemon} />
        </StyledTrainerOpponent>
      </StyledRoundPokemonsItem>
    </div>
  );
}

class BattleDetail extends React.Component {
  componentDidMount() {
    const { fetchDetailBattle, match } = this.props;
    const battleID = match.params.pk;
    fetchDetailBattle(battleID);
  }

  render() {
    const { denormalizedBattle } = this.props;
    if (isEmpty(denormalizedBattle)) return null;

    const { rounds } = denormalizedBattle;

    return (
      <div>
        <StyledItem>
          <Subtitle
            name="Battle Winner"
            img={fist}
          />

          <TrainerWinner
            creator={denormalizedBattle.trainer_creator_email}
            opponent={denormalizedBattle.trainer_opponent_email}
            winner={denormalizedBattle.trainer_winner_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Battle Trainers"
            img={player}
          />

          <Trainers
            creator={denormalizedBattle.trainer_creator_email}
            opponent={denormalizedBattle.trainer_opponent_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Rounds"
            img={fight}
          />

          <StyledRoundItem>
            <Round round={rounds[0]} index={0} />
            <Round round={rounds[1]} index={1} />
            <Round round={rounds[2]} index={2} />
          </StyledRoundItem>
        </StyledItem>
      </div>
    );
  }
}

Subtitle.propTypes = {
  name: PropTypes.string.isRequired,
  img: PropTypes.string.isRequired,
};

TrainerWinner.propTypes = {
  creator: PropTypes.string.isRequired,
  opponent: PropTypes.string.isRequired,
  winner: PropTypes.string.isRequired,
};

Trainers.propTypes = {
  creator: PropTypes.string.isRequired,
  opponent: PropTypes.string.isRequired,
};

RoundHeader.propTypes = {
  index: PropTypes.number.isRequired,
};

Pokemon.propTypes = {
  trainerteam: PropTypes.shape({
    id: PropTypes.number,
    api_id: PropTypes.number,
    name: PropTypes.string,
    sprite: PropTypes.string,
    attack: PropTypes.number,
    defense: PropTypes.number,
    hitpoints: PropTypes.number,
  }).isRequired,
};

Round.propTypes = {
  round: PropTypes.oneOfType([
    PropTypes.object,
  ]).isRequired,
  index: PropTypes.number.isRequired,
};

BattleDetail.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      pk: PropTypes.string,
    }).isRequired,
  }).isRequired,
  fetchDetailBattle: PropTypes.func.isRequired,
  denormalizedBattle: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
};

const mapStateToProps = (state) => {
  const { battle } = state;
  if (isEmpty(battle)) return null;

  const { payload } = battle;
  const denormalizedBattle = denormalize(payload.result, schemas.battle, payload.entities);

  return {
    denormalizedBattle,
  };
};

const mapDispatchToProps = dispatch => ({
  fetchDetailBattle: payload => dispatch(actions.fetchDetailBattle(payload)),
});


export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BattleDetail));
