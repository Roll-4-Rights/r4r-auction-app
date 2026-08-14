<template>
  <v-app>
    <CountdownBar v-if="campaignEndTime" :end-time="campaignEndTime" />
    <AnnouncementBar />
    <AppHeader />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CountdownBar from './components/CountdownBar.vue'
import AnnouncementBar from './components/AnnouncementBar.vue'
import AppHeader from './components/AppHeader.vue'

const campaignEndTime = ref('')

async function fetchCampaignSettings() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign`
    const response = await fetch(url)
    const data = await response.json()

    // Assumes single-row table, grabbing the first record
    campaignEndTime.value = data.list[0]?.auction_end_time ?? ''
  } catch (err) {
    console.error('Failed to load campaign settings', err)
  }
}

onMounted(() => {
  fetchCampaignSettings()
})
</script>
