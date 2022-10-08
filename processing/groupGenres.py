import sys
import pandas as pd
from utils.utils import group_bool_columns

def main():
    arg = sys.argv[1]

    data = pd.read_csv(arg)

    new_genre_column = 'Genres'
    genre_columns = ['GenreIsNonGame', 'GenreIsIndie', 'GenreIsAction', 'GenreIsAdventure', 'GenreIsCasual', 'GenreIsStrategy', 'GenreIsRPG', 'GenreIsSimulation', 'GenreIsEarlyAccess', 'GenreIsFreeToPlay', 'GenreIsSports', 'GenreIsRacing', 'GenreIsMassivelyMultiplayer']
    group_bool_columns(data, genre_columns, new_genre_column, 7)

    data.to_csv(arg, index=False)
