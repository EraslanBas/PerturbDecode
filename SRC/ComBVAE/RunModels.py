from libraries import *
from logger import setup_logger
from Training import train_model_CVAE, train_model_multilab, evaluate_model_CVAE, evaluate_model_CVAE_multilab, train_model_DenoisingAE, evaluate_model_DenoisingAE
from Utils import setup_lr_scheduler, setup_optimizer, save_checkpoint, load_checkpoint

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
from CVAE_model import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer
#from CVAE_model_noGuideEmbedding import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn
#from CVAE_multilableClas_model_2 import *
#from CVAE_model_conditionOnlyInDecoder import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer
#from DenoisingAE_model import *
#from CVAE_modelAdditiveCondition import E3ScreenDataset, VAE, Encoder, Decoder, get_loss_fn, EmbeddingLayer

@click.command()
# save and directory options
@click.option('--trainfile', 
              type=click.STRING, 
              default="./Notebooks/CombinatorialPerturbations/dataset/adataTR.h5ad",
              help='input training h5ad file')

@click.option("--controlfile", 
              type=click.STRING, 
              default="./Notebooks/CombinatorialPerturbations/dataset/adataTestControl.h5ad",
              help="test control cells h5ad file")

@click.option('--valfile', 
              type=click.STRING, 
              default='./Notebooks/CombinatorialPerturbations/dataset/adataVal.h5ad',
              help="validation h5ad file")

@click.option('--save_dir',
              type=click.STRING, 
              default='./Notebooks/CombinatorialPerturbations/outputs')

@click.option('--model_dir',
              type=click.STRING, 
              default='modelNoName')

@click.option('--seed',
              type=click.INT,
              default=42)

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

# training parameters
@click.option("--optimizer",
              type=click.STRING,
              default='adam',
              help="n_hidden")
@click.option("--scheduler",
              type=click.STRING,
              default='none',
              help="scheduler for learning rate decay")
@click.option("--alpha",
              type=click.FLOAT,
              default=1.0,
              help="weight of KL loss")
@click.option("--beta",
              type=click.FLOAT,
              default=0.0,
              help="weight of L1 loss")
@click.option("--theta",
              type=click.FLOAT,
              default=0.0,
              help="weight of multilabel classification")

@click.option("--batch_size",
              type=click.INT,
              default=1000,
              help="batch size")
@click.option("--num_workers",
              type=click.INT,
              default=40,
              help="number of workers")

@click.option("--gpu_number",
              type=click.STRING,
              default='0',
              help="number of workers")

@click.option("-lr",
              type=click.FLOAT,
              default=0.001,
              help="learning rate")
@click.option("--max_epochs",
              type=click.INT,
              default=8000,
              help="maximum number of epochs")
@click.option("--weight_decay",
              type=click.INT,
              default=0,
              help="weight decay")

# gpu options
@click.option("--use_gpu",
              type=click.BOOL,
              default=True,
              help="gpu usage")

@click.option("--project_dir",
              type=click.STRING,
              default="/home/eraslab1/Projects/E3Ligase/analysisSingle",
              help="Project directory")


