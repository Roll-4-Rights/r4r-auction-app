/*
  GOLD HOARD — the logic (no Vue in here, so it is easy to read).

  How it works
  ------------
  1. buildHoard() works out, once, where every coin of a FULL hoard sits: a low
     mound of coins. The coins are sorted so the ones near the middle of the
     bottom come first and the ones at the edges/top come last.
  2. drawHoard() shows only the first N of them, where N grows with the amount
     raised. So the pile starts as a few coins and spreads outwards and upwards.
     Gems appear on top of the pile as it grows, and a few sparkles twinkle.

  The artwork is just two small images (a coin and a strip of gems). They are
  listed in castle-art.css, so swapping them needs no code change. The darker
  coins deeper in the pile are made automatically from the one coin image.
*/

export interface Coin {
  x: number
  y: number
  shade: 0 | 1 | 2 // 0 = brightest (top of the pile), 2 = darkest (bottom)
  rank: number // order in which coins appear as the hoard grows
}

export interface Sparkle {
  x: number
  y: number
  delay: number
}

export interface HoardSprites {
  coin: HTMLImageElement | null
  gems: HTMLImageElement | null
  gemCount: number
  coinShades: CanvasImageSource[]
}

/* ------------------------------------------------------------- settings -- */
/** Even with $0 raised, this many coins are already lying there. */
const MIN_COINS = 6

/** Gems sit on top of the pile. `at` = how full the hoard must be for the gem
    to appear, `dx` = distance from the middle of the pile (in art pixels). */
const GEM_SLOTS = [
  { dx: -7, at: 0.3, kind: 0 },
  { dx: 11, at: 0.5, kind: 1 },
  { dx: -21, at: 0.7, kind: 2 },
  { dx: 25, at: 0.88, kind: 0 },
]

/* --------------------------------------------------------------- layout -- */
/** A small seeded random number generator, so the pile looks the same every time. */
function mulberry32(seed: number) {
  let a = seed
  return () => {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

/** Every coin of a full hoard, sorted by the order they should appear in. */
export function buildHoard(width: number, height: number, coinW = 6, coinH = 5, seed = 1234): Coin[] {
  const rand = mulberry32(seed)
  const cx = width / 2
  const halfSpan = width / 2 - coinW / 2
  const maxRise = height - coinH

  // How high the pile may be at a given distance from the middle (a rounded mound).
  const moundHeight = (centreX: number) => {
    const t = Math.abs(centreX - cx) / halfSpan
    return t >= 1 ? -1 : maxRise * Math.pow(1 - Math.pow(t, 2.2), 0.85)
  }

  const stepX = Math.max(2, Math.round(coinW * 0.66))
  const stepY = Math.max(1, Math.round(coinH * 0.4))
  const coins: Coin[] = []

  for (let row = 0; row * stepY <= maxRise; row++) {
    const rise = row * stepY
    const shift = (row % 2) * (stepX / 2)
    for (let centreX = coinW / 2 + shift; centreX <= width - coinW / 2; centreX += stepX) {
      if (rise > moundHeight(centreX)) continue
      const jitterX = Math.floor(rand() * 3) - 1
      const jitterY = Math.floor(rand() * 3) - 1
      const x = Math.round(centreX - coinW / 2 + jitterX)
      const y = Math.min(height - coinH, Math.max(0, Math.round(height - coinH - rise + jitterY)))
      const nx = (centreX - cx) / (width / 2)
      const ny = rise / height
      const rank = nx * nx * 0.75 + ny * ny * 1.1 + rand() * 0.05
      const level = maxRise === 0 ? 0 : rise / maxRise
      const shade = level < 0.3 ? 2 : level < 0.62 ? 1 : 0
      coins.push({ x, y, shade, rank })
    }
  }
  return coins.sort((a, b) => a.rank - b.rank)
}

const layoutCache = new Map<string, Coin[]>()
function getLayout(width: number, height: number, coinW: number, coinH: number) {
  const key = `${width}x${height}x${coinW}x${coinH}`
  let layout = layoutCache.get(key)
  if (!layout) {
    layout = buildHoard(width, height, coinW, coinH)
    layoutCache.set(key, layout)
  }
  return layout
}

/* -------------------------------------------------------------- sprites -- */
/** Reads an image address from castle-art.css (e.g. --art-coin). */
function artUrl(cssVar: string, fallback: string): string {
  const raw = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim()
  const match = raw.match(/url\(\s*['"]?([^'")]+)['"]?\s*\)/)
  return match ? match[1] : fallback
}

function loadImage(src: string): Promise<HTMLImageElement | null> {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => resolve(null) // no image? the hoard falls back to plain squares
    img.src = src
  })
}

