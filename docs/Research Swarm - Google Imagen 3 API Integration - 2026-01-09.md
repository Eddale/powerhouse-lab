# Research Swarm: Google Imagen 3 API Integration

**Research Date:** 2026-01-09
**Angles Investigated:** API Documentation, Python SDK, Reference Image Handling, Rate Limits & Pricing, Best Practices

---

## Executive Summary

Google's image generation landscape has evolved significantly. **Imagen 3 is being superseded by newer models** - particularly **Gemini 2.5 Flash Image (Nano Banana)** and **Gemini 3 Pro Image (Nano Banana Pro)**. The critical "reference image for character consistency" problem you flagged in CLAUDE.md **is now solvable** via these newer Gemini models, which support multi-image input and native character consistency.

**Key recommendation:** For carousel/batch image generation with consistent characters, use **Gemini 2.5 Flash Image** (production-ready) or **Gemini 3 Pro Image** (preview, supports up to 14 reference images and 5 people). Skip pure Imagen 3 - it's being deprecated for some features.

---

## Findings by Angle

### 1. API Documentation Angle

**Imagen 3 on Vertex AI:**
- Endpoint: `https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/imagen-3.0-generate-002:predict`
- Authentication: Bearer token via `gcloud auth print-access-token`
- Model versions: `imagen-3.0-generate-002` (standard), `imagen-3.0-fast-generate-001` (40% faster)

**Critical Deprecation Notice:**
- Imagen versions 1 and 2 deprecated June 24, 2025, removed September 24, 2025
- **Imagen subject model and style model tuning will be removed December 31, 2025**
- Imagen 4 is now available: `imagen-4.0-generate-001`, `imagen-4.0-ultra-generate-001`, `imagen-4.0-fast-generate-001`

**Gemini Image Models (Recommended):**
- `gemini-2.5-flash-image` - Production-ready, best for iterative/batch work
- `gemini-3-pro-image-preview` - Preview, best for character consistency (up to 14 reference images)

**Sources:**
- [Imagen 3 Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/3-0-generate)
- [Image Generation API Reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api)
- [Vertex AI Release Notes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes)

---

### 2. Python SDK Angle

**Two SDK Options:**

**Option A: Google GenAI SDK (Recommended for Gemini models)**
```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client(api_key='YOUR_GEMINI_API_KEY')

# Basic image generation
response = client.models.generate_images(
    model='imagen-3.0-generate-002',
    prompt='a portrait of a sheepadoodle wearing cape',
    config=types.GenerateImagesConfig(
        number_of_images=1,
    )
)

for generated_image in response.generated_images:
    image = Image.open(BytesIO(generated_image.image.image_bytes))
    image.save("output.png")
```

**Option B: Gemini 2.5 Flash Image (for conversational editing & consistency)**
```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GOOGLE_API_KEY env var

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Create a professional headshot of a business coach",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],  # Image-only output
        image_config=types.ImageConfig(
            aspect_ratio="1:1",  # Options: 1:1, 4:5, 16:9, etc.
        )
    )
)

# Extract image from response
for part in response.parts:
    if part.inline_data is not None:
        generated_image = part.as_image()
        generated_image.save("headshot.png")
```

**Option C: Vertex AI SDK (Enterprise)**
```python
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

vertexai.init(project=PROJECT_ID, location="us-central1")
model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
images = model.generate_images(
    prompt="Professional business coach portrait",
    number_of_images=4,
    aspect_ratio="1:1"
)
```

**Installation:**
```bash
pip install google-generativeai>=0.3.0
pip install pillow requests python-dotenv
```

