<!--
  GoldHoard — a pile of gold that grows as donations come in.

  Usage:   <GoldHoard :total="progress.total" />

  It fills up gradually from $0 to (stepSize * stages). By default that is
  $10,000 * 8 = $80,000, i.e. the hoard is full when the dragon reaches its
  8th stage. Set `stages` to match how many stages your dragon has.

  The coin and gem images come from castle-art.css. The pile logic is in hoard.ts.
-->
<template>
  <div class="hoard" aria-hidden="true">
    <div class="hoard__stage" :style="{ '--hoard-w': width, '--hoard-h': height }">
      <canvas ref="canvasEl" class="hoard__canvas" :width="width" :height="height"></canvas>
      <span
        v-for="(spark, i) in sparkles"
        :key="i"
        class="hoard__sparkle"
        :style="{
          left: `calc(${spark.x} * var(--px, 4px))`,
          top: `calc(${spark.y} * var(--px, 4px))`,
          animationDelay: `${spark.delay}s`,
        }"
      ></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import './castle-art.css'
import { loadHoardSprites, drawHoard, type HoardSprites, type Sparkle } from './hoard'

const props = withDefaults(
  defineProps<{
    /** Amount raised so far. */
    total: number
    /** How much each dragon stage is worth. */
    stepSize?: number
    /** How many stages until the hoard is completely full. */
    stages?: number
    /** Size of the drawing area, in art pixels. */
    width?: number
    height?: number
  }>(),
  { stepSize: 10000, stages: 8, width: 80, height: 28 },
)

const canvasEl = ref<HTMLCanvasElement | null>(null)
const sparkles = ref<Sparkle[]>([])
let sprites: HoardSprites | null = null

// 0 = empty, 1 = completely full
const fill = computed(() => Math.min(1, Math.max(0, props.total / (props.stepSize * props.stages))))

function render() {
  if (!canvasEl.value || !sprites) return
  sparkles.value = drawHoard(canvasEl.value, sprites, fill.value, props.width, props.height)
}

onMounted(async () => {
  sprites = await loadHoardSprites()
  render()
})
watch(fill, render)
</script>

<style>
.hoard {
  display: flex;
  justify-content: center;
  overflow: hidden; /* on narrow screens the outer edges of the pile are trimmed, not squashed */
}
.hoard__stage {
  position: relative;
  flex: none;
  width: calc(var(--hoard-w) * var(--px, 4px));
  height: calc(var(--hoard-h) * var(--px, 4px));
}
.hoard__canvas {
  display: block;
  width: 100%;
  height: 100%;
  image-rendering: pixelated;
}
.hoard__sparkle {
  position: absolute;
  width: calc(var(--art-sparkle-w) * var(--px, 4px));
  height: calc(var(--art-sparkle-h) * var(--px, 4px));
  background: var(--art-sparkle) no-repeat 0 0 / 100% 100%;
  image-rendering: pixelated;
  opacity: 0;
  animation: hoard-twinkle 2.7s ease-in-out infinite;
}
@keyframes hoard-twinkle {
  0%, 55%, 100% { opacity: 0; }
  70% { opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
  .hoard__sparkle { animation: none; opacity: 0.9; }
}
</style>
