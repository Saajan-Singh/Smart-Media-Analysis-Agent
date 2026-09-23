"""
image_analyzer.py -- Image to Text Extraction Engine

Authenticates to Azure AI Vision and extracts structured text data
(visual tags, OCR text) from local image files.
"""

import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from src import ENV_PATH, MEDIA_DIR

load_dotenv(dotenv_path=ENV_PATH)

# ---------------------------------------------------------------------------
# Azure AI Vision client setup
# ---------------------------------------------------------------------------

_endpoint = os.getenv("AZURE_VISION_ENDPOINT")
_key = os.getenv("AZURE_VISION_KEY")

if not _endpoint or not _key:
    print(
        "[Warning] Missing Azure Vision credentials. "
        "Ensure AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are set."
    )
    _client = None
else:
    _client = ImageAnalysisClient(_endpoint, AzureKeyCredential(_key))

# ---------------------------------------------------------------------------
# Determine which visual features are available in this Azure region.
#
# Caption and DenseCaptions are NOT supported in every region.  We request
# TAGS + READ (OCR) which are universally available, and attempt to add
# CAPTION on a best-effort basis.
# ---------------------------------------------------------------------------

_BASE_FEATURES = [VisualFeatures.TAGS, VisualFeatures.READ]


def _request_features_with_caption_fallback(image_data: bytes) -> object:
    """Try TAGS + READ + CAPTION + DENSE_CAPTIONS first, then CAPTION, then fall back to TAGS + READ only."""
    try:
        return _client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.DENSE_CAPTIONS] + _BASE_FEATURES,
        )
    except Exception:
        try:
            # Region does not support Dense Captions -- try standard Caption
            return _client.analyze(
                image_data=image_data,
                visual_features=[VisualFeatures.CAPTION] + _BASE_FEATURES,
            )
        except Exception:
            # Region does not support Caption or Dense Captions -- retry without them
            return _client.analyze(
                image_data=image_data,
                visual_features=_BASE_FEATURES,
            )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_image(image_path: str) -> dict:
    """Analyze a local image file and return structured extraction results.

    Parameters
    ----------
    image_path : str
        Path to a local image file (.png, .jpg, .jpeg).

    Returns
    -------
    dict
        {
            "source_file":   str,
            "caption":       str | None,
            "confidence":    float | None,
            "tags":          list[str],
            "ocr_lines":     list[str],
            "unified_text":  str          # Markdown-formatted string for indexing
        }
    """
    if not _client:
        return {
            "source_file": image_path,
            "caption": None,
            "confidence": None,
            "tags": [],
            "ocr_lines": [],
            "unified_text": "(Azure Vision client not configured)",
        }

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    result = _request_features_with_caption_fallback(image_data)

    # --- Parse caption (may be None if unsupported) -----------------------
    caption_text = None
    caption_confidence = None
    if hasattr(result, "caption") and result.caption is not None:
        caption_text = result.caption.text
        caption_confidence = result.caption.confidence

    # --- Parse dense captions ---------------------------------------------
    dense_captions: list[str] = []
    if hasattr(result, "dense_captions") and result.dense_captions is not None:
        for caption in result.dense_captions.list:
            dense_captions.append(caption.text)

    # --- Parse tags -------------------------------------------------------
    tags: list[str] = []
    if result.tags is not None:
        tags = [tag.name for tag in result.tags.list]

    # --- Parse OCR lines --------------------------------------------------
    ocr_lines: list[str] = []
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                ocr_lines.append(line.text)

    # --- Build unified Markdown string ------------------------------------
    sections: list[str] = []

    if caption_text:
        sections.append(
            f"**Visual Caption:** {caption_text} "
            f"(confidence: {caption_confidence * 100:.1f}%)"
        )

    if dense_captions:
        joined = "\n".join(f"- {dc}" for dc in dense_captions)
        sections.append(f"**Dense Captions:**\n{joined}")

    if tags:
        sections.append(f"**Visual Tags:** {', '.join(tags)}")

    if ocr_lines:
        joined = "\n".join(f"- {line}" for line in ocr_lines)
        sections.append(f"**OCR Text:**\n{joined}")

    unified_text = "\n\n".join(sections) if sections else "(no data extracted)"

    return {
        "source_file": image_path,
        "caption": caption_text,
        "confidence": caption_confidence,
        "tags": tags,
        "ocr_lines": ocr_lines,
        "unified_text": unified_text,
    }


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    default_path = os.path.join(MEDIA_DIR, "test.png")
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    print(f"Analyzing: {path}\n")
    data = analyze_image(path)

    if data["caption"]:
        print(f"Caption : {data['caption']} ({data['confidence'] * 100:.1f}%)")
    else:
        print("Caption : (not available in this region)")

    print(f"Tags    : {', '.join(data['tags'])}")
    print(f"OCR     : {len(data['ocr_lines'])} lines extracted")
    print()
    print("--- Unified Text for Indexing ---")
    print(data["unified_text"])
