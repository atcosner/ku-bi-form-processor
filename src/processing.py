import cv2
import logging
import pytesseract
from pathlib import Path
from typing import NamedTuple

from src.definitions.util import OcrField

logger = logging.getLogger(__name__)


class OcrResult(NamedTuple):
    field: OcrField
    roi_image_path: Path
    extracted_text: str


def process_ocr_field(working_dir: Path, aligned_image, field: OcrField) -> OcrResult:
    # Extract the region of interest from the larger image
    roi = aligned_image[
        field.region.y:field.region.y + field.region.height,
        field.region.x:field.region.x + field.region.width
    ]

    # Apply pre-processing to the ROI
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    roi = cv2.GaussianBlur(roi, (3, 3), 0)
    roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, (255, 255, 255))

    # Save the image off for further analysis
    sanitized_field_name = field.name.lower().replace(' ', '_')
    roi_image_path = working_dir / f'{sanitized_field_name}.png'
    assert not roi_image_path.exists(), f'Path ({roi_image_path}) already exists!'
    cv2.imwrite(str(roi_image_path), roi)

    # Attempt OCR on the image
    ocr_string = pytesseract.image_to_string(roi, lang='eng', config=f'--psm {field.segment}')

    # Post-processing on the returned string

    return OcrResult(
        field=field,
        roi_image_path=roi_image_path,
        extracted_text=ocr_string.strip(),
    )


def process_ocr_regions(working_dir: Path, aligned_image_path: Path, fields: list[OcrField]) -> list[OcrResult]:
    # Load the aligned image
    aligned_image = cv2.imread(str(aligned_image_path))

    # Process each OCR field
    results = []
    for field in fields:
        logger.info(f'Processing OCR field: {field.name}')
        result = process_ocr_field(
            working_dir=working_dir,
            aligned_image=aligned_image,
            field=field,
        )
        results.append(result)

    return results