def main(trainfile, controlfile, valfile, save_dir, model_dir,seed, n_cond_in, n_inputs, n_cond, n_latents, model_type, optimizer, scheduler, alpha, beta, theta, batch_size, num_workers, lr, max_epochs, weight_decay, use_gpu, project_dir, gpu_number):
    
    os.getcwd()
    os.chdir(project_dir)
    

    # os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
    # os.environ["CUDA_VISIBLE_DEVICES"]=gpu_number
    
    os.makedirs(os.path.join(save_dir, model_dir), exist_ok=True)
    logger = setup_logger(name="training_log", save_dir=os.path.join(save_dir, model_dir))
    logger.info(" ".join(sys.argv[1:]))        
        
    
    trainset = E3ScreenDataset(trainfile)
    trainloader = DataLoader(trainset,
                              batch_size=batch_size,
                         drop_last=True,
                         shuffle=True, 
                         num_workers=num_workers)
    
    
    testset = E3ScreenDataset(valfile)
    testloader = DataLoader(testset,
                            batch_size=batch_size,
                         drop_last=True,
                         shuffle=True, 
                         num_workers=num_workers)
    
    if model_type == "CVAE":
        print("CVAE")
        net = VAE(n_inputs=n_inputs,
                  n_latents=n_latents,
                  n_cond=n_cond,
                  n_cond_in=n_cond_in)
    elif model_type == "CVAE_multiLab":
        print("CVAE_multiLab")
        net = MultiLabClassVAE(n_inputs=n_inputs,
                      n_latents=n_latents,
                      n_cond=n_cond,
                      n_cond_in=n_cond_in)
    elif model_type == "DenoisingAE_model":
        print("DenoisingAE_model")
        net = DenoisingAE(n_inputs=n_inputs,
                      n_latents=n_latents,
                      n_cond=n_cond,
                      n_cond_in=n_cond_in)
    elif model_type == "MultiLabClassDenoisingAE_model":
        print("MultiLabClassDenoisingAE_model")
        net = MultiLabClassDenoisingAE(n_inputs=n_inputs,
                      n_latents=n_latents,
                      n_cond=n_cond,
                      n_cond_in=n_cond_in)
    
    
    optimizer = setup_optimizer(name=optimizer, param_list=[{'params': net.parameters(), 
                                                              'lr': lr,
                                                              'weight_decay': weight_decay}])


    if use_gpu:
        net.cuda()

    loss_tracked = 'test_loss' 
    
    if model_type == "CVAE":
        loss_fn = get_loss_fn(alpha, beta)
        test_summary = evaluate_model_CVAE(testloader=testloader if testloader is not None else trainloader,
                              model=net,
                              loss_fn=loss_fn)
    elif model_type == "CVAE_multiLab":
        loss_fn = get_loss_fn(alpha, beta, theta)
        test_summary = evaluate_model_CVAE_multilab(testloader=testloader if testloader is not None else trainloader,
                              model=net,
                              loss_fn=loss_fn)
    elif model_type == "DenoisingAE_model":
        loss_fn = get_loss_fn()
        test_summary = evaluate_model_DenoisingAE(testloader=testloader if testloader is not None else trainloader,
                              model=net,
                              loss_fn=loss_fn)
    
    
    best_loss = test_summary['test_loss']
    
    
    trainingErrors = []
    testErrors = []

    trainingBCE = []
    testBCE = []

    trainingKLD = []
    testKLD = []
    
    
    trainingL1 = []
    testL1 = []
    
    trainingMultilab = []
    testMultilab = []

    for epoch in range(max_epochs):
        
        logger.info("Epoch %s:" % epoch)
        net.cuda()
        
        if model_type == "CVAE": 
            train_summary = train_model_CVAE(trainloader=trainloader, 
                                    model=net, 
                                    optimizer=optimizer, loss_fn=loss_fn)
        elif model_type == "CVAE_multiLab":
            train_summary = train_model_multilab(trainloader=trainloader, 
                                    model=net, 
                                    optimizer=optimizer, loss_fn=loss_fn)
        elif model_type == "DenoisingAE_model":
            train_summary = train_model_DenoisingAE(trainloader=trainloader, 
                                    model=net, 
                                    optimizer=optimizer, loss_fn=loss_fn)
 
            
        #logger.info("Training summary: %s" % train_summary)
        #print("Training summary: %s" % train_summary)

        net.cuda()
        if model_type == "CVAE":
            
            test_summary = evaluate_model_CVAE(testloader=testloader if testloader is not None else trainloader,
                                      model=net,
                                      loss_fn=loss_fn)
        elif model_type == "CVAE_multiLab":
            
            test_summary = evaluate_model_CVAE_multilab(testloader=testloader if testloader is not None else trainloader,
                                      model=net,
                                      loss_fn=loss_fn)
        elif model_type == "DenoisingAE_model":
            
            test_summary = evaluate_model_DenoisingAE(testloader=testloader if testloader is not None else trainloader,
                                  model=net,
                                  loss_fn=loss_fn)

        #logger.info("Test summary: %s" % test_summary)
        #print("Test summary: %s" % test_summary)

        net.cuda()
        
        if scheduler != 'none':
            scheduler.step()
            
        trainingErrors.append(train_summary['train_loss'])
        testErrors.append(test_summary['test_loss'])

        trainingBCE.append(train_summary['BCE'].cpu().detach().numpy())
        testBCE.append(test_summary['BCE'].cpu().detach().numpy())

        if model_type == "CVAE" or model_type == "CVAE_multiLab":
            trainingKLD.append(train_summary['KLD'].cpu().detach().numpy())
            testKLD.append(test_summary['KLD'].cpu().detach().numpy())

            trainingL1.append(train_summary['l1Loss'].cpu().detach().numpy())
            testL1.append(test_summary['l1Loss'].cpu().detach().numpy())

        if model_type == "CVAE_multiLab":
            trainingMultilab.append(train_summary['classLoss'].cpu().detach().numpy())
            testMultilab.append(test_summary['classLoss'].cpu().detach().numpy())
        
 
        current_state = {'epoch': epoch,
                         'state_dict': net.cpu().state_dict(),
                         'best_loss': best_loss, 
                         'optimizer': optimizer.state_dict(),
                         'scheduler': scheduler.state_dict() if scheduler != 'none' else 'none'}

        if test_summary[loss_tracked] < best_loss:
            best_loss = test_summary[loss_tracked]
            current_state['best_loss'] = best_loss
            save_checkpoint(current_state=current_state, filename=os.path.join(save_dir,model_dir,"best.pth"))

        #logger.info("Best loss: %s" % best_loss)

      
    if model_type == "CVAE": 
        errorDF = pd.DataFrame({"TrainingError":trainingErrors,
                            "TestError":testErrors,
                            "Epoch":[x for x in range(0,len(testErrors))],
                            "Training_BCE_error":trainingBCE,
                            "Test_BCE_error":testBCE,
                            "Training_KLD_error":trainingKLD,
                            "Test_KLD_error":testKLD,
                            "Training_L1_error":trainingL1,
                            "Test_L1_error":testL1})
    elif model_type == "CVAE_multiLab":
           errorDF = pd.DataFrame({"TrainingError":trainingErrors,
                            "TestError":testErrors,
                            "Epoch":[x for x in range(0,len(testErrors))],
                            "Training_BCE_error":trainingBCE,
                            "Test_BCE_error":testBCE,
                            "Training_KLD_error":trainingKLD,
                            "Test_KLD_error":testKLD,
                            "Training_L1_error":trainingL1,
                            "Test_L1_error":testL1,
                            "Training_class_error" : trainingMultilab,
                            "Test_class_error" : testMultilab })  
    elif model_type == "DenoisingAE_model":
           errorDF = pd.DataFrame({"TrainingError":trainingErrors,
                            "TestError":testErrors,
                            "Epoch":[x for x in range(0,len(testErrors))],
                            "Training_BCE_error":trainingBCE,
                            "Test_BCE_error":testBCE})
    
  
    errorDF.to_pickle(os.path.join(save_dir,model_dir,"TrainTestErrors.pkl"))
    


if __name__ == '__main__':
    main()

