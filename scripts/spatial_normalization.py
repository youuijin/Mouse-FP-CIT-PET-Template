
"""
PET-only spatial normalization using the CT-guided
mouse [18F]FP-CIT PET template.

Requirements:
    pip install antspyx

Example:
    python spatial_normalization.py \
        --input subject_pet.nii.gz \
        --template template/FPCIT_PET_template.nii.gz \
        --output normalized_pet.nii.gz
"""

import argparse
from pathlib import Path

import ants


def spatial_normalization(input_path, template_path, output_path):
    """
    Register an individual PET image to the PET template
    using ANTs SyN registration with the Mattes metric.
    """

    # Load images
    fixed = ants.image_read(str(template_path))
    moving = ants.image_read(str(input_path))

    # SyN registration
    reg = ants.registration(
        fixed=fixed,
        moving=moving,
        type_of_transform="SyN",
        syn_metric="mattes"
    )

    # Warp PET image into template space
    normalized = ants.apply_transforms(
        fixed=fixed,
        moving=moving,
        transformlist=reg["fwdtransforms"],
        interpolator="linear"
    )

    # Save normalized PET image
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ants.image_write(normalized, str(output_path))

    print(f"Normalized PET saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="PET-only spatial normalization using ANTs SyN."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input PET image."
    )

    parser.add_argument(
        "--template",
        required=True,
        help="Path to the CT-guided PET template."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to the normalized PET image."
    )

    args = parser.parse_args()

    spatial_normalization(
        input_path=args.input,
        template_path=args.template,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
