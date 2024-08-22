# this file contains function and class related to I/0
import os
import glob
import sys
import multiprocessing
import nibabel as nib
import numpy as np
import json
import yaml
import pickle

from nibabel.freesurfer import read_annot
from nibabel.freesurfer.io import read_morph_data
import io_mesh



# region // functions to load files
def load_nifti_im_array(filename):
    """
    load a nifti file and return the data and affine matrix
    """
    img = nib.load(filename)
    data = img.get_fdata()
    return data 

def load_gii_im_array(filename:str):
    """_summary_
    this function load the data from .gii file 
    Args:
        filename (str): _description_
    """
    # TODO
    pass

def load_annot(file_path:str):
    """_summary_
    this function load the data from .annot file 
    Args:
        file_path (str): _description_
    """
    a, L, c = read_annot(file_path)
    annot_dict = {}
    return data


def load_thickness(file_path:str):
    """_summary_
    this function load the data from .thickness file 
    Args:
        file_path (str): _description_
    """
    
    data = read_morph_data(file_path)
    return data

def load_obj(file_path):
    """_summary_
    this function load the data from .obj file
    Args:   
        file_path (str): _description_
    """ 
    # TODO
    pass


def load_json(filename:str):
    """_summary_
    this function load the data from .json file 
    Args:
        filename (str): _description_
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def load_yaml(filename:str):
    """_summary_
    this function load the data from .yaml file 
    Args:
        filename (str): _description_
    """
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def load_pickle(data, file_path):
    """_summary_

    Args:
        data (_type_): _description_
        file_path (_type_): _description_
    """
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data 

def load_file(file_path:str, only_data=True):
    """_summary_

    Args:
        file_path (str): _description_
        only_data (bool, optional): _description_. Defaults to True.
    """
    # region // step 1, check the file extension
    parts = file_path.split('.')
    data_form = None
    if parts[-1] == 'nii':
        data_form = 'nii'
    elif parts[-1] == 'gz':
         if parts[-2] == 'nii':
            data_form = 'nii'
    elif parts[-1] == 'gii':
        data = 'gii'
    elif parts[-1] == 'json':
        data = 'json'
    elif parts[-1] == 'pkl':
        data = 'pkl'
    elif parts[-1] == 'yaml':
        data = 'yaml'
    elif parts[-1] == 'obj':
        data = 'obj'
    elif parts[-1] == 'ply':
        data = 'ply'
    elif parts[-1] =='annot':
        data = 'annot'
    elif parts[-1] == 'thickness':
        data = 'thickness'
    # endregion // step 1, check the file extension
    # region // step 2, load the data
    if only_data is True:
        if data_form == 'nii':
            data = load_nifti_im_array(file_path)
        elif data_form == 'gii':
            data = load_gii_im_array(file_path)
        elif data_form == 'json':
            data = load_json(file_path)
        elif data_form == 'pkl':    
            data = load_pickle(file_path)
        elif data_form == 'yaml':
            data = load_yaml(file_path)
        elif data_form == 'obj':
            data = load_obj(file_path)
        elif data_form == 'ply':
            data = load_ply(file_path)
        elif data_form == 'annot':
            data = load_annot(file_path)
        elif data_form == 'thickness':
            data = load_thickness(file_path)
    # endregion // step 2, load the data
    return data

# endregion // functions to load files

# region // functions to save files
def save_pickle(data, file_path):   
    """_summary_

    Args:
        data (_type_): _description_
        file_path (_type_): _description_
    """
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def save_json(data, filename:str):  
    """_summary_
    this function save the data to .json file 
    Args:
        data (_type_): _description_
        filename (str): _description_
    """
    with open(filename, 'w') as f:
        json.dump(data, f)

def save_yaml(data, filename:str):  
    """_summary_
    this function save the data to .yaml file 
    Args:
        data (_type_): _description_
        filename (str): _description_
    """
    with open(filename, 'w') as f:
        yaml.dump(data, f)


def save_file(data, file_path:str):
    """_summary_

    Args:
        data (_type_): _description_
        file_path (str): _description_
    """
    # region // step 1, check the file extension
    parts = file_path.split('.')
    data_form = None
    if parts[-1] == 'nii':
        data_form = 'nii'
    elif parts[-1] == 'gz':
         if parts[-2] == 'nii':
            data_form = 'nii'
    elif parts[-1] == 'gii':
        data = 'gii'
    elif parts[-1] == 'json':
        data = 'json'
    elif parts[-1] == 'pkl':
        data = 'pkl'
    elif parts[-1] == 'yaml':
        data = 'yaml'
    # endregion // step 1, check the file extension
    # region // step 2, save the data
    if data_form == 'nii':
        save_nifti_im_array(data, file_path)
    elif data_form == 'gii':
        save_gii_im_array(data, file_path)
    elif data_form == 'json':
        save_json(data, file_path)
    elif data_form == 'pkl':    
        save_pickle(data, file_path)
    elif data_form == 'yaml':
        save_yaml(data, file_path)  
    # endregion // step 2, save the data

# endregion // functions to save files

# region // function to extract the feateure as vector from volume or surface under the ROI
def extract_feat_in_ROI(feat, seg, roi_list=None, out_folder=None):
    """_summary_

    Args:
        feat (_type_): _description_
        seg (_type_): _description_
        roi_list (_type_, optional): _description_. Defaults to None.
        out_folder (_type_, optional): _description_. Defaults to None.
    """
    # region // get the roi_list1
    if roi_list is None:
        all_roi = np.unique(seg)
        roi_list1 = all_roi[all_roi>0]
    else:
        roi_list1 = roi_list 
    # endregion // get the roi_list1
    # region // get the feat and seg from file to memeory (if needed)
    if isinstance(feat, str):
        feat = load_file(feat, only_data=True)
    if isinstance(seg, str):
        seg = load_file(seg, only_data=True)
    # endregion // get the feat and seg from file to memeory (if needed)
    # region // extract the feature as vector from volume or surface under each ROI
    feat_vec = feat[:]
    seg_vec = seg[:]
    res_dict = {}
    for roi in roi_list1:
        res_dict[roi] = feat_vec[seg_vec==roi]
    # endregion // extract the feature as vector from volume or surface under each ROI
    # region // save the result to file (if needed)
    if out_folder is not None:
        os.makedirs(out_folder, exist_ok=True)
        for roi in roi_list1:
            out_path = os.path.join(out_folder,'roi_{}.pkl'.format(roi))
            save_pickle(res_dict[roi], out_path)
    # endregion // save the result to file (if needed)
    return res_dict

def extract_feat_in_ROI_parallel(data_dict, seg, out_folder=None, roi_list=None, cpu_num=1):
    """_summary_

    Args:
        data_dict (_type_): it is a dict, key is the image_name (ID) and val is a list  [feature path, dataset]
        seg (_type_): it is a path to the segmentation file or a extract ndarray for segmentation 
        roi_list (_type_, optional): _description_. Defaults to None.
        out_folder (_type_, optional): _description_. Defaults to None.
    """
    id_list = list(data_dict.keys())
    n = len(id_list)
    if isinstance(seg, str):
        seg = load_file(seg, only_data=True)
    os.makedirs(out_folder, exist_ok=True)
    if cpu_num ==1:
        for ind in range(n):
            im_id = id_list[ind]
            feat_file = data_dict[im_id][0]
            dataset = data_dict[im_id][1]
            out_folder1 = os.path.join(out_folder, dataset, im_id)
            _ = extract_feat_in_ROI(feat_file, seg, roi_list=roi_list, out_folder=out_folder1)
    else:
        pool = multiprocessing.Pool(processes=cpu_num)
        for ind in range(n):
            pool.apply_async(extract_feat_in_ROI, args=(data_dict[id_list[ind]][0], seg, roi_list, 
                                                        os.path.join(out_folder, data_dict[id_list[ind]][1], id_list[ind])))
        pool.close()    
        pool.join()

# endregion // function to extract the feateure as vector from volume or surface under the ROI

