from Src.training.Training import *
from Src.utils.Utils import *
from Src.utils.libraries import *
from Src.utils.logger import *
from Src.data.ScreenDataset import *
from Src.models.CVAE_basic import *
from Src.models.CVAE_GumbelMasked import *



def runTrainingComBVAE(model_dir,
                 trainfile, valfile, perturbationColumn, pertCategories,
                 n_inputs,n_cond_in, n_latents, n_cond,
                 model_type='CVAE_basic',
                 beta=1.0, tau=1.0, 
                 batch_size=100,lr=0.0001, weight_decay=1e-5, use_gpu=True, setGPU=False, gpu_number='0',
                 optimizer='adam', max_epochs=500, 
                 scheduler='none', scheduler_step_size=10, scheduler_gamma=0.5, num_workers=10, seed =1):
    
    
    """
    
    Parameters
    ----------
    model_dir : str
        Path to the directory where the model is saved.
    trainfile : str
        Path to the training .h5ad file.
    valfile : str
        Path to the validation .h5ad file.
    perturbationColumn : str
        Name of the categorical column in .obs field that contains which perturbation(s) the cell has. 
    pertCategories : list of str
        Ordered categories of the perturbations where the first element will be basic reference level.
    n_inputs : int
        Number of input response genes that will be considered.
    n_cond_in : int
        Number of perturbation conditions
    n_latents : int
        Number of latent components for the cell embeddings where the perturbation effects are factored out.
    n_cond : int
        Number of latents for the perturbation embeddings
    model_type : str
        Name of the model. Options are 'CVAE_basic', 'CVAE_Gumbel'
    beta : float
        KL divergence weight in the loss function. 
    tau : float
        Sparsity parameter of gumbel_sigmoid. Lower values induce more sparsity.
    batch_size : int
        Batch size during training.
    lr : float
        Learning rate. Default 0.0001.
    weight_decay: float
        L2 regularization of the model parameters (weights). 
        Determines how strongly the model is penalized for having large weights.
        Larger values lead to stronger regularization. Default 1e-5.
    use_gpu: boolean
        Whether to use GPU. Default is TRUE.
    setGPU: boolean
        Whether to use a specific GPU in the system. Default is FALSE.
    gpu_number: int
        If setGPU is TRUE, then specifies the number of the GPU to be used.
    optimizer: str
        Pytorch Optimizer to be used. Options are 'sgd', 'adam', 'RMSprop', 'Adagrad', 'Adadelta',
        'Adamax', 'LBFGS', 'SparseAdam', 'ASGD', 'RAdam'.    
    max_epochs: int
        Upper bound of number of epochs for the training.
    scheduler: str
        Scheduler for learning rate decay. Options are 'none' or 'StepLR'.
    scheduler_step_size: int
        StepLR scheduler step size. Default is 10.
    scheduler_gamma: float
        StepLR scheduler gamma. Default is 0.5.
    num_workers : int
        Number of worker processes. Default is 10.
    seed : int
        Seed that will be used.
    
    Returns
    -------
    None
        This function does not return anything.

    Raises
    ------
    ExceptionType
        When and why this exception is raised.

    Examples
    --------
    >>> function_name(1, 'test')
    Expected output

    Notes
    -----
    Any additional information, limitations, or special considerations.

    See Also
    --------
    related_function : Brief description of relationship.
    :return: Result description
    :rtype: pandas.DataFrame
    """
    

    os.makedirs(model_dir, exist_ok=True)
    
    logger = setup_logger(name="training_log", 
                          save_dir=model_dir)
    
    logger.info(" ".join(["model_dir =",model_dir,
                          "\n trainfile =",trainfile,
                          "\n valfile =",valfile,
                          "\n perturbationColumn =",perturbationColumn,
                          "\n model_type =",model_type, 
                          "\n n_inputs =",str(n_inputs),
                          "\n n_latents =",str(n_latents),
                          "\n n_cond =",str(n_cond),
                          "\n n_cond_in =",str(n_cond_in),
                          "\n beta =",str(beta),
                          "\n tau =",str(tau),
                          "\n batch_size =",str(batch_size),
                          "\n lr =",str(lr),
                          "\n weight_decay =",str(weight_decay),
                          "\n use_gpu =",str(use_gpu),
                          "\n setGPU =",str(setGPU),
                          "\n gpu_number =",str(gpu_number),
                          "\n optimizer =",optimizer,
                          "\n scheduler =",scheduler,
                          "\n scheduler_step_size =",str(scheduler_step_size),
                          "\n scheduler_gamma =",str(scheduler_gamma),
                          "\n num_workers = ",str(num_workers),
                          "\n max_epochs = ",str(max_epochs),
                          "\n seed =",str(seed)]))  
    
    # seed run
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if use_gpu:
        torch.cuda.manual_seed(seed)

    if setGPU:
        os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
        os.environ["CUDA_VISIBLE_DEVICES"]= str(gpu_number)
        torch.cuda.set_device(gpu_number)


    logger.info("Training data are loading...")
    
    trainset = ScreenDataset(h5adfile = trainfile, 
                             perturbationColumn=perturbationColumn,
                             pertCategories=pertCategories)
    trainloader = DataLoader(trainset,
                             batch_size=batch_size,
                             drop_last=True,
                             shuffle=True, 
                             num_workers=num_workers)
    
    logger.info("Training data are loaded.")
    
    
    logger.info("Validation data are loading...")
    
    testset = ScreenDataset(h5adfile = valfile,
                           perturbationColumn=perturbationColumn,
                           pertCategories=pertCategories)
    testloader = DataLoader(testset,
                            batch_size=batch_size,
                            drop_last=True,
                            shuffle=True, 
                            num_workers=num_workers)
    logger.info("Validation data are loaded.")
    
    if model_type == "CVAE_basic":
        print("CVAE_basic")
        logger.info("Model type is CVAE_basic") 
        
        net = CVAE_basic(n_inputs=n_inputs,
                          n_latents=n_latents,
                          n_cond=n_cond,
                          n_cond_in=n_cond_in)
        
    elif model_type == "CVAE_Gumbel":
        print("CVAE_Gumbel")
        logger.info("Model type is CVAE_Gumbel")
        
        net = CVAE_Gumbel(n_inputs=n_inputs,
                         n_latents=n_latents,
                         n_cond=n_cond,
                         n_cond_in=n_cond_in,
                         tau=tau)
        
    
    
    optimizer = setup_optimizer(name=optimizer, param_list=[{'params': net.parameters(), 
                                                              'lr': lr,
                                                              'weight_decay': weight_decay}])


    if use_gpu:
        net.cuda()

    loss_tracked = 'test_loss' 
    
    if model_type == "CVAE_basic":
        loss_fn = CVAE_basic_get_loss_fn(beta)       
    elif model_type == "CVAE_Gumbel":
        loss_fn = CVAE_Gumbel_get_loss_fn(beta)

        
    test_summary = evaluate_model_CVAE(testloader=testloader,
                                       model=net,
                                       loss_fn=loss_fn)
 
    
    best_loss = test_summary['test_loss']
    
    
    trainingErrors = []
    testErrors = []

    trainingBCE = []
    testBCE = []

    trainingKLD = []
    testKLD = []
    
    logger.info("Training is starting...")
    
    for epoch in range(max_epochs):
        
        logger.info("Epoch %s:" % epoch)
        net.cuda()
        
       
        train_summary = train_model_CVAE(trainloader=trainloader, 
                                        model=net, 
                                        optimizer=optimizer, 
                                        loss_fn=loss_fn)
            
        logger.info("Training summary: %s" % train_summary['train_loss'])
        print("Training summary: %s" % train_summary['train_loss'])

        net.cuda()
       
            
        test_summary = evaluate_model_CVAE(testloader=testloader ,
                                  model=net,
                                  loss_fn=loss_fn)
       
        logger.info("Test summary: %s" % test_summary['test_loss'])
        print("Test summary: %s" % test_summary['test_loss'])

        net.cuda()
        
        if scheduler != 'none':
            scheduler.step()
            
        trainingErrors.append(train_summary['train_loss'])
        testErrors.append(test_summary['test_loss'])

        trainingBCE.append(train_summary['BCE'].cpu().detach().numpy())
        testBCE.append(test_summary['BCE'].cpu().detach().numpy())

       
        trainingKLD.append(train_summary['KLD'].cpu().detach().numpy())
        testKLD.append(test_summary['KLD'].cpu().detach().numpy())

          
        current_state = {'epoch': epoch,
                         'state_dict': net.cpu().state_dict(),
                         'best_loss': best_loss, 
                         'optimizer': optimizer.state_dict(),
                         'scheduler': scheduler.state_dict() if scheduler != 'none' else 'none'}

        if test_summary[loss_tracked] < best_loss:
            best_loss = test_summary[loss_tracked]
            current_state['best_loss'] = best_loss
            save_checkpoint(current_state=current_state, 
                            filename=os.path.join(model_dir,"best.pth"))

        logger.info("Best loss: %s" % best_loss)

      
    
    errorDF = pd.DataFrame({"TrainingError":trainingErrors,
                            "TestError":testErrors,
                            "Epoch":[x for x in range(0,len(testErrors))],
                            "Training_BCE_error":trainingBCE,
                            "Test_BCE_error":testBCE,
                            "Training_KLD_error":trainingKLD,
                            "Test_KLD_error":testKLD})
  
  
    #errorDF.to_pickle(os.path.join(model_dir,"TrainTestErrors.pkl"))
    errorDF.to_csv(os.path.join(model_dir,"TrainTestErrors.csv"))
                                                     
    logger.info("Training is complete!")
    print("Training is complete!")                                                
                                                     
    

