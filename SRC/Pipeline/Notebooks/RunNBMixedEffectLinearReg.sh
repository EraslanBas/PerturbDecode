#!/bin/bash



for ((i=0;i<450;i+=50)); 
do 
  papermill -p setIndex_1 $i ./13_NBMixedEffectLinearReg ./3_NBMixedEffectLinearReg_${i}.ipynb &

done