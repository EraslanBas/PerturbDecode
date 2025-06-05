from Src.utils.Utils import *
from Src.utils.libraries import *

import gc
import multiprocessing
from multiprocessing import Pool, cpu_count
from statsmodels.api import OLS, add_constant

# Global variable to avoid copying X into each worker
X_shared = None

def init_worker(X_df):
    global X_shared
    X_shared = X_df

def fit_single_model(y_series):
    global X_shared
    dep_var_name = y_series.name
    indep_var_names = X_shared.columns.tolist()

    X_with_const = add_constant(X_shared, has_constant='add')
    model = OLS(y_series.values, X_with_const.values).fit()

    results = []
    for var, coef, pval in zip(['const'] + indep_var_names, model.params, model.pvalues):
        results.append({
            'dependent_variable': dep_var_name,
            'independent_variable': var,
            'coefficient': coef,
            'p_value': pval
        })

    return results

def fit_one_batch(allGuideMat, allExpMat, batchName, n_jobs: int = None):
    if not os.path.exists("./TmpOLSOuts/"):
        os.mkdir("./TmpOLSOuts/")

    if n_jobs is None:
        n_jobs = max(cpu_count() - 2, 1)

    # Downcast to save memory
    allGuideMat = allGuideMat.astype(np.float32)
    allExpMat = allExpMat.astype(np.float32)

    with Pool(processes=n_jobs, initializer=init_worker, initargs=(allGuideMat,)) as pool:
        results_nested = pool.map(fit_single_model, [allExpMat[col] for col in allExpMat.columns])

    flat_results = [item for sublist in results_nested for item in sublist]
    flat_results = pd.DataFrame(flat_results)
    flat_results.to_csv(f"./TmpOLSOuts/{batchName}.csv", index=False)

    # Free memory
    del allGuideMat, allExpMat, results_nested, flat_results
    gc.collect()

def inferEffectSizes(adata, perturbationsColumn, referenceLevel, covariates, par_test_target_interval=250):
    targetPerturbations = list(adata.obs["SelectedPerturbations"].unique())
    targetPerturbations.sort()
    targetPerturbations = [referenceLevel] + \
                          targetPerturbations[:targetPerturbations.index(referenceLevel)] + \
                          targetPerturbations[targetPerturbations.index(referenceLevel)+1:]

    adata.obs[perturbationsColumn] = pd.Categorical(
        adata.obs[perturbationsColumn],
        categories=targetPerturbations,
        ordered=True
    )

    designMatrix = pd.get_dummies(
        adata.obs[perturbationsColumn],
        drop_first=True
    )

    perturbationNames = designMatrix.columns
    covariate_df = adata.obs[covariates]
    designMatrix = pd.concat([designMatrix, covariate_df], axis=1)

    expressionMatrix = pd.DataFrame(adata.X, index=adata.obs.index, columns=adata.var_names)

    control_mask = adata.obs[perturbationsColumn] == referenceLevel
    controlExpressionMat = expressionMatrix.loc[control_mask]
    controlDesignMatrix = designMatrix.loc[control_mask]

    processes = []

    for i in range(0, len(perturbationNames), par_test_target_interval):
        print(f"Processing batch starting at index {i}")
        setIndex_1 = i
        setIndex_2 = min(i + par_test_target_interval, len(perturbationNames))

        selected_perturbations = perturbationNames[setIndex_1:setIndex_2]
        selColumns = list(selected_perturbations) + list(covariates)

        selected_mask = designMatrix[selected_perturbations].sum(axis=1) > 0
        tmpExpressionMat = expressionMatrix.loc[selected_mask]
        tmpDesignMatrix = designMatrix.loc[selected_mask, selColumns]
        controlDesignMatrixSel = controlDesignMatrix[selColumns]

        allExpMat = pd.concat([controlExpressionMat, tmpExpressionMat], axis=0)
        allGuideMat = pd.concat([controlDesignMatrixSel, tmpDesignMatrix], axis=0)

        p = multiprocessing.Process(
            target=fit_one_batch,
            args=(allGuideMat, allExpMat[:], f"Results_{setIndex_1}_{setIndex_2}")
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()




