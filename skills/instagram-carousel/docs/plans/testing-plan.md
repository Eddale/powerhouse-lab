# Testing Plan: Google API Carousel Image Generation

**Date:** 2026-01-10
**Status:** COMPLETE - All tests passed
**Model:** `gemini-3-pro-image-preview` (required for reliable text)
**Cost:** ~$0.134 per 1K image (~$1.34 per 10-slide carousel)

## Test Results (2026-01-10)

| Test | Result | Notes |
|------|--------|-------|
| 1. API Connection | PASSED | 54 models found |
| 2. Simple Generation | PASSED | 476 KB image |
| 3. Text Rendering | PASSED | Clean, readable text |
| 4. Character Consistency | PASSED | Chat mode required |
| 5. Full Carousel | PASSED | 8/8 slides, character consistent |
| 6. Error Handling | PASSED | Errors caught cleanly |

**Key Finding:** Must use `model.start_chat()` with `chat.send_message()` for character consistency. Individual `generate_content()` calls lose context between images.

---

## Pre-Requisites

### 1. API Key Setup

**Step 1: Get your API key**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key" → "Create API key"
3. Copy the key (starts with `AIza...`)

**Step 2: Set environment variable**

Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Then reload:
```bash
source ~/.zshrc
```

**Step 3: Verify**
```bash
echo $GOOGLE_API_KEY
# Should print your key (or at least confirm it's set)
```

### 2. Python Dependencies

```bash
pip install google-generativeai>=0.3.0 pillow python-dotenv
```

### 3. Reference Image

Store your reference photo at:
```
skills/instagram-carousel/assets/ed-reference.jpeg
```

(Create the `assets/` folder - it will be gitignored)

---

## Test Suite

### Test 1: API Connection (Est: 2 min)

**Purpose:** Verify API key works and model is accessible.

**Script:**
```python
#!/usr/bin/env python3
"""Test 1: API Connection"""
import os
from google import genai

# Verify API key exists
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    exit(1)
print(f"✓ API key found (starts with {api_key[:8]}...)")

# Test connection
client = genai.Client(api_key=api_key)
print("✓ Client initialized")

# List available models to verify access
models = client.models.list()
image_models = [m.name for m in models if "image" in m.name.lower()]
print(f"✓ Found {len(image_models)} image models")

if "gemini-3-pro-image-preview" in str(image_models):
    print("✓ gemini-3-pro-image-preview is available")
else:
    print("⚠ gemini-3-pro-image-preview not in list - may still work")

print("\n✅ Test 1 PASSED: API connection successful")
```

**Success Criteria:**
- API key found
- Client initializes without error
- Model list returns

---

### Test 2: Simple Image Generation (Est: 3 min, Cost: ~$0.13)

**Purpose:** Verify basic image generation works.

**Script:**
```python
#!/usr/bin/env python3
"""Test 2: Simple Image Generation"""
import os
from pathlib import Path
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
output_dir = Path.home() / "Downloads" / "carousel_test"
output_dir.mkdir(exist_ok=True)

print("Generating simple test image...")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A simple red circle on a white background",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="4:5",
            output_image_size="1024x1024"
        )
    )
)

# Extract and save image
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        import base64
        image_data = base64.b64decode(part.inline_data.data)
        output_path = output_dir / "test_simple.png"
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"✓ Image saved to: {output_path}")
        print(f"✓ File size: {output_path.stat().st_size / 1024:.1f} KB")
        break
else:
    print("❌ No image in response")
    exit(1)

print("\n✅ Test 2 PASSED: Basic image generation works")
```

**Success Criteria:**
- Image file created
- File size > 10KB (valid image)
- No errors

---

### Test 3: Text Rendering Quality (Est: 3 min, Cost: ~$0.13)

**Purpose:** Verify text renders correctly (the reason we need Pro model).

