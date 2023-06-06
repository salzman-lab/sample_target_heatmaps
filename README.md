Here is a script for generating sample-target heatmaps. This is adapted from Tavor’s code used during the SPLASH-1 revision to plot heatmaps with metadata labels and target sequence composition.
Uploading to GitHub shortly; here is the location on Sherlock.
/oak/stanford/groups/horence/george/sample_heatmaps.py
Usage:
Do source /oak/stanford/groups/horence/george/dog/bin/activate
Do python3 /oak/stanford/groups/horence/george/sample_heatmaps.py {dsName} {satcFolder} {outFolder} {anchorFile}
dsName an identifier used to prefix the output heatmap filenames.
satcFolder a path to the folder containing satc dump files (this path must end in /)
outFolder a path to a folder created by this script to store output heatmaps
anchorFile a path to a one-column, space or tab-delimited file containing anchors (file should not have a header)