**Sources:**
- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Imagen 3 Notebook Example](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen3_image_generation.ipynb)
- [Gemini API Imagen Docs](https://ai.google.dev/gemini-api/docs/imagen)

---

### 3. Reference Image Handling Angle (CRITICAL FINDING)

**The Problem You Identified:** "Programmatic reference image upload is an unsolved problem for automation"

**The Solution: It's Solved in Newer Models**

**Imagen 3 Customization (`imagen-3.0-capability-001`):**
- Supports up to 4 reference images
- Uses `referenceType` and `referenceId` system
- Limited to single-person consistency (cannot maintain 2+ people)

```json
{
  "instances": [{
    "prompt": "[$1] standing in a modern office",
    "referenceImages": [{
      "referenceType": "REFERENCE_TYPE_SUBJECT",
      "referenceId": 1,
      "referenceImage": {
        "bytesBase64Encoded": "BASE64_IMAGE_DATA"
      },
      "subjectImageConfig": {
        "subjectDescription": "professional man",
        "subjectType": "SUBJECT_TYPE_PERSON"
      }
    }]
  }],
  "parameters": {"sampleCount": 4}
}
```

**Gemini 2.5 Flash Image (Better Option):**
- Character consistency built into the model's reasoning
- Multi-turn conversation maintains character across generations
- Supports up to 5 images of humans for consistency
- No complex reference image API - just describe in conversation

**Gemini 3 Pro Image (Best Option for Carousels):**
- Supports up to **14 reference images** total
- Up to 6 images of objects (high-fidelity inclusion)
- Up to 5 images of humans (character consistency)
- Explicit role assignments: "Image A: pose", "Image B: face reference"

**Practical Approach for Carousels:**
1. Upload a reference photo in the first message
2. Generate carousel slide 1
3. Continue conversation, referencing the established character
4. Model maintains consistency across the carousel series

**Sources:**
- [Image Customization API](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api-customization)
- [Subject Customization](https://cloud.google.com/vertex-ai/generative-ai/docs/image/subject-customization)
- [Gemini 3 Pro Image](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)

---

### 4. Rate Limits & Pricing Angle

**Pricing (Per Image):**

| Model | Price | Notes |
|-------|-------|-------|
| Imagen 3 Fast | $0.02 | 40% faster, slightly lower quality |
| Imagen 3 Standard | $0.04 | Highest quality |
| Gemini 2.5 Flash Image | ~$0.039 | 1290 tokens/image at $30/M tokens |
| Imagen 4 | $0.02-0.08 | Varies by version |

**Free Tier:**
- Google AI Studio: 500-1000 images/day via web interface
- **API access requires billing** - no free tier for programmatic image generation
- Tier 1 (billing enabled) required for API access

**Rate Limits:**
- Measured in IPM (Images Per Minute), not tokens
- Free tier: 10-15 requests/minute
- Limits are per-project, not per-API-key
- RPD (Requests Per Day) resets at midnight Pacific

**Tier System:**
- Tier 1: Basic billing enabled
- Tier 2: After $250 cumulative spend + 30 days (24-48hr activation)
- Tier 3: Higher volumes, custom arrangements

**Batch Processing:**
- Gemini 2.5 Flash Image: Up to 50 images per request
- Imagen 3: `number_of_images` parameter accepts 1-4 per call

**December 2025 Update:**
- Quota adjustments may cause unexpected 429 errors
- Web interface limits unchanged; API limits tightened

**Sources:**
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Google AI Studio Image Limits Guide](https://www.aifreeapi.com/en/posts/google-ai-studio-image-generation-limits)

---

### 5. Best Practices Angle

**For Carousel/Social Media Image Generation:**

**Consistency Patterns:**
1. **Prompt Templates:** Keep image direction stable with consistent template structure
2. **Separate Concerns:** Break prompts into subject, context, style, lighting segments
3. **Iterative > Perfect First Try:** Expect 2-3 refinement cycles

**Seed for Reproducibility:**
- Same seed + same prompt + same model version = same image
- Useful for regenerating with minor tweaks

**Batch Generation Architecture:**
```
1. Generate character reference image
2. Store character description as template
3. For each carousel slide:
   - Use consistent prompt template
   - Reference the character description
   - Maintain aspect ratio (1:1 or 4:5 for Instagram)
4. Review and regenerate any inconsistent slides
```

**n8n Workflow Pattern (Alternative):**
- Sequential generation: each image based on previous
- Helps maintain narrative consistency
- Auto-publish to Instagram/TikTok

**Aspect Ratios for Social:**

| Platform | Aspect Ratio | Imagen Parameter |
|----------|--------------|------------------|
| Instagram Feed | 1:1 or 4:5 | `"1:1"` or `"4:5"` |
| Instagram Stories | 9:16 | `"9:16"` |
| LinkedIn Carousel | 1:1 | `"1:1"` |
| Twitter/X | 16:9 | `"16:9"` |

**Key Tips:**
- All generated images include SynthID watermark (invisible, identifies as AI-generated)
- Use `enhance_prompt=True` for higher quality (auto-expands your prompt)
- Restart conversation if character features drift after many edits

**Sources:**
- [DataCamp Imagen 3 Tutorial](https://www.datacamp.com/tutorial/imagen-3)
- [Gemini 2.5 Flash Prompting Guide](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [n8n Carousel Workflow](https://n8n.io/workflows/4028-generate-and-publish-carousels-for-tiktok-and-instagram-with-gpt-image-1/)

---

## Recommendations

### For Your Carousel Integration

**Recommended Approach:**

1. **Use Gemini 2.5 Flash Image** (`gemini-2.5-flash-image`) for production
   - Character consistency via conversational editing
   - ~$0.04/image, fast latency
   - Can process multiple images in single request

2. **Upgrade to Gemini 3 Pro Image** when it goes GA
   - 14 reference images for maximum control
   - Better for complex multi-person scenarios

3. **Skip pure Imagen 3** for carousel work
   - Reference image handling is clunky
   - Subject/style tuning being deprecated Dec 31, 2025

**Implementation Pattern:**
```python
# Pseudo-code for carousel generation
def generate_carousel(character_ref_image, slide_prompts, api_key):
    client = genai.Client(api_key=api_key)
    images = []

    # First slide with reference
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            character_ref_image,  # Upload as bytes
            f"Generate an image matching this person's appearance: {slide_prompts[0]}"
        ],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="1:1")
        )
    )
    images.append(extract_image(response))

    # Subsequent slides maintain conversation context
    for prompt in slide_prompts[1:]:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=f"Same person, new scene: {prompt}",
            config=...
        )
        images.append(extract_image(response))

    return images
```

### Cost Estimate for Carousel Batch

| Scenario | Images | Cost (Gemini 2.5) | Cost (Imagen 3) |
|----------|--------|-------------------|-----------------|
| Single carousel (10 slides) | 10 | $0.39 | $0.40 |
| Weekly content (5 carousels) | 50 | $1.95 | $2.00 |
| Monthly batch | 200 | $7.80 | $8.00 |

Essentially equivalent pricing, but Gemini 2.5 Flash offers better character consistency features.

---

## Open Questions (Need Testing)

1. **Multi-turn API:** Does the Gemini API maintain character context across separate API calls, or only within a single conversation thread?

2. **Reference Image Quality:** What resolution/format works best for reference images? PNG vs JPG? Minimum dimensions?

3. **Batch Limits:** Can you truly do 50 images per request with Gemini 2.5 Flash, and what's the practical timeout?

4. **Gemini 3 Pro GA Timeline:** When does `gemini-3-pro-image-preview` become production-ready?

5. **SynthID Detection:** Does the invisible watermark affect downstream usage (e.g., Instagram compression)?

---

## Next Steps

1. **Set up API access:** Enable billing on Google Cloud, get API key
2. **Test character consistency:** Run a proof-of-concept with 3-5 carousel slides
3. **Build skill:** Create `carousel-image-generator` skill wrapping the API
4. **Update CLAUDE.md:** Replace "unsolved problem" note with working solution

---

## Sources

### Official Documentation
- [Imagen 3 Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/3-0-generate)
- [Gemini API Image Generation](https://ai.google.dev/gemini-api/docs/imagen)
- [Image Customization API](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api-customization)
- [Gemini 3 Pro Image](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- [Gemini 2.5 Flash Image](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-image)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)

### Tutorials & Guides
- [A Developer's Guide to Imagen 3 on Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/a-developers-guide-to-imagen-3-on-vertex-ai)
- [DataCamp Imagen 3 Tutorial](https://www.datacamp.com/tutorial/imagen-3)
- [Gemini 2.5 Flash Prompting Guide](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [Introducing Gemini 2.5 Flash Image](https://developers.googleblog.com/introducing-gemini-2-5-flash-image/)

### SDKs & Code Examples
- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Imagen 3 Notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen3_image_generation.ipynb)
- [n8n Carousel Workflow](https://n8n.io/workflows/4028-generate-and-publish-carousels-for-tiktok-and-instagram-with-gpt-image-1/)

---

*Generated by Research Swarm agent - 2026-01-09*
