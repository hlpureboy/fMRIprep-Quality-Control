'''
Author: Yingjie Peng
Date: 2022-04-03 20:44:11
LastEditTime: 2022-04-04 13:04:14
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/freesurfer/freesurfer.py

'''
import os
import csv
import numpy as np
import pandas as pd
from ..bids import SubjectQC,BIDSQC
import logging 
def readAsegStats(path_aseg_stats):
    """
    A function to read aseg.stats files.

    """

    # read file
    with open(path_aseg_stats) as stats_file:
        aseg_stats = stats_file.read().splitlines()

    # initialize
    aseg = dict()

    # read measures
    for line in aseg_stats:
        if '# Measure BrainSeg,' in line:
            aseg.update({'BrainSeg' : float(line.split(',')[3])})
        elif '# Measure BrainSegNotVent,' in line:
            aseg.update({'BrainSegNotVent' : float(line.split(',')[3])})
        elif '# Measure BrainSegNotVentSurf,' in line:
            aseg.update({'BrainSegNotVentSurf' : float(line.split(',')[3])})
        elif '# Measure VentricleChoroidVol,' in line:
            aseg.update({'VentricleChoroidVol' : float(line.split(',')[3])})
        elif '# Measure lhCortex,' in line:
            aseg.update({'lhCortex' : float(line.split(',')[3])})
        elif '# Measure rhCortex,' in line:
            aseg.update({'rhCortex' : float(line.split(',')[3])})
        elif '# Measure Cortex,' in line:
            aseg.update({'Cortex' : float(line.split(',')[3])})
        elif '# Measure lhCerebralWhiteMatter,' in line:
            aseg.update({'lhCerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure rhCerebralWhiteMatter,' in line:
            aseg.update({'rhCerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure CerebralWhiteMatter,' in line:
            aseg.update({'CerebralWhiteMatter' : float(line.split(',')[3])})
        elif '# Measure SubCortGray,' in line:
            aseg.update({'SubCortGray' : float(line.split(',')[3])})
        elif '# Measure TotalGray,' in line:
            aseg.update({'TotalGray' : float(line.split(',')[3])})
        elif '# Measure SupraTentorial,' in line:
            aseg.update({'SupraTentorial' : float(line.split(',')[3])})
        elif '# Measure SupraTentorialNotVent,' in line:
            aseg.update({'SupraTentorialNotVent' : float(line.split(',')[3])})
        elif '# Measure SupraTentorialNotVentVox,' in line:
            aseg.update({'SupraTentorialNotVentVox' : float(line.split(',')[3])})
        elif '# Measure Mask,' in line:
            aseg.update({'Mask' : float(line.split(',')[3])})
        elif '# Measure BrainSegVol-to-eTIV,' in line:
            aseg.update({'BrainSegVol_to_eTIV' : float(line.split(',')[3])})
        elif '# Measure MaskVol-to-eTIV,' in line:
            aseg.update({'MaskVol_to_eTIV' : float(line.split(',')[3])})
        elif '# Measure lhSurfaceHoles,' in line:
            aseg.update({'lhSurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure rhSurfaceHoles,' in line:
            aseg.update({'rhSurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure SurfaceHoles,' in line:
            aseg.update({'SurfaceHoles' : float(line.split(',')[3])})
        elif '# Measure EstimatedTotalIntraCranialVol,' in line:
            aseg.update({'EstimatedTotalIntraCranialVol' : float(line.split(',')[3])})
        elif 'Left-Lateral-Ventricle' in line:
            aseg.update({'Left-Lateral-Ventricle' : float(line.split()[3])})
        elif 'Left-Inf-Lat-Vent' in line:
            aseg.update({'Left-Inf-Lat-Vent' : float(line.split()[3])})
        elif 'Left-Cerebellum-White-Matter' in line:
            aseg.update({'Left-Cerebellum-White-Matter' : float(line.split()[3])})
        elif 'Left-Cerebellum-Cortex' in line:
            aseg.update({'Left-Cerebellum-Cortex' : float(line.split()[3])})
        elif 'Left-Thalamus-Proper' in line:
            aseg.update({'Left-Thalamus-Proper' : float(line.split()[3])})
        elif 'Left-Caudate' in line:
            aseg.update({'Left-Caudate' : float(line.split()[3])})
        elif 'Left-Putamen' in line:
            aseg.update({'Left-Putamen' : float(line.split()[3])})
        elif 'Left-Pallidum' in line:
            aseg.update({'Left-Pallidum' : float(line.split()[3])})
        elif '3rd-Ventricle' in line:
            aseg.update({'3rd-Ventricle' : float(line.split()[3])})
        elif '4th-Ventricle' in line:
            aseg.update({'4th-Ventricle' : float(line.split()[3])})
        elif 'Brain-Stem' in line:
            aseg.update({'Brain-Stem' : float(line.split()[3])})
        elif 'Left-Hippocampus' in line:
            aseg.update({'Left-Hippocampus' : float(line.split()[3])})
        elif 'Left-Amygdala' in line:
            aseg.update({'Left-Amygdala' : float(line.split()[3])})
        elif 'CSF' in line:
            aseg.update({'CSF' : float(line.split()[3])})
        elif 'Left-Accumbens-area' in line:
            aseg.update({'Left-Accumbens-area' : float(line.split()[3])})
        elif 'Left-VentralDC' in line:
            aseg.update({'Left-VentralDC' : float(line.split()[3])})
        elif 'Left-vessel' in line:
            aseg.update({'Left-vessel' : float(line.split()[3])})
        elif 'Left-choroid-plexus' in line:
            aseg.update({'Left-choroid-plexus' : float(line.split()[3])})
        elif 'Right-Lateral-Ventricle' in line:
            aseg.update({'Right-Lateral-Ventricle' : float(line.split()[3])})
        elif 'Right-Inf-Lat-Vent' in line:
            aseg.update({'Right-Inf-Lat-Vent' : float(line.split()[3])})
        elif 'Right-Cerebellum-White-Matter' in line:
            aseg.update({'Right-Cerebellum-White-Matter' : float(line.split()[3])})
        elif 'Right-Cerebellum-Cortex' in line:
            aseg.update({'Right-Cerebellum-Cortex' : float(line.split()[3])})
        elif 'Right-Thalamus-Proper' in line:
            aseg.update({'Right-Thalamus-Proper' : float(line.split()[3])})
        elif 'Right-Caudate' in line:
            aseg.update({'Right-Caudate' : float(line.split()[3])})
        elif 'Right-Putamen' in line:
            aseg.update({'Right-Putamen' : float(line.split()[3])})
        elif 'Right-Pallidum' in line:
            aseg.update({'Right-Pallidum' : float(line.split()[3])})
        elif 'Right-Hippocampus' in line:
            aseg.update({'Right-Hippocampus' : float(line.split()[3])})
        elif 'Right-Amygdala' in line:
            aseg.update({'Right-Amygdala' : float(line.split()[3])})
        elif 'Right-Accumbens-area' in line:
            aseg.update({'Right-Accumbens-area' : float(line.split()[3])})
        elif 'Right-VentralDC' in line:
            aseg.update({'Right-VentralDC' : float(line.split()[3])})
        elif 'Right-vessel' in line:
            aseg.update({'Right-vessel' : float(line.split()[3])})
        elif 'Right-choroid-plexus' in line:
            aseg.update({'Right-choroid-plexus' : float(line.split()[3])})
        elif '5th-Ventricle' in line:
            aseg.update({'5th-Ventricle' : float(line.split()[3])})
        elif 'WM-hypointensities' in line:
            aseg.update({'WM-hypointensities' : float(line.split()[3])})
        elif 'Left-WM-hypointensities' in line:
            aseg.update({'Left-WM-hypointensities' : float(line.split()[3])})
        elif 'Right-WM-hypointensities' in line:
            aseg.update({'Right-WM-hypointensities' : float(line.split()[3])})
        elif 'non-WM-hypointensities' in line:
            aseg.update({'non-WM-hypointensities' : float(line.split()[3])})
        elif 'Left-non-WM-hypointensities' in line:
            aseg.update({'Left-non-WM-hypointensities' : float(line.split()[3])})
        elif 'Right-non-WM-hypointensities' in line:
            aseg.update({'Right-non-WM-hypointensities' : float(line.split()[3])})
        elif 'Optic-Chiasm' in line:
            aseg.update({'Optic-Chiasm' : float(line.split()[3])})
        elif 'CC_Posterior' in line:
            aseg.update({'CC_Posterior' : float(line.split()[3])})
        elif 'CC_Mid_Posterior' in line:
            aseg.update({'CC_Mid_Posterior' : float(line.split()[3])})
        elif 'CC_Central' in line:
            aseg.update({'CC_Central' : float(line.split()[3])})
        elif 'CC_Mid_Anterior' in line:
            aseg.update({'CC_Mid_Anterior' : float(line.split()[3])})
        elif 'CC_Anterior' in line:
            aseg.update({'CC_Anterior' : float(line.split()[3])})

    # return
    return aseg


def outlierTable():
    """
    A function to provide normative values for Freesurfer segmentations and 
    parcellations.

    """

    # define

    outlierDict = dict([
        ('Left-Accumbens-area',   dict([('lower' ,    210.87844594754), ('upper',   718.01022026916)])),
        ('Right-Accumbens-area',  dict([('lower' ,    304.86134907845), ('upper',   751.63838456345)])),
        ('Left-Amygdala',         dict([('lower' ,   1179.73655974083), ('upper',  1935.09415214717)])),
        ('Right-Amygdala',        dict([('lower' ,   1161.54746836742), ('upper',  2002.14187676668)])),
        ('Brain-Stem',            dict([('lower' ,  18048.54263155760), ('upper', 25300.51090318110)])),
        ('Left-Caudate',          dict([('lower' ,   2702.73311142764), ('upper',  4380.54479618196)])),
        ('Right-Caudate',         dict([('lower' ,   2569.61140834210), ('upper',  4412.61035536070)])),
        ('Left-Hippocampus',      dict([('lower' ,   3432.26483953083), ('upper',  4934.43236139507)])),
        ('Right-Hippocampus',     dict([('lower' ,   3580.74371035841), ('upper',  5067.49668145829)])),
        ('Left-Pallidum',         dict([('lower' ,    935.47686324176), ('upper',  1849.42861796994)])),
        ('Right-Pallidum',        dict([('lower' ,   1078.14975428593), ('upper',  1864.08951102817)])),
        ('Left-Putamen',          dict([('lower' ,   3956.23134409153), ('upper',  6561.97642872937)])),
        ('Right-Putamen',         dict([('lower' ,   3768.88684356957), ('upper',  6142.52870810603)])),
        ('Left-Thalamus-Proper',  dict([('lower' ,   6483.36121320953), ('upper',  9489.46749012527)])),
        ('Right-Thalamus-Proper', dict([('lower' ,   6065.70220487045), ('upper',  8346.88382091555)])),
        ('Left-VentralDC',        dict([('lower' ,   3182.42264293449), ('upper',  4495.77412707751)])),
        ('Right-VentralDC',       dict([('lower' ,   3143.88280953869), ('upper',  4407.63641978371)]))
        ])

    # return
    return outlierDict


class FreesurferAsegQC(object):
    """
    A class to provide a quality control for Freesurfer segmentations
    """
    def __init__(self, subject_aseg_path):
        """
        A function to initialize the class.
        
        Args:
            subject_aseg_path (str): The path to the subject's aseg.stats file.

        """

        self.subject_aseg_path = subject_aseg_path

    @property
    def features(self):
        if os.path.exists(self.subject_aseg_path):
            return readAsegStats(self.subject_aseg_path)
        else:
            raise IOError('The path to the aseg.stats file does not exist.')
    

class fMRIprepFreesurferFeature(object):
    """
    A class to provide a quality control for Freesurfer segmentations
    """
    def __init__(self,freesurfer_path:str, bids:BIDSQC):
        """
        A function to initialize the class.
        
        Args:
            freesurfer_path (str): The path to the subject's freesurfer directory.
            bids (BIDSQC): The BIDSQC object.

        """
        
        self.freesurfer_path = freesurfer_path
        self.bids = bids
    @property
    def features(self):
        """
        A function to return the features.

        Returns:
            pd.DataFrame: The features.
        
        """
        results = []
        for subject in self.bids.subjects:
            aseg_path = os.path.join(self.freesurfer_path, subject.subject_id,'stats', 'aseg.stats')
            try:
                features = FreesurferAsegQC(aseg_path).features
                features['subject_id'] = subject.subject_id
                results.append(features)
            except Exception as e:
                logging.warning(f'{subject.subject_id} failed to run. {e}')
        
        return pd.DataFrame(results)
