from libraries import *
from parameters import *


import statsmodels.api as sm
import statsmodels.formula.api as smf
import sys
import multiprocessing
import time

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri


activity = ro.r(r'''
    function(allGuideMat, allExpMat,my_formula,setIndex_1) {
        library("MASS")
        library("lme4")

        coefDF = data.frame()

        for(i in seq(1,length(colnames(allExpMat)),1)){

            print(i)
            tryCatch(
                expr = {
                       allGuideMat["y"] = allExpMat[,i]
                       myFit <- glmer.nb(formula(my_formula), 
                                         data = allGuideMat, 
                                         control = glmerControl(optimizer="bobyqa", 
                                                                calc.derivs = FALSE))
                       k <- summary(myFit)
                       myDF <- data.frame(coefficients(k))
                       myDF$coefNames <- dimnames(coefficients(k))[[1]]
                       myDF$respGene = colnames(allExpMat)[i]
                       coefDF <- rbind(coefDF, myDF)
                       print(coefDF)
                },
                error = function(e){ 
                    print(e)
                },
                finally = {
                    # (Optional)
                    # Do this at the end before quitting the tryCatch structure...
                }
            )
        }
        
        write.csv(coefDF, paste0("./TmpMixedEffectNBLMOuts/coefs_",setIndex_1,".csv"), row.names=FALSE, quote=FALSE)

        }
''')

def MixedEfNB_model(allGuideMat, allExpMat, KOGenes, setIndex_1, setIndex_2):
    
    allVars = pd.Series(KOGenes[setIndex_1:setIndex_2]) 
    all_columns = "+".join(allVars[~allVars.isin(["leiden"])])
    all_columns = all_columns +  "+n_genes+mt_frac"
    my_formula = "y~" + all_columns + " + (1 | leiden)"
    
    r_allGuideMat = ro.conversion.get_conversion().py2rpy(allGuideMat)
    r_allExpMat = ro.conversion.get_conversion().py2rpy(allExpMat)
    r_my_formula = ro.conversion.get_conversion().py2rpy(my_formula)
    r_setIndex_1 = ro.conversion.get_conversion().py2rpy(setIndex_1)
    
    myDatframe = {}
    myDatframe['allGuideMat'] = r_allGuideMat
    myDatframe['allExpMat'] = r_allExpMat
    myDatframe['my_formula'] = r_my_formula
    myDatframe['setIndex_1'] = r_setIndex_1
    
    activity(myDatframe['allGuideMat'], 
         myDatframe['allExpMat'], 
         myDatframe['my_formula'],
         myDatframe['setIndex_1'])
    
    return()

def MixedEfNormal_model(allGuideMat, allExpMat, KOGenes, setIndex_1, setIndex_2):
    
    allVars = pd.Series(KOGenes[setIndex_1:setIndex_2]) 
    all_columns = "+".join(allVars[~allVars.isin(["leiden"])])
    all_columns = all_columns +  "+n_genes+mt_frac"
    my_formula = "y~" + all_columns 
    
    allTargets = allExpMat.columns
    allExpMat = np.array(allExpMat)
    
    allRes = pd.DataFrame()
    
    for i in range(0,len(allTargets),1):

        allGuideMat["y"] = allExpMat[:,i]
        est = smf.mixedlm(my_formula, 
                          allGuideMat, 
                          groups=allGuideMat["leiden"], 
                          missing='drop')
        mdf = est.fit(method=["bfgs"])
        
        k = mdf.summary()
        res = pd.DataFrame( k.tables[1])
        res["respGene"] = allTargets[i]
        
        allRes = pd.concat([allRes,res])
    
    allRes.to_csv("./TmpMixedEffectNBLMOuts/coefs_"+str(setIndex_1)+".csv")


