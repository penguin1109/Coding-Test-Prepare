from scipy.spatial.transform import Rotation as R
import nibabel as nib
import numpy as np
import os
import sys

sys.path.append(os.getcwd())
# from _6_ori_check import make_transpose_dict, create_transpose_matrix, get_rot_mat
from ori_check import make_transpose_dict, create_transpose_matrix, get_rot_mat
# if __name__ == "__main__":
#     rot_axis = np.eye(3)[2]
#     rotation_matrix = R.from_rotvec(np.pi / 2 * rot_axis).as_matrix()
#     print(np.round(rotation_matrix))
#     print(rotation_matrix.astype(int).astype(float))

# def get_reflection_matrix(inv_dim_dict):
#     for key, value in inv_dim_dict.items():


if __name__ == "__main__":
    src_path =  'C:\\Users\\user\\Desktop\\yonsei_cancer_lab\\ORI_TEST_DATA'
    out_path = 'C:\\Users\\user\\Desktop\\yonsei_cancer_lab\\ORI_TEST_DEBUG';os.makedirs(out_path, exist_ok=True)
    # fname = 'HCP15_150625_restore_MR.nii'
    fname = 'severance_256_FBB.nii'
    # fname = 'ADNI_4214.nii'
    

    fpath = os.path.join(src_path, fname)

    nii = nib.load(fpath)
    nii_arr = nii.get_fdata()
    nii_affine = nii.affine

    axcodes = nib.aff2axcodes(nii_affine)
    dim_match, transpose_axes = make_transpose_dict(axcodes)
    

    inv_dim_match = {value:key for key, value in dim_match.items()}
    inv_transpose_axes = tuple([inv_dim_match[i] for i in range(3)])

    ## (1) Check transpose ##
    transposed = np.transpose(nii_arr, axes = transpose_axes)
    print("TRANSPOSE_AXES", transpose_axes)
    transpose_matrix = create_transpose_matrix(axes_order=inv_transpose_axes)

    # transpose_matrix[1] *= -1
    # transpose_matrix[2] *= -1
    ## (2) Check roatate ##
    if 'A' in axcodes:
        k = 1
    else:
        k=3
    

    rotated = np.rot90(transposed, k=k, axes=(0,1))
    # rotated = np.rot90(nii_arr, k=k, axes=(0, 1))
    # rotation_matrix = get_rot_mat(4-k, inv_dict=inv_dim_match)
    rotation_matrix = get_rot_mat(4-k, inv_dict=inv_dim_match)

    ## (3) Check flip ##

    combined_matrix = np.dot(transpose_matrix, rotation_matrix) # transpose를 제일 먼저 하기 때문에 combined transformation matrix에서는 transpose matrix를 앞단에 ..? # 
    # combined_matrix = transpose_matrix
    # combined_matrix = rotation_matrix
    changed_affine = np.dot(combined_matrix, nii_affine)
    # changed_affine = np.dot(nii_affine, combined_matrix)
    # changed_affine = nii_affine
    print("rotation", rotation_matrix)
    print("transpose", transpose_matrix)
    print("changed", changed_affine)
    print("org", nii_affine)
    print("axcode", axcodes)
    print("inv", inv_dim_match)
    # new_nii = nib.nifti1.Nifti1Image(transposed, affine=changed_affine)
    new_nii = nib.nifti1.Nifti1Image(rotated, affine=changed_affine)

    if nii.get_qform(coded=True)[0] != None:
        new_nii.set_qform(affine=changed_affine)
        
    new_nii.set_sform(affine=changed_affine)
    dest_path = os.path.join(out_path, fname.split('.')[0]);os.makedirs(dest_path, exist_ok=True)
    # nib.save(new_nii, os.path.join(dest_path, "transpose.nii"))
    nib.save(new_nii, os.path.join(dest_path, "rotate.nii"))