# Integration Plan: Google API for Automated Carousel Image Generation

**Date:** 2026-01-09
**Status:** Draft - Awaiting Ed's Input
**Research:** See `/docs/Research Swarm - Google Imagen 3 API Integration - 2026-01-09.md`

---

## Executive Summary

The instagram-carousel agent currently outputs prompts for manual use in Nano Banana Pro (Google AI Studio web interface). This integration will enable **automatic image generation** via the Google API, solving the "reference image consistency" problem you flagged in CLAUDE.md.

**Key insight:** The solution isn't Imagen 3 - it's **Gemini 2.5 Flash Image**, which maintains character consistency through conversational context.

**Cost:** ~$0.40 per 10-slide carousel (~$8/month at 200 images)

---

## Architecture Decision

### Option A: Extend the Agent (Recommended)

Add image generation as an **optional Phase 13** in the existing agent pipeline.

```
Current:  Agent → Prompts → Manual Generation in AI Studio
Proposed: Agent → Prompts → [Optional] API Generation → Images + Prompts
```

**Pros:**
- Single workflow - Ed says "create carousel" and gets images
- Character consistency handled in one API conversation
- Agent already has all context (prompts, audience, metaphor)

**Cons:**
- Requires API key management
- Adds latency (~20-30s for full carousel)
- Agent becomes more complex

### Option B: Separate Image Generation Skill

Create a new `carousel-image-generator` skill the agent can invoke.

```
Agent → Prompts + Save to file → Skill reads file → API → Images
```

**Pros:**
- Clean separation of concerns
- Skill could be reused for other image generation
- Easier to test independently

**Cons:**
- Two-step process (agent then skill)
- Context handoff complexity (reference images, character consistency)
- Breaks the "single command" flow

### Recommendation: Option A

For carousel generation specifically, character consistency requires **conversational context** - the API remembers the character across slides. Breaking this into a separate skill loses that context. Keep it in the agent.

---

## Technical Implementation Plan

### Phase 1: Foundation (Pre-requisites)

1. **Enable Google Cloud Billing**
   - Create project or use existing
   - Enable Gemini API
   - Generate API key for `gemini-2.5-flash-image`

2. **Environment Setup**
   ```bash
   # Add to your environment (secure location)
   export GOOGLE_API_KEY="your-api-key"
   ```

3. **Install Dependencies**
   ```bash
   pip install google-generativeai>=0.3.0 pillow python-dotenv
   ```

### Phase 2: Create API Tool

Build `/home/user/powerhouse-lab/skills/instagram-carousel/tools/generate_images.py`:

```python
#!/usr/bin/env python3
"""
Carousel Image Generator
Uses Gemini 2.5 Flash Image for character-consistent carousel generation.
"""

import os
import sys
import json
import base64
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def load_reference_image(path: str) -> bytes:
    """Load and encode reference image."""
    with open(path, "rb") as f:
        return f.read()

def generate_carousel_images(
    prompts: list[str],
    output_dir: str,
    reference_image_path: str = None,
    aspect_ratio: str = "4:5"
) -> list[str]:
    """
    Generate carousel images with character consistency.

    Args:
        prompts: List of image prompts (one per slide)
        output_dir: Directory to save generated images
        reference_image_path: Optional path to character reference image
        aspect_ratio: Image aspect ratio (default 4:5 for Instagram)

    Returns:
        List of paths to generated images
    """
    client = genai.Client()  # Uses GOOGLE_API_KEY env var

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_paths = []

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=aspect_ratio)
    )

    for i, prompt in enumerate(prompts, 1):
        print(f"Generating slide {i}/{len(prompts)}...", file=sys.stderr)

        if i == 1 and reference_image_path:
            # First slide: include reference image for character consistency
            ref_image = load_reference_image(reference_image_path)
            content = [
                types.Part.from_bytes(ref_image, mime_type="image/png"),
                f"Generate an image matching this person's appearance. {prompt}"
            ]
        elif i == 1:
            # First slide without reference
            content = prompt
        else:
            # Subsequent slides: maintain character from conversation
            content = f"Same character as previous images. {prompt}"

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=content,
            config=config
        )

        # Extract and save image
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image_path = output_path / f"slide_{i:02d}.png"
                image.save(str(image_path))
                generated_paths.append(str(image_path))
                break

    return generated_paths

def main():
    """CLI interface for carousel generation."""
    if len(sys.argv) < 3:
        print("Usage: generate_images.py <prompts_json> <output_dir> [reference_image]")
        print("  prompts_json: Path to JSON file with list of prompts")
        print("  output_dir: Directory to save generated images")
        print("  reference_image: Optional path to character reference image")
        sys.exit(1)

    prompts_file = sys.argv[1]
    output_dir = sys.argv[2]
    reference_image = sys.argv[3] if len(sys.argv) > 3 else None

    with open(prompts_file) as f:
        prompts = json.load(f)

    paths = generate_carousel_images(prompts, output_dir, reference_image)

    # Output JSON array of generated paths
    print(json.dumps(paths))

if __name__ == "__main__":
    main()
```

