# Castle art guide

All castle artwork is plain PNG (transparent background) in `public/castle/`.
Every sprite is listed in `src/components/castle/castle-art.css`. That file is the
only one to edit when real art arrives; `CastleFrame.vue` never names an image.

## Swapping a sprite
1. Save the new PNG into `public/castle/` with the **same file name**.
2. If its size differs, update that sprite's `-w` / `-h` numbers in `castle-art.css`.
3. Redeploy. Nothing else changes.

Sizes below are in **art pixels** (the PNG's own pixels). The site draws every art
pixel 4 screen pixels wide, so a 32 px tower shows as 128 px on screen.

| File | Size | How it's used |
|---|---|---|
| `tower-cap.png` | 32x24 | Top of each tower: battlements. The bottom edge must join `tower-body.png`. |
| `tower-body.png` | 32x32 | Tower stone. **Tiles top-to-bottom** (top and bottom edges must match). |
| `tower-ivy.png` | 32x64 | Transparent ivy over the tower. **Tiles top-to-bottom.** |
| `tower-window.png` | 8x14 | Arrow slit. Three per tower. |
| `tower-banner.png` | 16x32 | Banner hanging from the tower top. Desktop only. |
| `wall-top.png` | 12x8 | Battlement strip along the wall. **Tiles left-to-right.** |
| `wall-body.png` | 32x32 | Wall stone. **Tiles both ways.** |
| `panel-frame.png` | 16x16 | Wooden frame around the text. 9-slice: 4 px corners, 8 px edge pieces that repeat, transparent middle. |
| `parchment.png` | 16x16 | Paper behind the text. **Tiles both ways.** Keep it quiet so text stays readable. |
| `gate.png` | 40x44 | Castle gate under the text. |
| `torch.png` | 32x16 | Animation strip: 2 frames of 16x16 side by side. More frames? Change `--art-torch-frames`. |
| `grass.png` | 16x12 | Ground strip. **Tiles left-to-right.** Top 3 rows are blades. |
| `sky-clouds.png` | 96x40 | Clouds. **Tiles left-to-right.** |
| `sun.png` | 24x24 | Sun. Desktop only. |
| `coin.png` | 6x5 | One gold coin (gold hoard). Any size works. Darker coins are made automatically. |
| `gems.png` | 15x5 | Three gems side by side, 5x5 each (gold hoard). |
| `sparkle.png` | 7x7 | Twinkle over the gold hoard. |

## Notes for an artist
- Draw at 1x with no anti-aliasing or blur. Export PNG with transparency.
- The **right tower is the left tower mirrored**. Light the towers from the left;
  the edge that touches the wall is on the **right** side of the image.
- On small screens the towers are **trimmed, not shrunk**: only the right-hand 8
  (phones) or 20 (tablets) columns of the tower images are visible. Keep ivy and
  important detail toward the right side of `tower-body.png` and `tower-ivy.png`.
- Palette in the placeholders is sunny sandstone, warm shadows, fresh greens, blue sky.
