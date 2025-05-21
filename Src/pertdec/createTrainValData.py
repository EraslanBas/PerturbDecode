from Src.utils.libraries import *
import random


def createTrainValData(inAdata, perturbationColumn, pertCategories, dataDir, valSetPercent = 0.2):
    
    
    """
    
    Parameters
    ----------
    
    ininAdata : anndata
        Anndata object that has the single cell gene expression values in .X matrix
    
    perturbationColumn : str
        Name of the .obs column of the ininAdata that contains the perturbations IDs 
        that will be used for fitting the ComBVAE model.
        
    pertCategories : list of str
        Levels of the perturbation categories. The first element will be the reference category.
    
    dataDir : str
        Path of the directory where the cerated training and validation data will be stored.
        
    valSetPercent : float
        Percent of the all perturbation data that will be used for validation, 
        where the rest will be utilized for training the ComBVAE model. 
        
    Returns
    -------
    None
        This function does not return anything.

    """
    
    inAdata.obs[perturbationColumn] = pd.Categorical(
                                                    inAdata.obs[perturbationColumn],
                                                    categories=pertCategories, 
                                                    ordered=True) 
    allSet = set(range(inAdata.shape[0]))

    valSet =  set(random.sample(allSet, int(inAdata.shape[0]*0.2)))
    trainSet = allSet - valSet
    
    inAdataTrain = inAdata[list(trainSet),:].copy()
    inAdataVal = inAdata[list(valSet),:].copy()
    
    if inAdataTrain.raw is not None:
        del inAdataTrain.raw
    
    if inAdataVal.raw is not None:
        del inAdataVal.raw
    
    inAdataTrain.write(os.path.join(dataDir,"pertDecTrain.h5ad"), 
                            compression='gzip')
    inAdataVal.write(os.path.join(dataDir,"pertDecValidation.h5ad"), 
                          compression='gzip')