### Phase 3: Update Agent Pipeline

Add **Phase 13: Generate Images (Optional)** to `.claude/agents/instagram-carousel.md`:

```markdown
### Phase 13: Generate Images (Optional)

**Trigger:** User has API key configured AND requests automatic generation.

**Detection:**
- Check if `GOOGLE_API_KEY` environment variable exists
- Look for phrases: "generate images", "create images", "automatic", "with images"

**If triggered:**

1. **Save prompts to JSON:**
   ```
   /tmp/carousel_prompts_[timestamp].json
   ```

2. **Run generation tool:**
   ```bash
   python3 skills/instagram-carousel/tools/generate_images.py \
     /tmp/carousel_prompts_[timestamp].json \
     /tmp/carousel_images_[timestamp]/ \
     [reference_image_path if provided]
   ```

3. **Verify outputs:**
   - Check all images generated
   - Display file paths
   - Report any failures

4. **Update output:**
   - Add "Generated Images" section with file paths
   - Note which slides succeeded/failed

**If NOT triggered:**
- Skip this phase (current behavior)
- Prompts ready for manual generation in AI Studio
```

### Phase 4: Handle Reference Images

**The Character Consistency Flow:**

```
1. Ed provides reference photo (optional)
   ↓
2. Agent asks "Do you want to appear as narrator?" (existing Phase 1)
   ↓
3. If yes: store reference image path in carousel context
   ↓
4. Phase 13: Pass reference image to first API call
   ↓
5. API maintains character across all subsequent slides
```

**Key insight:** Gemini 2.5 Flash Image uses conversational context. We don't need to send the reference image with every prompt - just the first one. The model "remembers" the character.

---

## Testing Routine

### Test 1: API Connection (5 min)

```python
# test_api_connection.py
from google import genai

client = genai.Client()
print("API connection successful")

# Simple generation test
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A simple red circle on white background",
    config={"response_modalities": ["IMAGE"]}
)
print(f"Response parts: {len(response.parts)}")
```

**Success criteria:** Response contains image part

### Test 2: Character Consistency (15 min)

```python
# test_character_consistency.py
"""
Generate 3 slides with same character to verify consistency.
"""
prompts = [
    "A professional business coach standing confidently in a modern office",
    "Same person now sitting at a desk, looking at camera, teaching",
    "Same person standing by a whiteboard, pointing at a diagram"
]

# Generate with NO reference image first
# Then generate WITH reference image
# Compare consistency
```

**Success criteria:** Character features (face, clothing, body type) remain consistent across slides

### Test 3: Full Carousel Pipeline (30 min)

```python
# test_full_carousel.py
"""
Full integration test:
1. Load a real carousel output (prompts from Phase 8)
2. Generate all 8 images
3. Verify consistency and quality
"""
```

**Success criteria:**
- All 8 images generated
- Character consistent across slides
- Text placement matches prompt intent
- Total time < 2 minutes

