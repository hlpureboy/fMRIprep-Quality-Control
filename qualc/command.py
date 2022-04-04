'''
Author: Yingjie Peng
Date: 2022-04-04 13:20:39
LastEditTime: 2022-04-04 14:58:02
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/command.py

'''
import argparse
import logging
import os
from matplotlib import pyplot as plt

from .qc import FuncQC,MRIQC,FreeSurferQC
from .func import fMRIprepFuncFeature
from .freesurfer import fMRIprepFreesurferFeature
from . import __version__
from .bids import BIDSQC

def paser_args():
    parser = argparse.ArgumentParser(description='QC command version {}'.format(__version__))



    parser.add_argument('-v', '--verbose', action='store_true',help='verbose')
    parser.add_argument('-fmriprep','--fmriprep_path',required=True,type=str, help='path to fmriprep')
    parser.add_argument('-o','--output_path',required=True,type=str, help='path to output')
    parser.add_argument('--func', action='store_true', help='func qc')
    parser.add_argument('--fs', action='store_true', help='fs qc')
    # fd threshold
    parser.add_argument('--fd_threshold',type=float,default=0.5, help='fd threshold, default 0.5')
    # fs threshold
    parser.add_argument('--fs_threshold',type=int,default=10, help='fs threshold, default 10')
    # fs level
    parser.add_argument('--fs_level',type=str,default='group', help='fs level [group,prior], default group')
    # tsne 
    parser.add_argument('--tsne', action='store_true', help='tsne plot outline')
    # plot type
    parser.add_argument('--plot_type',type=str,default='distribution', help='plot type [distribution,bar],default distribution')
    return parser


def func_qc(bids,fd_threshold,out_path,plot_type='distribution',tsne=False):   
    features = fMRIprepFuncFeature(bids).features
    features.to_csv(os.path.join(out_path,'func_qc.csv'),index=False)
    func_qc = FuncQC(features,drop_columns=['session','run','task'])
    # check head motion
    fig,ax = plt.subplots(1,1,figsize=(8,4))
    func_qc.check_head_motion(threshold=fd_threshold,ax=ax,plot_type=plot_type)
    fig.savefig(os.path.join(out_path,'func_head_motion.png'))
    if tsne:
        func_qc.tsne()
        fig,ax = plt.subplots(1,1,figsize=(8,8))
        func_qc.plot_anomaly_subject(ax=ax)
        fig.savefig(os.path.join(out_path,'func_anomaly_subject.png'))
    return func_qc.threshold_delete_ids

def fs_qc(fs_path,bids,fs_threshold,level,out_path,plot_type='distribution',tsne=False):
    features = fMRIprepFreesurferFeature(fs_path,bids).features
    features.to_csv(os.path.join(out_path,'fs_qc.csv'),index=False)
    fs_qc = FreeSurferQC(features,level=level)
    fig,ax = plt.subplots(1,1,figsize=(8,4))
    fs_qc.detect_aseg_stats(fs_threshold,ax=ax,plot_type=plot_type)
    fig.savefig(os.path.join(out_path,'fs_aseg_stats.png'))
    fs_qc.detect_aseg_stats_df.to_csv(os.path.join(out_path,'fs_aseg_stats.csv'),index=False)
    if tsne:
        fs_qc.tsne()
        fig,ax = plt.subplots(1,1,figsize=(8,8))
        fs_qc.plot_anomaly_subject(ax=ax)
        fig.savefig(os.path.join(out_path,'fs_anomaly_subject.png'))
        
    return fs_qc.threshold_delete_ids



def main():
    paser = paser_args()
    args = paser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    bids_path = os.path.join(args.fmriprep_path,'fmriprep')
    fs_path = os.path.join(args.fmriprep_path,'freesurfer')
    out_path = args.output_path
    os.makedirs(out_path,exist_ok=True)

    bids = BIDSQC(bids_path)
    ids = []
    if args.func:
        _ids = func_qc(bids,args.fd_threshold,out_path,args.plot_type,args.tsne)
        logging.info('func qc delete ids: {}'.format(_ids))
        ids.extend(_ids)
    if args.fs:
        _ids = fs_qc(fs_path,bids,args.fs_threshold,args.fs_level,out_path,args.plot_type,args.tsne)
        logging.info('fs qc delete ids: {}'.format(_ids))
        ids.extend(_ids)
    with open(os.path.join(out_path,'outlier_subject_ids'),'w') as f:
        f.write('\n'.join(ids))

if __name__ == '__main__':
    main()
