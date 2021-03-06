'''
Author: Yingjie Peng
Date: 2022-03-31 21:54:41
LastEditTime: 2022-04-07 14:39:18
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/func/func.py

'''
import logging
from multiprocessing import Pool
import pandas as pd 
import numpy as np

from nilearn import image
from ..utils import calculate_S, calculate_FD,normalize,pearson_coef,spearman_coef
from ..bids import RunQC,BIDSQC
import os
from tqdm import tqdm 
from multiprocessing import Pool
import warnings

warnings.filterwarnings('ignore')

class HeadMotionQC(object):
    def __init__(self,head_motion_matrix:np.ndarray,fd=None,fd_kind='normal') -> None:
        """init HeadMotion

        Args:
            head_motion_matrix (np.ndarray): head_motion_matrix

            fd (np.ndarray, optional): Defaults to None.
            
            fd_kind(str): ['normal' or 'strict']  default strict

        Raises:
            ValueError: head motion shape is not (?,6)
        """
        if head_motion_matrix.shape[-1] != 6:
            raise ValueError("head motion shape is not (?,6)")
        if fd_kind not in ['normal','strict']:
            raise ValueError("kind must be normal or strict")
        self.s = calculate_S(head_motion_matrix[:,0],head_motion_matrix[:,1],head_motion_matrix[:,2])
        if fd is None:
            self.fd = calculate_FD(head_motion_matrix)
        else:
            # nan replace with 0
            self.fd = fd.copy()
            self.fd[np.isnan(self.fd)] = 0
        self.fd_kind = fd_kind

    @property
    def features(self):
        """get features 

        Returns:
            dict : mean and max of s and fd
        """
        data = {'mean-s':self.s.mean(),'max-s':self.s.max(),'mean-fd':self.fd.mean(),
                    'max-fd':self.fd.max()
                    }
        if self.fd_kind =='normal':
            return  data
        else:
            # if kind =='strict' add fd>0.5mm or not the 20% fd >0.20 mm
            data['fd>0.5mm'] = (self.fd>0.5).sum()

            data['fd>0.2mm(%)'] = (self.fd>0.2).sum()/len(self.fd)
            return data

class FuncImageQC(object):
    def __init__(self,ref_path) -> None:
        """init 

        Args:
            ref_path (str): fmri ref path
        """
        self.ref_path = ref_path
        self.t1_path = os.path.dirname(os.path.dirname(__file__))+'/template/MNI152_T1_2mm.nii.gz'
    @property
    def features(self):
        if len(self.ref_path) == 0:
            logging.warning("{} not exists".format(self.ref_path))
            return {'pearson':np.nan,'spearman':np.nan}
        t1_img = image.resample_to_img(self.t1_path,self.ref_path)
        t1_img_data = np.asarray(t1_img.dataobj).flatten()
        ref_img_data = np.asarray(image.load_img(self.ref_path).dataobj).flatten()
        t1_img_data = normalize(t1_img_data)
        ref_img_data = normalize(ref_img_data)
        pearson = pearson_coef(t1_img_data,ref_img_data)
        spearman = spearman_coef(t1_img_data,ref_img_data)
        return {'pearson':pearson,'spearman':spearman}

class fMRIprepFuncRunQC(object):
    def __init__(self,run_qc:RunQC,fd_kind='normal') -> None:
        """init
            
            Args:
                run_qc (RunQC): run_qc
                fd_kind(str): normal or strict default normal
        """
        self.run_qc = run_qc
        self.fd_kind = fd_kind
    
    @property
    def features(self):
        """get features
        
        Returns:
            dict: features
        """
        func_img = FuncImageQC(self.run_qc.func_file)

        info = {
            "subject_id":self.run_qc.subject_id,
            'session':self.run_qc.session,
            'run':self.run_qc.run,
            'task':self.run_qc.task,
        }
        info.update(func_img.features)
        if len(self.run_qc.func_tsv)==0:
            logging.warning("{} not exists".format(self.run_qc.func_tsv))
            data = {'mean-s':np.nan,'max-s':np.nan,'mean-fd':np.nan,'max-fd':np.nan}
            # add strict type
            if self.fd_kind =='strict':
                data['fd>0.5mm'] = np.nan
                data['fd>0.2mm(%)'] = np.nan
            info.update(data)
            return info
        
        df = pd.read_csv(self.run_qc.func_tsv,sep='\t')
        head_motion_matrix = df[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']].values
        fd = df['framewise_displacement'].values
        head_motion_qc = HeadMotionQC(head_motion_matrix,fd,self.fd_kind)
        info.update(head_motion_qc.features)
        return info

class fMRIprepFuncFeature(object):
    def __init__(self,bids_qc:BIDSQC,n_process=40,fd_kind='normal') -> None:
        self.bids_qc = bids_qc
        self.n_process = 40
        self.fd_kind = fd_kind
    def _parser_run_(self,run_qc:RunQC):
        return fMRIprepFuncRunQC(run_qc,self.fd_kind).features
    
    @property
    def features(self):
        run_qcs =[]
        for subject in  self.bids_qc.subjects:
            for session in subject.sessions:
                for run in session.runs:
                    run_qcs.append(run)
        with Pool(self.n_process) as p:
            features = list(tqdm(p.imap(self._parser_run_,run_qcs),total=len(run_qcs),desc='fmri runs qc:'))
        return pd.DataFrame(features)