from perturbdecode.utils.Utils import *
from perturbdecode.utils.libraries import *
from sklearn.metrics.pairwise import cosine_distances



def visualizePerturbationEmbeddings(perturbationEmbeddings, perturbationsList, clusteringRes=1.5, n_neighbors=10):
    
    '''
    Method for visualizing the perturbation embeddings.
        
    perturbationEmbeddings : numpy.ndarrayr
        Perturbation embeddings extracted with extract_model_embeddings().
        
    perturbationsList : list
        Perturbation info of each cell extracted with extract_model_embeddings().
        
    clusteringRes : float
        Resolution for leiden clustering.

    n_neighbors : int
        Number of nearest neighbours used when contructing the kNN graph.
        
        
    '''    
    
    PertEmbedDF = pd.DataFrame(perturbationEmbeddings)
    PertEmbedDF["pert"] = perturbationsList
    
    PertEmbedDF = PertEmbedDF.drop_duplicates()
    
    PertEmbedDF.index = PertEmbedDF.pert
    
    PertEmbedDF.drop('pert', axis=1, inplace=True)

    
    respAnnDat = sc.AnnData(X=PertEmbedDF)
    respAnnDat.obs["pertIndex"] = list(PertEmbedDF.index)

    pairwiseDistCosine = pd.DataFrame(cosine_distances(respAnnDat.X, 
                                      respAnnDat.X))

    pairwiseDistCosine.index = respAnnDat.obs["pertIndex"]
    pairwiseDistCosine.columns = respAnnDat.obs["pertIndex"]


    visAnnDat = sc.AnnData(X=pairwiseDistCosine)
    visAnnDat.obs["pertIndex"] = list(pairwiseDistCosine.index)

    sc.pp.neighbors(visAnnDat, use_rep='X', n_neighbors=n_neighbors)
    sc.tl.leiden(visAnnDat, resolution=clusteringRes)
    sc.tl.umap(visAnnDat)
    sc.pl.umap(visAnnDat, 
               color='leiden',
               size=10,  
               legend_fontoutline=3, 
               #legend_loc = 'center',
               legend_fontsize=14,
               legend_fontweight='normal')
    
    return respAnnDat, visAnnDat