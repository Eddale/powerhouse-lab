# Instagram Carousel Skill - TODO

## Future Enhancements

### Visual Storytelling Training
- [ ] Research great comic book artists (storytelling through panels, not just pretty pictures)
- [ ] Study how masters use images to carry narrative weight
- [ ] Update manga-style-guide.md with storytelling principles
- [ ] Goal: Images do heavy lifting in the story, not just illustrate text

### Multi-Input Support
- [ ] Accept YouTube video URLs (pull transcript, extract key points)
- [ ] Accept PDF documents
- [ ] Accept raw text/topics (already works)
- [ ] Detect input type and route to appropriate parser

### Audience Context
- [ ] Pull target audience from mission-context by default
- [ ] Ask for audience override only when context doesn't apply
- [ ] Pass audience to hook-stack-evaluator for "Speak Their Lingo" scoring
- [ ] Consider: Different carousel styles for different audiences?

## Open Questions

### Character Limit
- Current: 25-char limit enforced
- Testing: Does shorter text provide enough value to the reader?
- Tension: Clean rendering vs. meaningful content
- Need: More real-world testing before finalizing

## Ideas Parking Lot

- Style library beyond manga (minimal, branded, photographic?)
- Batch carousel generation from article series
- QA agent to verify text rendered correctly in generated images
- Automated image generation via Gemini API (post-MVP)
