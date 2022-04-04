<!--
 * @Author: Yingjie Peng
 * @Date: 2022-04-04 13:10:09
 * @LastEditTime: 2022-04-04 14:59:09
 * @LastEditors: Yingjie Peng
 * @Description: Define by yourself
 * @FilePath: /QC/REAME.md
 * 
-->
# Quality Control(qualc)
一款为fmriprep生成的质量控制系统，可以帮助你快速的检查质量，并且可以帮助你更好的控制质量。
## 安装
```bash
python setup.py install
```
## 命令行使用
```bash
qualc -h

usage: qualc [-h] [-v] -fmriprep FMRIPREP_PATH -o OUTPUT_PATH [--func] [--fs]
             [--fd_threshold FD_THRESHOLD] [--fs_threshold FS_THRESHOLD]
             [--fs_level FS_LEVEL] [--tsne] [--plot_type PLOT_TYPE]

QC command version 0.0.1

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose
  -fmriprep FMRIPREP_PATH, --fmriprep_path FMRIPREP_PATH
                        path to fmriprep
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        path to output
  --func                func qc
  --fs                  fs qc
  --fd_threshold FD_THRESHOLD
                        fd threshold, default 0.5
  --fs_threshold FS_THRESHOLD
                        fs threshold, default 10
  --fs_level FS_LEVEL   fs level [group,prior], default group
  --tsne                tsne plot outline
  --plot_type PLOT_TYPE
                        plot type [distribution,bar],default distribution
```
## python使用
```python
from qualc import FuncQC,MRIQC,FreeSurferQC
from qualc.func import fMRIprepFuncFeature
from qualc.mri import fMRIprepMRIFeature
from qualc.freesurfer import fMrepFreesurferFeature
from qualc.bids import BIDSQC


# 不想写惹

```
