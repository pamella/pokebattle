from django.conf.urls import url

from pokemons.endpoints import ListPokemonEndpoint


app_name = 'pokemons'

urlpatterns = [
    url(r'^pokemons/$', ListPokemonEndpoint.as_view(), name='list_pokemon_endpoint'),

]