/** A darker copy of an image (for coins deeper in the pile). */
function darken(img: HTMLImageElement, factor: number): HTMLCanvasElement {
  const canvas = document.createElement('canvas')
  canvas.width = img.naturalWidth
  canvas.height = img.naturalHeight
  const ctx = canvas.getContext('2d')!
  ctx.drawImage(img, 0, 0)
  const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height)
  for (let i = 0; i < pixels.data.length; i += 4) {
    pixels.data[i] *= factor
    pixels.data[i + 1] *= factor
    pixels.data[i + 2] *= factor
  }
  ctx.putImageData(pixels, 0, 0)
  return canvas
}

export async function loadHoardSprites(): Promise<HoardSprites> {
  const [coin, gems] = await Promise.all([
    loadImage(artUrl('--art-coin', '/castle/coin.png')),
    loadImage(artUrl('--art-gems', '/castle/gems.png')),
  ])
  const gemCount =
    parseInt(getComputedStyle(document.documentElement).getPropertyValue('--art-gems-count'), 10) || 3
  const coinShades: CanvasImageSource[] = coin ? [coin, darken(coin, 0.82), darken(coin, 0.64)] : []
  return { coin, gems, gemCount, coinShades }
}

/* --------------------------------------------------------------- drawing -- */
/**
 * Paints the hoard onto a canvas (1 canvas pixel = 1 art pixel; the CSS scales it up).
 * `fill` runs from 0 (nothing raised) to 1 (full hoard). Returns where to put sparkles.
 */
export function drawHoard(
  canvas: HTMLCanvasElement,
  sprites: HoardSprites,
  fill: number,
  width: number,
  height: number,
): Sparkle[] {
  const ctx = canvas.getContext('2d')
  if (!ctx) return []
  ctx.imageSmoothingEnabled = false
  ctx.clearRect(0, 0, width, height)

  const coinW = sprites.coin?.naturalWidth ?? 6
  const coinH = sprites.coin?.naturalHeight ?? 5
  const coins = getLayout(width, height, coinW, coinH)
  const count = Math.min(coins.length, Math.max(MIN_COINS, Math.round(fill * coins.length)))
  const visible = coins.slice(0, count)

  // Paint the lowest coins first so the higher ones sit on top of them.
  const paintOrder = [...visible].sort((a, b) => b.y - a.y || a.x - b.x)
  for (const coin of paintOrder) {
    if (sprites.coinShades.length) {
      ctx.drawImage(sprites.coinShades[coin.shade], coin.x, coin.y)
    } else {
      ctx.fillStyle = ['#ffd54a', '#f2b322', '#c98a12'][coin.shade]
      ctx.fillRect(coin.x, coin.y + 1, coinW, coinH - 2)
    }
  }

  // Gems rest on whatever coins are showing at that spot.
  if (sprites.gems) {
    const gemW = Math.floor(sprites.gems.naturalWidth / sprites.gemCount)
    const gemH = sprites.gems.naturalHeight
    for (const slot of GEM_SLOTS) {
      if (fill < slot.at) continue
      const gemX = Math.round(width / 2 + slot.dx - gemW / 2)
      const under = visible.filter((c) => Math.abs(c.x + coinW / 2 - (gemX + gemW / 2)) <= coinW)
      if (!under.length) continue
      const top = Math.min(...under.map((c) => c.y))
      ctx.drawImage(sprites.gems, (slot.kind % sprites.gemCount) * gemW, 0, gemW, gemH, gemX, top - gemH + 2, gemW, gemH)
    }
  }

  // Up to three sparkles, over the highest coins that are far enough apart.
  const sparkles: Sparkle[] = []
  if (fill >= 0.12) {
    for (const coin of [...visible].sort((a, b) => a.y - b.y)) {
      if (sparkles.length >= 3) break
      if (sparkles.every((s) => Math.abs(s.x - coin.x) >= 14)) {
        sparkles.push({ x: coin.x + Math.round(coinW / 2) - 3, y: coin.y - 5, delay: sparkles.length * 0.9 })
      }
    }
  }
  return sparkles
}
