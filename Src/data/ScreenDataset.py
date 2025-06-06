from Src.utils.libraries import *
from pandas.api.types import CategoricalDtype


class ScreenDataset(Dataset):
    """
        Perturbation screen data set.
    """
 
    def __init__(self, h5adfile, perturbationColumn, pertCategories):
        """
        Initialize the perturbation dataset.

        Args:
            h5adfile : str
                Path to the h5adfile that contains the anndata object.
            perturbationColumn : str
               Name of the categorical column in .obs field that contains which perturbation the cell has. 
            pertCategories : list of str
               Ordered categories of the perturbations where the first element will be basic reference level.
                
        """

        self.data = sc.read(h5adfile)
        
        # Assume pertCategories is the full ordered list
        cat_type = CategoricalDtype(categories=pertCategories, ordered=True)

        self.data.obs[perturbationColumn] = self.data.obs[perturbationColumn].astype(cat_type)
        
         ## perturbations
        self.pertlist = list(self.data.obs[perturbationColumn])


        # Generate one-hot encoding
        one_hot_pert_id = pd.get_dummies(self.data.obs[perturbationColumn], prefix='Pert')

        # Drop the reference level manually
        ref_col = f'Pert_{pertCategories[0]}'
        if ref_col in one_hot_pert_id.columns:
            one_hot_pert_id.drop(columns=[ref_col], inplace=True)

        # Ensure all other categories are present in the same order
        expected_cols = [f'Pert_{cat}' for cat in pertCategories[1:]]
        one_hot_pert_id = one_hot_pert_id.reindex(columns=expected_cols, fill_value=0)
 

        self.perturbations = pertCategories[1:]
        
        ## One hot encoded perturbation matrix
        self.X = one_hot_pert_id.to_numpy()
        
        ## Log normalized expression matrix 
        if scipy.sparse.issparse(self.data.X):
            self.y = self.data.X.toarray()
        else:
            self.y = self.data.X
        
       

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        #y = self.data.X[idx:idx+1]
        y = self.y[idx]
        X = self.X[idx]
        pertlist = self.pertlist[idx]
        return {'y': torch.from_numpy(y).float(),
                'X': torch.from_numpy(X).float(),
                'pertlist':pertlist}
    
    
    def get_genes(self):
        "Return list of genes"
        return list(self.data.var_names)

    def get_targets(self):
        "Return list of perturbations"
        return list(self.perturbations)  
    

    
