<template>
  <div class="countdown-bar">
    <span class="countdown-label">The Auction Closes:</span>

    <div class="countdown-timer">
      <div class="countdown-segment">
        <span class="countdown-number">{{ days }}</span>
        <span class="countdown-unit">days</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-segment">
        <span class="countdown-number">{{ hours }}</span>
        <span class="countdown-unit">hours</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-segment">
        <span class="countdown-number">{{ minutes }}</span>
        <span class="countdown-unit">mins</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-segment">
        <span class="countdown-number">{{ seconds }}</span>
        <span class="countdown-unit">secs</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  endTime: string
}>()

const days = ref('00')
const hours = ref('00')
const minutes = ref('00')
const seconds = ref('00')

let intervalId: number | undefined

function updateCountdown() {
  const end = new Date(props.endTime).getTime()
  const now = new Date().getTime()
  const distance = end - now

  if (distance < 0) {
    days.value = '00'
    hours.value = '00'
    minutes.value = '00'
    seconds.value = '00'
    return
  }

  const d = Math.floor(distance / (1000 * 60 * 60 * 24))
  const h = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
  const s = Math.floor((distance % (1000 * 60)) / 1000)

  days.value = String(d).padStart(2, '0')
  hours.value = String(h).padStart(2, '0')
  minutes.value = String(m).padStart(2, '0')
  seconds.value = String(s).padStart(2, '0')
}

onMounted(() => {
  updateCountdown()
  intervalId = window.setInterval(updateCountdown, 1000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>
.countdown-bar {
  background-color: #000000;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 8px 16px;
  font-family: serif;
}

.countdown-timer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.countdown-segment {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.countdown-number {
  font-size: 1.4rem;
  font-weight: bold;
}

.countdown-unit {
  font-size: 0.65rem;
  text-transform: uppercase;
}

.countdown-colon {
  font-size: 1.4rem;
  font-weight: bold;
  padding-bottom: 14px;
}
</style>