from libraries import *
from logger import setup_logger
from CVAE_model import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer
#from CVAE_model_noGuideEmbedding import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn

#from CVAE_model_2 import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer
#from CVAE_multilableClas_model_2 import *
#from DenoisingAE_model import *


from Training import train_model_CVAE, train_model_multilab, evaluate_model_CVAE, evaluate_model_CVAE_multilab

import torch
from torch.utils.data import Dataset, DataLoader

import bisect
from itertools import accumulate
import argparse

import sys
import os
import logger

import torch.nn as nn

import torch
from torch import optim

import click

import statsmodels.api as sm

@click.command()
# save and directory options
@click.option('--trainfile', 
              type=click.STRING, 
              default="./Notebooks/CombinatorialPerturbations/dataset/adataTR.h5ad",
              help='input training h5ad file')

# model parameters
@click.option("--n_cond_in",
              type=click.INT,
              default=6,
              help="number of conditions")
@click.option("--n_inputs",
              type=click.INT,
              default=1041,
              help="number of response genes")
@click.option("--n_cond",
              type=click.INT,
              default=64,
              help="number of latents for the condition embeddings")
@click.option("--n_latents",
              type=click.INT,
              default=64,
              help="number of latents for the gene embeddings")
@click.option("--model_type",
              type=click.STRING,
              default="CVAE",
              help="model type")


@click.option('--save_dir',
              type=click.STRING, 
              default='./Notebooks/CombinatorialPerturbations/outputs')

@click.option('--model_dir',
              type=click.STRING, 
              default='modelNoName')

@click.option("--batch_size",
              type=click.INT,
              default=1000,
              help="batch size")
@click.option("--num_workers",
              type=click.INT,
              default=60,
              help="number of workers")

@click.option("--project_dir",
              type=click.STRING,
              default="/home/eraslab1/Projects/E3Ligase/analysisSingle",
              help="Project directory")


def computeReconstSinglesFC(trainfile, model_type, n_inputs, n_latents, n_cond, n_cond_in, save_dir, model_dir, batch_size, num_workers, project_dir):
    
    os.getcwd()
    os.chdir(project_dir)

    observedDat = sc.read(trainfile)
    
    if model_type == "CVAE":   
        net = VAE(n_inputs=n_inputs,
                  n_latents=n_latents,
                  n_cond=n_cond,
                  n_cond_in=n_cond_in)
    elif model_type == "CVAE_multiLab":
        net = MultiLabClassVAE(n_inputs=n_inputs,
                      n_latents=n_latents,
                      n_cond=n_cond,
                      n_cond_in=n_cond_in)
    elif model_type == "DenoisingAE_model":
        net = DenoisingAE(n_inputs=n_inputs,
                      n_latents=n_latents,
                      n_cond=n_cond,
                      n_cond_in=n_cond_in)
        
    net.load_state_dict(torch.load(os.path.join(save_dir,model_dir,"best.pth"))['state_dict'])
    
    
    dataset = E3ScreenDataset(trainfile)
    dataloader = DataLoader(dataset,
                            batch_size=batch_size,
                            drop_last=False,
                            shuffle=False,
                            num_workers=num_workers)
    
    
    total_generated_samples = []

    for sample in dataloader:
        with torch.no_grad():
            input = sample['y'].cuda() if next(net.parameters()).is_cuda else sample['y']
            condition = sample['X'].cuda() if next(net.parameters()).is_cuda else sample['X']
            embeddings = net.inference(input, condition)
            generated_samples = net.generate(embeddings, condition)

        total_generated_samples.append(generated_samples)

    total_generated_samples = torch.cat(total_generated_samples, 0)
    total_generated_samples = total_generated_samples.cpu().numpy()
    
    
    reconsExpressionMatrix = pd.DataFrame(total_generated_samples)
    reconsExpressionMatrix.columns = observedDat.var_names
    reconsExpressionMatrix.index = observedDat.obs.index
    
    
    guideMatrix = observedDat.obs[["K_0", "K_1", "K_2", "K_3", "K_4", "K_5"]]
    guideMatrix.loc[:,"intercept"] = 1
           
    pvalDF = pd.DataFrame()
    coefDF = pd.DataFrame()
   
    for i in range(0,1041,1):
        est = sm.OLS(np.array(reconsExpressionMatrix)[:,i], guideMatrix)
        est2 = est.fit().summary2().tables[1]
        pvalDF[str(i)] = est2['P>|t|']
        coefDF[str(i)] = est2['Coef.']
 
        
    coefDF.columns = reconsExpressionMatrix.columns
    pvalDF.columns = reconsExpressionMatrix.columns

    coefDF.index = guideMatrix.columns
    pvalDF.index = guideMatrix.columns

    
    pvalDF.to_csv(os.path.join(save_dir,model_dir,"ReconstFC_Pval.csv"))   
    coefDF.to_csv(os.path.join(save_dir,model_dir,"ReconstFC_Coef.csv"))   
   

 
if __name__ == '__main__':
    computeReconstSinglesFC()