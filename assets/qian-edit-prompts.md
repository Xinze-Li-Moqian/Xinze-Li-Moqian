# Name and hexagram edit prompts

Method: built-in imagegen. Initial identity asset: [moqian-qian-hero.png](moqian-qian-hero.png). Current asset: [moqian-studio-hero.png](moqian-studio-hero.png), edited from [moqian-qian-hero-aligned.png](moqian-qian-hero-aligned.png).

## Studio welcome and blue yang line

Final asset: [moqian-studio-hero.png](moqian-studio-hero.png), 2172 × 724. Method: built-in imagegen, editing the aligned banner. Checked the exact welcome text, traditional name, six-row pattern, blue fourth row, preserved subtitles, and alignment.

```text
Use case: precise-object-edit and text-localization. Edit target: the provided existing wide GitHub profile banner. Make exactly two small edits while preserving the rest of the image and the 3:1 landscape composition. (1) In the six-row Qian hexagram immediately left of the name, recolor ONLY the single continuous horizontal bar — the FOURTH ROW FROM THE TOP, equivalently THIRD FROM THE BOTTOM — from gold to a harmonious muted slate/ice blue, approximately #7FAAC4. Keep all five broken yin rows gold, with their two segments per row unchanged. Preserve the exact six-row pattern TOP TO BOTTOM: broken, broken, broken, solid, broken, broken. Do not add, remove, resize, or shift any row. Keep the emblem vertically centered on the Chinese characters exactly as in the input. (2) Replace the small spaced uppercase overline 'RESEARCH / OPEN SOURCE / COMMUNITY' with the exact text 'WELCOME TO MOQIAN-STUDIO', on one line, at the same location, with the same small pale-blue uppercase typography and letter spacing. Preserve the main name exactly '墨謙 · Moqian' (traditional Chinese 謙), all of its original typography and alignment. Preserve the lower text exactly 'Build things.' and 'Help communities grow.' Preserve the thin rule, navy background, entire gold-and-blue tree and roots, lighting, crop, spacing and every other visual detail. Do not create a redesign or a mockup. Return the complete edited banner, same 3:1 aspect ratio.
```

## Vertical alignment revision

Final asset: [moqian-qian-hero-aligned.png](moqian-qian-hero-aligned.png). Method: built-in imagegen. The selected edit uses the original banner and [qian-alignment-reference.svg](qian-alignment-reference.svg), followed by a correction restoring the top broken row. Earlier trial outputs were not published.

### Compact emblem with layout reference

```text
Image 1 is the existing full banner to edit. Image 2 is a VECTOR LAYOUT REFERENCE illustrating the requested alignment of the small gold six-row symbol with the Chinese name. Replace ONLY the tall gold symbol in image 1 with a NEW SMALLER COMPACT six-row gold symbol. Use image 2 to match the vertical alignment: the symbol and the Chinese characters have the same vertical center, and the symbol fits within the Chinese characters' top and bottom edges. The current symbol in image 1 is oversized and bottom-heavy, so noticeably reduce the symbol's height by about ONE QUARTER and move its center upward; do not leave it at its old size or position. Its bottom row must end ABOVE the Latin q descender and at or slightly above the Chinese baseline. Preserve the original Chinese typography and text from image 1, not the reference font. The new icon must have exactly six rows like image 2, from top to bottom: broken, broken, broken, solid, broken, broken; exactly five yin rows and one yang row. Preserve horizontal placement beside the name, gold palette and overall visual style. Preserve all other content from image 1: exact main name 墨謙 · Moqian, top small text, subtitles, horizontal rule, dark background, entire tree illustration and dimensions. Output the full original 3:1 banner with the visibly smaller, vertically centered gold emblem.
```

### Restore the top row

```text
Repair ONLY the tiny gold symbol left of 墨謙 in the supplied banner. It currently has FIVE rows because one broken row was accidentally omitted at the TOP. Add precisely ONE NEW BROKEN GOLD ROW ABOVE the current top row, with the same bar thickness, gold color, width and centered gap. Keep the current FIVE rows exactly in their current positions. The new top row should be one normal row-step above the current top row, so it begins at roughly the same height as the top of the Chinese characters. Do not append any row at the bottom! Add the missing broken row at the TOP only. The resulting six rows top-to-bottom MUST be: broken, broken, broken, solid, broken, broken. The ONLY solid row is now the FOURTH from the top. Exactly six rows with eleven gold bar segments. Keep every other pixel and element of this banner as before: traditional name 墨謙 · Moqian, all other text, exact tree illustration, colors, horizontal rule, full 2172x724 canvas. Do not resize or move any of the existing five gold rows. This edit solely inserts two short gold rectangles ABOVE the existing five-row icon to restore the correct six-row hexagram.
```


## Identity edit

```text
Edit the supplied GitHub profile banner. Preserve the 3:1 aspect ratio, dark navy background, right-hand gold-and-blue knowledge tree illustration, all roots, the top small 'RESEARCH / OPEN SOURCE / COMMUNITY' text, and the lower two lines 'Build things.' and 'Help communities grow.' and the thin rule. Make ONLY these identity changes in the left-hand title area: replace the large all-caps 'MOQIAN' with the exact single-line bilingual name '墨謙 · Moqian'. Use traditional Chinese 謙, NOT simplified 谦. The title must be exactly 墨謙, a centered middle dot, then title-case Moqian, with only M capitalized. Use refined crisp pale ice-blue typography, Traditional Chinese glyphs harmonious with the Latin geometric sans-serif. Adjust title size to fit on ONE line comfortably without overlapping the tree. Immediately beside the title on its LEFT, add a small gold six-line I Ching hexagram for Modesty, number 15, 謙 ䷎. It must consist of EXACTLY SIX equally spaced horizontal rows, visually compact and aligned with the title: top to bottom row 1 is two separated short bars (broken yin), row 2 two separated short bars, row 3 two separated short bars, row 4 ONE continuous full-width bar (solid yang), row 5 two separated short bars, row 6 two separated short bars. Thus the ONLY continuous line is the FOURTH from top, THIRD from bottom. Exactly five broken rows and one solid row, total six rows. Both halves of each broken row same length, same centered gap; all rows same total width; crisp rectangular gold bars. Draw no enclosing circle, no extra stroke, no labels or numbers near the hexagram. Maintain generous spacing between the symbol and the name and leave all other design details unchanged. This is a precise banner edit, not a new layout or a mockup.
```

## Six-line correction

```text
Image 1 is the EDIT TARGET: an existing finished banner. Image 2 is a REFERENCE DIAGRAM showing the EXACT CORRECT six-line hexagram. Make one tiny correction to image 1 ONLY: the golden symbol at the left of '墨謙 · Moqian' currently has only FIVE rows. ADD the missing SIXTH broken row at the bottom, below its existing bottom row, same thickness, width, spacing and gold material. The corrected emblem must have exactly SIX rows as image 2: top-to-bottom BROKEN, BROKEN, BROKEN, SOLID, BROKEN, BROKEN. Rows 1,2,3,5,6 each have two separated horizontal bars; row 4 is one full-width bar. There are eleven rectangular gold bar segments in total, arranged as six levels. Copy the six-row geometry of reference image 2, scaled to the small emblem; do not paste its background rectangle. Keep all existing typography, including exact Traditional Chinese '墨謙 · Moqian', every other word, the right tree, the palette, composition, canvas dimensions, and all other elements UNCHANGED. Do not move, rewrite, replace or stylize any text. This is just adding the missing bottom broken line to repair the hexagram, not redesigning the banner.
```
