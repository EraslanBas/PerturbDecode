from libraries import *
from parameters import *


import statsmodels.api as sm
import statsmodels.formula.api as smf
import sys
import multiprocessing
import time


def RunRegression(KOGuides_altStr, setIndex_1, setIndex_2, 
                    controlExpressionMat, controlGuideMat, 
                    geneExpressionMat, geneGuideMat):
    
    allExpMat = np.concatenate((controlExpressionMat, 
                                geneExpressionMat))
    allGuideMat = pd.concat([controlGuideMat,
                             geneGuideMat])
    
    allRes = pd.DataFrame()
    
    for i in range(0,len(geneExpressionMat.columns),1):

        allVars = pd.Series(KOGuides_altStr[setIndex_1:setIndex_2]) 
        myForm = pd.concat([allVars, pd.Series(["n_genes","mt_frac","leiden"])])

        myFormula = "+".join(myForm)
        my_formula = "y~" + myFormula
        allGuideMat["y"] = allExpMat[:,i]
        
        if par_test_guide_method == 'NB':
            mod1 = smf.glm(formula=my_formula,
                           data=allGuideMat, 
                           family=sm.families.NegativeBinomial()).fit()
        elif par_test_guide_method == 'OLS':
            mod1 = smf.ols(formula=my_formula,
               data=allGuideMat).fit()
            
        k = mod1.summary()
        res = pd.DataFrame( k.tables[1])
        res["respGene"] = geneExpressionMat.columns[i]
        
        allRes = pd.concat([allRes,res])
    
    allRes.to_csv("./TmpReg/GuideRegTest_"+str(setIndex_1)+"_"+str(setIndex_2)+".csv", index=False)



if __name__ == "__main__":
    
    
    os.getcwd()
    os.chdir(projectDir)
    
    start_time = time.perf_counter()

    adata = sc.read(par_save_filename_7)

    allGeneNames = adata.uns['AllExpGeneNames']
    allBarcodeNames = adata.uns['feature_barcode_names']
    
    controlBarcodes = allBarcodeNames[[(x.startswith((par_not_target_control_prefix, 
                                                      par_nongene_site_control_prefix))) for x in allBarcodeNames]]
    
    adata.obs["ControlGuidesAll"] = adata.obs[controlBarcodes].sum(axis=1)

    guideMatrix = adata.obs[adata.uns['feature_KO_barcode_names_filtered']]
    KOGuides = pd.Series(adata.uns['feature_KO_barcode_names_filtered'])
    ##Gene names that start with a number are replaced with "X"+gene_name
    KOGuides_altStr = ["X"+x if x[0].isdigit() else x for x in KOGuides ]
    KOGuides_altStr = [x.replace("-","_") for x in KOGuides_altStr ]
    guideMatrix.columns = KOGuides_altStr



    df = adata.obs[["n_genes", "mt_frac", "leiden" ]]
    guideMatrix = guideMatrix.join(df)

    if par_test_guide_method == 'NB':
        expressionMatrix = pd.DataFrame(adata.raw.X.A)
        expressionMatrix.columns = allGeneNames.iloc[:,0]
        expressionMatrix = expressionMatrix[adata.var_names]
        expressionMatrix.index = adata.obs.index
    elif par_test_guide_method == 'OLS':
        expressionMatrix = pd.DataFrame(adata.X)
        expressionMatrix.columns = adata.var_names
        expressionMatrix.index = adata.obs.index


    controlExpressionMat = expressionMatrix.loc[adata.obs["ControlGuidesAll"] == 1,]
    controlGuideMat = guideMatrix.loc[adata.obs["ControlGuidesAll"] == 1,]
    
    processes = []
    
    ## Create a temporary folder to save the temp files
    if not os.path.exists("./TmpReg/"):
        os.mkdir("./TmpReg/")
    
    for i in range(0,len(KOGuides),par_test_guide_interval):
        setIndex_1 = i
        
        if setIndex_1 + par_test_guide_interval < len(KOGuides):
            setIndex_2 = setIndex_1 + par_test_guide_interval
        else:
            setIndex_2 = len(KOGuides)
        
        
        selColumns = pd.concat([pd.Series(KOGuides_altStr[setIndex_1:setIndex_2]), 
                                pd.Series(["n_genes", "mt_frac", "leiden"])])

        geneExpressionMat = expressionMatrix.loc[adata.obs[KOGuides[setIndex_1:setIndex_2]].sum(axis=1) > 0,]
        geneGuideMat = guideMatrix.loc[adata.obs[KOGuides[setIndex_1:setIndex_2]].sum(axis=1) > 0,]
        geneGuideMat=geneGuideMat[selColumns]
        
        controlGuideMatSel=controlGuideMat[selColumns]

        p = multiprocessing.Process(target = RunRegression, args=(KOGuides_altStr, setIndex_1, setIndex_2,
                                                                   controlExpressionMat, controlGuideMatSel,
                                                                   geneExpressionMat, geneGuideMat))
        p.start()
        processes.append(p)
    
    
    # Joins all the processes 
    for p in processes:
        p.join()
 
    finish_time = time.perf_counter()
    
    print(f"Program finished in {finish_time-start_time} seconds")
    
    ##Combine all results
    allRes = pd.DataFrame()
    for i in range(0,len(KOGuides),par_test_guide_interval):
        setIndex_1 = i

        if setIndex_1 + par_test_guide_interval < len(KOGuides):
            setIndex_2 = setIndex_1 + par_test_guide_interval
        else:
            setIndex_2 = len(KOGuides)

        res =pd.read_csv("./TmpReg/GuideRegTest_"+str(setIndex_1)+"_"+str(setIndex_2)+".csv")
        allRes = pd.concat([allRes,res])
        
    allRes.columns = ['guides', 'coef', 'stderr', 'z', 'pval', '[0.025', '0.975', 'respGene'] 
    allRes = allRes[~allRes.guides.isin(['Intercept', 'n_genes', 'mt_frac', 'NaN']) & 
                    ~allRes.guides.isnull() &  
                    ~allRes.guides.str.contains("leiden", case=False, na=False) ]
 
    
    allRes.to_csv(par_guide_testres_file, index=False)
    
   
    

