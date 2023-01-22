from libraries import *
from logger import setup_logger
from CVAE_model import ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer
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

@click.command()
# save and directory options


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

@click.option('--save_dir',
              type=click.STRING, 
              default='./Notebooks/CombinatorialPerturbations/outputs/K_singles')

@click.option('--model_dir',
              type=click.STRING, 
              default='modelNoName')


@click.option("--model_type",
              type=click.STRING,
              default="CVAE",
              help="model type")
@click.option("--controlfile", 
              type=click.STRING, 
              default="./Notebooks/CombinatorialPerturbations/dataset/adataTestControl.h5ad",
              help="test control cells h5ad file")


@click.option("--batch_size",
              type=click.INT,
              default=1000,
              help="batch size")
@click.option("--num_workers",
              type=click.INT,
              default=80,
              help="number of workers")

@click.option("--project_dir",
              type=click.STRING,
              default="/home/eraslab1/Projects/E3Ligase/analysisSingle",
              help="Project directory")

@click.option("--use_gpu",
              type=click.BOOL,
              default=False,
              help="gpu usage")


def GenerateCells(n_cond_in, n_inputs, n_cond, n_latents, save_dir, model_dir, model_type, controlfile, batch_size, num_workers, project_dir, use_gpu):
    os.getcwd()
    os.chdir(project_dir)
    
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
        
    net.load_state_dict(torch.load(os.path.join(save_dir,model_dir,"best.pth"))['state_dict'])
    
    
    dataset = ScreenDataset(controlfile)
    dataloader = DataLoader(dataset, 
                            batch_size=batch_size,
                            drop_last=False,
                            shuffle=False,
                            num_workers=num_workers)
    
    num_conditions = len(dataset.get_targets())
    
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
    
    os.makedirs(os.path.join(save_dir, model_dir, 'generated_samples'), exist_ok=True)
    
    for name, target_condition in target_conditions_dict.items():
        # if use_gpu:
        #     target_condition = target_condition.cuda()

        fPath = Path(os.path.join(save_dir, model_dir, 'generated_samples', name+'_best.npy'))

        if(fPath.is_file()):
            print(fPath)
        else:
            print(target_condition)
            generated_samples = generate_targeted_samples(dataloader, net, target_condition)
            sfile = os.path.join(save_dir, model_dir, 'generated_samples', name+'_best.npy')
            np.save(sfile, generated_samples)



    
    
def generate_targeted_samples(testloader, model, target_condition):
    model.eval()
    print(target_condition)
    total_generated_samples = []

    # for sample in testloader:
    #     with torch.no_grad():
    #         #input = sample['y'].cuda() if next(model.parameters()).is_cuda else sample['y']
    #         #condition = sample['X'].cuda() if next(model.parameters()).is_cuda else sample['X']
    #         input = sample['y']
    #         condition = sample['X']
    #         embeddings = model.inference(input, condition)
    #         new_condition = condition[:]
    #         new_condition[:, :len(target_condition)] = target_condition
    #         generated_samples = model.generate(embeddings, new_condition)
    #         total_generated_samples.append(generated_samples)


    with torch.no_grad():
        dataloader_iterator = iter(testloader)
        
        for i in range(len(testloader)):
            try:
                sample = next(dataloader_iterator)
            except StopIteration:
                dataloader_iterator = iter(testloader)
                sample = next(dataloader_iterator)
                
            input = sample['y']
            condition = sample['X']
            embeddings = model.inference(input, condition)
            new_condition = condition[:]
            new_condition[:, :len(target_condition)] = target_condition
            generated_samples = model.generate(embeddings, new_condition)
            total_generated_samples.append(generated_samples)
        
        
        total_generated_samples = torch.cat(total_generated_samples, 0)
        #total_generated_samples = total_generated_samples.cpu().numpy()
        total_generated_samples = total_generated_samples.numpy()

    return total_generated_samples


if __name__ == '__main__':
    GenerateCells()