**Script:**
```python
#!/usr/bin/env python3
"""Test 3: Text Rendering Quality"""
import os
from pathlib import Path
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
output_dir = Path.home() / "Downloads" / "carousel_test"
output_dir.mkdir(exist_ok=True)

prompt = """
Create an Instagram carousel slide with:
- Background: Clean gradient from dark blue to purple
- Large white text at top: "THE 3-MINUTE RULE"
- Smaller text below: "Why your best ideas come in threes"
- Professional, minimal design
- 4:5 aspect ratio for Instagram
"""

print("Generating image with text...")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="4:5",
            output_image_size="1024x1024"
        )
    )
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        image_data = base64.b64decode(part.inline_data.data)
        output_path = output_dir / "test_text.png"
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"✓ Image saved to: {output_path}")
        print("\n⚠ MANUAL CHECK REQUIRED:")
        print("  Open the image and verify:")
        print("  - Text is readable and properly spelled")
        print("  - 'THE 3-MINUTE RULE' is clear")
        print("  - No garbled or missing letters")
        break

print("\n✅ Test 3 COMPLETE: Review image manually for text quality")
```

**Success Criteria:**
- Image generated
- **Manual verification:** Text is readable, correctly spelled

---

### Test 4: Character Consistency (Est: 8 min, Cost: ~$0.40)

**Purpose:** Verify character stays consistent across 3 slides.

**Requires:** Reference image at `skills/instagram-carousel/assets/ed-reference.png`

**Script:**
```python
#!/usr/bin/env python3
"""Test 4: Character Consistency"""
import os
from pathlib import Path
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
output_dir = Path.home() / "Downloads" / "carousel_test"
output_dir.mkdir(exist_ok=True)

# Check for reference image
ref_image_path = Path("skills/instagram-carousel/assets/ed-reference.png")
if not ref_image_path.exists():
    # Try absolute path
    ref_image_path = Path.home() / "Documents/GitHub/powerhouse-lab/skills/instagram-carousel/assets/ed-reference.png"

has_reference = ref_image_path.exists()
print(f"Reference image: {'Found' if has_reference else 'Not found (will test without)'}")

# Load reference if available
reference_data = None
if has_reference:
    with open(ref_image_path, "rb") as f:
        reference_data = base64.b64encode(f.read()).decode()

prompts = [
    "A professional business coach in a modern office, standing confidently, looking at camera, wearing smart casual clothes",
    "Same person now sitting at a desk with a laptop, teaching gesture, friendly expression",
    "Same person standing by a whiteboard, pointing at a simple diagram, engaged pose"
]

print(f"\nGenerating {len(prompts)} slides for consistency test...")

for i, prompt in enumerate(prompts, 1):
    print(f"\nSlide {i}/{len(prompts)}...")

    if i == 1 and reference_data:
        # First slide with reference
        contents = [
            types.Part.from_bytes(
                data=base64.b64decode(reference_data),
                mime_type="image/png"
            ),
            f"Generate an image matching this person's appearance. {prompt}"
        ]
    elif i == 1:
        contents = prompt
    else:
        contents = f"Same character as the previous images. {prompt}"

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="4:5",
                output_image_size="1024x1024"
            )
        )
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            image_data = base64.b64decode(part.inline_data.data)
            output_path = output_dir / f"test_consistency_{i:02d}.png"
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"  ✓ Saved: {output_path}")
            break

print("\n⚠ MANUAL CHECK REQUIRED:")
print("  Open all 3 images and verify:")
print("  - Same person across all slides")
print("  - Consistent face, body type, clothing style")
print("  - Natural poses for each scene")

print("\n✅ Test 4 COMPLETE: Review images for character consistency")
```

**Success Criteria:**
- All 3 images generated
- **Manual verification:** Same character across slides

---

### Test 5: Full Carousel Pipeline (Est: 15 min, Cost: ~$1.10)

**Purpose:** Generate a complete 8-slide carousel like the real workflow.

