<template>
  <div v-if="announcements.length > 0" class="announcement-bar">
    <v-btn icon="mdi-chevron-left" variant="text" size="small" @click="previous" />

    <span class="announcement-text">{{ currentMessage }}</span>

    <v-btn icon="mdi-chevron-right" variant="text" size="small" @click="next" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const announcements = ref<any[]>([])
const currentIndex = ref(0)
let autoAdvanceId: number | undefined

const currentMessage = computed(() =>
  announcements.value[currentIndex.value]?.message ?? ''
)

function next() {
  currentIndex.value = (currentIndex.value + 1) % announcements.value.length
  resetAutoAdvance()
}

function previous() {
  currentIndex.value =
    (currentIndex.value - 1 + announcements.value.length) % announcements.value.length
  resetAutoAdvance()
}

function startAutoAdvance() {
  autoAdvanceId = window.setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % announcements.value.length
  }, 6000)
}

function resetAutoAdvance() {
  if (autoAdvanceId) clearInterval(autoAdvanceId)
  startAutoAdvance()
}

async function fetchAnnouncements() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/announcements`
    const response = await fetch(url)
    const data = await response.json()
    announcements.value = data.list.filter((a: any) => a.active)
    if (announcements.value.length > 0) startAutoAdvance()
  } catch (err) {
    console.error('Failed to load announcements', err)
  }
}

onMounted(() => {
  fetchAnnouncements()
})

onUnmounted(() => {
  if (autoAdvanceId) clearInterval(autoAdvanceId)
})
</script>

<style scoped>
.announcement-bar {
  background-color: #c15a3e;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 6px 16px;
}

.announcement-text {
  font-size: 0.9rem;
}
</style>