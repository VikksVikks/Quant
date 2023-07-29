# import ExoticOption
import numpy as np

from Control_Engine import ControlEngine
from Options import AsianOption, PayoffCall, BarrierDownOut, BarrierDownIn, PayoffPut
from Path_Generator import PathGenerator

# Constants and Run Dicts
S = 100
vol = 0.1
r = 0.05
d = 0.03
K = 103
T = 1
Barrier = 80

Asian_Dict = {'Task1': {'option': AsianOption, 'payoff': PayoffCall, 'freq': 12},
              'Task2': {'option': AsianOption, 'payoff': PayoffCall, 'freq': 4},
              'Task3': {'option': AsianOption, 'payoff': PayoffCall, 'freq': 52}
              }

Barrier_Dict = {'Task1': {'option': BarrierDownOut, 'payoff': PayoffCall, 'barrier': 80, 'freq': 12},
                'Task2': {'option': BarrierDownIn, 'payoff': PayoffCall, 'barrier': 80, 'freq': 12},
                'Task3': {'option': BarrierDownOut, 'payoff': PayoffPut, 'barrier': 80, 'freq': 12},
                'Task4': {'option': BarrierDownOut, 'payoff': PayoffPut, 'barrier': 120,
                          'freq': [0.05, 0.15, 0.25, 0.35, 0.45, 0.55,
                                   0.65, 0.75, 0.85, 0.95, 1]}
                }


def Main_Run(args):
    number_sims = 1000
    if ('sims' in args):
        number_sims = args['sims']

    # Run Asian:
    asian_results_dict = {}
    if ('Asian' in args):

        for task, params in Asian_Dict.items():
            option_class = params['option']
            payoff_class = params['payoff']
            freq = params['freq']
            times = get_times(freq)

            payoff = payoff_class(K)
            option = option_class(T, K, payoff)
            _generator = PathGenerator(S, r, d, vol, times)
            engine = ControlEngine(vol, d, r, S, option, _generator)  # vol, d, r, spot, product, generator
            engine.run_simulation(number_sims)
            asian_results_dict[task] = (engine.option_price, engine.cum_avg_list, engine.sqrt_err)

    # Run Barrier Sim:
    barrier_results_dict = {}
    if ('Barrier' in args):
        for task, params in Barrier_Dict.items():
            option_class = params['option']
            payoff_class = params['payoff']
            freq = params['freq']

            if isinstance(freq, list):
                times = np.array(freq)
            else:
                times = get_times(freq)
            payoff = payoff_class(K)
            option = option_class(T, K, Barrier, payoff)
            _generator = PathGenerator(S, r, d, vol, times)
            engine = ControlEngine(vol, d, r, S, option, _generator)  # vol, d, r, spot, product, generator
            engine.run_simulation(number_sims)
            barrier_results_dict[task] = (engine.option_price, engine.cum_avg_list, engine.sqrt_err)

    # display results:
    for key, val in asian_results_dict.items():
        print('Asian Task Results:')
        print(f'{key} Option Price {val[0]} and Error {val[2]}')

    for key, val in barrier_results_dict.items():
        print('Barrier Task Results:')
        print(f'{key} Option Price {val[0]} and Error {val[2]}')
    print('done')


def get_times(freq):
    times = np.zeros(freq)

    for i in range(len(times)):
        times[i] = (i + 1) * 1 / freq
    return times


# Run Code
Main_Run({'Asian': 1, 'Barrier': 1, 'sims': 10000})