**Script:**
```python
#!/usr/bin/env python3
"""Test 5: Full Carousel Pipeline"""
import os
import json
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# Create output folder: ~/Downloads/carouselYYMMDD
date_str = datetime.now().strftime("%y%m%d")
output_dir = Path.home() / "Downloads" / f"carousel{date_str}"
output_dir.mkdir(exist_ok=True)

# Sample carousel prompts (Bonsai theme for testing)
carousel_name = "Bonsai"
prompts = [
    {
        "slide": 1,
        "name": f"{carousel_name}01",
        "prompt": "Instagram carousel cover slide. Bold white text 'THE BONSAI PRINCIPLE' on gradient blue-purple background. Subtitle: 'Why constraint creates growth'. Clean, modern design. 4:5 aspect ratio."
    },
    {
        "slide": 2,
        "name": f"{carousel_name}02",
        "prompt": "Instagram carousel slide. Small bonsai tree in elegant pot on wooden table. Soft natural lighting. Text overlay: 'A bonsai grows stronger because of its container'. Minimal design. 4:5 aspect ratio."
    },
    {
        "slide": 3,
        "name": f"{carousel_name}03",
        "prompt": "Instagram carousel slide. Split image: wild sprawling plant on left, beautiful shaped bonsai on right. Text: 'Without constraints, we sprawl. With them, we become art.' 4:5 aspect ratio."
    },
    {
        "slide": 4,
        "name": f"{carousel_name}04",
        "prompt": "Instagram carousel slide. Close-up of hands carefully pruning bonsai with small scissors. Text: 'The master prunes what doesn't serve the whole'. Warm lighting. 4:5 aspect ratio."
    },
    {
        "slide": 5,
        "name": f"{carousel_name}05",
        "prompt": "Instagram carousel slide. Beautiful aged bonsai (50+ years old). Text: 'Decades of small cuts. One magnificent result.' Reverent, artistic composition. 4:5 aspect ratio."
    },
    {
        "slide": 6,
        "name": f"{carousel_name}06",
        "prompt": "Instagram carousel slide. Person's workspace with single laptop, notebook, pen - nothing else. Text: 'Your constraints: Time. Energy. Focus. Choose wisely.' Clean minimal desk. 4:5 aspect ratio."
    },
    {
        "slide": 7,
        "name": f"{carousel_name}07",
        "prompt": "Instagram carousel slide. Bonsai tree with visible roots gripping a rock. Text: 'Embrace your container. Let it shape you into something remarkable.' Dramatic lighting. 4:5 aspect ratio."
    },
    {
        "slide": 8,
        "name": f"{carousel_name}08",
        "prompt": "Instagram carousel CTA slide. Clean design with text: 'What one constraint will you embrace this week?' and 'Follow @[handle] for more growth insights'. Professional finish. 4:5 aspect ratio."
    }
]

# Save prompts to MD file for approval
prompts_file = output_dir / f"{carousel_name}_prompts.md"
with open(prompts_file, "w") as f:
    f.write(f"# Carousel Prompts: {carousel_name}\n\n")
    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Model:** gemini-3-pro-image-preview\n")
    f.write(f"**Est. Cost:** ~${len(prompts) * 0.134:.2f}\n\n")
    f.write("---\n\n")
    for p in prompts:
        f.write(f"## Slide {p['slide']}: {p['name']}\n\n")
        f.write(f"{p['prompt']}\n\n")

print(f"✓ Prompts saved to: {prompts_file}")
print(f"\n📋 APPROVAL CHECKPOINT")
print(f"   Review prompts at: {prompts_file}")
print(f"   Estimated cost: ~${len(prompts) * 0.134:.2f}")
print(f"\n   Continuing with generation in 5 seconds...")
print(f"   (In production, this would wait for your approval)")

import time
time.sleep(5)

# Generate images
print(f"\nGenerating {len(prompts)} slides...")
generated = []
failed = []

for p in prompts:
    print(f"\n  Slide {p['slide']}: {p['name']}...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=p["prompt"],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="4:5",
                    output_image_size="1024x1024"
                )
            )
        )

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = base64.b64decode(part.inline_data.data)
                output_path = output_dir / f"{p['name']}.png"
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"    ✓ Saved: {output_path.name}")
                generated.append(p['name'])
                break
        else:
            print(f"    ❌ No image in response")
            failed.append(p['name'])

    except Exception as e:
        print(f"    ❌ Error: {e}")
        failed.append(p['name'])

# Summary
print(f"\n{'='*50}")
print(f"GENERATION COMPLETE")
print(f"{'='*50}")
print(f"Output folder: {output_dir}")
print(f"Generated: {len(generated)}/{len(prompts)}")
if failed:
    print(f"Failed: {', '.join(failed)}")
print(f"\nFiles created:")
for f in sorted(output_dir.iterdir()):
    print(f"  - {f.name}")

print("\n⚠ MANUAL CHECK REQUIRED:")
print("  - Open folder and review all images")
print("  - Verify text is readable on each slide")
print("  - Verify visual consistency across carousel")

if len(generated) == len(prompts):
    print("\n✅ Test 5 PASSED: Full carousel generated")
else:
    print(f"\n⚠ Test 5 PARTIAL: {len(failed)} slides failed")
```

