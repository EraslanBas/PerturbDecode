#!/bin/bash




for ((i=40;i<41;i+=1)); 
do 
    # python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKOSingles_leidenRegOut_res005_train.h5ad" --model_dir=model_alpha_${i}_KOSingles_leidenRegOut_res005  &
 
    
   
   
 python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_gumbel_v3_tau05_1  &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_gumbel_v3_tau05_1 &
   
   
   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_gumbel_v3_tau05_1 &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_gumbel_v3_tau05_1  &
   






 python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_gumbel_v3_tau05_2  &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_gumbel_v3_tau05_2 &
   
   
   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_gumbel_v3_tau05_2 &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_gumbel_v3_tau05_2  &








 python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_gumbel_v3_tau05_3  &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_gumbel_v3_tau05_3 &
   
   
   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_gumbel_v3_tau05_3 &



   python ComputeLogFCOfPredictionsAll.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_gumbel_v3_tau05_3  &





done
