'''
Author: Yingjie Peng
Date: 2022-03-31 22:09:30
LastEditTime: 2022-04-02 19:36:48
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/utils.py

'''
import numpy as np
from nilearn import image
from scipy.stats import spearmanr
def normalize(data):
    """
    Normalize data to [0, 1]
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def pearson_coef(x,y):
    """pearson corr 

    Args:
        x (np.ndarray): x
        y (np.ndarray): y

    Returns:
        folat: pearson corr 
    """
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        return np.corrcoef(x.flatten(),y.flatten())[0,1]
    elif isinstance(x, str) and isinstance(y, str):
        return np.corrcoef(image.load_img(x).get_data().flatten(),
                           image.load_img(y).get_data().flatten())[0,1]

def spearman_coef(x,y):
    """spearman corr 

    Args:
        x (np.ndarray): x
        y (np.ndarray): y

    Returns:
        folat: spearman corr 
    """
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        return spearmanr(x.flatten(),y.flatten())[0]
    elif isinstance(x, str) and isinstance(y, str):
        return spearmanr(image.load_img(x).get_fdata().flatten(),
                            image.load_img(y).get_fdata().flatten())[0]

def calculate_FD(motion_params):
    """
    Method to calculate Framewise Displacement (FD)  as per Power et al., 2012
    Parameters
    ----------
    motion_params
        movement parameters vector 
    Returns
    -------
    out_file : string
        Frame-wise displacement (1-d array)
        file path
    """
    rotations = np.transpose(np.abs(np.diff(motion_params[:3, :])))
    translations = np.transpose(np.abs(np.diff(motion_params[3:6, :])))

    fd = np.sum(translations, axis=1) + \
         (50 * np.pi / 180) * np.sum(rotations, axis=1)
    fd = np.insert(fd, 0, 0)
    return fd

def calcuate_rmsfd(fd:np.ndarray):
    """calcuate_rmsfd

    Args:
        fd (np.ndarray): Framewise Displacement

    Raises:
        ValueError: fd shape is not (?,1) or (?,6)

    Returns:
        np.ndarry : rmsfd
    """
    if fd.shape[-1] ==1 :
        return fd
    elif fd.shape[-1]==6:
        return calculate_FD(fd)
    else:
        raise ValueError("fd shape is not (?,1) or (?,6)")


def calculate_S(x,y,z):
    """
    Calculate the S value for the given x,y,z
    """
    return np.sqrt(np.square(x) + np.square(y) + np.square(z))