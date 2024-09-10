# this file is used to make the data management on the feature, mask, and model
# it's function  => get_feat_im_path_dict(im_list, data_dict, data_root): only for Yuchuan's data preprocess folder structure
import os, glob, os
import proj_io
import multiprocessing
import time 
import numpy as np

MASK_PATH_DICT = {'cat_base': {'path': '/Users/sunzhuo/Downloads/Voxel_Aging/mask/volume/cat_base/cat.nii'},
                  'neuromorphic':{'path': '/Users/sunzhuo/Downloads/Voxel_Aging/mask/volume/neuromorphometrics/neuromorphometrics.nii'}} # it is a dict, key is the mask name, value is the mask path TODO
PREPROCESS_DATA_ROOT ='/Users/sunzhuo/Downloads/Voxel_Aging/PPMI' # it is a string, it is the root path of the preprocess dataict, key is the preprocess_tool name, value is the preprocess_tool path TODO
CLINIAL_DATA_CSV = '' # a csv_path that 

def load_roi_feat_to_feat_mat(data_list, data_dict_list, data_root, roi_list_list, out_path_list, config={}):
    """_summary_
    this function is used to load the roi feature to the feature matrix
    Args:
        data_list (list): it is a list, each element is a list, as [im_id, dataset]
        data_dict_list (_type_): it is a list of dict, each dict is a data description
        roi_list_list (_type_): _description_
        out_folder (_type_): _description_
    """
    # region // step_1, get the setting from the config
    mask_path_dict = config.get('mask_path_dict', MASK_PATH_DICT)
    clinical_data_csv = config.get('clinical_data_csv', CLINIAL_DATA_CSV)
    preprocess_data_root = config.get('preprocess_data_root', PREPROCESS_DATA_ROOT)
    cpu_num = config.get('cpu_num', 4)
    print(' ===>>> finish step 1, get the information from config')
    # endregion // step_1, get the setting from the config
    # region // step_2, check the input
    nd = len(data_dict_list)
    n2 = len(roi_list_list)
    n3 = len(out_path_list)
    assert nd == n2, 'the number of data_dict_list and roi_list_list should be the same'
    assert nd == n3, 'the number of data_dict_list and out_path_list should be the same'
    print(' ===>>> finish step_2, check the input')
    # endregion // step_2, check the input
    # region // step_3, load the data
    for dind in range(nd):
        re_compute_list = []
        data_dict = data_dict_list[dind]
        print(f'======data_dict_list[{dind}], {time.ctime()}=======')
        print(data_dict)
        roi_list = roi_list_list[dind]
        # region // step 3.1, load the data description from the data_dict
        mask = data_dict['mask']
        feat_type = data_dict['feat_type']
        feat_type_detail = data_dict['feat_type_detail']
        process_tool = data_dict['process_tool']
        tool_version = data_dict['tool_version']
        mask_path = mask_path_dict[mask]['path']
        # endregion // lstep 3.1, oad the data description from the data_dict
        # region // step 3.1.1, get the roi_list
        if roi_list is None:
            seg = proj_io.load_file(mask_path)
            all_roi = np.unique(seg)
            roi_list = all_roi[all_roi>0]

        # endregion // step 3.1.1, get the roi_list
        # region // step 3.2, check which roi_wise feat extraction need to be done
        folder1 = os.path.join(data_root, feat_type, feat_type_detail, process_tool, tool_version, mask)
        for im_id, dataset in data_list:
            # feat_type/feat_type_detail/preprocess_tool/version/mask_name/dataset/visit_id/ROI_name.pkl
            im_folder = os.path.join(folder1, dataset, im_id)
            if check_exist_all_roi(im_folder, roi_list) is False:
                re_compute_list.append([im_id, dataset])

        if len(re_compute_list) > 0:
            print(f' ===>>> There are {len(re_compute_list)} images need to be recompute to extract roi-wise features, {time.ctime()}')
            feat_im_path_dict = get_feat_im_path_dict(re_compute_list, data_dict, data_root=preprocess_data_root)
            print(' ===>>> feat_im_path_dict')
            print(feat_im_path_dict)
            proj_io.extract_feat_in_ROI_parallel(feat_im_path_dict, mask_path, out_folder=folder1, roi_list=roi_list, cpu_num=cpu_num)
            print(f' ===>>> Finish at {time.ctime()}')
        else:
            print(f'====>>>>>> already has all the roi_wise feat extracted in the disk')
        # endregion // step 3.2, check which roi_wise feat extraction need to be done
        # region // step 3.3, extract the roi-wise feat_vec into the feat_mat
        print(f' === collecting the roi-wise feat_vec into the feat_mat, for {len(roi_list)} ROIs, {time.ctime()}')
        out_path0 = out_path_list[dind]
        out_root0 = os.path.split(out_path0)[0]
        os.makedirs(out_root0, exist_ok=True)
        for roi in roi_list:
            feat_vec_list = []
            for im_id, dataset in data_list:
                im_folder = os.path.join(folder1, dataset, im_id)
                feat_pkl = os.path.join(im_folder, 'roi_{}.pkl'.format(roi))
                feat_vec = proj_io.load_pickle(feat_pkl).reshape((1, -1))
                feat_vec_list.append(feat_vec)
            feat_mat = np.concatenate(feat_vec_list, axis=0)
            out_pkl = out_path0+'_roi_{}.pkl'.format(roi)
            proj_io.save_pickle(feat_mat, out_pkl)
        print(f' === Finish collecting the roi-wise feat_vec into the feat_mat, {time.ctime()}')

        # endregion // step 3.3, extract the roi-wise feat_vec into the feat_mat
    # endregion // step_3, load the data
