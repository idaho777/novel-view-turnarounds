import numpy as np
import sys

from tempfile import TemporaryFile

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

b = np.load(sys.argv[1])
print(dir(b))
print(b.files)

orig_views_names = ['0000.png', '0003.png', '0006.png', '0009.png', '0012.png', '0015.png', '0018.png', '0021.png']
orig_views = [0, 3, 6, 9, 12, 15, 18, 21]
turn_views = [0, 315, 270, 225, 180, 135, 90, 45]


outfile = TemporaryFile()

save_dict = {}
for i in range(len(orig_views)):
    cam_str = f'camera_mat_{orig_views[i]}'
    wor_str = f'world_mat_{orig_views[i]}'
    cam_mat = b[cam_str]
    wor_mat = b[wor_str]
    cam_mat_inv = np.linalg.inv(cam_mat)
    wor_mat_inv = np.linalg.inv(wor_mat)
    save_dict[f'camera_mat_{i}'] = cam_mat
    save_dict[f'world_mat_{i}'] = wor_mat
    save_dict[f'camera_mat_inv_{i}'] = cam_mat_inv
    save_dict[f'world_mat_inv_{i}'] = wor_mat_inv

    print(save_dict[f'world_mat_{i}'])


np.savez_compressed('cameras.npz', **save_dict)
