'''
Author: Yingjie Peng
Date: 2022-03-31 21:54:25
LastEditTime: 2022-04-03 18:02:41
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/bids.py

'''
import logging
import os
from glob import glob
from tqdm import tqdm 
from multiprocessing import Pool

class BIDSQC:
    def __init__(self, bids_dir,n_process=40):
        self.bids_dir = bids_dir
        self.subjects = self.get_subjects(n_process=n_process)
    def _parser_subject_(self,subject_id):
        return SubjectQC(self.bids_dir,subject_id)

    def get_subjects(self,n_process=40):
        subject_ids = []
        _reg_path_ = '{}/sub-*'.format(self.bids_dir)
        for subject_path in glob(_reg_path_):
            if os.path.isdir(subject_path):
                subject_ids.append(subject_path.split('/')[-1])
        with Pool(n_process) as p:
            subjects = list(tqdm(p.imap(self._parser_subject_,subject_ids),total=len(subject_ids),desc='load bids'))    
        
        return subjects

class SubjectQC():
    def __init__(self, bids_dir, subject_id):
        self.bids_dir = bids_dir
        self.subject_id = subject_id
        self.sessions = self.get_session_list()
    def get_session_list(self):
        session_list = []
        fun_flag =False
        try:
            for session in os.listdir(os.path.join(self.bids_dir, '{}'.format(self.subject_id))):
                if session == 'func':
                    fun_flag = True
                if os.path.isdir(os.path.join(self.bids_dir, '{}'.format(self.subject_id), session)) and session.startswith('ses-'):
                    session_list.append(SessionQC(self.bids_dir, self.subject_id, session))
                    
            if len(session_list) == 0:
                logging.warning('No session found for subject {}'.format(self.subject_id))
                if fun_flag:
                    logging.warning('But funcional data found for subject {}'.format(self.subject_id))
                    return [SessionQC(self.bids_dir, self.subject_id, '')]
        except Exception as e:
            logging.warning("parser seesion error")
        return session_list

class SessionQC():
    def __init__(self, bids_dir, subject_id, session):
        self.session = session
        self.subject_id = subject_id
        self.bids_dir = bids_dir
        self.runs = self.get_runs()
    def get_runs(self):
        runs = []
        _runs = []
        try:
            for file in os.listdir(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session,'func')):
                run_name = None
                for name in file.split('_'):
                    if name.startswith('run'):
                        run_name = name
                    if name.startswith('task'):
                        task_name = name
                    
                        runs.append((run_name, task_name))
            
            for run_name, task_name in set(runs):
                _runs.append(RunQC(self.bids_dir, self.subject_id, self.session, run_name,task_name))
        except Exception as e:
            logging.warning("parser run error")
        return _runs
    @property
    def anat_t1_file(self):
        files = glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'anat', '*space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz'))
        if len(files) == 0:
            return ""   
        else:
            return files[0]
        #return glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'anat', '*space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz'))[0]
    @property
    def anat_brain_mask(self):
        files = glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'anat', '*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'))
        if len(files) == 0:
            return ""
        else:
            return files[0]
        # return glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'anat', '*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'))[0]

class RunQC():
    def __init__(self, bids_dir, subject_id, session, run,task):
        self.run = run
        self.subject_id = subject_id
        self.session = session
        self.bids_dir = bids_dir
        self.task = task
        self.fiel_first_name = subject_id+'_'
        if len(session)!=0:
            self.fiel_first_name += session+'_'
        if run is not None:
            self.fiel_first_name += run+'_'
        self.fiel_first_name += task +'_'
    @property
    def func_file(self):
        files = glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'func', '*{}*space-MNI152NLin2009cAsym_boldref.nii.gz'.format(self.fiel_first_name)))
        if len(files) == 0:
            return ""
        return files[0]
    @property
    def func_tsv(self):
        files = glob(os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'func', '*{}*desc-confounds_timeseries.tsv'.format(self.fiel_first_name)))
        if len(files) == 0:
            return ""
        return files[0]
        #return os.path.join(self.bids_dir, '{}'.format(self.subject_id), self.session, 'func', self.fiel_first_name+'desc-confounds_timeseries.tsv')


# bids = BIDSQC('/localdata/data/dataset/hospital/xiehe/derivative_GE750/fmriprep')
# print(bids.subjects[0].session_list[0].runs[0].func_file)
# print(bids.subjects[0].session_list[0].anat_t1_file)
# print(bids.subjects[0].session_list[0].anat_brain_mask)
# print(bids.subjects[0].session_list[0].runs[0].func_tsv)