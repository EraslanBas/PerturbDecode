
This repository hosts the Python and R Jupyter notebooks used to perform the analyses described in the manuscript “Systematically Characterizing the Roles of E3-Ligase Family Members in Inflammatory Responses with Massively Parallel Perturb-seq” by Geiger-Schuller, Eraslan et al.

Analysis steps requiring visual inspection are implemented as Jupyter notebooks, while the remaining components are executed via command-line scripts for scalability and automation.

This pipeline includes the code for the following steps taken :

  * Data QC and preprocessing
  * Identification of the effects of perturbations on genes 
  * Learning the regulatory topology of perturbed and impacted genes 
  * Relating the regulatory (genetic) topology to physical interactions 


<img width="879" alt="Screen Shot 2022-12-18 at 8 01 09 PM" src="https://user-images.githubusercontent.com/45662603/208345270-31443000-600f-4f46-810f-9432e8ed70e0.png">


## File and Directory Structure

SRC/Pipeline/parameters.py file contains all the user defined parameters and input/output file names.    

 
