Here is a script for generating sample-target heatmaps. This is a simplification of Tavor Baharav’s code used during the SPLASH-1 revision to perform SATC unpacking, to plot heatmaps with metadata labels, to visualize target sequence composition, and to report SPLASH metrics.

Usage: <br> <br>
Do `source /oak/stanford/groups/horence/george/dog/bin/activate` <br>
Do `python3 /oak/stanford/groups/horence/george/sample_heatmaps.py {dsName} {satcFolder} {outFolder} {anchorFile}` <br> <br>
`dsName` is an identifier used to prefix the output heatmap filenames .<br>
`satcFolder` is a path to the folder containing satc dump files (this path must end in /) <br>
`outFolder` is a path to a folder created by this script to store output heatmaps <br>
`anchorFile` s a path to a one-column, space or tab-delimited file containing anchors (file should not have a header) <br>
