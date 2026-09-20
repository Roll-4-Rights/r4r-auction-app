<template>
  <div class="announcement-bar" :class="{ 'is-ready': messages.length > 0 }" v-if="loading || messages.length">
    <button class="announcement-arrow" @click="prev" aria-label="Previous">
      <v-icon size="16">mdi-chevron-left</v-icon>
    </button>
    
    <div class="announcement-window">
      <TransitionGroup v-if="messages.length" name="slide">
        <!-- Render every item using the active class mapping to preserve height mechanics -->
        <span 
          v-for="(msg, i) in messages" 
          :key="i" 
          :class="['announcement-text', { active: i === index }]"
        >
          {{ msg }}
        </span>
      </TransitionGroup>
    </div>
    
    <button class="announcement-arrow" @click="next" aria-label="Next">
      <v-icon size="16">mdi-chevron-right</v-icon>
    </button>
  </div>
</template>




<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const messages = ref<string[]>([])
const index = ref(0)
const loading = ref(true)

let intervalId: ReturnType<typeof setInterval> | undefined

function prev() {
  index.value = (index.value - 1 + messages.value.length) % messages.value.length
  resetInterval()
}
function next() {
  index.value = (index.value + 1) % messages.value.length
  resetInterval()
}

function startInterval() {
  if (messages.value.length <= 1) return
  intervalId = setInterval(() => {
    index.value = (index.value + 1) % messages.value.length
  }, 7000) // seconds per announcement
}

function resetInterval() {
  if (intervalId) clearInterval(intervalId)
  startInterval()
}

async function fetchAnnouncements() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/banner-messages`
    const res = await fetch(url)
    const data = await res.json()
    
    const rawData = Array.isArray(data) ? data : []
    messages.value = rawData
      .reverse()
      .map((r: any) => r.Message)
      .filter(Boolean)
  } catch (err) {
    console.error('Failed to load banner messages', err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchAnnouncements()
  startInterval()
  
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>





<style scoped>
.announcement-bar {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  background: #b1522f;
  color: #fff;
  font-size: 0.75rem;
  letter-spacing: 0.02em;
  padding: 10px 12px; 
  width: 100%;
}

.announcement-window {
  /* Turn the text container into a single grid track */
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  overflow: hidden;
  width: 100%;
  justify-items: center;
  align-items: center;
}

.announcement-text {
  text-align: center;
  width: 100%;
  white-space: normal; 
  word-break: break-word;
  padding: 0 8px;
  
  /* Force every single message to stack into the exact same grid cell.
     The container will automatically stretch to fit the absolute tallest message, 
     preventing the banner from bouncing! */
  grid-area: 1 / 1 / 2 / 2; 
  position: relative; 
  
  /* Hide the elements visually but leave their layouts readable by the browser engine */
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

/* Make the targeted item fully visible and interactive */
.announcement-text.active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.3s ease;
}

/* New incoming message slides from off-screen right */
.slide-enter-from {
  transform: translate3d(100%, 0, 0);
  opacity: 0;
}

/* Outgoing message slides left over the background layer */
.slide-leave-to {
  transform: translate3d(-100%, 0, 0);
  opacity: 0;
}

/*  orange bar shows straight away; its contents fade in once messages arrive */
.announcement-bar > * {
  opacity: 0;
  transition: opacity 0.4s ease;
}
.announcement-bar.is-ready > * {
  opacity: 1;
}
.announcement-bar:not(.is-ready) {
  pointer-events: none;
}
</style>
