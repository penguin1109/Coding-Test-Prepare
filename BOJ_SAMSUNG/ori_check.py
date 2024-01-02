import nibabel as nib
# import dicom2nifti
import numpy as np
import copy
from scipy.spatial.transform import Rotation as R

def create_transpose_matrix(axes_order):
    n = len(axes_order)

    transpose_matrix = np.eye(n + 1)
    for i, axis in enumerate(axes_order):
        transpose_matrix[i, :] = (np.arange(n + 1) == axis).astype(int)

    return transpose_matrix

def make_transpose_dict(axcodes):
    dim_match = {} # Nifti uses RAH+ #
    # H가 곧 Superior이고 같은 쌍으로 F, 즉 Inferior #
    for di, code in enumerate(axcodes):
        if code in ['R', 'L']:
            dim_match[0] = di
        elif code in ['A', 'P']:
            dim_match[1] = di
        elif code in ['S', 'I']:
            dim_match[2] = di
    transpose_axes = tuple([dim_match[0], dim_match[1], dim_match[2]])

    return dim_match, transpose_axes

def create_flip_matrix(axis):
    flip_matrix = np.eye(4)
    flip_matrix[axis, axis] = -1

    return flip_matrix

def get_rot_mat(k, inv_dict):
    axis = inv_dict[2]
    rot_axis = np.eye(3)[axis]
    r = R.from_rotvec(k*np.pi/2*rot_axis)
    mat = r.as_matrix()
    aff = np.eye(4)
    aff[:3, :3] = mat
    
    return aff

