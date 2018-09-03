import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class NaiveNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()    # self.board_x is the number of variables
                                                            # self.board_y is the size of the embedding
        self.action_size = game.getActionSize()
        self.args = args

        super(NaiveNNet, self).__init__()

        if torch.cuda.is_available():




            self.fc1 = nn.Linear(self.board_y, 64).cuda()


            self.fc2 = nn.Linear(64, 256).cuda()

            self.fc3 = nn.Linear(256, 32).cuda()

            self.fc4 = nn.Linear(32, 2).cuda()

            self.fc5 = nn.Linear(32, 1).cuda()

        else:


            self.fc1 = nn.Linear(self.board_y, 64)


            self.fc2 = nn.Linear(64, 256)

            self.fc3 = nn.Linear(256, 32)

            self.fc4 = nn.Linear(32, 2)

            self.fc5 = nn.Linear(32, 1)


        torch.nn.init.xavier_uniform(self.fc1.weight)
        torch.nn.init.xavier_uniform(self.fc2.weight)
        torch.nn.init.xavier_uniform(self.fc3.weight)
        torch.nn.init.xavier_uniform(self.fc4.weight)
        torch.nn.init.xavier_uniform(self.fc5.weight)


    def forward(self, s):

        s = s.view(-1, self.board_x, self.board_y)



        s = F.relu(self.fc1(s))

        s = F.relu(self.fc2(s))

        s = self.fc3(s)

        pi = self.fc4(s)

        pi = pi.view(-1, self.action_size)

        v = self.fc5(s)

        v = v.view(-1, self.board_x)

        v = v.mean(1)

        return F.log_softmax(pi, dim=1), F.tanh(v)
