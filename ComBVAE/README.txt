#### scripts to run in order ######

1) python RunModels.py  --alpha=0.5 --model_dir=model_0 &

2) python InspectReconstruction.py --model_dir=model_0 &

3) python GenerateCells.py --model_dir=model_0 &

4) python ComputeLogFCOfPredictionsAll.py --model_dir=model_0 &



