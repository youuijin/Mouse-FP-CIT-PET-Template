"""Convert Allen CCF structure NRRD directly to the fixed PET template voxel grid.

No intermediate atlas grid, no 0.1-mm intermediate image, no debug files.
The fixed center and PET grid were obtained from the user's validated references.
The 90-degree coronal rotation is an intentional anatomy rotation.
"""
import argparse
from pathlib import Path

import nibabel as nib
import nrrd
import numpy as np
from scipy.ndimage import affine_transform

# World-space center of atlas.nii (mm); fixed alignment offset
TARGET_CENTER = np.array([-0.05000001, 1.15000039, -1.15000015])
# Output PET template grid
PET_SHAPE = (61, 48, 81)
PET_AFFINE = np.array([
    [0.2, 0, 0, -6],
    [0, -0.2, 0, 6],
    [0, 0, 0.2, -9],
    [0, 0, 0, 1],
], dtype=float)


def convert(input_path, output_path):
    data, header = nrrd.read(str(input_path))
    if data.ndim != 3:
        raise ValueError('Expected a 3D structure mask')
    directions = np.asarray(header['space directions'], dtype=float).T / 1000.0
    space = str(header.get('space', '')).lower()
    if space in ('left-posterior-superior', 'lps'):
        directions = np.diag([-1., -1., 1.]) @ directions
    elif space not in ('right-anterior-superior', 'ras'):
        raise ValueError(f'Unsupported NRRD space: {space}')

    # A coronal clockwise 90-degree array rotation (axes 0,2) maps
    # rotated index (i,j,k) to source index (N0-1-k, j, i).
    # Preserve the previously validated empirical direction convention:
    # the rotated image uses the source axis directions, with a new center.
    old_from_rotated = np.array([
        [0., 0., -1., data.shape[0] - 1.],
        [0., 1., 0., 0.],
        [1., 0., 0., 0.],
        [0., 0., 0., 1.],
    ])
    rotated_shape = np.array([data.shape[2], data.shape[1], data.shape[0]])
    rotated_affine = np.eye(4)
    rotated_affine[:3, :3] = directions
    rotated_affine[:3, 3] = TARGET_CENTER - directions @ ((rotated_shape - 1) / 2)

    # Map each PET voxel directly into original NRRD array coordinates.
    pet_to_source = old_from_rotated @ np.linalg.inv(rotated_affine) @ PET_AFFINE
    output_data = affine_transform(
        (data != 0).astype(np.uint8),
        matrix=pet_to_source[:3, :3],
        offset=pet_to_source[:3, 3],
        output_shape=PET_SHAPE,
        order=0,
        mode='constant',
        cval=0,
        prefilter=False,
    )
    out = nib.Nifti1Image(output_data, PET_AFFINE)
    out.set_qform(PET_AFFINE, code=1)
    out.set_sform(PET_AFFINE, code=1)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(out, str(path))
    print(f'Saved: {path} | shape: {out.shape} | nonzero: {int(output_data.sum())}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Allen structure mask.nrrd')
    parser.add_argument('--output', required=True, help='Output.nii.gz')
    args = parser.parse_args()
    convert(args.input, args.output)


if __name__ == '__main__':
    main()
