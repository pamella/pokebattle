import React from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { withFormik, Form, Field } from 'formik';
import { isEmpty } from 'lodash';
import { denormalize } from 'normalizr';
import schemas from 'utils/schema';
import battleActions from 'actions/battle';
import userActions from 'actions/user';
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

class BattleCreateForm extends React.Component {
  componentDidMount() {
    const { fetchListUser } = this.props;
    fetchListUser();
  }

  render() {
    const { denormalizedUsers } = this.props;
    if (isEmpty(denormalizedUsers)) return null;

    // Redirect after form submit
    const { submitStatus } = this.props;
    if (submitStatus === STATUS_201) {
      return <Redirect to={Urls['battles:list_battle']()} />;
    }
    console.log('props ', this.props);

    return (
      <CreateBattleContainerStyled>
        <h2>Select your opponent and your team to battle!</h2>

        <Form>
          <p>
            Opponent:
            <Field component="select" name="trainer_opponent">
              {denormalizedUsers.map(user => (
                <option value={{ user }.user.id}>{{ user }.user.email}</option>
              ))}
            </Field>
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
  }
}

BattleCreateForm.propTypes = {
  fetchListUser: PropTypes.func.isRequired,
  denormalizedUsers: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  submitStatus: PropTypes.number,
};

BattleCreateForm.defaultProps = {
  submitStatus: 0,
};

const mapStateToProps = (state) => {
  // to add: load pokemons
  const { battle, user } = state;
  const submitStatus = battle.payload;

  if (isEmpty(user)) return null;
  const denormalizedUsers = denormalize(
    user.payload.result, schemas.listUsers, user.payload.entities,
  );

  return {
    submitStatus,
    denormalizedUsers,
  };
};

const mapDispatchToProps = dispatch => ({
  fetchListUser: () => dispatch(userActions.fetchListUser()),
  postCreateBattle: battle => dispatch(battleActions.postCreateBattle(battle)),
});


export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate(BattleCreateForm));
