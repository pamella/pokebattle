/* eslint-disable camelcase */
import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import axios from 'axios';
import styled from 'styled-components';
import { isEmpty } from 'lodash';
import setDetailBattleAction from '../../../../actions';
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
  const { creator_pokemon, opponent_pokemon } = round;
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
  trainerteam: PropTypes.string.isRequired,
};

Round.propTypes = {
  round: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
};

class BattleDetail extends React.Component {
  constructor(props) {
    super(props);
    // this is going to be replaced by router in next sprint card
    const url = window.location.href;
    const battleID = url.substring(url.lastIndexOf('detail/') + 7);

    this.state = {
      endpoint: '/api/battle/'.concat(battleID),
    };
  }

  componentDidMount() {
    const { endpoint } = this.state;
    const { setDetailBattle } = this.props;

    axios.get(endpoint)
      .then((response) => {
        setDetailBattle(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    const { battle } = this.props;
    const aux = battle.battle;

    if (isEmpty(aux)) return null;

    const { rounds } = aux;

    return (
      <div>
        <StyledItem>
          <Subtitle
            name="Battle Winner"
            img={fist}
          />

          <TrainerWinner
            creator={aux.trainer_creator_email}
            opponent={aux.trainer_opponent_email}
            winner={aux.trainer_winner_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Battle Trainers"
            img={player}
          />

          <Trainers
            creator={aux.trainer_creator_email}
            opponent={aux.trainer_opponent_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Rounds"
            img={fight}
          />

          <StyledRoundItem>
            {rounds.map((round, index) => <Round round={round} index={index} />)}
          </StyledRoundItem>
        </StyledItem>
      </div>
    );
  }
}

BattleDetail.propTypes = {
  setDetailBattle: PropTypes.func.isRequired,
  battle: PropTypes.string,
};

BattleDetail.defaultProps = {
  battle: '',
};

const mapStateToProps = state => ({
  battle: state.battle,
});

const mapDispatchToProps = dispatch => ({
  setDetailBattle: battle => dispatch(setDetailBattleAction(battle)),
});


export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
