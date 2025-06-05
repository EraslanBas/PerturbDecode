from Src.utils.Utils import *
from Src.utils.libraries import *
from sklearn.metrics.pairwise import cosine_distances
import pingouin as pg

def selectWorkingGuides(pertEmbedAnndat, controlGuideIdentifiers,
                        numberOfGuidesPerTarget, pValThreshold=0.05,
                        correlationThreshold = 0, method='pearson'):
    
        
    """
    Select conditionally dependent guides targeting the same gene.

    This method identifies guide RNAs that target the same gene and exhibit significantly similar 
    phenotypic effects, based on statistical thresholds applied to partial correlations computed 
    based on perturbation embeddings.

    Parameters
    ----------
    pertEmbedAnndat : anndata.AnnData
        The AnnData object returned by `visualizePerturbationEmbeddings()`, containing perturbation 
        embeddings for both targeting and control guides.

    controlGuideIdentifiers : list of str
        List of identifiers used to define control guides (e.g., "NOTarget", "NonGeneSite").

    numberOfGuidesPerTarget : int
        Expected number of guides designed to target each gene.

    pValThreshold : float
        P-value cutoff for selecting guides that induce significantly similar phenotypic changes.
        Default : 0.05.

    correlationThreshold : float
        Partial correlation threshold used to determine similarity between guides based on their cosine 
        distances to all other guides given the control guides's cosine distances. Default : 0.

    method : str
        Method used to compute partial correlations, default : 'pearson'.

    Returns
    -------
    selectedGuides : list of str
        List of selected guides.
        
    GuideDependencies : pandas.DataFrame
        Data frame containing the test results of the tested pairs of guides targeting the same gene.

    """

    pairwiseDist = pd.DataFrame(cosine_distances(pertEmbedAnndat.X, 
                                             pertEmbedAnndat.X))
    
    pairwiseDist.columns = pertEmbedAnndat.obs["pertIndex"]
    pairwiseDist.index = pertEmbedAnndat.obs["pertIndex"]
    
    pairwiseDist = pairwiseDist.sort_index(axis=1).sort_index(axis=0)
    
    allControlGuides = []
    
    controlGuides = [x.split("_")[0] in controlGuideIdentifiers for x in pairwiseDist.index]
    controlGuides = list(pairwiseDist.loc[controlGuides, controlGuides].index)
    
    targetGenes = list(set([x.split("_")[0] for x in pairwiseDist.index]))
    targetGenes.sort()
    targetGenes = [x for x in targetGenes if x not in controlGuideIdentifiers]
    
    allres = []

    for elem in targetGenes:
        for i in range(0,numberOfGuidesPerTarget):
            for j in range(i+1,numberOfGuidesPerTarget):

                if ((elem+"_"+str(i) in pairwiseDist.columns) & (elem+"_"+str(j) in pairwiseDist.columns)):
                    k = pg.partial_corr(data=pairwiseDist,
                                    x=elem+"_"+str(i), y=elem+"_"+str(j), 
                                    covar=controlGuides,
                                    method=method).round(3)

                    allres.append({"TargetGene": elem, 
                                 "Guide1": elem+"_"+str(i),
                                 "Guide2": elem+"_"+str(j),
                                 "Pval":k["p-val"][0],
                                 "Rho":k.r[0]
                                })

    df = pd.DataFrame(allres)
    
    df_selected = df.loc[(df.Pval < pValThreshold) & (df.Rho > correlationThreshold),]
    
    selectedGuides = list(set(list(df_selected.Guide1.unique()) + list(df_selected.Guide2.unique())))
    selectedGuides.sort()
    
    return selectedGuides, df





    