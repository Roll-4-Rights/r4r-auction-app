<template>
  <v-container class="py-6 py-md-10 px-2 px-sm-6" max-width="900">

    <!-- The castle artwork lives in src/components/castle/ -->
    <CastleFrame>
      <div class="fade-in-content" :class="{ 'is-loaded': contentReady }">

        <!-- Campaign Header -->
        <div class="text-left mb-8">
          <p class="text-caption font-weight-bold text-uppercase text-medium-emphasis mb-1" style="letter-spacing: 0.08em;">
            Welcome, traveler! Thank you for joining us in support of the 
          </p>
          <h1 class="text-h4 font-weight-black mb-2 castle-heading">
            {{ campaign.name || 'Campaign Name' }}
          </h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            {{ campaign.tagline || 'some info here.' }}
          </p>
        </div>

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- Benefiting Charity -->
        <div class="d-flex align-center mb-4">
          <v-avatar size="64" class="mr-4" color="grey-lighten-3">
            <v-img v-if="campaign.charityLogoUrl" :src="campaign.charityLogoUrl" alt="Charity logo" cover></v-img>
            <v-icon v-else icon="mdi-hand-heart-outline" size="30" color="grey-darken-1"></v-icon>
          </v-avatar>
          <div>
            <p class="castle-label text-medium-emphasis mb-0">In Aid Of</p>
            <p class="text-h6 font-weight-bold text-black mb-0">
              {{ campaign.charityName || 'No charity selected yet' }}
            </p>
            <a
              v-if="websiteLink"
              :href="websiteLink"
              target="_blank"
              rel="noopener"
              class="text-caption font-weight-bold"
              style="color: #0B4F6C; text-decoration: none;"
            >
              {{ campaign.charityWebsite }}
            </a>
          </div>
        </div>

        <p class="text-body-2 text-medium-emphasis mb-8">
          {{ campaign.charityDescription || 'long info' }}
        </p>

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- Campaign Dates -->
        <v-row class="mb-6" no-gutters>
          <v-col cols="6">
            <p class="castle-label text-medium-emphasis mb-0">The Gates Open</p>
            <p class="text-subtitle-2 font-weight-bold text-black">{{ formattedStartDate }}</p>
          </v-col>
          <v-col cols="6">
            <p class="castle-label text-medium-emphasis mb-0">The Gates Close</p>
            <p class="text-subtitle-2 font-weight-bold text-black">{{ formattedEndDate }}</p>
          </v-col>
        </v-row>

        <!-- Raised total + progress toward next dragon awakening -->
        <div class="mb-8">
          <div class="d-flex justify-space-between mb-2">
            <p class="castle-label text-medium-emphasis mb-0">{{ formattedRaised }} raised</p>
            <!-- <p class="text-caption text-medium-emphasis mb-0">
               {{ formattedNextMilestone }}
            </p> -->
          </div>
          <v-progress-linear
            :model-value="progress.progressWithinMilestone * 100"
            height="10"
            rounded
            color="#0B4F6C"
            bg-color="grey-lighten-3"
          ></v-progress-linear>
        </div>

        <!-- Dragon Progress Tracker — animation state changes at each $10k milestone -->
        <DragonProgressTracker
          :total="progress.total"
          :current-milestone="progress.currentMilestone"
          :next-milestone="progress.nextMilestone"
        />

        <!-- Gold hoard: grows as the total grows. stepSize/stages should match
             the dragon's own milestones (see DragonProgressTracker). -->
        <GoldHoard :total="progress.total" :step-size="10000" :stages="8" />

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- Call to Action: links to the "Charity Direct Donate Link" column -->
        <div class="d-flex justify-end">
          <v-btn
            v-if="donateLink"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2 text-white castle-btn castle-btn-label"
            :href="donateLink"
            target="_blank"
            rel="noopener"
          >
            Add to the Hoard
          </v-btn>
          <v-btn
            v-else
            color="grey-lighten-1"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2"
            disabled
          >
            Donate link not set yet
          </v-btn>
        </div>

      </div>
    </CastleFrame>
  </v-container>
</template>






