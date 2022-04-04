'''
Author: Yingjie Peng
Date: 2022-04-01 09:46:31
LastEditTime: 2022-04-04 13:03:29
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/mri/mri.py

'''

from nilearn import plotting, image,masking
from ..bids import SessionQC,BIDSQC
import os
import numpy as np
from tqdm import tqdm 
from multiprocessing import Pool
import pandas as pd

class GM_Voxel(object):
    def __init__(self,t1_mni152_path,t1_mni152_brain_mask):
        self.t1_mni152_path = t1_mni152_path
        self.t1_mni152_brain_mask = t1_mni152_brain_mask
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.spm_whole_brain_path = os.path.join(base_path,'template','spm_whole_brain.nii.gz')
        self.spm_gm_mask_path = os.path.join(base_path,'template','GM_brain.nii.gz')
    @property
    def features(self):
        if len(self.t1_mni152_path) == 0:
            d  = {}
            for key in np.unique(np.asarrray(image.load_img(self.spm_gm_mask_path).dataobj))[1:]:
                d[key] = np.nan
            return d
        brain_data = masking.apply_mask(self.t1_mni152_path,self.t1_mni152_brain_mask)
        brain_img = masking.unmask(brain_data,self.t1_mni152_brain_mask)
        brain_img_res = image.resample_to_img(brain_img,self.spm_whole_brain_path,interpolation='linear')
        brain_img_res_data = np.asarray(brain_img_res.dataobj)
        gm_data = np.asarray(image.load_img(self.spm_gm_mask_path).dataobj)
        info = {}
        for roi_index  in np.unique(gm_data)[1:]:
            info[roi_index] = brain_img_res_data[gm_data == roi_index].mean()
        return info

class fMRIprepMRISessionQC(object):
    def __init__(self,session_qc:SessionQC):
        self.session_qc = session_qc
    
    @property
    def features(self):
        
        features = GM_Voxel(self.session_qc.anat_t1_file,self.session_qc.anat_brain_mask).features
        features['subject_id'] = self.session_qc.subject_id
        features['session'] = self.session_qc.session
        return features
class fMRIprepMRIFeature(object):
    def __init__(self,bids_qc:BIDSQC,n_process=40) -> None:
        self.bids_qc = bids_qc
        self.n_process = n_process
    
    def _parser_run_(self,session_qc:SessionQC):
        return fMRIprepMRISessionQC(session_qc).features
    @property
    def features(self):
        sessions = []
        for subject in self.bids_qc.subjects:
            for session in subject.sessions:
                sessions.append(session)
        with Pool(self.n_process) as p:
            features = list(tqdm(p.imap(self._parser_run_,sessions),total=len(sessions),desc='mri bids qc'))
        return pd.DataFrame(features)