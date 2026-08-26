<!-- filepath: c:\Users\gamer\Documents\Roll4Rights\r4r-auction-app\src\components\DragonProgressTracker.vue -->
<template>
  <div class="dragon-tracker">
    <svg viewBox="0 0 300 200" class="dragon-svg" :class="`stage-${stage}`">
      <defs>
        <radialGradient id="emberGlow" cx="50%" cy="72%" r="55%">
          <stop offset="0%" stop-color="#ff8a3d" :stop-opacity="glowOpacity" />
          <stop offset="100%" stop-color="#ff8a3d" stop-opacity="0" />
        </radialGradient>
      </defs>

      <ellipse cx="150" cy="162" rx="130" ry="42" fill="url(#emberGlow)" class="ember" />

      <!-- Curled tail -->
      <path
        d="M55,150 Q30,130 40,105 Q50,85 75,90 Q60,110 70,130 Q78,142 95,148 Z"
        fill="#33424f"
        class="tail"
      />

      <!-- Body -->
      <path
        d="M65,148 Q90,80 175,88 Q235,93 248,138 Q205,162 150,157 Q100,162 65,148 Z"
        fill="#3a4a5a"
        class="body-shape"
      />

      <!-- Wing — moved AFTER body so it renders on top, made larger + fan-shaped -->
      <path
        d="M160,90 Q180,35 235,30 Q260,45 250,75 Q235,60 210,68 Q225,85 210,100 Q190,85 175,95 Z"
        fill="#2c3a47"
        stroke="#1c2732"
        stroke-width="1.5"
        class="wing"
      />

      <!-- Head / snout -->
      <path
        d="M175,88 Q212,82 232,100 Q222,112 205,110 Q188,108 175,98 Z"
        fill="#3f5060"
        class="head-shape"
      />

      <!-- Wing -->
      <path
        d="M170,92 Q205,52 252,72 Q222,96 178,96 Z"
        fill="#2c3a47"
        class="wing"
      />

      <!-- Eye -->
      <circle cx="212" cy="98" r="3.5" class="eye" :class="{ open: stage >= 1 }" />

      <!-- Smoke wisp, fades in at stage 2+ -->
      <path
        d="M228,92 Q234,84 230,76 Q238,80 236,68"
        stroke="#ffb15c"
        stroke-width="2"
        fill="none"
        stroke-linecap="round"
        class="smoke"
      />
    </svg>

    <div class="dragon-caption">
      <p class="milestone-label">${{ formattedTotal }} raised</p>
      <p class="milestone-sub" v-if="stage < maxStage">
        ${{ formattedRemaining }} until the dragon stirs again...
      </p>
      <p class="milestone-sub awake" v-else>
        The dragon is fully awake!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  total: number
  currentMilestone: number
  nextMilestone: number
}>()

const maxStage = 4
const milestoneStep = 10000

const stage = computed(() =>
  Math.min(Math.floor(props.currentMilestone / milestoneStep), maxStage)
)

const glowOpacity = computed(() => 0.15 + (stage.value / maxStage) * 0.5)
const formattedTotal = computed(() => Math.floor(props.total).toLocaleString())
const formattedRemaining = computed(() =>
  Math.max(props.nextMilestone - props.total, 0).toLocaleString()
)
</script>

<style scoped>
.dragon-tracker {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.dragon-svg {
  width: 100%;
  max-width: 320px;
  animation: breathe 3s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.015); }
}

.eye {
  fill: transparent;
  transition: fill 0.6s ease;
}
.eye.open {
  fill: #ffcc4d;
}

.wing {
  transform-origin: 178px 96px;
  transition: transform 0.9s ease;
}
.stage-2 .wing { transform: rotate(-5deg); }
.stage-3 .wing { transform: rotate(-12deg); }
.stage-4 .wing { transform: rotate(-20deg); }

.smoke {
  opacity: 0;
  transition: opacity 0.8s ease;
}
.stage-2 .smoke,
.stage-3 .smoke,
.stage-4 .smoke {
  opacity: 0.7;
}

.tail {
  transition: opacity 0.6s ease;
}
.stage-4 .tail {
  opacity: 0.85;
}

.ember {
  transition: opacity 1s ease;
}

.dragon-caption {
  margin-top: 10px;
}
.milestone-label {
  font-weight: 700;
  font-size: 1.25rem;
  color: #7a3a12;
}
.milestone-sub {
  font-size: 0.85rem;
  color: rgba(0, 0, 0, 0.55);
  margin-top: 2px;
}
.milestone-sub.awake {
  color: #d9822b;
  font-weight: 600;
}
</style>