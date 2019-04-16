import { schema } from 'normalizr';

const pokemon = new schema.Entity('pokemons');
const round = new schema.Entity('rounds', {
  creator_pokemon: [pokemon],
  opponent_pokemon: [pokemon],
});
const battle = new schema.Entity('battles', {
  rounds: {
    0: [round],
    1: [round],
    2: [round],
  },
});
const listBattles = [battle];

export default {
  battle,
  listBattles,
};
