import numpy as np
import os
import glob
from tqdm import tqdm
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import seaborn as sns
import sys

dsName = sys.argv[1]
satcFolder= sys.argv[2]
outFolder = sys.argv[3]
anchorFile = sys.argv[4]
runSATC = True

### Parse satc files to normal files
def parseSATC():
    print('parsing SATC')
    Path(outFolder+'/satc_unpacked/').mkdir(parents=True, exist_ok=True)
    for fname in tqdm(glob.glob(satcFolder+'/*result.bin*.satc')):
        outFile = outFolder+'/satc_unpacked/'+fname.split('.')[-2]+'.dump'
        cmd=f"/oak/stanford/groups/horence/george/RNOMAD_0.3.8/bin/satc_dump --anchor_list {anchorFile} {fname} {outFile}"
        print(cmd,flush=True)
        os.system(cmd)
        
### Generate counts dataframe from dumped files
def generateCtsDf():
    dfArr = []
    for fname in tqdm(glob.glob(outFolder+'/satc_unpacked/*.dump')):
        dfArr.append(pd.read_csv(fname,names=['id','anchor','target','counts'],sep='\t'))
    
    ctsDf = pd.concat(dfArr)

    id_to_sample_mapping = pd.read_csv(satcFolder+'/sample_name_to_id.mapping.txt',names=['sample','id'],sep=' ')

    ctsDf = pd.merge(ctsDf,id_to_sample_mapping).drop(columns='id')
    ctsDf = ctsDf.groupby(['anchor','target','sample']).counts.sum().reset_index()
    ctsDf.to_csv(outFolder+'/countsDf.tsv',sep='\t')
    return ctsDf

### Report the progress in the Slurm output file.
print('running', flush=True)

statusStr = "Dataset: {}\nAnchor file: {}\nSATC folder: {}\nOut folder: {}".format(
dsName, anchorFile,satcFolder,outFolder
)
print(statusStr, flush=True)

### Unpack SATC files and use them to generate a table having columns: anchor, target, sample, count. 
if runSATC:
    parseSATC()
ctsDf = generateCtsDf()

### Pivot the resulting table so it is indexed in anchor and target, having columns for each sample, and values for the anchor-target sample counts. 
pivot1 = pd.pivot_table(ctsDf, values='counts',index=['anchor','target'],columns='sample').fillna(0)

### For each anchor in the resulting file:
for anchor in ctsDf['anchor'].unique():
    
    ### Subset the counts matrix to just this anchor. 
    pivot = pivot1.loc[anchor]
    
    ### Sort by row sum and remove rows having sum < 5. 
    pivot = pivot.assign(sum=pivot.sum(axis=1)).sort_values(by='sum',ascending=False)[pivot[pivot.columns[-1]]>4].iloc[:,:-1]
    
    ### Sort by column sum and remove columns having sum < 5. 
    p = pivot.sum(axis=0).reset_index().sort_values(by=0,ascending=False)
    p = p[p[0]>4]
    pivot = pivot[list(p['sample'])]
    
    ### If there exist such rows and columns (having sums > 4), then generate a heatmap. 
    if pivot.shape[0]:
        fig, ax = plt.subplots(figsize=(12,12))
        sns.heatmap(pivot, annot=True, ax=ax, annot_kws={'rotation': 90})
        plt.tight_layout()
        plt.savefig(outFolder+'/'+dsName+'_'+anchor+'.pdf')
        plt.close()