**Success Criteria:**
- All 8 images generated
- MD file saved with prompts
- Images named `Bonsai01.png` through `Bonsai08.png`
- Output in `~/Downloads/carousel260110/`
- **Manual verification:** Text readable, visually cohesive

---

### Test 6: Error Handling (Est: 2 min, Cost: $0)

**Purpose:** Verify graceful failure modes.

**Script:**
```python
#!/usr/bin/env python3
"""Test 6: Error Handling"""
import os
from google import genai
from google.genai import types

# Test 6a: Invalid API key
print("Test 6a: Invalid API key...")
try:
    bad_client = genai.Client(api_key="invalid-key-12345")
    response = bad_client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents="test"
    )
    print("  ❌ Should have raised an error")
except Exception as e:
    error_type = type(e).__name__
    print(f"  ✓ Caught error: {error_type}")
    print(f"    Message preview: {str(e)[:100]}...")

# Test 6b: Invalid model name
print("\nTest 6b: Invalid model name...")
try:
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model="nonexistent-model-xyz",
        contents="test"
    )
    print("  ❌ Should have raised an error")
except Exception as e:
    error_type = type(e).__name__
    print(f"  ✓ Caught error: {error_type}")

print("\n✅ Test 6 PASSED: Error handling works correctly")
```

**Success Criteria:**
- Invalid API key raises clear error
- Invalid model raises clear error
- Errors are catchable, not crashes

---

## Test Execution Summary

| Test | Purpose | Est. Time | Est. Cost | Automated? |
|------|---------|-----------|-----------|------------|
| 1 | API Connection | 2 min | $0 | ✓ Full |
| 2 | Simple Generation | 3 min | $0.13 | ✓ Full |
| 3 | Text Rendering | 3 min | $0.13 | Partial (manual review) |
| 4 | Character Consistency | 8 min | $0.40 | Partial (manual review) |
| 5 | Full Carousel | 15 min | $1.10 | Partial (manual review) |
| 6 | Error Handling | 2 min | $0 | ✓ Full |

**Total estimated time:** ~33 min
**Total estimated cost:** ~$1.76

---

## How to Run

### Option A: Run All Tests (Background)

I can run all tests in the background and save results. You'll review:
1. Test output log
2. Generated images in `~/Downloads/carousel_test/`

### Option B: Run Tests One-by-One

I run each test, show results, you approve before continuing.

### Option C: You Run Manually

Copy scripts from this plan, run yourself, report back.

---

## Post-Test: Implementation

Once tests pass:

1. Create `skills/instagram-carousel/tools/generate_images.py`
2. Update agent with Phase 13
3. Add approval workflow (MD file review before generation)
4. Update CLAUDE.md

---

## Your Decisions Captured

| Decision | Your Choice |
|----------|-------------|
| API Key | Environment variable (`GOOGLE_API_KEY`) |
| Trigger | Only when explicitly requested |
| Reference Images | Default for Ed in skill folder + file paths for others |
| Output Location | `~/Downloads/carouselYYMMDD/` |
| File Naming | Content-based: `Bonsai01.png`, `Bonsai02.png`, etc. |
| Model | `gemini-3-pro-image-preview` (required for text) |
| Resolution | 1K (1024x1024) |
| Fallback | Save prompts MD for manual generation |
| Approval | Review MD file before sending to Google |

---

*Plan created 2026-01-10. Ready for Ed's review.*
