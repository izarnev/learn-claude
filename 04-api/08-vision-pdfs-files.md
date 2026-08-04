---
title: "08 · Vision, PDFs, and the Files API"
---

# 08 · Vision, PDFs, and the Files API

**What you'll learn:** getting images and documents into the API efficiently.

---

## Images

Three ways to supply one:

```python
# Base64
{
    "type": "image",
    "source": {"type": "base64", "media_type": "image/jpeg", "data": b64_string},
}

# URL
{"type": "image", "source": {"type": "url", "url": "https://example.com/chart.png"}}

# Files API
{"type": "image", "source": {"type": "file", "file_id": "file_abc123"}}
```

Supported: JPEG, PNG, GIF, WebP.

### Cost

Images are converted to tokens based on dimensions. **Resize before uploading.** A 4000×3000 screenshot costs several thousand tokens; the same content at 1500px costs a fraction and is usually just as legible.

Rule of thumb: if you can read it comfortably at the size you're sending, so can Claude.

### The crop technique

Anthropic's testing shows consistent uplift when Claude can "zoom in" on relevant image regions. If you're building something image-heavy, give Claude a **crop tool** — there's an [official recipe](https://platform.claude.com/cookbook/multimodal-crop-tool). It's one of the cheapest accuracy wins available.

### Multiple images

Current Opus models handle multi-image contexts notably better than earlier generations. Label them in the text so Claude can refer to them:

```python
content = [
    {"type": "text", "text": "Image 1 — current design:"},
    {"type": "image", "source": {...}},
    {"type": "text", "text": "Image 2 — proposed redesign:"},
    {"type": "image", "source": {...}},
    {"type": "text", "text": "List every difference in the navigation."},
]
```

### Coordinates

For tasks needing spatial precision — bounding boxes, UI element locations — see [Coordinates and bounding boxes](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates).

### Video

Not directly supported. Split into frames and send those. Works well for short clips.

---

## PDFs

```python
{
    "type": "document",
    "source": {"type": "base64", "media_type": "application/pdf", "data": b64_pdf},
}
```

Claude processes both the text and the visual layout — so charts, tables and scanned pages work, not just extractable text.

**Cost note:** visual processing costs substantially more per page than text. For a text-only PDF where layout doesn't matter, extracting the text yourself and sending it as text is much cheaper.

Decision rule:

| PDF | Send as |
|---|---|
| Text-only, layout irrelevant | Extracted text |
| Charts, complex tables, forms, scans | The PDF itself |
| Very long, but you need one section | Extract that section |

See [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support).

---

## The Files API

Upload once, reference many times.

```python
uploaded = client.beta.files.upload(
    file=("report.pdf", open("report.pdf", "rb"), "application/pdf"),
    betas=["files-api-2025-04-14"],
)

response = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    betas=["files-api-2025-04-14"],
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "file", "file_id": uploaded.id}},
            {"type": "text", "text": "Summarise the key findings."},
        ],
    }],
)
```

**Why it matters:**

- No re-uploading the same file across requests
- Required for getting files **into** and **out of** the code execution container — which is how you feed data to Agent Skills and retrieve the documents they produce
- Cleaner than base64 for anything large

---

## Grounding: the pattern that prevents hallucination

The same technique from [01-foundations/02](../01-foundations/02-prompting-fundamentals.md), now in code:

```python
prompt = """
<method>
1. Extract every passage from the document relevant to the question into
   <quotes> tags, with page numbers.
2. Answer using only those quotes, in <answer> tags.
3. If the quotes are insufficient for a complete answer, say what's missing in
   <answer> rather than filling the gap.
</method>

<question>{question}</question>
"""
```

Step 3 is the one people leave out and the one that stops confident invention.

For production RAG, use the [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) feature instead — it gives sentence-level citations back to your source documents natively, which is both more reliable and cheaper than a prompted pattern.

---

## Try it

**Exercise 1 — Image cost.**
Send the same screenshot at 4000px and 1500px. Compare `usage.input_tokens` and answer quality.

**Exercise 2 — Chart extraction.**
Extract data from a chart image into a structured output ([module 06](06-structured-outputs.md)). Verify against the axes yourself.

**Exercise 3 — PDF, two ways.**
Take a text-heavy PDF. Send it as a document, and separately as extracted text. Compare cost and answer quality. Decide your default.

**Exercise 4 — Files API pipeline.**
Upload a CSV, use code execution to analyse it, and download the resulting chart via the Files API.

**Exercise 5 — Citations.**
Build a small RAG system using the Citations feature. Verify every citation on ten questions.

**Exercise 6 — Crop tool.**
Implement a crop tool as a client tool. Run an image-heavy task with and without it. Measure the accuracy difference.

---

## Checkpoint

- You resize images before sending them
- You know when a PDF should go as a document and when as extracted text
- You use Citations rather than a prompted quote pattern for production RAG

---

## Going deeper

- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
- [Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Coordinates and bounding boxes](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates)
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Crop tool recipe](https://platform.claude.com/cookbook/multimodal-crop-tool)
