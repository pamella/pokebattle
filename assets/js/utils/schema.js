import { schema } from 'normalizr';

const pokemon = new schema.Entity('pokemon');
const battle = new schema.Entity('battle');

export default {
  pokemon,
  battle,
};
