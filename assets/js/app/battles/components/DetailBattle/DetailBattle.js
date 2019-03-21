import React from 'react';
import PropTypes from 'prop-types';


function Subtitle(props) {
  const { name } = props;
  return (
    <div>
      <h2 className="subtitle">
        {name}
      </h2>
    </div>
  );
}

Subtitle.propTypes = {
  name: PropTypes.string.isRequired,
};

class BattleDetail extends React.Component {
  constructor() {
    super();
    this.state = {
      name: 'Battle Winner',
    };
  }

  render() {
    const { name } = this.state;

    return (
      <div>
        <Subtitle name={name} />
      </div>
    );
  }
}

export default BattleDetail;
