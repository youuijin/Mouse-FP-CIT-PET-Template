# Mouse [¹⁸F]FP-CIT PET Template

This repository provides the PET template and preprocessing scripts associated with the research entitled:

**Development and Evaluation of a CT-Guided Mouse [¹⁸F]FP-CIT PET Template for PET-Only Spatial Normalization**

The CT-guided [¹⁸F]FP-CIT PET template was developed to enable PET-only spatial normalization of mouse brain PET images. This repository includes the finalized PET template in NIfTI format, an example script for PET spatial normalization, and a script for generating volume-of-interest (VOI) masks from the Allen Mouse Brain Common Coordinate Framework (CCF).

## 1. PET Template

The template was constructed using CT-guided spatial normalization to improve anatomical consistency in mouse [¹⁸F]FP-CIT PET imaging.

The finalized template is provided in NIfTI format (`.nii.gz`) and can be used for PET-only spatial normalization without requiring individual CT images.

## 2. PET Spatial Normalization

An example Python script (`spatial_normalization.py`) is provided for registering individual mouse [¹⁸F]FP-CIT PET images to the CT-guided PET template.

Spatial normalization is performed using **ANTs SyN registration with the Mattes similarity metric**.

### Requirements

```bash
pip install antspyx
```

### Usage

```bash
python scripts/spatial_normalization.py \
    --input subject_pet.nii.gz \
    --template template/FP-CIT_template.nii.gz \
    --output normalized_pet.nii.gz
```

The resulting PET image is spatially normalized into the template space and can be used for subsequent VOI-based regional quantification.

## 3. VOI Masks

VOI masks are derived from the **Allen Mouse Brain Common Coordinate Framework (CCFv3, 2017 annotation)**, developed by the Allen Institute for Brain Science.

The following regions were used in our study:

| Structure ID | Region | Usage |
|---|---|---|
| 485 | Dorsal striatum (STRd) | Target region |
| 528 | Cerebellar cortex (CBX) | Reference region |

### Original VOI Masks

- [STRd — structure_485.nrrd](https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/structure_masks/structure_masks_10/structure_485.nrrd)
- [CBX — structure_528.nrrd](https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/structure_masks/structure_masks_10/structure_528.nrrd)

### Additional Brain Regions

Researchers requiring other VOIs can download the corresponding structure masks from the [Allen CCF 2017 Structure Mask Directory](https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/structure_masks/structure_masks_10/).

## 4. VOI Preprocessing

The provided Python script (`convert_allen_voi.py`) converts the original Allen CCF structure masks into the spatial coordinate system of the PET template.

The preprocessing includes:

1. Conversion of NRRD spatial coordinates from µm to mm.
2. Orientation adjustment and origin alignment.
3. Resampling to 0.2 mm isotropic voxel resolution using nearest-neighbor interpolation.
4. Adjustment to the PET template dimensions and spatial coordinates.

### Requirements

```bash
pip install numpy scipy nibabel pynrrd
```

### Usage

Download the desired structure mask from the Allen CCF directory and run:

```bash
python scripts/convert_allen_voi.py \
    --input structure_485.nrrd \
    --output 485_STRd.nii.gz
```

The resulting NIfTI mask is generated in the PET template space for regional quantification.

## 5. Data Source and Attribution

The VOI masks are derived from the Allen Mouse Brain Common Coordinate Framework (CCFv3, 2017 annotation), developed by the Allen Institute for Brain Science.

Original Allen CCF structure masks are not redistributed in this repository. Users should download the source data directly from the Allen Institute and follow its applicable terms of use.

### Reference

Wang, Q., Ding, S.-L., Li, Y., et al. (2020). The Allen Mouse Brain Common Coordinate Framework: A 3D Reference Atlas. *Cell*, 181(4), 936–953.e20.

https://doi.org/10.1016/j.cell.2020.04.007

## 6. License

The source code is distributed under the MIT License.

The PET template is distributed under the Creative Commons Attribution 4.0 International (CC BY 4.0) License.

Allen CCF source data remain subject to the terms established by the Allen Institute for Brain Science.