def check_exist_all_roi(root, roi_list):
    """_summary_
    this function is used to check if all the roi exist in the root folder
    Args:
        root (_type_): _description_
        roi_list (_type_): _description_
    """
    has_all = True
    for roi in roi_list:
        roi_path = os.path.join(root,'roi_{}.pkl'.format(roi))
        if not os.path.exists(roi_path):
            has_all = False
            break
    return has_all

def get_feat_im_path_dict(im_list, data_dict, data_root):
    """_summary_
    this function is used to get the feat_im_path_dict
    Args:
        im_list (_type_): _description_
        data_dict (_type_): _description_
    """
    # region // load the data description from the data_dict
    mask = data_dict['mask']
    feat_type = data_dict['feat_type']
    feat_type_detail = data_dict['feat_type_detail']
    process_tool = data_dict['process_tool']
    tool_version = data_dict['tool_version']
    mask_path = MASK_PATH_DICT[mask]
    # endregion // load the data description from the data_dict
    # region // get the feat_im path for each im_id
    res_dict = {}
    for im_id, dataset in im_list:
        feat_path = None
        if process_tool in ['CAT12']:
            im_folder1 = os.path.join(data_root, im_id, 'T1w', im_id,'mri')
            if feat_type == 'volume':
                im_folder2 = os.path.join(im_folder1,'mri')
                if feat_type_detail == 'Modulated_gray_matter_density':
                    feat_path = os.path.join(im_folder2, 'mwp1nu.nii')
                elif feat_type_detail == 'Modulated_white_matter_density':
                    feat_path = os.path.join(im_folder2, 'mwp2nu.nii')
                else:
                    raise Exception(f'unknown feat_type_detail => {feat_type_detail} for process_tool => {process_tool}, feat_type => {feat_type}')
            else:
                 raise Exception(f'unknown feat_type => {feat_type} for process_tool => {process_tool}')
        elif process_tool in ['FreeSurfer']:
            im_folder1 = os.path.join(data_root, im_id, 'T1w', im_id)
            if feat_type == 'surface':
                im_folder2 = os.path.join(im_folder1, 'surf')
                if feat_type_detail == 'rh_thickness':
                    feat_path = os.path.join(im_folder2, 'rh.thichness')
                elif feat_type_detail == 'lh_thickness':
                    feat_path = os.path.join(im_folder2, 'lh.thichness')
                elif feat_type_detail == 'rh_curv':
                    feat_path = os.path.join(im_folder2, 'rh.curv')
                elif feat_type_detail == 'lh_curv':
                    feat_path = os.path.join(im_folder2, 'lh.curv')
                elif feat_type_detail == 'rh_sulc':
                    feat_path = os.path.join(im_folder2, 'rh.sulc')
                elif feat_type_detail == 'lh_sulc':
                    feat_path = os.path.join(im_folder2, 'lh.sulc')
                else:
                    raise Exception(f'unknown feat_type_detail => {feat_type_detail}')
            else:
                raise Exception(f'unknown feat_type => {feat_type} for process_tool => {process_tool}')
        else:
            raise Exception(f'unknown process_tool => {process_tool}')
        res_dict[im_id] =  [feat_path, dataset]
    # endregion // get the feat_im path for each im_id
    return res_dict

def generate_sub_roi_feat(data_list, data_dict_list, data_root, roi_list_list, cpu_num=4):
    """_summary_
    this function is used to generate the roi feat and save it to disk for each subject each roi
    Args:
        data_list (_type_): it is a list, each element is [im_id, datset]
        data_dict_list (_type_): it is a list of dict, each 
        data_root (_type_): _description_
        roi_list_list (_type_): _description_
        cpu_num (int, optional): _description_. Defaults to 4.
    """
    n1 = len(data_dict_list)
    n2 = len(roi_list_list)
    assert n1 == n2, f'len(data_dict_list) => {n1} != len(roi_list_list) => {n2}'
    for dind in range(n1): # for each data_dict
        data_dict = data_dict_list[dind]
        roi_list = roi_list_list[dind]
        # region // load the data description from the data_dict
        mask = data_dict['mask']
        feat_type = data_dict['feat_type']
        feat_type_detail = data_dict['feat_type_detail']
        process_tool = data_dict['process_tool']
        tool_version = data_dict['tool_version']
        mask_path = MASK_PATH_DICT[mask]
        # endregion // load the data description from the data_dict
        # region // get the feat_im path for each im_id
        print(f'======data_dict_list[{dind}], {time.ctime()}=======')
        print(data_dict)
        folder1 = os.path.join(data_root, feat_type, feat_type_detail, process_tool, tool_version, mask)
        feat_im_path_dict = get_feat_im_path_dict(data_list, data_dict, data_root=preprocess_data_root)
        proj_io.extract_feat_in_ROI_parallel(feat_im_path_dict, mask_path, out_folder=folder1, roi_list=roi_list, cpu_num=cpu_num)
        # endregion // get the feat_im path for each im_id