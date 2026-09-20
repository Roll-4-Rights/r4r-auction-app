<template>
  <v-container class="py-10 px-6" max-width="900">

    <!-- Same card style as the other pages -->
    <v-card
      class="rounded-2xl border-0 mb-12"
      style="background-color: #FFFFFF !important; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03) !important;"
      elevation="0"
    >
      <v-card-text class="pa-6 pa-md-10 fade-in-content" :class="{ 'is-loaded': contentReady }">

        <!-- Charity header: logo, name, website -->
        <div class="d-flex align-center mb-8">
          <v-avatar size="96" class="mr-5" color="grey-lighten-3">
            <v-img v-if="charity.charityLogoUrl" :src="charity.charityLogoUrl" alt="Charity logo" cover></v-img>
            <v-icon v-else icon="mdi-hand-heart-outline" size="40" color="grey-darken-1"></v-icon>
          </v-avatar>
          <div>
            <h1 class="text-h4 font-weight-black text-black mb-1">
              {{ charity.charityName || 'No charity selected yet' }}
            </h1>
            <a
              v-if="websiteLink"
              :href="websiteLink"
              target="_blank"
              rel="noopener"
              class="text-caption font-weight-bold"
              style="color: #0B4F6C; text-decoration: none;"
            >
              {{ charity.charityWebsite }}
            </a>
          </div>
        </div>

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- About the charity (line breaks typed in NocoDB are kept) -->
        <p class="text-body-1 text-medium-emphasis mb-8" style="white-space: pre-line;">
          {{ charity.charityDescription || 'More information about this charity is coming soon.' }}
        </p>

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- Call to Action: links to the "Charity Website" column -->
        <div class="d-flex justify-end">
          <v-btn
            v-if="websiteLink"
            color="#0B4F6C"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2 text-white"
            :href="websiteLink"
            target="_blank"
            rel="noopener"
          >
            Visit {{ charity.charityName || 'the charity' }}
          </v-btn>
          <v-btn
            v-else
            color="grey-lighten-1"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2"
            disabled
          >
            Charity website not set yet
          </v-btn>
        </div>

      </v-card-text>
    </v-card>
  </v-container>
</template>




<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Charity {
  charityName: string
  charityLogoUrl: string
  charityWebsite: string
  charityDescription: string
}

const charity = ref<Charity>({
  charityName: '', charityLogoUrl: '', charityWebsite: '', charityDescription: ''
})

// Stays false until the real data has arrived, so the page never shows placeholder text first
const contentReady = ref(false)

// Adds https:// when someone forgets it, so links don't turn into pages on your own site
const withHttps = (value: string) => {
  const link = (value || '').trim()
  if (!link) return ''
  return /^https?:\/\//i.test(link) ? link : `https://${link}`
}
const websiteLink = computed(() => withHttps(charity.value.charityWebsite))

// The charity details live in the same NocoDB "Campaign" table, so they come from the campaign-info route
const loadCharityInfo = async () => {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign-info`
    const res = await fetch(url)
    charity.value = await res.json()
  } catch (err) {
    console.error('Failed to load charity info:', err)
  }
}

onMounted(async () => {
  // Safety net: show the card anyway if the API is slow or down
  const timer = setTimeout(() => { contentReady.value = true }, 3000)
  await loadCharityInfo()
  clearTimeout(timer)
  contentReady.value = true
})
</script>


<style scoped>
.fade-in-content {
  opacity: 0;
  transition: opacity 0.4s ease;
}
.fade-in-content.is-loaded {
  opacity: 1;
}
</style>