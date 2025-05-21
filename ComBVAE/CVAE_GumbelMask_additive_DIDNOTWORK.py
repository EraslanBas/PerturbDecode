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
        self.covariates = self.data.uns["covariates"]
        print(self.covariates)
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
    

    
class VAE(nn.Module):

    def __init__(self, n_inputs, n_latents, n_cond, n_cond_in):
        super().__init__()

        self.n_inputs = n_inputs
        self.n_latents = n_latents
        self.n_cond = n_cond

        self.encoder = Encoder(n_inputs=n_inputs, n_latents=n_latents, n_cond=n_cond)
        self.decoder = Decoder(n_inputs=n_inputs, n_latents=n_latents, n_cond=n_cond)
        self.embedding = EmbeddingLayer(n_in=n_cond_in, n_out=n_cond)

    def forward(self, x, c):

        c = self.embedding(c)

        means, log_var = self.encoder(x, c)
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        z = eps * std + means

        recon_x = self.decoder(z, c)

        return recon_x, x, means, log_var, c

    def inference(self, x, c):
        c = self.embedding(c)
        means, _ = self.encoder(x, c)
        return means

    def generate(self, z, c):
        c = self.embedding(c)
        recon_x = self.decoder(z, c)
        return recon_x

    def get_embedding(self, c):
        return self.embedding(c)


    
class Encoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.encoder = nn.Sequential(nn.Linear(n_inputs, 512),
                                     nn.BatchNorm1d(512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, 512),
                                    )

        self.linear_means = nn.Linear(512, n_latents)
        self.linear_log_var = nn.Linear(512, n_latents)

    def forward(self, x, c):
        
        x = self.encoder(x)
        means = self.linear_means(x)
        logvar = self.linear_log_var(x)
        return means, logvar

    
class Decoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.decoder = nn.Sequential(nn.Linear(n_latents, 512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, n_inputs),
                                    )

    def forward(self, z, c):
        x = (z+c)
        x = self.decoder(x)
        return x

        
def get_loss_fn(alpha, beta):

    def vae_loss_fn(recon_x, x, mean, log_var, c):
        BCE = torch.nn.functional.mse_loss(
            recon_x, x, reduction='sum')
        KLD = -0.5 * torch.sum(1 + log_var - mean.pow(2) - log_var.exp())
        
        l1Loss = torch.sum(torch.abs(c))

        return (BCE + alpha*KLD)/x.size(0), BCE, KLD, l1Loss

    return vae_loss_fn


class EmbeddingLayer(nn.Module):
    def __init__(self, n_in, n_out):
        super(EmbeddingLayer, self).__init__()
        self.embedding_layer = nn.Sequential(nn.Linear(n_in, n_out),
                                             nn.BatchNorm1d(n_out),
                                             nn.ReLU(inplace=True))
        self.mysoftmax = nn.Softmax(dim=-1)
        
    def gumbel_sigmoid(self, embeds, tau=0.5, hard=False):
        gumbels = -torch.log(-torch.log(torch.rand_like(embeds) + 1e-20) + 1e-20)
        y = embeds + gumbels
        #y_soft = self.mysoftmax(y / tau)
        y_soft = torch.sigmoid(y / tau)

        #y_soft = F.sigmoid(y / tau)
        if hard:
            return (y_soft == y_soft.max(dim=-1, keepdim=True)[0]).float()
        else:
            return y_soft


    def forward(self, x):
        y_emb = self.embedding_layer(x)
        y_emb_gumbel = self.gumbel_sigmoid(y_emb, hard=False)
        return y_emb_gumbel

