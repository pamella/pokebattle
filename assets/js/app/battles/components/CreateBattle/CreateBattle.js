import React from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { withFormik, Form, Field } from 'formik';
import actions from 'actions/battle';
import Urls from 'utils/urls';
import { STATUS_201 } from '../../../../constants/request_status';


const CreateBattleContainerStyled = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
`;

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
  },
});

const BattleCreateForm = (props) => {
  const { submitStatus } = props;
  if (submitStatus === STATUS_201) {
    return <Redirect to={Urls['battles:list_battle']()} />;
  }

  return (
    <CreateBattleContainerStyled>
      <h2>Select your opponent and your team to battle!</h2>

      <Form>
        <p>
          Opponent:
          <Field type="text" name="trainer_opponent" />
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
    </CreateBattleContainerStyled>
  );
};

BattleCreateForm.propTypes = {
  submitStatus: PropTypes.number,
};

BattleCreateForm.defaultProps = {
  submitStatus: 0,
};

const mapStateToProps = state => ({
  // to add: get users and pokemons
  submitStatus: state.battle.payload,
});

const mapDispatchToProps = dispatch => ({
  postCreateBattle: battle => dispatch(actions.postCreateBattle(battle)),
});


export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate(BattleCreateForm));
