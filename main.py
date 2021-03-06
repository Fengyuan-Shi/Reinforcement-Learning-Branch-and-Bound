from Coach import Coach
from ActorCritic.ActorCritic import ActorCritic
from naive.BB import BB
from naive.pytorch.NNet import NNetWrapper as nn
from utils import *
from pyibex import *
from generateFunctions import generateFunctions
from GFwithMonomial import GFwithMonomial as GF

args = dotdict({
    'numIters': 20,
    'numEps': 20,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './ckpsss/',
    'load_model': False,
    'load_folder_file': ('./ckpsss','best.pth.tar'),
    'numItersForTrainExamplesHistory': 1,

})

if __name__=="__main__":
    #
    #100 * sqrt(abs(y-0.01*x^2)) + 0.01 * abs(x+10)
    #((sin(x^2-y^2))^2-0.5)/(1+0.001*(x^2+y^2))^2
    #-20 * exp(-0.2*sqrt(0.5*(x^2+y^2)))-exp(0.5*(cos(2*3.1415926535*x)+cos(2*3.1415926535*y)))+2.71828+20"

    i = 0

    generator = GF(["x1","x2"],[3,3],-5,5,20)
    generator.randomPara()
    function = generator.generateString(generator.coe, generator.degree_matrix)
    f = Function("x1","x2", function)
    #f = Function("x", "y", "-20 * exp(-0.2*sqrt(0.5*(x^2+y^2)))-exp(0.5*(cos(2*3.1415926535*x)+cos(2*3.1415926535*y)))+2.71828+20")
    #Define the input domain of the function -- both[0.5,5] for x and y
    input_box = IntervalVector(2,[-5,5])
    #Define the output range (i.e. desired value of the function) -- f range [1,1]
    output_range = Interval(-999,999)

    g = BB(f, input_box, output_range, generator.generateFunc)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args, i)

    i+= 1

    c.learn()

    while True:
        generator = GF(["x1","x2"],[3,3],-5,5,20)
        generator.randomPara()
        function = generator.generateString(generator.coe, generator.degree_matrix)
        f = Function("x1","x2", function)
        #f = Function("x", "y", "-20 * exp(-0.2*sqrt(0.5*(x^2+y^2)))-exp(0.5*(cos(2*3.1415926535*x)+cos(2*3.1415926535*y)))+2.71828+20")
        #Define the input domain of the function -- both[0.5,5] for x and y
        input_box = IntervalVector(2,[-5,5])
        #Define the output range (i.e. desired value of the function) -- f range [1,1]
        output_range = Interval(-999,999)

        g = BB(f, input_box, output_range, generator.generateFunc)
        nnet = nn(g)


        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

        c = Coach(g, nnet, args, i)

        i += 1

        c.learn()
