#!/usr/bin/env python3
"""
Carousel Image Generator
========================
Generates character-consistent carousel images using Google's Gemini 3 Pro Image API.

Uses chat mode to maintain character consistency across all slides.
Requires GOOGLE_API_KEY environment variable.

Usage:
    python3 generate_images.py <prompts_json> <output_dir> [--reference <image_path>] [--name <carousel_name>]

Arguments:
    prompts_json    Path to JSON file containing list of prompt strings
    output_dir      Directory to save generated images (created if doesn't exist)

Options:
    --reference     Path to reference image for character consistency
    --name          Carousel name for file naming (default: "Slide")
    --ed            Use Ed's default reference image

Example:
    python3 generate_images.py prompts.json ~/Downloads/carousel260110 --ed --name Bonsai
"""

import os
import sys
import json
import argparse
import warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings("ignore")

# Default reference image location
DEFAULT_ED_REFERENCE = Path(__file__).parent.parent / "assets" / "ed-reference.jpeg"


def load_reference_image(path: Path) -> bytes:
    """Load reference image as bytes."""
    with open(path, "rb") as f:
        return f.read()


def generate_carousel_images(
    prompts: list[str],
    output_dir: Path,
    reference_image_path: Path = None,
    carousel_name: str = "Slide"
) -> dict:
    """
    Generate carousel images with character consistency using chat mode.

    Args:
        prompts: List of image prompts (one per slide)
        output_dir: Directory to save generated images
        reference_image_path: Path to character reference image (optional)
        carousel_name: Base name for output files (e.g., "Bonsai" -> Bonsai01.png)

    Returns:
        dict with 'generated' (list of paths) and 'failed' (list of slide numbers)
    """
    import google.generativeai as genai

    # Configure API
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load reference image if provided
    ref_data = None
    if reference_image_path and reference_image_path.exists():
        ref_data = load_reference_image(reference_image_path)
        print(f"Reference image: {reference_image_path.name}", file=sys.stderr)

    # Create model and start chat session for character consistency
    model = genai.GenerativeModel("gemini-3-pro-image-preview")
    chat = model.start_chat(history=[])

    generated = []
    failed = []

    for i, prompt in enumerate(prompts, 1):
        slide_name = f"{carousel_name}{i:02d}"
        print(f"Generating {slide_name}...", file=sys.stderr)

        try:
            if i == 1 and ref_data:
                # First slide with reference image
                response = chat.send_message([
                    {"mime_type": "image/jpeg", "data": ref_data},
                    f"This is my reference photo. Use this exact person's appearance throughout all images. {prompt}"
                ])
            else:
                # Subsequent slides - chat maintains character context
                response = chat.send_message(prompt)

            # Extract and save image
            saved = False
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    output_path = output_dir / f"{slide_name}.png"
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    generated.append(str(output_path))
                    print(f"  Saved: {slide_name}.png", file=sys.stderr)
                    saved = True
                    break

            if not saved:
                failed.append(i)
                print(f"  Warning: No image in response for slide {i}", file=sys.stderr)

        except Exception as e:
            failed.append(i)
            print(f"  Error on slide {i}: {str(e)[:60]}", file=sys.stderr)

    return {
        "generated": generated,
        "failed": failed,
        "total": len(prompts),
        "output_dir": str(output_dir)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate character-consistent carousel images using Gemini API"
    )
    parser.add_argument("prompts_json", help="Path to JSON file with list of prompts")
    parser.add_argument("output_dir", help="Directory to save generated images")
    parser.add_argument("--reference", help="Path to reference image for character consistency")
    parser.add_argument("--name", default="Slide", help="Carousel name for file naming")
    parser.add_argument("--ed", action="store_true", help="Use Ed's default reference image")

    args = parser.parse_args()

    # Load prompts
    prompts_path = Path(args.prompts_json)
    if not prompts_path.exists():
        print(f"Error: Prompts file not found: {prompts_path}", file=sys.stderr)
        sys.exit(1)

    with open(prompts_path) as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        print("Error: Prompts JSON must be a list of strings", file=sys.stderr)
        sys.exit(1)

    # Determine reference image
    reference_path = None
    if args.ed:
        reference_path = DEFAULT_ED_REFERENCE
        if not reference_path.exists():
            print(f"Warning: Ed's reference image not found at {reference_path}", file=sys.stderr)
            reference_path = None
    elif args.reference:
        reference_path = Path(args.reference)
        if not reference_path.exists():
            print(f"Warning: Reference image not found: {reference_path}", file=sys.stderr)
            reference_path = None

    # Generate images
    output_dir = Path(args.output_dir)
    result = generate_carousel_images(
        prompts=prompts,
        output_dir=output_dir,
        reference_image_path=reference_path,
        carousel_name=args.name
    )

    # Output result as JSON (for parsing by caller)
    print(json.dumps(result, indent=2))

    # Exit with error if any failed
    if result["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
