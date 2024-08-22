import yaml 
import data_manage
import proj_io


# yaml 



if __name__ == "__main__":
    # load config file
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # load data
    data = data_manage.load_data(config["data_path"])

    # project data
    proj_io.project_data(data, config["output_path"])