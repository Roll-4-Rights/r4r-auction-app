<template>
  <div class="countdown-bar" :class="{ 'is-ready': ready }">
    <span class="countdown-label">{{ countdownLabel }}</span>

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
        <span class="countdown-unit">minutes</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-segment">
        <span class="countdown-number">{{ seconds }}</span>
        <span class="countdown-unit">seconds</span>
      </div>
    </div>
  </div>
</template>






<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue'

const props = defineProps<{
  startTime: string
  endTime: string
}>()


const days = ref('00')
const hours = ref('00')
const minutes = ref('00')
const seconds = ref('00')
const countdownLabel = ref('')
const ready = computed(() => !!props.endTime)

let intervalId: number | undefined


function updateCountdown() {

const now = new Date().getTime()
const start = props.startTime ? new Date(props.startTime.replace(' ', 'T')).getTime() : 0
const end = props.endTime ? new Date(props.endTime.replace(' ', 'T')).getTime() : 0


let distance = 0

// Teaser State: Before the auction opens
if (now < start) {
  countdownLabel.value = 'The Auction Starts In:'
  distance = start - now
} 
// Live State: Auction is currently active
else if (now >= start && now < end) {
  countdownLabel.value = 'The Auction Closes:'
  distance = end - now
} 
// Expired State: Auction is completely finished
else {
  countdownLabel.value = 'The Auction Has Closed!'
  days.value = '00'
  hours.value = '00'
  minutes.value = '00'
  seconds.value = '00'
  if (intervalId) clearInterval(intervalId)
  return // Stops the function here so it doesn't do further math
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



watch(
  [() => props.startTime, () => props.endTime], // 1. Source array
  ([_newStart, newEnd]) => {                     // 2. Callback parameters
    
    // 3. Only run the code if at least the end date has successfully landed
    if (newEnd) {
      if (intervalId) clearInterval(intervalId) // Wipes older loops out
      updateCountdown()                         // Fires the math once instantly
      intervalId = window.setInterval(updateCountdown, 1000) // Ticks every second
    }
    
  }
)



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

/* to show black bar shows straight away; its contents fade in once the dates arrive */
.countdown-bar > * {
  opacity: 0;
  transition: opacity 0.4s ease;
}
.countdown-bar.is-ready > * {
  opacity: 1;
}
</style>