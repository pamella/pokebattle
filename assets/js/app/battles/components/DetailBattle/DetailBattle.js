import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import fist from '../../../../../images/icons/fist.png';
import player from '../../../../../images/icons/player.png';
import fight from '../../../../../images/icons/fight.png';


const StyledItem = styled.div`
  margin-bottom: 80px;
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

Subtitle.propTypes = {
  name: PropTypes.string.isRequired,
  img: PropTypes.string.isRequired,
};

function BattleDetail() {
  return (
    <div>
      <StyledItem>
        <Subtitle
          name="Battle Winner"
          img={fist}
        />
      </StyledItem>

      <StyledItem>
        <Subtitle
          name="Battle Trainers"
          img={player}
        />
      </StyledItem>

      <StyledItem>
        <Subtitle
          name="Rounds"
          img={fight}
        />
      </StyledItem>
    </div>
  );
}

export default BattleDetail;
