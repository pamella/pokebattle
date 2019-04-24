import React from 'react';
import { Redirect } from 'react-router-dom';
import Select from 'react-select';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { withFormik, Form, Field } from 'formik';
import { isEmpty } from 'lodash';
import { denormalize } from 'normalizr';
import schemas from 'utils/schema';
import battleActions from 'actions/battle';
import userActions from 'actions/user';
import pokemonActions from 'actions/pokemon';
import Urls from 'utils/urls';
import { STATUS_201 } from '../../../../constants/request_status';


const CreateBattleContainerStyled = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
`;

const BattleCreateInnerForm = (props) => {
  const { denormalizedUsers, denormalizedPokemons } = props;
  const selectedOption = 'mudar aq';
  console.log('props ', props);

  const handleChange = () => {
    console.log('Option selected:', selectedOption);
  };

  const CustomOption = ({ innerRef, innerProps, data }) => (
    <div ref={innerRef} {...innerProps}>
      <img src={data.sprite} alt="pokemon" />
      <span>{data.name}</span>
    </div>
  );

  return (
    <CreateBattleContainerStyled>
      <h2>Select your opponent and your team to battle!</h2>

      <Form>
        <div>
          Opponent:
          <Field component="select" name="trainer_opponent">
            {denormalizedUsers.map(user => (
              <option value={{ user }.user.id}>{{ user }.user.email}</option>
            ))}
          </Field>
        </div>
        <div>
          Pokemon:
          <Select
            name="pokemon_1"
            value={selectedOption}
            onChange={handleChange}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          Round:
          <Field component="select" name="order_1">
            <option value="0">First</option>
            <option value="1">Second</option>
            <option value="2">Third</option>
          </Field>
        </div>
        <div>
          Pokemon:
          <Select
            name="pokemon_2"
            value={selectedOption}
            onChange={handleChange}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          Round:
          <Field component="select" name="order_2">
            <option value="0">First</option>
            <option value="1">Second</option>
            <option value="2">Third</option>
          </Field>
        </div>
        <div>
          Pokemon:
          <Select
            name="pokemon_3"
            value={selectedOption}
            onChange={handleChange}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          Round:
          <Field component="select" name="order_3">
            <option value="0">First</option>
            <option value="1">Second</option>
            <option value="2">Third</option>
          </Field>
        </div>

        <Field type="submit" value="Challenge now" />
      </Form>
    </CreateBattleContainerStyled>
  );
};

const BattleCreateForm = withFormik({
  mapPropsToValues: () => ({
    trainer_opponent: '',
    pokemon_1: '',
    order_1: 0,
    pokemon_2: '',
    order_2: 1,
    pokemon_3: '',
    order_3: 2,
  }),

  handleSubmit: (values, { props }) => {
    props.postCreateBattle(values);
  },
})(BattleCreateInnerForm);

class BattleCreate extends React.Component {
  componentDidMount() {
    const { fetchListUser, fetchListPokemon } = this.props;
    fetchListUser();
    fetchListPokemon();
  }

  render() {
    const { denormalizedUsers, denormalizedPokemons, submitStatus } = this.props;

    if (isEmpty(denormalizedUsers) || isEmpty(denormalizedPokemons)) return null;

    // Redirect after form submit
    if (submitStatus === STATUS_201) {
      return <Redirect to={Urls['battles:list_battle']()} />;
    }

    return (
      <div>
        <h2>Select your opponent and your team to battle!</h2>
        <BattleCreateForm
          denormalizedUsers={denormalizedUsers}
          denormalizedPokemons={denormalizedPokemons}
        />
      </div>
    );
  }
}

BattleCreateInnerForm.propTypes = {
  denormalizedUsers: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
  denormalizedPokemons: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
};

BattleCreateInnerForm.defaultProps = {
  denormalizedUsers: [],
  denormalizedPokemons: [],
};

BattleCreate.propTypes = {
  fetchListUser: PropTypes.func.isRequired,
  fetchListPokemon: PropTypes.func.isRequired,
  denormalizedUsers: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
  denormalizedPokemons: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
  submitStatus: PropTypes.number,
};

BattleCreate.defaultProps = {
  submitStatus: 0,
  denormalizedUsers: [],
  denormalizedPokemons: [],
};

const mapStateToProps = (state) => {
  const { battle, user, pokemon } = state;
  const submitStatus = battle.payload;

  if (isEmpty(user) || isEmpty(pokemon)) return null;
  const denormalizedUsers = denormalize(
    user.payload.result, schemas.listUsers, user.payload.entities,
  );
  const denormalizedPokemons = denormalize(
    pokemon.payload.result, schemas.listPokemons, pokemon.payload.entities,
  );

  return {
    submitStatus,
    denormalizedUsers,
    denormalizedPokemons,
  };
};

const mapDispatchToProps = dispatch => ({
  fetchListUser: () => dispatch(userActions.fetchListUser()),
  fetchListPokemon: () => dispatch(pokemonActions.fetchListPokemon()),
  postCreateBattle: battle => dispatch(battleActions.postCreateBattle(battle)),
});

export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate);
