import numpy as np
import nibabel as nib




def convert_spherical_roi_coords_to_nifti(template_nifti_path, spherical_coords, radius, output_nifti_path, spherical_labels=None):
    """Function that converts RAS coordinates to spheres on a nifti image

    Function that takes a path to a template nifti in the desired space, coordinates
    to points in the image that will define spherical ROIs, radii that specify the size of
    the ROIs (one entry per sphere), and creates a nifti image with spherical ROIs (labeled
    in ascending order unless otherwise specified) saved to a specified path. 

    Parameters
    ----------

    template_nifti_path : str
	path to a template nifti file with the desired dimensions/transforms for the output image

    spherical_coords : list
	list, where each entry is a three element array with the RAS coordinates for a sphere

    radius : list
	list of radii for each sphere (needs to have same length of spherical_coords)
    
    output_nifti_path : str
	the path to the nifti file that will be created to house the mask

    spherical_labels : list, optional
	a list with same length as spherical_coords that defines the numerical value each
	sphere should take. If not provided spheres will be ordered 1, 2, 3... etc.

    """
    
    template_nifti = nib.load(template_nifti_path)
    affine = template_nifti.affine
    mask_vol = np.zeros(template_nifti.get_fdata().shape)
    
    for i in range(mask_vol.shape[0]):
        for j in range(mask_vol.shape[1]):
            for k in range(mask_vol.shape[2]):
                
                temp_ras = np.matmul(affine,[i, j, k, 1])[0:3]
                for l in range(len(spherical_coords)):

                    distance = np.linalg.norm(spherical_coords[l] - temp_ras)

                    if radius[l] <= distance:

                        if type(spherical_labels) == None:
                            mask_vol[i,j,k] = l + 1
                        else:
                            mask_vol[i,j,k] = spherical_labels[l]
                        break
                        
    template_header = template_nifti.header
    img = nib.nifti1Image(mask_vol, affine, header = template_header)
    nib.save(img, output_nifti_path)
    
    
    
    
    
    
def nifti_rois_to_time_signals(input_timeseries_nii_path, input_mask_nii_path, demedian_before_averaging = True):
    """Function that applies a parcellation a 4d nifti timeseries 

    Function that takes an input 4d nifti file, a 3d nifti mask with non-zero
    regions specifying different ROIs, and calculates the average time-signal
    for each region of interest. By default, each voxel's timeseries is normalized
    by its temporal median, prior to spatial averaging among all other voxels in the
    region of interest (unless demedian_before_averaging is set to False). Any NaNs
    are ignored in calculation.

    Parameters
    ----------

    input_timeseries_nii_path : str
	path to a 4d nifti file whose timeseries should be parcellated

    input_mask_nii_path : str
	path to a 3d nifti file whose non-zero values represent unique regions,
	within which the signal from the input timeseries will be averaged

    demedian_before_averaging : bool, optional
	whether or not to demedian each voxel's signal before averaging. Defaults
	to True.


   Returns
   -------

   nifti_time_series : numpy.ndarray
	an array with shape <n_regions, n_timepoints> containing the average time signal
	within different regions of interest 

   unique_mask_vals : numpy.ndarray
	an array with shape <n_regions> that contains the values from input_mask_nii that
	can be used to match timeseries to mask regions

   parc_mean_median_signal_intensities : numpy.ndarray
	an array with shape <n_regions> that has the average signal intensity for each region,
	calculated by the spatial average of temporal medians of each voxel.

    """
    
    input_ts_nii = nib.load(input_timeseries_nii_path)
    input_mask_nii = nib.load(input_mask_nii_path)
    
    input_mask_matrix = input_mask_nii.get_fdata()
    input_ts_matrix = input_ts_nii.get_fdata()
    unique_mask_vals = np.unique(input_mask_matrix)
    unique_mask_vals.sort()
    unique_mask_vals = unique_mask_vals[1:]
    
    nifti_time_series = np.zeros((unique_mask_vals.shape[0], input_ts_matrix.shape[3]))
    parc_mean_median_signal_intensities = np.zeros(unique_mask_vals.shape[0])



    for i in range(len(unique_mask_vals)):

        inds = np.where(input_mask_matrix == unique_mask_vals[i])
        temp_timeseries = input_ts_matrix[inds]

        voxel_medians = np.nanmedian(temp_timeseries, axis=1)
        voxel_medians[np.where(voxel_medians < 0.001)] = np.nan

        if demedian_before_averaging:
            temp_timeseries = temp_timeseries/voxel_medians[:,None]
            
        
            
        nifti_time_series[i,:] = np.nanmean(temp_timeseries, axis=0)
        parc_mean_median_signal_intensities[i] = np.nanmean(voxel_medians)
        
    return nifti_time_series, unique_mask_vals, parc_mean_median_signal_intensities

