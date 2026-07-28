from perturbdecode.utils.Utils import *
from perturbdecode.utils.libraries import *
from perturbdecode.utils.logger import *
from perturbdecode.data.ScreenDataset import *
from perturbdecode.models.CVAE_basic import *
from perturbdecode.models.CVAE_GumbelMasked import *
import torch.multiprocessing as mp


def extract_model_embeddings(model_dir, datafile, perturbationColumn, pertCategories, 
                             n_inputs, n_cond_in, n_latents, n_cond, 
                             model_type='CVAE_basic', batch_size=100, num_workers=10 ):
    
    '''
    Method for extracting the perturbation embeddings after the model fit.
        
    model_dir : str
        Path to the directory where the model is saved.
        
    datafile : str
        Path to the .h5ad file.
    
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
        Name of the model. Options are 'CVAE_basic', 'CVAE_Gumbel'. Default is 'CVAE_basic'.
    
    batch_size : int
        Batch size during training. Default is 100.
        
    num_workers : int
        Number of worker processes. Default is 10.

    '''
    
    mp.set_sharing_strategy('file_system')

    logger = setup_logger(name="embeddingExtraction_log", 
                      save_dir=model_dir)

        
    dataSet = ScreenDataset(h5adfile = datafile, 
                             perturbationColumn=perturbationColumn,
                             pertCategories=pertCategories)
    dataL = DataLoader(dataSet,
                       batch_size=batch_size,
                       drop_last=True,
                       shuffle=True, 
                       num_workers=num_workers)
 

    if model_type == "CVAE_basic":
        print("CVAE_basic")
        logger.info("Model type is CVAE_basic") 
        
        model = CVAE_basic(n_inputs=n_inputs,
                          n_latents=n_latents,
                          n_cond=n_cond,
                          n_cond_in=n_cond_in)
        
    elif model_type == "CVAE_Gumbel":
        print("CVAE_Gumbel")
        logger.info("Model type is CVAE_Gumbel")
        
        model = CVAE_Gumbel(n_inputs=n_inputs,
                            n_latents=n_latents,
                            n_cond=n_cond,
                            n_cond_in=n_cond_in,
                            tau=tau)
        
    print(os.path.join(model_dir,"best.pth"))
    model.load_state_dict(torch.load(os.path.join(model_dir,"best.pth"))['state_dict'])

    model.eval()

    perturbations = []
    factoredOutCellEmbeddings = []
    perturbationEmbeddings = []
    perturbationsList = []

    for idx, sample in tqdm(enumerate(dataL)):
        with torch.no_grad():            
            input = sample['y'].cuda() if next(model.parameters()).is_cuda else sample['y']
            condition = sample['X'].cuda() if next(model.parameters()).is_cuda else sample['X']
            embed = model.inference(input, condition)
            conditionEmbed = model.get_embedding(condition)
            
            pertlist = sample['pertlist'].cuda() if next(model.parameters()).is_cuda else sample['pertlist']
            
            perturbationsList = perturbationsList + pertlist
            perturbations.append(condition.data.cpu().numpy())
            factoredOutCellEmbeddings.append(embed.data.cpu().numpy())
            perturbationEmbeddings.append(conditionEmbed.data.cpu().numpy())


    perturbations = np.concatenate(perturbations, axis=0)
    factoredOutCellEmbeddings = np.concatenate(factoredOutCellEmbeddings, axis=0)    
    perturbationEmbeddings = np.concatenate(perturbationEmbeddings, axis=0)    
            
    return perturbations, factoredOutCellEmbeddings, perturbationEmbeddings, perturbationsList
