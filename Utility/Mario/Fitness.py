from .SummervilleAgent import percent_completable
from Utility.GridTools import columns_into_rows

def summerville_helper(columns, start_position):
    '''
    This uses an A* agent to tell if a level is playable. It should be pretty
    close to perfect.
    '''
    return percent_completable(10, start_position, (columns))

def percent_playable(columns):
    length = len('X-------------')
    columns.insert(0, 'X-------------')
    columns.insert(0, 'X-------------')
    columns.append('X-------------')
    columns.append('X-------------')

    fitness = summerville_helper(columns_into_rows(columns), (1, length - 2, -1))

    columns.pop(0)
    columns.pop(0)
    columns.pop()
    columns.pop()

    return fitness

def summerville_fitness(grammar):
    def slow_fitness(columns):
        bad_transitions = grammar.count_bad_n_grams(columns)
        return bad_transitions + 1 - percent_playable(columns)
    return slow_fitness