def confirm_nii_orientation(nii_obj):
    org_header = copy.deepcopy(nii_obj.header)
    org_affine = copy.deepcopy(nii_obj.affine)
    print(org_affine)

    def change_srow(nii_obj, dim_match):
        srow_x = nii_obj.header['srow_x'];srow_y = nii_obj.header['srow_y'];srow_z = nii_obj.header['srow_z']
        srows = [srow_x, srow_y, srow_z]
    
        inv = {value:key for key, value in dim_match.items()}
        changed_srows = [np.array(srows[inv[i]]) for i in range(3)]

        nii_obj.header['srow_x'] = changed_srows[0];nii_obj.header['srow_y'] = changed_srows[1];nii_obj.header['srow_z'] = changed_srows[2]
        changed_srows.append(np.array([0., 0., 0., 1.]))
        new_affine = np.stack(changed_srows, axis=0)

        return nii_obj, new_affine
    
    def change_dim(nii_obj, dim_match):
        dim_arr = nii_obj.header['dim']
        pixdim_arr = nii_obj.header['pixdim']
        inv = {value:key for key, value in dim_match.items()}
        for i in range(1, 4):
            nii_obj.header['dim'][i] = dim_arr[inv[i-1]+1]
            nii_obj.header['pixdim'][i] = pixdim_arr[inv[i-1]+1]
        for i in range(5, len(dim_arr)):
            idx = i-5
            nii_obj.header['dim'][i] = dim_arr[inv[idx]+5]
            nii_obj.header['pixdim'][i] = pixdim_arr[inv[idx]+5]
        
        return nii_obj
    
    def change_quaternion(nii_obj, dim_match): ## quaternion (복소수) ## 
        inv = {value:key for key, value in dim_match.items()}
        quat_dict = {0 : 'quatern_b', 1: 'quatern_c', 2 : 'quatern_d'}
        nii_obj.header['quatern_b'] = nii_obj.header[quat_dict[inv[0]]]
        nii_obj.header['quatern_c'] = nii_obj.header[quat_dict[inv[1]]]
        nii_obj.header['quatern_d'] = nii_obj.header[quat_dict[inv[2]]]

        return nii_obj


    axcodes = nib.aff2axcodes(nii_obj.affine)
    nii_arr = nii_obj.get_fdata()
    print(axcodes)
    
    dim_match = {} # Nifti uses RAH+ #
    # H가 곧 Superior이고 같은 쌍으로 F, 즉 Inferior #
    for di, code in enumerate(axcodes):
        if code in ['R', 'L']:
            dim_match[0] = di
        elif code in ['A', 'P']:
            dim_match[1] = di
        elif code in ['S', 'I']:
            dim_match[2] = di
    transpose_axes = tuple([dim_match[0], dim_match[1], dim_match[2]])
    
    ## (1) RAH+ form이 맞도록 transform ##
    inv = {value:key for key, value in dim_match.items()}
    inv_transpose_axes = tuple([inv[0], inv[1], inv[2]])
    # new_affine[:3, :] = new_affine[[*inv_transpose_axes], :]
    # nii_obj, new_affine = change_srow(nii_obj, dim_match) # 먼저 새로운 affine transformation matrix를 구해줌 #
    new_affine = copy.deepcopy(org_affine)
    transposed = np.transpose(nii_arr, axes=transpose_axes)
    if 'A' in axcodes:
        k=1
    else:
        k=3
    transformed = np.rot90(transposed, k=k, axes=(0,1)) ## 2번쨰 axis가 Axial Plane이니까 (0,1)번째 Z축 기준으로 rotate ##
    rot_mat = get_rot_mat(k=-k, inv_dict=dim_match)
    
    # rot_axis = np.eye(4)[inv[2]][:3]
    # rot_mat = create_rotation_matrix(angle=180 * k, axis=rot_axis)
    flip_lr, flip_hf = False, False
    if 'R' not in axcodes: ## 좌우 대칭 뒤집기 ##
        transformed = np.flip(transformed, axis=1)
        flip_lr=True
        # i = inv[1]
        # arr = np.eye(4);arr[i][i] *= -1
        # # rot_mat = np.dot(arr.T, rot_mat)
        # rot_mat = np.dot(rot_mat, arr)
        
    if 'S' in axcodes: ## 머리부터 발까지 순서 뒤집기 ##
        transformed = np.flip(transformed, axis=2) # transformed[:, :, ::-1]
        flip_hf = True
        # i = inv[2]
        # arr = np.eye(4);arr[i][i] *= -1
        # # rot_mat = np.dot(arr.T, rot_mat)
        # rot_mat = np.dot(rot_mat, arr)
    """
    transformed 배열은 모두 동일하게 (Coronal Sagittal Axial) 평면들이 각 축마다 보이는 것을 알 수 있다.
    또 동일하게
    Coronal slice: Posterior -> Anterior
    Sagittal slice: Left -> Right
    Axial slice: Head(Superior) -> Feet(Inferior)
    
    RAS+라는 것은 Right, Anterior, Superior에서 모두 시작한다는 것이다.
    """
    # else: 
        # new_affine[2][2] = new_affine[2][2] * -1
    # new_affine = np.dot(new_affine, rot_mat)
    flip_hf_matrix, flip_lr_matrix = None, None
    if flip_hf:
        flip_hf_matrix = create_flip_matrix(2)
    if flip_lr:
        flip_lr_matrix = create_flip_matrix(1)
        
    # new_affine = np.dot(rot_mat, new_affine)
    transpose_matrix = create_transpose_matrix(axes_order=inv_transpose_axes)
    
    combined_matrix = flip_hf_matrix
    if combined_matrix is None:
        combined_matrix = flip_lr_matrix
    elif flip_lr_matrix is not None:
        combined_matrix = np.dot(flip_lr_matrix, combined_matrix)
        
    if combined_matrix is None:
        combined_matrix = rot_mat
    else:
        combined_matrix = np.dot(rot_mat, combined_matrix)
    combined_matrix = np.dot(transpose_matrix, combined_matrix)
    # new_affine[:3, :] = new_affine[[*inv_transpose_axes], :]
    print(inv)
    new_affine = np.dot(combined_matrix, org_affine)

    ## (2) 변형된 nifti array에 맞게 nii_obj의 header값도 같이 변경 ##
    ## (3) nii_obj 최종 업데이트 ##
    new_nii = nib.nifti1.Nifti1Image(transformed, affine=new_affine)# , header=nii_obj.header)
    new_nii.set_qform(affine=new_affine)
    new_nii.set_sform(affine=new_affine)
    # new_nii = nib.nifti1.Nifti1Image(transformed, affine=org_affine, header=org_header)

    return new_nii
            

if __name__ == "__main__":
    from glob import glob
    import os
    print(os.getcwd())
    input_path = 'C:\\Users\\user\\Desktop\\yonsei_cancer_lab\\ORI_TEST_DATA'
    output_path = 'C:\\Users\\user\\Desktop\\yonsei_cancer_lab\\ORI_OUT';os.makedirs(output_path, exist_ok=True)
    test_files = glob(input_path + "/*.nii")
    print(test_files)
    for fi, test_file in enumerate(test_files):
        fname = os.path.basename(test_file)
        nii_obj = nib.load(test_file)
        new_nii = confirm_nii_orientation(nii_obj)
        nib.save(new_nii, os.path.join(output_path, fname))
    