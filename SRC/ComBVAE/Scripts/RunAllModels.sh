#!/bin/bash

# python RunModels.py  --beta=0 --model_dir=model_0 &

# python RunModels.py  --beta=0.00001 --model_dir=model_000001 &

# python RunModels.py  --beta=0.0001 --model_dir=model_00001 &

# python RunModels.py  --beta=0.001 --model_dir=model_0001 &

# python RunModels.py  --beta=0.01 --model_dir=model_001 &

# python RunModels.py  --beta=0.1 --model_dir=model_01  &

# python RunModels.py  --beta=1 --model_dir=model_1 



# python RunModels.py  --beta=0 --theta=100 --model_type="CVAE_multiLab" --model_dir=model_00_multilab &

# python RunModels.py  --beta=0 --theta=1000 --model_type="CVAE_multiLab" --model_dir=model_000_multilab &

# python RunModels.py  --beta=0 --theta=10000 --model_type="CVAE_multiLab" --model_dir=model_0000_multilab &

# python RunModels.py  --beta=0 --theta=100000 --model_type="CVAE_multiLab" --model_dir=model_00000_multilab &

# python RunModels.py  --beta=0 --theta=1000000 --model_type="CVAE_multiLab" --model_dir=model_000000_multilab &

# python RunModels.py  --beta=0 --theta=10000000 --model_type="CVAE_multiLab" --model_dir=model_0000000_multilab


### See whether the results change when you input the condition only to the decoder
# python RunModels.py  --beta=0 --model_dir=model2_0 &

# python RunModels.py  --beta=0.00001 --model_dir=model2_000001 &

# python RunModels.py  --beta=0.0001 --model_dir=model2_00001 &

# python RunModels.py  --beta=0.001 --model_dir=model2_0001 &

# python RunModels.py  --beta=0.01 --model_dir=model2_001 &

# python RunModels.py  --beta=0.1 --model_dir=model2_01  &

# python RunModels.py  --beta=1 --model_dir=model2_1 


# python RunModels.py  --alpha=0.6 --model_dir=model_alpha_0_6 &

# python RunModels.py  --alpha=0.8 --model_dir=model_alpha_0_8 &

# python RunModels.py  --alpha=0.85 --model_dir=model_alpha_0_85 &

# python RunModels.py  --alpha=0.9 --model_dir=model_alpha_0_9 &

# python RunModels.py  --alpha=0.95 --model_dir=model_alpha_0_95 &

# python RunModels.py  --alpha=1 --model_dir=model_alpha_1 &

# python RunModels.py  --alpha=1.001 --model_dir=model_alpha_1_001 &

# python RunModels.py  --alpha=1.005 --model_dir=model_alpha_1_005 &

# python RunModels.py  --alpha=1.05 --model_dir=model_alpha_1_05 &

# python RunModels.py  --alpha=1.1 --model_dir=model_alpha_1_1 &

# python RunModels.py  --alpha=1.3 --model_dir=model_alpha_1_3 &

# python RunModels.py  --alpha=1.5 --model_dir=model_alpha_1_6 &

# python RunModels.py  --alpha=1.7 --model_dir=model_alpha_1_7 &

# python RunModels.py  --alpha=2 --model_dir=model_alpha_2 &


# python RunModels.py --n_latents=32 --n_cond=32 --alpha=0.6 --model_dir=model_alpha_0_6_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=0.8 --model_dir=model_alpha_0_8_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=0.85 --model_dir=model_alpha_0_85_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=0.9 --model_dir=model_alpha_0_9_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=0.95 --model_dir=model_alpha_0_95_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1 --model_dir=model_alpha_1_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.001 --model_dir=model_alpha_1_001_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.005 --model_dir=model_alpha_1_005_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.05 --model_dir=model_alpha_1_05_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.1 --model_dir=model_alpha_1_1_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.3 --model_dir=model_alpha_1_3_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.5 --model_dir=model_alpha_1_5_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=1.7 --model_dir=model_alpha_1_7_32 &

# python RunModels.py --n_latents=32 --n_cond=32 --alpha=2 --model_dir=model_alpha_2_32 &



# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.6 --model_dir=model_alpha_1_6_n_cond32 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.65 --model_dir=model_alpha_1_65_cond32 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.7 --model_dir=model_alpha_1_7_cond32 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.75 --model_dir=model_alpha_1_75_cond32 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.8 --model_dir=model_alpha_1_8_cond32 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.85 --model_dir=model_alpha_1_85_cond32 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --max_epochs=10000 --n_cond=32 --alpha=1.9 --model_dir=model_alpha_1_9_cond32 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.6 --model_dir=model_alpha_1_6_n_cond16 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.65 --model_dir=model_alpha_1_65_cond16 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.7 --model_dir=model_alpha_1_7_cond16 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.75 --model_dir=model_alpha_1_75_cond16 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.8 --model_dir=model_alpha_1_8_cond16 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.85 --model_dir=model_alpha_1_85_cond16 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --max_epochs=10000 --n_cond=16 --alpha=1.9 --model_dir=model_alpha_1_9_cond16 &





#python RunModels.py  --n_cond=6 --model_dir=model_noGuideEmbedding &
# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=0.5 --model_dir=model_alpha_1_8_cond32_mlabTheta_05_2 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=1 --model_dir=model_alpha_1_8_cond32_mlabTheta_1_2 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=2 --model_dir=model_alpha_1_8_cond32_mlabTheta_2_2 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=3 --model_dir=model_alpha_1_8_cond32_mlabTheta_3_2 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=4 --model_dir=model_alpha_1_8_cond32_mlabTheta_4_2 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=5 --model_dir=model_alpha_1_8_cond32_mlabTheta_5_2 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=6 --model_dir=model_alpha_1_8_cond32_mlabTheta_6_2 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=7 --model_dir=model_alpha_1_8_cond32_mlabTheta_7_2 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=8 --model_dir=model_alpha_1_8_cond32_mlabTheta_8_2 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=9 --model_dir=model_alpha_1_8_cond32_mlabTheta_9_2 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=10 --model_dir=model_alpha_1_8_cond32_mlabTheta_10_2 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=11 --model_dir=model_alpha_1_8_cond32_mlabTheta_11_2 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=12 --model_dir=model_alpha_1_8_cond32_mlabTheta_12_2 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=13 --model_dir=model_alpha_1_8_cond32_mlabTheta_13_2 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=14 --model_dir=model_alpha_1_8_cond32_mlabTheta_14_2 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=15 --model_dir=model_alpha_1_8_cond32_mlabTheta_15_2 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --model_type=CVAE_multiLab --n_cond=32 --alpha=1.85 --theta=16 --model_dir=model_alpha_1_8_cond32_mlabTheta_16_2 &



# python RunModels.py --model_type=DenoisingAE_model --n_cond=32 --model_dir=model_DenoisingAE_multiLab_cond32

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1 --model_dir=model_alpha_1_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.1 --model_dir=model_alpha_1_1_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.2 --model_dir=model_alpha_1_2_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.3 --model_dir=model_alpha_1_3_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.4 --model_dir=model_alpha_1_4_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.5 --model_dir=model_alpha_1_5_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.6 --model_dir=model_alpha_1_6_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.7 --model_dir=model_alpha_1_7_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.8 --model_dir=model_alpha_1_8_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.85 --model_dir=model_alpha_1_85_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=1.9 --model_dir=model_alpha_1_9_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.0 --model_dir=model_alpha_2_0_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.1 --model_dir=model_alpha_2_1_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.2 --model_dir=model_alpha_2_2_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.3 --model_dir=model_alpha_2_3_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.4 --model_dir=model_alpha_2_4_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.5 --model_dir=model_alpha_2_5_second &





# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.6 --model_dir=model_alpha_2_6_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.7 --model_dir=model_alpha_2_7_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.8 --model_dir=model_alpha_2_8_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.9 --model_dir=model_alpha_2_9_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=3.0 --model_dir=model_alpha_3_0_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=3.1 --model_dir=model_alpha_3_1_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.2 --model_dir=model_alpha_3_2_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.3 --model_dir=model_alpha_3_3_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.4 --model_dir=model_alpha_3_4_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.5 --model_dir=model_alpha_3_5_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=3.6 --model_dir=model_alpha_3_6_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=3.7 --model_dir=model_alpha_3_7_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=3.8 --model_dir=model_alpha_3_8_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=3.9 --model_dir=model_alpha_3_9_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=4.0 --model_dir=model_alpha_4_0_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=4.1 --model_dir=model_alpha_4_1_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=4.2 --model_dir=model_alpha_4_2_second &



# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=0.9 --model_dir=model_alpha_0_9_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=0.8 --model_dir=model_alpha_0_8_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=0.7 --model_dir=model_alpha_0_7_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=0.6 --model_dir=model_alpha_0_6_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=0.5 --model_dir=model_alpha_0_5_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=0.4 --model_dir=model_alpha_0_4_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=0.3 --model_dir=model_alpha_0_3_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=0.2 --model_dir=model_alpha_0_2_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=0.1 --model_dir=model_alpha_0_1_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=0 --model_dir=model_alpha_0_second &







# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=0.5 --model_dir=model_alpha_0_5_additive &


# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=0.6 --model_dir=model_alpha_0_6_additive &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=0.7 --model_dir=model_alpha_0_7_additive &


# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=0.8 --model_dir=model_alpha_0_8_additive &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=0.9 --model_dir=model_alpha_0_9_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1 --model_dir=model_alpha_1_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.1 --model_dir=model_alpha_1_1_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.2 --model_dir=model_alpha_1_2_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.3 --model_dir=model_alpha_1_3_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.4 --model_dir=model_alpha_1_4_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=1.5 --model_dir=model_alpha_1_5_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.6 --model_dir=model_alpha_1_6_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.7 --model_dir=model_alpha_1_7_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.8 --model_dir=model_alpha_1_8_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=1.85 --model_dir=model_alpha_1_85_additive &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=1.9 --model_dir=model_alpha_1_9_additive &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.0 --model_dir=model_alpha_2_0_additive &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.1 --model_dir=model_alpha_2_1_additive &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=2.2 --model_dir=model_alpha_2_2_additive &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.3 --model_dir=model_alpha_2_3_additive &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.4 --model_dir=model_alpha_2_4_additive &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=2.5 --model_dir=model_alpha_2_5_additive &


#export CUDA_VISIBLE_DEVICES=0"
# python RunModels.py  --alpha=2.6 --model_dir=model_alpha_2_6_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.7 --model_dir=model_alpha_2_7_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.8 --model_dir=model_alpha_2_8_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=2.9 --model_dir=model_alpha_2_9_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=3.0 --model_dir=model_alpha_3_0_additive &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=3.1 --model_dir=model_alpha_3_1_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.2 --model_dir=model_alpha_3_2_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.3 --model_dir=model_alpha_3_3_additive &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=3.4 --model_dir=model_alpha_3_4_additive &



# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=4.3 --model_dir=model_alpha_4_3_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=4.4 --model_dir=model_alpha_4_4_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=4.5 --model_dir=model_alpha_4_5_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=4.6 --model_dir=model_alpha_4_6_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=4.7 --model_dir=model_alpha_4_7_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=4.8 --model_dir=model_alpha_4_8_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=4.9 --model_dir=model_alpha_4_9_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=5.0 --model_dir=model_alpha_5_0_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=5.1 --model_dir=model_alpha_5_1_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=5.2 --model_dir=model_alpha_5_2_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=5.3 --model_dir=model_alpha_5_3_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=5.4 --model_dir=model_alpha_5_4_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=5.5 --model_dir=model_alpha_5_5_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=5.6 --model_dir=model_alpha_5_6_second &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py  --alpha=5.7 --model_dir=model_alpha_5_7_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py  --alpha=5.8 --model_dir=model_alpha_5_8_second &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py  --alpha=5.9 --model_dir=model_alpha_5_9_second &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py  --alpha=6.0 --model_dir=model_alpha_6_0_second &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=0.2 --model_dir=model_alpha_0_2_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=0.5 --model_dir=model_alpha_0_5_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=0.7 --model_dir=model_alpha_0_7_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=1.0 --model_dir=model_alpha_1_0_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=2.5 --model_dir=model_alpha_2_5_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=3.0 --model_dir=model_alpha_3_0_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=3.5 --model_dir=model_alpha_3_5_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=4.0 --model_dir=model_alpha_4_0_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=4.5 --model_dir=model_alpha_4_5_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=5.0 --model_dir=model_alpha_5_0_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad"  --alpha=5.5 --model_dir=model_alpha_5_5_K2K3_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3_K1K3.h5ad" --alpha=6.0 --model_dir=model_alpha_6_0_K2K3_K1K3_6 &





# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=0.2 --model_dir=model_alpha_0_2_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=0.5 --model_dir=model_alpha_0_5_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=0.7 --model_dir=model_alpha_0_7_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=1.0 --model_dir=model_alpha_1_0_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=2.5 --model_dir=model_alpha_2_5_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=3.0 --model_dir=model_alpha_3_0_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=3.5 --model_dir=model_alpha_3_5_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=4.0 --model_dir=model_alpha_4_0_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=4.5 --model_dir=model_alpha_4_5_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=5.0 --model_dir=model_alpha_5_0_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad"  --alpha=5.5 --model_dir=model_alpha_5_5_K2K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K2K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K2K3.h5ad" --alpha=6.0 --model_dir=model_alpha_6_0_K2K3_6 &



# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=0.2 --model_dir=model_alpha_0_2_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=0.5 --model_dir=model_alpha_0_5_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="0"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=0.7 --model_dir=model_alpha_0_7_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=1.0 --model_dir=model_alpha_1_0_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=2.5 --model_dir=model_alpha_2_5_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=3.0 --model_dir=model_alpha_3_0_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=3.5 --model_dir=model_alpha_3_5_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="3"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=4.0 --model_dir=model_alpha_4_0_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="1"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=4.5 --model_dir=model_alpha_4_5_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=5.0 --model_dir=model_alpha_5_0_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad"  --alpha=5.5 --model_dir=model_alpha_5_5_K1K3_6 &

# export CUDA_VISIBLE_DEVICES="2"
# python RunModels.py --trainfile="./Notebooks/CombinatorialPerturbations/dataset/training_K1K3.h5ad" --valfile="./Notebooks/CombinatorialPerturbations/dataset/validation_K1K3.h5ad" --alpha=6.0 --model_dir=model_alpha_6_0_K1K3_6 &









export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=0 --model_dir=model_alpha_0_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=0.1 --model_dir=model_alpha_0_1_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=0.2 --model_dir=model_alpha_0_2_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=0.3 --model_dir=model_alpha_0_3_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=0.4 --model_dir=model_alpha_0_4_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=0.5 --model_dir=model_alpha_0_5_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=0.6 --model_dir=model_alpha_0_6_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=0.7 --model_dir=model_alpha_0_7_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=0.8 --model_dir=model_alpha_0_8_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=0.9 --model_dir=model_alpha_0_9_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=1 --model_dir=model_alpha_1_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=1.2 --model_dir=model_alpha_1_2_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=1.4 --model_dir=model_alpha_1_4_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=1.6 --model_dir=model_alpha_1_6_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=1.8 --model_dir=model_alpha_1_8_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=2.0 --model_dir=model_alpha_2_0_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=2.2 --model_dir=model_alpha_2_2_v7 &

export CUDA_VISIBLE_DEVICES="3"
python RunModels.py  --alpha=2.4 --model_dir=model_alpha_2_4_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=2.6 --model_dir=model_alpha_2_6_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=2.8 --model_dir=model_alpha_2_8_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=3.0 --model_dir=model_alpha_3_0_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=3.2 --model_dir=model_alpha_3_2_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=3.4 --model_dir=model_alpha_3_4_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=3.6 --model_dir=model_alpha_3_6_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=3.8 --model_dir=model_alpha_3_8_v7 &

export CUDA_VISIBLE_DEVICES="3"
python RunModels.py  --alpha=4.0 --model_dir=model_alpha_4_0_v7 &

export CUDA_VISIBLE_DEVICES="3"
python RunModels.py  --alpha=4.2 --model_dir=model_alpha_4_2_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=4.4 --model_dir=model_alpha_4_4_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=4.6 --model_dir=model_alpha_4_6_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=4.8 --model_dir=model_alpha_4_8_v7 &

export CUDA_VISIBLE_DEVICES="1"
python RunModels.py  --alpha=5.0 --model_dir=model_alpha_5_0_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=5.2 --model_dir=model_alpha_5_2_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=5.4 --model_dir=model_alpha_5_4_v7 &

export CUDA_VISIBLE_DEVICES="3"
python RunModels.py  --alpha=5.6 --model_dir=model_alpha_5_6_v7 &

export CUDA_VISIBLE_DEVICES="0"
python RunModels.py  --alpha=5.8 --model_dir=model_alpha_5_8_v7 &

export CUDA_VISIBLE_DEVICES="2"
python RunModels.py  --alpha=6.0 --model_dir=model_alpha_6_0_v7 &
