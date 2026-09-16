<!-- filepath: c:\Users\gamer\Documents\Roll4Rights\r4r-auction-app\src\components\DragonProgressTracker.vue -->
<template>
  <div class="dragon-tracker">
    <div class="dragon-image-wrap">
      <transition name="dragon-fade" mode="out-in">
        <img
          :key="stage"
          :src="stageImages[stage]"
          :alt="`Dragon at stage ${stage}`"
          class="dragon-image"
        />
      </transition>
      <div class="ember-glow" :style="{ opacity: glowOpacity }"></div>
    </div>

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

// TODO: swap these placeholders for the artist's final delivered files
// (same filenames, dropped into src/assets/dragon/, and this import list
// won't need to change at all).
// import stage0 from '@/assets/dragon/stage-0.png'
// import stage1 from '@/assets/dragon/stage-1.png'
// import stage2 from '@/assets/dragon/stage-2.png'
// import stage3 from '@/assets/dragon/stage-3.png'
// import stage4 from '@/assets/dragon/stage-4.png'

const props = defineProps<{
  total: number
  currentMilestone: number
  nextMilestone: number
}>()

const maxStage = 4
const milestoneStep = 10000

const stageImages = [stage0, stage1, stage2, stage3, stage4]

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

.dragon-image-wrap {
  position: relative;
  width: 100%;
  max-width: 320px;
}

.dragon-image {
  width: 100%;
  display: block;
  animation: breathe 3s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.015); }
}

/* Soft ember glow behind the dragon, intensifies as milestones progress */
.ember-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at 50% 72%,
    rgba(255, 138, 61, 0.6) 0%,
    rgba(255, 138, 61, 0) 60%
  );
  transition: opacity 1s ease;
  z-index: -1;
}

/* Crossfade between stage images */
.dragon-fade-enter-active,
.dragon-fade-leave-active {
  transition: opacity 0.6s ease;
}
.dragon-fade-enter-from,
.dragon-fade-leave-to {
  opacity: 0;
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