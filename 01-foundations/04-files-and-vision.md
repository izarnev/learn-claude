# 04 · Files, images, and vision

**What you'll learn:** how to get material into Claude effectively, and how to work with images and PDFs without wasting context or getting hallucinated readings.

---

## What you can upload

In the chat apps you can attach:

- **Documents** — PDF, DOCX, TXT, MD, RTF, CSV
- **Spreadsheets** — XLSX, CSV
- **Images** — PNG, JPG, GIF, WEBP
- **Code** — any text-based source file
- **Data** — JSON, XML, YAML

You can drag and drop, paste directly (screenshots especially), or use the attachment button.

Limits on file size and count vary by plan and change over time — see [Upload files to Claude](https://support.claude.com/en/articles/8241126-upload-files-to-claude).

---

## How Claude actually reads a file

This is worth understanding because it explains several confusing behaviours.

**Text files** are converted to text and placed in the context window. Straightforward.

**PDFs** are handled two ways depending on the surface and the document. Text-based PDFs get extracted as text. PDFs with meaningful visual layout — charts, scanned pages, complex tables — are also processed as **images**, so Claude can see the layout. Image processing costs substantially more tokens per page.

**Images** are converted into tokens based on dimensions. A large screenshot can cost a few thousand tokens. Resizing a 4000px screenshot down to 1500px before uploading saves real money and usually loses nothing.

**Spreadsheets** are converted to a text representation. For anything with formulas, pivot logic, or many sheets, this loses fidelity — use Claude for Excel (module [02-power-user/05](../02-power-user/05-claude-in-your-apps.md)) or ask Claude to write code against the file instead.

### The consequence

Everything you attach consumes context on **every subsequent turn**. Attaching a 300-page PDF and then having a 30-turn conversation is expensive and, past a point, degrades quality.

**Better patterns:**

- Attach only the pages or sections you need
- For repeated use of the same material, put it in a **Project** knowledge base (module [02-power-user/01](../02-power-user/01-projects.md)) so it's retrieved rather than always resident
- For very large corpora, let Claude write code to search the files rather than reading them all

---

## Working with documents well

### Ask for evidence, not just answers

The quote-grounding pattern from [module 02](02-prompting-fundamentals.md) matters most here:

> Find the passages in the attached contract relevant to termination rights. Quote them verbatim in `<quotes>` tags with page numbers. Then, based only on those quotes, answer: under what circumstances can either party terminate early?

This turns "Claude summarised the contract" into "Claude located and cited the clauses", which is a different reliability class entirely.

### Multiple documents: label them

```xml
<documents>
  <document index="1">
    <source>2025-contract-v3.pdf</source>
    <document_content>{{...}}</document_content>
  </document>
  <document index="2">
    <source>2024-contract-signed.pdf</source>
    <document_content>{{...}}</document_content>
  </document>
</documents>

What changed between these two contracts? Cite the document index for each difference.
```

Without labels, Claude will conflate them. With labels, it can cite.

### Verify anything that matters

Claude is very good at reading documents and still occasionally wrong. For anything consequential — legal, financial, medical, compliance — treat its output as a first pass by a capable assistant, not as ground truth. Ask for citations and check them.

---

## Vision

Claude can see images. Practically, that means:

| Use case | Works well |
|---|---|
| Reading text in a screenshot | Yes — including handwriting, usually |
| Describing a photo | Yes |
| Reading a chart or graph | Yes, with care — verify the numbers |
| Debugging a UI from a screenshot | Yes, this is genuinely useful |
| Reading a diagram or architecture drawing | Yes |
| Extracting a table from an image | Yes |
| Precise pixel measurements | No |
| Counting many small objects | Unreliable |
| Distinguishing very similar colours | Unreliable |

### The crop technique

Anthropic's own testing shows a consistent uplift when Claude can "zoom in" on relevant regions of an image. If you're building something image-heavy, give Claude a crop tool. In chat, do it manually: crop to the region you care about before uploading. A cropped 800px region beats a full 4000px screenshot both for accuracy and for cost.

### Multiple images

Current Opus models handle multi-image contexts notably better than earlier generations. When you upload several, label them:

> Image 1 is the current design, image 2 is the proposed redesign. List every difference in the navigation.

### Video

Not directly supported — but you can split a video into frames and upload those. This works surprisingly well for short clips.

---

## Try it

**Exercise 1 — Grounded document QA.**
Take a real PDF from your work (10+ pages). Ask a factual question directly. Then ask with the quote-extraction pattern. Verify both answers against the document. Note whether the ungrounded one was right, and whether you could have *told* it was right.

**Exercise 2 — Screenshot debugging.**
Screenshot any website with a layout you find ugly or broken. Ask Claude what's wrong and how to fix it. Then ask for the CSS.

**Exercise 3 — Chart extraction.**
Find a chart image (no underlying data). Ask Claude to extract the data as a table. Check it against the axes yourself. This calibrates how much you should trust chart reading.

**Exercise 4 — Crop test.**
Take a dense screenshot — a full spreadsheet or dashboard. Ask a question about one small region. Then crop to that region and ask again. Compare accuracy.

**Exercise 5 — Context cost.**
Attach a large PDF and have a 15-turn conversation. Then start fresh, extract the three relevant pages, and have the same conversation. Note the speed difference.

---

## Checkpoint

- You know why attaching a big PDF makes a long conversation expensive, and what to do instead
- You use quote grounding by default on documents that matter
- You know the crop trick and why it works

---

## Going deeper

- [Upload files to Claude](https://support.claude.com/en/articles/8241126-upload-files-to-claude)
- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
- [Coordinates and bounding boxes](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates)
- [Files API](https://platform.claude.com/docs/en/build-with-claude/files) — for programmatic use, covered in [04-api/08](../04-api/08-vision-pdfs-files.md)
