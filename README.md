# PerturbDecode
## An end-to-end computational pipeline for large Perturb-seq screens


PerturbDecode is a framework developed for the automated analysis of large-scale Perturb-seq screens. The workflow in PerturbDecode consists of: 


  * Data QC and preprocessing
  * Identification of the effects of perturbations on genes with parallel processes
  * Learning the regulatory topology of perturbed and impacted genes for single and/or combinatorial perturbations
  * Relating the regulatory (genetic) topology to physical interactions 



<img width="879" alt="Screen Shot 2022-12-18 at 8 01 09 PM" src="https://user-images.githubusercontent.com/45662603/208345270-31443000-600f-4f46-810f-9432e8ed70e0.png">


## User Manual

PerturbDecode pipeline consists of a set of Python and R Jupyter notebooks and scripts. Analysis steps which require visual inspection are coded as Jupyter notebooks, while the rest are called from the command line. SRC/Pipeline/parameters.py file contains all the user defined parameters and input/output file names.    

Detailed explanations of each step will be included here soon.



## 

SRC/ManuscriptFigures folder contains the analysis scripts developed for generating the figures presented in "Systematically characterizing the roles of E3-ligase family members in inflammatory responses with massively parallel Perturb-seq", Geiger-Schuller, Eraslan et al.
