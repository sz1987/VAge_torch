this repo is for the voxel aging project using pytorch (previous use MxNet). 

# Code structure 
VAge_torch:
  voxel_age: # the main folder for the code 
    model.py
    train.py
    loss.py
    graph.py
    io.py
    vis.py
    data_manage.py
    
  demo_test: 
  README.md


# Working Plan
##2024-week-31:
* [] download the demo data folder
* [] make the io.py, to finish the following functionality
* [] read single visit feature from feature data file
* [] read the mask from mask file
*  [] make the saved folder structure and saved file as the following structure
        feat_root/feat_type/preprocess_tool/version/visit_id/mask_name/ROI_name.pkl
        feat_type: a sting, 'volumn', 'surface' or .....
        
  [] make a dict that save the visit_id => clinical information
  [] given the list of sub_id, and required feat_type, processing_tools, version, mask_name, ROI_list (if it is not given, extract all ROIs), 
     generate a list of ROI_Feature_matrix, 
  



##2024-week-32:
[] graph.py
  [] constuct the sparse matrix from the segmentation mask (volumn or surface....)
  [] convert the sparse matrix into torch data format
[] loss.py (parts)
  [] data fitting loss term
  [] SAR loss term
  [] sum of weighted loss
  [] loss log save
  [] loss plot
[] model.py (parts)
  [] non-segment linear model
  [] non-segment logistic model
  [] non-segment general logistic model
  [] some shared/fixed parameter in a single ROI
[] train.py (parts)
  [] single ROI, non-segmented model fitting
[] vis.py (parts)
  [] multi-slice grid plot overlay with heatmap
  [] fixed plot heatmap range for multiple slice overlay plot



##2024-week-33:
