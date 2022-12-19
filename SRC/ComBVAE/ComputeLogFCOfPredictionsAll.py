from libraries import *
from logger import setup_logger
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
from os.path import exists

@click.command()

@click.option('--trainfile', 
              type=click.STRING, 
              default="./Notebooks/CombinatorialPerturbations/dataset/adataTR.h5ad",
              help='input training h5ad file')


# save and directory options
@click.option('--save_dir',
              type=click.STRING, 
              default='./Notebooks/CombinatorialPerturbations/outputs/K_singles')

@click.option('--model_dir',
              type=click.STRING, 
              default='modelNoName')

@click.option("--project_dir",
              type=click.STRING,
              default="/home/eraslab1/Projects/E3Ligase/analysisSingle",
              help="Project directory")


def ComputeLFCOfGenerated(trainfile, save_dir, model_dir, project_dir):
    os.getcwd()
    os.chdir(project_dir)
    
    observedDat = sc.read(trainfile)
    num_conditions = 6
    
    target_conditions_dict = {}
    for i in range(num_conditions):
        for j in range(i, num_conditions):
            condition = torch.zeros(num_conditions)
            condition[i] = 1
            if j == i:
                name = f'perturb_K{i}'
            else:
                name = f'perturb_K{i}_K{j}'
                condition[j] = 1
            target_conditions_dict[name] = condition

    ctrl_condition = torch.zeros(num_conditions)
    target_conditions_dict['perturb_ctrl'] = ctrl_condition
    
    
    expressionMatrix = np.load(os.path.join(save_dir, model_dir, 'generated_samples/perturb_ctrl_best.npy'), allow_pickle=True)



    guideMatrix = pd.DataFrame(np.zeros((220000, 22)))
    guideMatrix.columns = target_conditions_dict.keys()
    guideMatrix.loc[0:9999,"perturb_ctrl"] = 1
    i=10000

    for name, target_condition in target_conditions_dict.items():
        if name != "perturb_ctrl":
            print(name)
            pertCells = np.load(os.path.join(save_dir, model_dir, "generated_samples", name+"_best.npy"), allow_pickle=True)
            expressionMatrix = np.concatenate((expressionMatrix, pertCells))
            guideMatrix.loc[i:(i+9999),name] = 1
            i = i+10000
            print(expressionMatrix.shape)

    
    guideMatrix = guideMatrix.drop(['perturb_ctrl'], axis=1)
    guideMatrix.loc[:,"intercept"] = 1
                                
                                
    pvalDF = pd.DataFrame()
    coefDF = pd.DataFrame()
   
    for i in range(0,1041,1):
        print(i)
        est = sm.OLS(np.array(expressionMatrix)[:,i], guideMatrix)
        est2 = est.fit().summary2().tables[1]
        pvalDF[str(i)] = est2['P>|t|']
        coefDF[str(i)] = est2['Coef.']
 
        
    coefDF.columns = observedDat.var_names
    pvalDF.columns = observedDat.var_names

    coefDF.index = guideMatrix.columns
    pvalDF.index = guideMatrix.columns

    
    pvalDF.to_csv(os.path.join(save_dir,model_dir,"PredictedFC_Pval.csv"))   
    coefDF.to_csv(os.path.join(save_dir,model_dir,"PredictedFC_Coef.csv"))   
   

if __name__ == '__main__':
    ComputeLFCOfGenerated()