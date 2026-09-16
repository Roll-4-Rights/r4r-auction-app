<template>
  <div class="announcement-bar" v-if="messages.length">
    <button class="announcement-arrow" @click="prev" aria-label="Previous">
      <v-icon size="16">mdi-chevron-left</v-icon>
    </button>
    <span class="announcement-text">{{ messages[index] }}</span>
    <button class="announcement-arrow" @click="next" aria-label="Next">
      <v-icon size="16">mdi-chevron-right</v-icon>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const messages = ref<string[]>([])
const index = ref(0)

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
  }, 5000) // 5s per announcement
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
    messages.value = Array.isArray(data)
      ? data.map((r: any) => r.Message).filter(Boolean)
      : []
  } catch (err) {
    console.error('Failed to load banner messages', err)
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
  padding: 6px 12px;
}
.announcement-text {
  text-align: center;
}
.announcement-arrow {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}
</style>