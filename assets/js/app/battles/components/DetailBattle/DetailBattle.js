import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import styled from 'styled-components';
import { isEmpty } from 'lodash';
import fist from '../../../../../images/icons/fist.png';
import player from '../../../../../images/icons/player.png';
import fight from '../../../../../images/icons/fight.png';


const StyledItem = styled.div`
  margin-bottom: 80px;
`;

const StyledTrainerCreator = styled.span`
  color: #008ae6;
`;

const StyledTrainerOpponent = styled.span`
  color: #da0000;
`;

function Subtitle(props) {
  const { name, img } = props;
  return (
    <div>
      <h2>
        <img src={img} alt="" />
        {name}
      </h2>
    </div>
  );
}

function TrainerWinner(props) {
  const { creator, opponent, winner } = props;
  const isCreatorWinner = winner === creator;
  return (
    <div>
      { isCreatorWinner
        ? <StyledTrainerCreator><b>{creator}</b></StyledTrainerCreator>
        : <StyledTrainerOpponent><b>{opponent}</b></StyledTrainerOpponent>
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

function Round(props) {
  const { round } = props;
  if (isEmpty(round)) return null;
  return (
    <div>
      <h3>Round </h3>
      <div>
        {round[0].creator_pokemon.id}
        {console.log('rr ', { round })}
      </div>
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

Round.propTypes = {
  round: PropTypes.string.isRequired,
};

class BattleDetail extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      endpoint: '/api/battle/61',
      data: [],
    };
  }

  componentDidMount() {
    const { endpoint } = this.state;
    axios.get(endpoint)
      .then((response) => {
      // handle success
        this.setState(() => ({ data: response.data }));
      })
      .catch((error) => {
      // handle error
        console.log(error);
      });
  }

  render() {
    const { data } = this.state;
    const { rounds } = data;
    return (
      <div>
        <StyledItem>
          <Subtitle
            name="Battle Winner"
            img={fist}
          />

          <TrainerWinner
            creator={data.trainer_creator_email}
            opponent={data.trainer_opponent_email}
            winner={data.trainer_winner_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Battle Trainers"
            img={player}
          />

          <Trainers
            creator={data.trainer_creator_email}
            opponent={data.trainer_opponent_email}
          />
        </StyledItem>

        <StyledItem>
          <Subtitle
            name="Rounds"
            img={fight}
          />

          <Round round={rounds} />
        </StyledItem>
      </div>
    );
  }
}

export default BattleDetail;
