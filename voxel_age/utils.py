from sklearn.model_selection import KFold
import numpy as np
import yaml 
import pandas as pd 

""" todo in this file
# TODO: #1 random split cv and get the index
# TODO: #2 get the result of the cv train/test data
 """

def get_cv_index(n,k,random_seed=False):
    """_summary_: get the index of the cv train/test data

    Args:
        n (_type_): the number of samples
        k (_type_): the target number of splits
        random_seed (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    if random_seed:
        np.random.seed(random_seed)
    arr = np.arange(n)
    # 打乱数组
    np.random.shuffle(arr)
    # 
    size1 = n // k
    size2 = n - size1 * k
    # for the first size2 groups, we add one more sample (size1+1) for each group
    groups = [ arr[g*(size1+1):(g+1)*(size1+1)]  for g in range(size2)]
    pos = size2 * (size1+1)
    # for the rest groups, we add size1 samples for each group
    groups2 = [ arr[g*size1+size2:(g+1)*size1+size2] for g in range(size2,k)]
    groups.extend(groups2)
    for g in k:
        all = copy.deepcopy()
        # train_index = 
        # tesst_index
    return groups


def read_yaml(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def config_parse(config_path):
    """_summary_: parse the config file

    Args:
        config_path (_type_): _description_
    """
    config0 = read_yaml(config_path)
    config = {}
    # region // step 1, make the data 
    dict1 = config0['data']
    dict2 = {}
    # region // step 1.1, make the data_list
    data_list_df = pd.read_csv(dict1['data_list_file'])
    img_name_list = list(data_list_df['img_name'])
    dataset_list = list(data_list_df['dataset_name'])
    n = data_list_df.shape[0]
    data_list = [[img_name_list[ind], dataset_list[ind]] for ind in range(n)]
    dict2['data_list'] = data_list
    # endregion // step 1.1, make the data_list
    # region // step 1.2, make the data_dict_list
    dict2['data_dict_list'] = dict1['data_dict_list']
    # endregion // step 1.2, make the data_dict_list
    # region // step 1.3, load the output feature root
    dict2['sys_config'] = dict1['sys_config']
    dict2['out_root'] = dict1['out_root']
    # endregion // step 1.3, load the output feature root
    config['data'] = dict2

    # endregion //  step 1, make the data 

    # region // make the split


    # endregion // make the split
    return config