if __name__ == "__main__":
    
    
    os.getcwd()
    os.chdir(projectDir)
    
    start_time = time.perf_counter()

    adata = sc.read('outputs/anndata/adata-hash-features_singlets_SingleKO_08122020_PerGENE.h5ad')
    

    KOGenes = adata.uns['feature_barcode_names_filtered_GENES']
    KOGenes = KOGenes[KOGenes != "GENE_CONTROL_"]

    guideMatrix = adata.obs[KOGenes]

    ## Add covariates that should be corrected for
    df = adata.obs[["n_genes", "mt_frac", "leiden" ]]
    guideMatrix = guideMatrix.join(df)
    
    
    if par_test_target_dist == 'NB':
        expressionMatrix = pd.DataFrame(adata.raw.X.A)
        expressionMatrix.columns = adata.uns['AllExpGeneNames'].iloc[:,0]
        expressionMatrix = expressionMatrix[adata.var_names]
        expressionMatrix.index = adata.obs.index
    elif par_test_target_dist == 'Normal':
        expressionMatrix = pd.DataFrame(adata.X)
        expressionMatrix.columns = adata.var_names
        expressionMatrix.index = adata.obs.index


    controlExpressionMat = expressionMatrix.loc[adata.obs["GENE_CONTROL_"] == 1,]
    controlGuideMat = guideMatrix.loc[adata.obs["GENE_CONTROL_"] == 1,]
    controlExpressionMat = controlExpressionMat.iloc[0:5000,:]
    controlGuideMat = controlGuideMat.iloc[0:5000,:]

    processes = []
    
    ## Create a temporary folder to save the temp files
    if not os.path.exists("./TmpMixedEffectNBLMOuts/"):
        os.mkdir("./TmpMixedEffectNBLMOuts/")
    
    
    for i in range(0,len(KOGenes),par_test_target_interval):
        setIndex_1 = i
        
        if setIndex_1 +  par_test_target_interval< len(KOGenes):
            setIndex_2 = setIndex_1 + par_test_target_interval
        else:
            setIndex_2 = len(KOGenes)
        

        selColumns = pd.concat([pd.Series(KOGenes[setIndex_1:setIndex_2]), 
                                pd.Series(["n_genes", "mt_frac", "leiden"])])
        

        geneExpressionMat = expressionMatrix.loc[adata.obs[KOGenes[setIndex_1:setIndex_2]].sum(axis=1) > 0,]
        geneGuideMat = guideMatrix.loc[adata.obs[KOGenes[setIndex_1:setIndex_2]].sum(axis=1) > 0,]
        geneGuideMat=geneGuideMat[selColumns]
        
        controlGuideMatSel=controlGuideMat[selColumns]

        allExpMat = np.concatenate((controlExpressionMat, geneExpressionMat))
        allExpMat = pd.DataFrame(allExpMat)
        allExpMat.columns = adata.var_names
    
        allGuideMat = controlGuideMatSel.append(geneGuideMat)

        if par_test_target_model== 'MixedEfNB':
            p = multiprocessing.Process(target = MixedEfNB_model, args=(allGuideMat, 
                                                                        allExpMat, 
                                                                        KOGenes, 
                                                                        setIndex_1, 
                                                                        setIndex_2))
        elif par_test_target_model== 'MixedEfNormal':
            p = multiprocessing.Process(target = MixedEfNormal_model, args=(allGuideMat, 
                                                                        allExpMat, 
                                                                        KOGenes, 
                                                                        setIndex_1, 
                                                                        setIndex_2))
        p.start()
        processes.append(p)
    
    
    # Joins all the processes 
    for p in processes:
        p.join()
 
    finish_time = time.perf_counter()
    
    print(f"Program finished in {finish_time-start_time} seconds")
    
    ##Combine all results
    allRes = pd.DataFrame()
    for i in range(0,len(KOGenes),par_test_target_interval):
        setIndex_1 = i

        if setIndex_1 + par_test_guide_interval < len(KOGenes):
            setIndex_2 = setIndex_1 + par_test_guide_interval
        else:
            setIndex_2 = len(KOGenes)

        res =pd.read_csv("./TmpMixedEffectNBLMOuts/coefs_"+str(setIndex_1)+".csv")
        allRes = pd.concat([allRes,res])
        os.remove("./TmpMixedEffectNBLMOuts/coefs_"+str(setIndex_1)+".csv")
        
    if par_test_target_model== 'MixedEfNB':
        allRes = allRes.iloc[:,[4,0,3,5]]
        allRes.columns = ['KO_gene', 'coef', 'p_value', 'respGene'] 
        allRes = allRes[~allRes.KO_gene.isin(['(Intercept)', 'n_genes', 'mt_frac', 'NaN']) & 
                        ~allRes.KO_gene.isnull()]
    elif par_test_target_model== 'MixedEfNormal':
        allRes = allRes.iloc[:,[0,1,4,7]]
        allRes.columns = ['KO_gene', 'coef', 'p_value', 'respGene'] 
        allRes = allRes[~allRes.KO_gene.isin(['Intercept', 'n_genes', 'mt_frac', 'NaN', 'Group Var']) & 
                ~allRes.KO_gene.isnull()]

    
    allRes.to_csv(par_test_target_file, index=False)
    
   