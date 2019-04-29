import React from 'react';
import { Redirect } from 'react-router-dom';
import { SortableContainer, SortableElement } from 'react-sortable-hoc';
import arrayMove from 'array-move';
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


// Styled
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
  flex-wrap: wrap;
  width: 100%;
  margin: 30px auto;
  cursor: pointer;

  .css-1pcexqc-container {
    width: 70%;
  }
`;

const ErrorMessageDivStyled = styled.div`
  color: red;
`;


// Components
const BattleCreateInnerForm = (props) => {
  const {
    denormalizedUsers, denormalizedPokemons,
    values, setFieldValue, errors,
  } = props;

  const handlePokemonChange = (newPokemon, index) => {
    const pokemonList = values.pokemons;
    pokemonList[index] = newPokemon;
    setFieldValue('pokemons', pokemonList);
  };

  const onSortEnd = ({ oldIndex, newIndex }) => {
    const newPokemons = arrayMove(values.pokemons, oldIndex, newIndex);
    setFieldValue('pokemons', newPokemons);
  };

  const CustomOption = option => (
    <div ref={option.innerRef} {...option.innerProps} {...option}>
      <img src={option.data.sprite} alt="pokemon" />
      <span>{option.data.name}</span>
    </div>
  );

  const SortableItem = SortableElement(({ selectedPokemon, onPokemonChange }) => (
    <CreateBattleRowStyled>
      <Select
        placeholder="Search pokemon..."
        components={{ Option: CustomOption }}
        options={denormalizedPokemons}
        value={selectedPokemon}
        onChange={onPokemonChange}
      />
    </CreateBattleRowStyled>
  ));

  const SortableList = SortableContainer(({ items, onPokemonChange }) => (
    <div>
      {items.map((pokemon, index) => (
        <SortableItem
          // index required by SortableElement HOC
          // eslint-disable-next-line react/no-array-index-key
          key={`item-${index}`}
          index={index}
          selectedPokemon={pokemon}
          onPokemonChange={newPokemon => onPokemonChange(newPokemon, index)}
        />
      ))}
    </div>
  ));

  return (
    <CreateBattleContainerStyled>
      <h2>Select your opponent and your team to battle!</h2>

      <Form>
        <CreateBattleRowStyled>
          Opponent:
          <Field component="select" name="trainer_opponent">
            <option value="" disabled>Select an opponent</option>
            {denormalizedUsers.map(user => (
              <option value={{ user }.user.id}>{{ user }.user.email}</option>
            ))}
          </Field>
          <ErrorMessage
            name="trainer_opponent"
            render={msg => <ErrorMessageDivStyled>{msg}</ErrorMessageDivStyled>}
          />
        </CreateBattleRowStyled>

        Pokemons:
        <SortableList
          distance={10}
          transitionDuration={200}
          items={values.pokemons}
          onSortEnd={onSortEnd}
          onPokemonChange={(newPokemon, index) => handlePokemonChange(newPokemon, index)}
        />
        <ErrorMessage
          name="pokemons"
          render={msg => <ErrorMessageDivStyled>{msg}</ErrorMessageDivStyled>}
        />
        {errors.pokemons
          ? <ErrorMessageDivStyled>{errors.pokemons}</ErrorMessageDivStyled>
          : null
        }

        <Field type="submit" value="Challenge now" />
      </Form>
    </CreateBattleContainerStyled>
  );
};

const battleCreateFormSchema = Yup.object().shape({
  trainer_opponent: Yup.number().required('Select an opponent to challenge.'),
  pokemons: Yup.array().of(
    Yup.object().shape({
      api_id: Yup.number()
        .positive()
        .integer(),
      attack: Yup.number()
        .positive()
        .integer(),
      defense: Yup.number()
        .positive()
        .integer(),
      hitpoints: Yup.number()
        .positive()
        .integer(),
      id: Yup.number()
        .positive()
        .integer(),
      label: Yup.string(),
      name: Yup.string(),
      sprite: Yup.string().url(),
      value: Yup.number()
        .positive()
        .integer(),
    }).nullable().required('Select a pokemon for your team.'),
  ).required(''),
});

const BattleCreateForm = withFormik({
  mapPropsToValues: () => ({
    trainer_opponent: '',
    pokemons: [null, null, null],
  }),

  validationSchema: battleCreateFormSchema,

  validate: (values) => {
    const { pokemons } = values;
    const errors = {};
    if (pokemons.length === 3) {
      let sum = 0;
      pokemons.map((p) => {
        sum += p.attack;
        sum += p.defense;
        sum += p.hitpoints;
        return sum;
      });
      if (sum > 600) {
        errors.pokemons = 'Trainer, your pokemon team stats can not sum more than 600 points.';
      }
    }
    return errors;
  },

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
  values: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  setFieldValue: PropTypes.func.isRequired,
  errors: PropTypes.oneOfType([
    PropTypes.object,
  ]).isRequired,
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
