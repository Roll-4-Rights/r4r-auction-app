<template>
  <v-app>
    <CountdownBar v-if="campaignEndTime" :end-time="campaignEndTime" />
    <AnnouncementBar />
    <SiteHeader />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CountdownBar from './components/CountdownBar.vue'
import AnnouncementBar from './components/AnnouncementBar.vue'
import SiteHeader from './components/SiteHeader.vue'

const campaignEndTime = ref('')

async function fetchCampaignSettings() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign`
    const res = await fetch(url)
    const data = await res.json()

    if (data.error) {
      console.error('Campaign settings error:', data.error)
      return
    }

    const records = data.list ?? []
    campaignEndTime.value = records[0]?.['Auction End Time'] ?? ''
  } catch (err) {
    console.error('Failed to load campaign settings', err)
  }
}

onMounted(() => {
  fetchCampaignSettings()
})
</script>
