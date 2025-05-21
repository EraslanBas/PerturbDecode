#!/bin/bash



for ((i=40;i<41;i+=1)); 
do 

    
       # python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res01.h5ad"   --model_dir=model_alpha_${i}_KOSingles_leidenRegOut_res01_gumbel_v3_hard_tau2 --n_cond=64 --n_latents=64 --n_inputs=1011 &



# python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res02.h5ad"  --model_dir=model_alpha_${i}_KODoubles_4_leidenRegOut_res02 --n_cond=64 --n_latents=64 --n_inputs=947 &



#    python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res04.h5ad"  --model_dir=model_alpha_${i}_KODoubles_4_leidenRegOut_res04 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
#    python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res041.h5ad"  --model_dir=model_alpha_${i}_KODoubles_4_leidenRegOut_res041 --n_cond=64 --n_latents=64 --n_inputs=883 &



#    python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res08.h5ad"  --model_dir=model_alpha_${i}_KODoubles_4_leidenRegOut_res08 --n_cond=64 --n_latents=64 --n_inputs=776 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res02.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_1 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res04.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_1 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res041.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_1 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res08.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_1 --n_cond=64 --n_latents=64 --n_inputs=776 &








   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res02.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_2 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res04.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_2 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res041.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_2 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res08.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_2 --n_cond=64 --n_latents=64 --n_inputs=776 &









   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res02.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res02_3 --n_cond=64 --n_latents=64 --n_inputs=947 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res04.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res04_3 --n_cond=64 --n_latents=64 --n_inputs=884 &
   
   
   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res041.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res041_3 --n_cond=64 --n_latents=64 --n_inputs=883 &



   python GenerateCells.py --controlfile="/home/eraslab1/Projects/E3Ligase/analysisSingle/ComboData_v2/outputs/anndata/adataControl_leidenRegOut_res08.h5ad"   --model_dir=model_alpha_${i}_KODoubles_2_leidenRegOut_res08_3 --n_cond=64 --n_latents=64 --n_inputs=776 &



done


