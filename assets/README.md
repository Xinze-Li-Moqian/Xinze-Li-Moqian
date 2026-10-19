# Profile artwork

## Current direction

The profile draws on the visual language of [CloK](https://www.clok.tech/): a nearly black navy ground, pale blue typography, fine gold botanical forms, and generous space between sections. The tree connects the profile's existing theme of growing open-source communities to this visual direction.

- Current banner: [`moqian-qian-hero.png`](moqian-qian-hero.png), 2172 × 724 pixels; title **墨謙 · Moqian**.
- Palette: navy `#090E16`, pale blue `#E3F2FC`, restrained gold and cyan accents.
- Method: generated with the built-in imagegen tool. The artwork is original; CloK's site illustration was not copied into this asset.
- The README body uses native headings, text, and links so it remains searchable, selectable, and compatible with GitHub's light and dark themes.
- Earlier banners: [`moqian-clok-hero.png`](moqian-clok-hero.png) and [`grow.svg`](grow.svg), retained as earlier designs.

## Name and hexagram

The title uses traditional Chinese **墨謙**, a middle dot, and title-case **Moqian**. Its gold emblem is **謙**, hexagram 15 (䷎), with earth above mountain: 坤上艮下.

The six rows are, from top to bottom: **broken, broken, broken, solid, broken, broken**. The only solid line is the fourth from the top, or third from the bottom. Checked against the six line names in [《周易·謙》](https://zh.wikisource.org/zh-hant/周易/謙): 初六、六二、九三、六四、六五、上六.

The exact geometry used as the correction reference is preserved in [`qian-hexagram-reference.svg`](qian-hexagram-reference.svg). The final raster was visually checked for six rows and eleven gold bar segments.

The built-in imagegen edit instructions are recorded in [qian-edit-prompts.md](qian-edit-prompts.md).

## Generation prompt

```text
Use case: ads-marketing. Asset type: a finished ultra-wide 3:1 GitHub personal-profile header, designed to be readable when shown at 850 px width. Create a polished original banner for Moqian, a researcher, open-source contributor and community grower. The visual language is a scholarly, contemplative research website: nearly black navy background #090e16, large pale ice-blue geometric sans-serif typography like Jost, subtle muted gold and cyan botanical/circuit linework. This is a personal profile, not a company or product. Composition: left 55% dedicated to text with generous breathing room, right 45% a detailed yet airy original tree of connected ideas with fine gold branches, restrained blue veins and a few small budding leaves; roots transition into a sparse network of delicate nodes. The tree is elegant, partly like an antique botanical engraving, partly like a map of mathematical knowledge. Keep dark negative space between branches, and fade the illustration naturally into the dark backdrop. No fantasy scene, no glowing sci-fi HUD, no busy background. Exact text, only these four elements: small uppercase top-left 'RESEARCH / OPEN SOURCE / COMMUNITY'; very large main title 'MOQIAN'; below it in two readable lines 'Build things.' and 'Help communities grow.' All text crisp, spelled exactly, aligned left. No other text, no buttons, no logos, no border, no watermark. Use a restrained thin pale-blue horizontal rule near the lower left to match an editorial layout. Flat image ready to be embedded as a wide GitHub README banner, not a mockup or screenshot. Landscape 3:1 aspect ratio.
```
