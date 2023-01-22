from libraries import *

import torch
from torch.utils.data import Dataset, DataLoader

import bisect
from itertools import accumulate
import argparse

import sys
import os

import torch.nn as nn

import torch
from torch import optim


class ScreenDataset(Dataset):
    def __init__(self, h5adfile):
        self.data = sc.read(h5adfile)
        self.covariates = adata.uns["covariates"]
        self.X = self.data.obs[ self.covariates ].to_numpy()
        self.y = self.data.X


    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        #y = self.data.X[idx:idx+1]
        y = self.y[idx]
        X = self.X[idx]
        return {'y': torch.from_numpy(y).float(), 'X': torch.from_numpy(X).float()}
    
    
    def get_genes(self):
        """ Return list of genes """
        return list(self.data.var_names)

    def get_targets(self):
        """ Return list of ko targets """
        return list(self.covariates)  
    

    
class MultiLabClassDenoisingAE(nn.Module):

    def __init__(self, n_inputs, n_latents, n_cond, n_cond_in):
        super().__init__()

        self.n_inputs = n_inputs
        self.n_latents = n_latents
        self.n_cond = n_cond

        self.encoder = Encoder(n_inputs=n_inputs, n_latents=n_latents, n_cond=n_cond)
        self.decoder = Decoder(n_inputs=n_inputs, n_latents=n_latents, n_cond=n_cond)
        self.embedding = EmbeddingLayer(n_in=n_cond_in, n_out=n_cond)
        self.multilab = MultilabClass(n_inputs = n_inputs, n_cond_in = n_cond_in)

    def forward(self, x, c):

        c_embed = self.embedding(c)
        
        noisy_x = addNoise(x)

        z = self.encoder(noisy_x, c_embed)

        recon_x = self.decoder(z, c_embed)
        
        predClass = self.multilab(recon_x)

        return recon_x, x, means, c_embed, predClass, c

    def inference(self, x, c):
        c = self.embedding(c)
        means = self.encoder(x, c)
        return means

    def generate(self, z, c):
        c = self.embedding(c)
        recon_x = self.decoder(z, c)
        return recon_x

    def get_embedding(self, c):
        return self.embedding(c)


class MultilabClass(nn.Module):
    def __init__(self, n_inputs, n_cond_in):
        super().__init__()

        self.mlab = nn.Sequential(nn.Linear(n_inputs, 512),
                                     nn.BatchNorm1d(512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, n_cond_in),
                                )

    def forward(self, x):       
        predClass = self.mlab(x)
        return predClass
    
class Encoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.encoder = nn.Sequential(nn.Linear(n_inputs+n_cond, 512),
                                     nn.BatchNorm1d(512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, 512),
                                    )

        self.linear_means = nn.Linear(512, n_latents)
        
    def forward(self, x, c):
        
        x = torch.cat((x, c), dim=1)
        x = self.encoder(x)
        means = self.linear_means(x)
       
        return means

    
class Decoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.decoder = nn.Sequential(nn.Linear(n_latents + n_cond, 512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, n_inputs),
                                    )

    def forward(self, z, c):
        x = torch.cat((z, c), dim=1)
        x = self.decoder(x)
        return x


def addNoise(x): 
    normal = torch.distributions.Normal(0, 1)
    
    return x + normal.sample(sample_shape=torch.Size(x.shape))

        
def get_loss_fn(alpha, beta, theta):
    
    def multiLabDenosingAE_loss_fn(recon_x, x, means, c_embed, predClass, c):
        
        BCE = torch.nn.functional.mse_loss(
            recon_x, x, reduction='sum')
     
        
        myMLC = torch.nn.BCEWithLogitsLoss(reduction='sum')
        classLoss = theta*myMLC(predClass, c)

        return (BCE + classLoss)/x.size(0), BCE, classLoss

    return multiLabDenosingAE_loss_fn


class EmbeddingLayer(nn.Module):
    def __init__(self, n_in, n_out):
        super(EmbeddingLayer, self).__init__()
        self.embedding_layer = nn.Sequential(nn.Linear(n_in, n_out))

    def forward(self, x):
        return self.embedding_layer(x)