<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import DragonProgressTracker from '@/components/DragonProgressTracker.vue'
import CastleFrame from '@/components/castle/CastleFrame.vue'
import GoldHoard from '@/components/castle/GoldHoard.vue'

interface Campaign {
  name: string
  tagline: string
  charityName: string
  charityLogoUrl: string
  charityWebsite: string
  charityDirectDonateLink: string
  charityDescription: string
  startDate: string
  endDate: string
}

const campaign = ref<Campaign>({
  name: '', tagline: '', charityName: '', charityLogoUrl: '',
  charityWebsite: '', charityDirectDonateLink: '', charityDescription: '', startDate: '', endDate: ''
})

const progress = ref({
  total: 0,
  currentMilestone: 0,
  nextMilestone: 10000,
  progressWithinMilestone: 0
})

// Stays false until the real data has arrived, so the page never shows placeholder text first
const contentReady = ref(false)

// The .replace makes NocoDB's date format readable in every browser (including Safari)
const formatDateTime = (value: string) => {
  if (!value) return 'TBD'
  const parsed = new Date(value.replace(' ', 'T'))
  if (isNaN(parsed.getTime())) return 'TBD'
  return parsed.toLocaleString(undefined, {
    month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit'
  })
}

const formattedStartDate = computed(() => formatDateTime(campaign.value.startDate))
const formattedEndDate = computed(() => formatDateTime(campaign.value.endDate))
const formattedRaised = computed(() => `$${progress.value.total.toLocaleString()}`)
// const formattedNextMilestone = computed(() => `$${progress.value.nextMilestone.toLocaleString()}`)

// Adds https:// when someone forgets it, so links don't turn into pages on your own site
const withHttps = (value: string) => {
  const link = (value || '').trim()
  if (!link) return ''
  return /^https?:\/\//i.test(link) ? link : `https://${link}`
}
const donateLink = computed(() => withHttps(campaign.value.charityDirectDonateLink))
const websiteLink = computed(() => withHttps(campaign.value.charityWebsite))

let pollHandle: ReturnType<typeof setInterval> | null = null

// Hits Flask progress route
const refreshProgress = async () => {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign-progress`
    const res = await fetch(url)
    const data = await res.json()

    progress.value = {
      total: data.total ?? 0,
      currentMilestone: data.currentMilestone ?? 0,
      nextMilestone: data.nextMilestone ?? 10000,
      progressWithinMilestone: data.progressWithinMilestone ?? 0
    }
  } catch (err) {
    console.error('Failed to refresh campaign progress:', err)
  }
}

// Hits flat Flask metadata route
const loadCampaignInfo = async () => {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign-info`
    const res = await fetch(url)
    campaign.value = await res.json()
  } catch (err) {
    console.error('Failed to load campaign info:', err)
  }
}

onMounted(async () => {
  pollHandle = setInterval(refreshProgress, 20000) // Poll for donation updates
  // Safety net: show the card anyway if the API is slow or down
  const timer = setTimeout(() => { contentReady.value = true }, 3000)
  await Promise.all([loadCampaignInfo(), refreshProgress()])
  clearTimeout(timer)
  contentReady.value = true
})

onUnmounted(() => {
  if (pollHandle) clearInterval(pollHandle)
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

/* Pixel-style display font for the campaign title, labels and button, to match
   the castle art. Body copy (tagline, descriptions) stays in the readable serif
   already used elsewhere on the page. Swap the font name below to change it. */
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@500;700&display=swap');

.castle-heading {
  font-family: 'Pixelify Sans', Georgia, serif;
  color: #5b3a1a;
  letter-spacing: 0.02em;
}
.castle-label {
  font-family: 'Pixelify Sans', Georgia, serif;
  font-size: 0.8rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
.castle-btn-label {
  font-family: 'Pixelify Sans', Georgia, serif;
  letter-spacing: 0.03em;
}
/* Warm bronze button instead of the flat corporate blue, to match the wood
   and gold in the castle art. */
.castle-btn {
  background-color: #8a5a2b !important;
  border: 2px solid #5b3a1a;
}
.castle-btn:hover {
  background-color: #a8703a !important;
}
</style>