# Castle art source

`make_castle_art.py` is the actual code that drew every picture in
`public/castle/` — the towers, ivy, wall, gate, torches, coins, hills, and
so on. Nothing here is used by the live website; it's a one-off tool you run
on your own computer to (re)generate the PNG files, which are what the site
actually loads.

Every picture is its own small function near the bottom of the file (search
for `def make_` to jump between them), so it's a reasonable way to see how
each effect works — the brick tiling, the ivy's sine-wave vine, the coin
pile's random placement, and so on.

## Running it

You need Python 3 and the Pillow library:

```
pip install Pillow
python make_castle_art.py output-folder
```

That creates `output-folder/` with all 17 (now 18, with hills) PNG files in
it. Copy whichever ones you change into your project's `public/castle/`
folder, using the same file names, and they'll show up on your site with no
other changes needed — see ART-GUIDE.md in src/components/castle/ for what
each file is and how it tiles.

## A good first experiment

Open the file and find `STONE = [...]` near the top — that's the five shades
used for every brick wall, brightest to darkest. Change one hex color and
re-run the script; every tower, wall and gate top re-shades to match.
