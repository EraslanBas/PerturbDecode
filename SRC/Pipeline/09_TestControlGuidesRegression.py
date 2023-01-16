from libraries import *
from parameters import *


import statsmodels.api as sm
import statsmodels.formula.api as smf
import sys
import multiprocessing
import time


def RunRegression(adataControl, controlGuides, guideIndex, expressionMatrix):
    
    geneCol = controlGuides[[guideIndex]].tolist() + ["n_genes", "mt_frac", "leiden"]
    
    allGuideMat = adataControl.obs[geneCol]
    
    allVars = pd.Series(geneCol) 
    all_columns = "+".join(allVars)
    my_formula = "y~" + all_columns
    

    allRes = pd.DataFrame()
    
    for j in range(0,20,1):

        allGuideMat["y"] = np.array(expressionMatrix)[:,j]
        
        if par_test_guide_method == 'NB':
            mod1 = smf.glm(formula=my_formula,
                           data=allGuideMat, 
                           family=sm.families.NegativeBinomial()).fit()
        elif par_test_guide_method == 'OLS':
            mod1 = smf.ols(formula=my_formula,
               data=allGuideMat).fit()
            
        k = mod1.summary()
        res = pd.DataFrame( k.tables[1])
        res["respGene"] = expressionMatrix.columns[j]
        
        allRes = pd.concat([allRes,res])
    
    allRes.to_csv("./TmpReg/GuideControlRegTest_"+str(guideIndex)+".csv", 
                  index=False)
    return()
      


    
### Test each control guide one-versus-rest

if __name__ == "__main__":
    
    
    os.getcwd()
    os.chdir(projectDir)
    
    start_time = time.perf_counter()

    adata = sc.read(par_save_filename_7)
    allGeneNames = adata.uns['AllExpGeneNames']
    
    controlGuides = adata.obs.columns[[ (x.startswith(par_nongene_site_control_prefix) or 
                                             x.startswith(par_not_target_control_prefix))
                                           for x in adata.obs.columns]]
    
    
    
    fBarMat = adata.obs[controlGuides]
    
    
    fBarMat[fBarMat>0] = 1
    adataControl = adata[fBarMat.sum(axis=1) > 0,:]
    
    
    if par_test_guide_method == 'NB':
        expressionMatrix = pd.DataFrame(adataControl.raw.X.A)
        expressionMatrix.columns = allGeneNames.iloc[:,0]
        expressionMatrix = expressionMatrix[adataControl.var_names]
        expressionMatrix.index = adataControl.obs.index
    elif par_test_guide_method == 'OLS':
        expressionMatrix = pd.DataFrame(adataControl.X)
        expressionMatrix.columns = adataControl.var_names
        expressionMatrix.index = adataControl.obs.index

    
    processes = []
    
    ## Create a temporary folder to save the temp files
    if not os.path.exists("./TmpReg/"):
        os.mkdir("./TmpReg/")
    
    for i in range(0,len(controlGuides),1):
        
        p = multiprocessing.Process(target = RunRegression, args=(adataControl, 
                                                                  controlGuides, 
                                                                  i, 
                                                                  expressionMatrix))
        p.start()
        processes.append(p)
    
    
    # Joins all the processes 
    for p in processes:
        p.join()
 
    finish_time = time.perf_counter()
    
    print(f"Program finished in {finish_time-start_time} seconds")
    
    ##Combine all results
    
    allRes = pd.DataFrame()
    for i in range(0,len(controlGuides),1):
        res =pd.read_csv("./TmpReg/GuideControlRegTest_"+str(i)+".csv")
        allRes = pd.concat([allRes,res])
        os.remove("./TmpReg/GuideControlRegTest_"+str(i)+".csv")
        
    allRes.columns = ['guides', 'coef', 'stderr', 'z', 'pval', '[0.025', '0.975', 'respGene'] 
    allRes = allRes[~allRes.guides.isin(['Intercept', 'n_genes', 'mt_frac', 'NaN']) & 
                    ~allRes.guides.isnull() &  
                    ~allRes.guides.str.contains("leiden", case=False, na=False) ]
 
    
    allRes.to_csv(par_control_testres_file, index=False)
    
   
    

