import React from 'react';
import { Redirect } from 'react-router-dom';
import Select from 'react-select';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { connect } from 'react-redux';
import {
  withFormik, Form, Field, ErrorMessage,
} from 'formik';
import * as Yup from 'yup';
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
  width: 100%;
  margin: auto;

  Form {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 500px;
  }
`;

const CreateBattleRowStyled = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 15px auto;

  .css-1pcexqc-container {
    width: 70%;
  }
`;

const BattleCreateInnerForm = (props) => {
  const {
    denormalizedUsers, denormalizedPokemons, setFieldValue,
  } = props;

  const handleChangePokemon = (selectedPokemon, fieldName) => {
    setFieldValue(fieldName.name, selectedPokemon.name);
  };

  const CustomOption = option => (
    <div ref={option.innerRef} {...option.innerProps}>
      <img src={option.data.sprite} alt="pokemon" />
      <span>{option.data.name}</span>
    </div>
  );

  return (
    <CreateBattleContainerStyled>
      <h2>Select your opponent and your team to battle!</h2>

      <Form>
        <CreateBattleRowStyled>
          Opponent:
          <Field component="select" name="trainer_opponent">
            {denormalizedUsers.map(user => (
              <option value={{ user }.user.id}>{{ user }.user.email}</option>
            ))}
          </Field>
          <ErrorMessage name="trainer_opponent" />
        </CreateBattleRowStyled>

        <CreateBattleRowStyled>
          Pokemon:
          <Select
            name="pokemon_1"
            onChange={handleChangePokemon}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          <ErrorMessage name="pokemon_1" />
        </CreateBattleRowStyled>

        <CreateBattleRowStyled>
          Pokemon:
          <Select
            name="pokemon_2"
            onChange={handleChangePokemon}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          <ErrorMessage name="pokemon_2" />
        </CreateBattleRowStyled>

        <CreateBattleRowStyled>
          Pokemon:
          <Select
            name="pokemon_3"
            onChange={handleChangePokemon}
            options={denormalizedPokemons}
            components={{ Option: CustomOption }}
          />
          <ErrorMessage name="pokemon_3" />
        </CreateBattleRowStyled>

        <Field type="submit" value="Challenge now" />
      </Form>
    </CreateBattleContainerStyled>
  );
};

const battleCreateFormSchema = Yup.object().shape({
  trainer_opponent: Yup.number().required('Select an opponent to challenge.'),
  pokemon_1: Yup.string().required('Select a pokemon for your team.'),
  pokemon_2: Yup.string().required('Select a pokemon for your team.'),
  pokemon_3: Yup.string().required('Select a pokemon for your team.'),
});

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

  validationSchema: battleCreateFormSchema,

  handleSubmit: (values, { props }) => {
    props.submitHandler(values);
  },
})(BattleCreateInnerForm);

class BattleCreate extends React.Component {
  componentDidMount() {
    const { fetchListUser, fetchListPokemon } = this.props;
    fetchListUser();
    fetchListPokemon();
  }

  render() {
    const {
      denormalizedUsers, denormalizedPokemons, submitStatus, postCreateBattle,
    } = this.props;

    if (isEmpty(denormalizedUsers) || isEmpty(denormalizedPokemons)) return null;

    // Redirect after form submit
    if (submitStatus === STATUS_201) {
      return <Redirect to={Urls['battles:list_battle']()} />;
    }

    return (
      <BattleCreateForm
        denormalizedUsers={denormalizedUsers}
        denormalizedPokemons={denormalizedPokemons}
        submitHandler={postCreateBattle}
      />
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
  setFieldValue: PropTypes.func.isRequired,
};

BattleCreateInnerForm.defaultProps = {
  denormalizedUsers: [],
  denormalizedPokemons: [],
};

BattleCreateForm.propTypes = {
  submitHandler: PropTypes.func.isRequired,
};

BattleCreate.propTypes = {
  fetchListUser: PropTypes.func.isRequired,
  fetchListPokemon: PropTypes.func.isRequired,
  postCreateBattle: PropTypes.func.isRequired,
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
