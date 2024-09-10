import yaml 
import data_manage
import proj_io
import utils
import os


# yaml 
def run(op, config1=None, config_path=None):
    if config_path is not None:
        config = utils.config_parse(config_path)
    else:
        config = {}
    if config1 is not None:
        config.update(config1)
    if op == "take_feat":
        config = config['data']
        sys_data_config = config["sys_config"]
        data_list = config["data_list"]
        data_dict_list = config["data_dict_list"]
        data_root = sys_data_config['roi_feat_root']
        roi_list_list = [data_dict['roi_list'] for data_dict in data_dict_list]
        out_root = config['out_root']
        os.makedirs(out_root, exist_ok=True)
        os.makedirs(data_root, exist_ok=True)
        out_path_list = [os.path.join(out_root, dd['process_tool'] + '_' +dd['feat_type_detail'], dd['mask']) for dd in data_dict_list]

        data_manage.load_roi_feat_to_feat_mat(data_list, data_dict_list, data_root, roi_list_list, out_path_list, config=sys_data_config)
    elif op == "train":
        #TODO
        pass
    elif op == "recon":
        #TODO
        pass



if __name__ == "__main__":
    # load config file
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # load data
    data = data_manage.load_data(config["data_path"])

    # project data
    proj_io.project_data(data, config["output_path"])