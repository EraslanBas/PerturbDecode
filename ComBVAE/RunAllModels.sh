#!/bin/bash


for ((i=40;i<41;i+=1)); 
do 
    
       # python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res01_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res01_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res01_gumbel_v2_tau2 --n_cond=64 --n_latents=64 --n_inputs=1011 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_4 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_4 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_4 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_4 --n_cond=64 --n_latents=64 --n_inputs=776 &








   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_5 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_5 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_5 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_5 --n_cond=64 --n_latents=64 --n_inputs=776 &











   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res02_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_6 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res04_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_6 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res041_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_6 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python RunModels.py --trainfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_train.h5ad" --valfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataKODoubles_2_leidenRegOut_res08_test.h5ad"  --alpha=$i --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_6 --n_cond=64 --n_latents=64 --n_inputs=776 &



done









