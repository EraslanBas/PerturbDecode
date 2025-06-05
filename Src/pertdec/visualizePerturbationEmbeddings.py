from Src.utils.Utils import *
from Src.utils.libraries import *



def visualizePerturbationEmbeddings(perturbationEmbeddings, perturbationsList, clusteringRes=1.5):
    
    '''
    Method for visualizing the perturbation embeddings.
        
    perturbationEmbeddings : numpy.ndarrayr
        Perturbation embeddings extracted with extract_model_embeddings().
        
    perturbationsList : list
        Perturbation info of each cell extracted with extract_model_embeddings().
        
    clusteringRes : float
        Resolution for leiden clustering.
        
    '''    
    
    PertEmbedDF = pd.DataFrame(perturbationEmbeddings)
    PertEmbedDF["pert"] = perturbationsList
    
    PertEmbedDF = PertEmbedDF.drop_duplicates()
    
    PertEmbedDF.index = PertEmbedDF.pert
    
    PertEmbedDF.drop('pert', axis=1, inplace=True)
    
    respAnnDat = sc.AnnData(X=PertEmbedDF)
    respAnnDat.obs["pertIndex"] = list(PertEmbedDF.index)

    sc.pp.neighbors(respAnnDat, use_rep='X')
    sc.tl.leiden(respAnnDat, resolution=clusteringRes)
    sc.tl.umap(respAnnDat)
    sc.pl.umap(respAnnDat, 
               color='leiden',
               size=10,  
               legend_fontoutline=3, 
               legend_loc = 'center',
               legend_fontsize=14,
               legend_fontweight='normal')
    
    return respAnnDat