### Test 4: Error Handling (10 min)

Test failure modes:
- Invalid API key → Clear error message
- Network timeout → Retry with exponential backoff
- Rate limit (429) → Queue and retry
- Partial failure → Save successful images, report failures

---

## Open Questions for Ed

### 1. API Key Management
How do you want to handle the API key?
- a) Environment variable (`GOOGLE_API_KEY`)
- b) Stored in a config file (gitignored)
- c) Prompt for it when needed

### 2. Generation Trigger
When should images auto-generate?
- a) Always (when API key present)
- b) Only when explicitly requested ("generate images")
- c) Ask each time ("Generate images now? Y/N")

### 3. Reference Image Workflow
Current agent asks "Do you want to appear as narrator?" If yes:
- a) User attaches image in chat → agent saves to temp location → passes to API
- b) User provides file path → agent uses directly
- c) Store a "default reference image" for Ed's character

### 4. Output Location
Where should generated images go?
- a) Zettelkasten (with carousel notes)
- b) Downloads folder
- c) Dedicated `~/carousel-images/[date]/` folder

### 5. Quality vs Speed
Which model for production?
- a) `gemini-2.5-flash-image` - Faster, ~$0.04/image, good consistency
- b) `gemini-3-pro-image-preview` - Slower, better consistency, 14 reference images
- c) Start with (a), upgrade to (b) when it's GA

### 6. Fallback Behavior
If image generation fails:
- a) Still save prompts (current behavior) so you can generate manually
- b) Retry failed slides once
- c) Both

---

## Implementation Timeline

| Phase | Description | Depends On |
|-------|-------------|------------|
| 1 | Enable billing, get API key | Ed's Google Cloud |
| 2 | Build generate_images.py tool | Phase 1 |
| 3 | Test API connection + consistency | Phase 2 |
| 4 | Update agent with Phase 13 | Phase 3 success |
| 5 | Full integration testing | Phase 4 |
| 6 | Update CLAUDE.md (solved problem) | Phase 5 |

---

## Cost Projection

| Usage Level | Images/Month | Monthly Cost |
|-------------|--------------|--------------|
| Light (2 carousels/week) | 80 | $3.12 |
| Medium (5 carousels/week) | 200 | $7.80 |
| Heavy (daily carousels) | 300 | $11.70 |

Negligible cost for significant automation gain.

---

## CLAUDE.md Update (When Complete)

Replace in CLAUDE.md:

```markdown
### Image Generation with Nano Banana Pro

When generating carousel images or any multi-image set with a consistent character:
1. **Reference image required** - Upload photo with first prompt
2. **Add consistency instruction** - Include "maintain consistent character appearance from reference" in all prompts
3. **Test before finalizing** - Generate in Google AI Studio, verify quality, then commit
4. **API consideration** - Programmatic reference image upload is an unsolved problem for automation
```

With:

```markdown
### Image Generation with Nano Banana Pro

Carousel images can be generated automatically via the Google API:

1. **API setup:** Set `GOOGLE_API_KEY` environment variable
2. **Reference image optional:** Upload once, API maintains consistency via conversation
3. **Model:** `gemini-2.5-flash-image` (production) or `gemini-3-pro-image-preview` (best quality)
4. **Cost:** ~$0.04/image (~$0.40 per 10-slide carousel)

Manual generation in AI Studio still works - just use the prompts from the carousel output.

See `skills/instagram-carousel/docs/plans/google-api-integration.md` for technical details.
```

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `skills/instagram-carousel/tools/generate_images.py` | Create | API wrapper script |
| `skills/instagram-carousel/tools/requirements.txt` | Create | Python dependencies |
| `.claude/agents/instagram-carousel.md` | Modify | Add Phase 13 |
| `CLAUDE.md` | Modify | Update "unsolved problem" note |
| `skills/instagram-carousel/docs/ROADMAP.md` | Modify | Log this improvement |

---

*Plan created 2026-01-09. Awaiting Ed's answers to open questions before implementation.*
