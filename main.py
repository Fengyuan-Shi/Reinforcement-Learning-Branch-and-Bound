from Coach import Coach
from othello.OthelloGame import OthelloGame as Game
from BBNNet import NNetWrapper as nn
from utils import *
from pyibex import *
from BB import BB

args = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    f = Function("x", "y", "x*exp(sin(x-y))")
    #Define the input domain of the function
    input_box = IntervalVector(2, [0.5,5])
    #Define the output range (i.e. desired value of the function)
    output_range = Interval(1,1)

    g = BB(f, input_box, output_range,10)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
