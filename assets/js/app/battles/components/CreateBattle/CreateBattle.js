import React from 'react';
import { withFormik, Form, Field } from 'formik';

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

  handleSubmit: (values) => {
    console.log(values);
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

export default BattleCreate(BattleCreateForm);
