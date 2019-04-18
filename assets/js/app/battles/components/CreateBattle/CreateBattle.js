import React from 'react';
import { connect } from 'react-redux';
import { withFormik, Form, Field } from 'formik';
import actions from 'actions';
// import apiPostWrapper from 'utils/api';

const BattleCreate = withFormik({
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
    // apiPostWrapper.post('/api/create_battle', values)
    //   .then(response => response.data)
    //   .catch(error => new Error(error));
  },
});

const BattleCreateForm = () => (
  <Form>
    <p>
      Opponent:
      <Field type="email" name="trainer_opponent" />
    </p>
    <p>
      Pokemon:
      <Field type="text" name="pokemon_1" />
      Round:
      <Field component="select" name="order_1">
        <option value="0">First</option>
        <option value="1">Second</option>
        <option value="2">Third</option>
      </Field>
    </p>
    <p>
      Pokemon:
      <Field type="text" name="pokemon_2" />
      Round:
      <Field component="select" name="order_2">
        <option value="0">First</option>
        <option value="1">Second</option>
        <option value="2">Third</option>
      </Field>
    </p>
    <p>
      Pokemon:
      <Field type="text" name="pokemon_3" />
      Round:
      <Field component="select" name="order_3">
        <option value="0">First</option>
        <option value="1">Second</option>
        <option value="2">Third</option>
      </Field>
    </p>

    <Field type="submit" value="Challenge now" />
  </Form>
);

const mapStateToProps = state => ({
  // to add: get users and pokemons
  test: state.battle,
});

const mapDispatchToProps = dispatch => ({
  postCreateBattle: battle => dispatch(actions.postCreateBattle(battle)),
});

// export default BattleCreate(BattleCreateForm);
export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate(BattleCreateForm));
