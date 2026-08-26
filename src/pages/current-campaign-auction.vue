<template>
  <v-container class="py-10 px-6" max-width="900">

    <!-- Master Layout Card Container — matches donator-information.vue -->
    <v-card
      class="rounded-2xl border-0 mb-12"
      style="background-color: #FFFFFF !important; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03) !important;"
      elevation="0"
    >
      <v-card-text class="pa-6 pa-md-10">

        <!-- Campaign Header -->
        <div class="text-left mb-8">
          <p class="text-caption font-weight-bold text-uppercase text-medium-emphasis mb-1" style="letter-spacing: 0.08em;">
            Current Campaign!
          </p>
          <h1 class="text-h4 font-weight-black text-black mb-2">
            {{ campaign.name || 'Campaign name here' }}
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
            <p class="text-caption text-medium-emphasis mb-0">Benefiting</p>
            <p class="text-h6 font-weight-bold text-black mb-0">
              {{ campaign.charityName || 'No charity selected yet' }}
            </p>
            <a
              v-if="campaign.charityWebsite"
              :href="campaign.charityWebsite"
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
            <p class="text-caption text-medium-emphasis mb-0">Starts</p>
            <p class="text-subtitle-2 font-weight-bold text-black">{{ formattedStartDate }}</p>
          </v-col>
          <v-col cols="6">
            <p class="text-caption text-medium-emphasis mb-0">Ends</p>
            <p class="text-subtitle-2 font-weight-bold text-black">{{ formattedEndDate }}</p>
          </v-col>
        </v-row>

        <!-- Fundraising Goal + Progress -->
        <div class="mb-8">
          <div class="d-flex justify-space-between mb-2">
            <p class="text-caption text-medium-emphasis mb-0">{{ formattedRaised }} raised</p>
            <p class="text-caption text-medium-emphasis mb-0">Goal: {{ formattedGoal }}</p>
          </div>
          <v-progress-linear
            :model-value="progressPercent"
            height="10"
            rounded
            color="#0B4F6C"
            bg-color="grey-lighten-3"
          ></v-progress-linear>
        </div>

        <!-- Progress Tracker -->
        <DragonProgressTracker
          :total="progress.total"
          :current-milestone="progress.currentMilestone"
          :next-milestone="progress.nextMilestone"
        />

        <v-divider class="mb-6 opacity-50"></v-divider>

        <!-- Call to Action -->
        <div class="d-flex justify-end">
          <v-btn
            v-if="campaign.charityWebsite"
            color="#0B4F6C"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2 text-white"
            :href="campaign.charityWebsite"
            target="_blank"
            rel="noopener"
          >
            Visit {{ campaign.charityName || 'Charity' }}
          </v-btn>
          <v-btn
            v-else
            color="grey-lighten-1"
            variant="flat"
            size="large"
            class="text-none font-weight-bold rounded-lg px-8 py-2"
            disabled
          >
            Charity link not set yet
          </v-btn>
        </div>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { apiService } from '@/services/api'
import DragonProgressTracker from '@/components/DragonProgressTracker.vue'

interface Campaign {
  name: string
  tagline: string
  charityName: string
  charityLogoUrl: string
  charityWebsite: string
  charityDescription: string
  startDate: string
  endDate: string
}

const campaign = ref<Campaign>({
  name: '',
  tagline: '',
  charityName: '',
  charityLogoUrl: '',
  charityWebsite: '',
  charityDescription: '',
  startDate: '',
  endDate: ''
})

// Start Date / End Date are now full datetimes (charity runs end at a specific time),
// so format them for display rather than showing the raw ISO string.
const formatDateTime = (value: string) => {
  if (!value) return 'TBD'
  const parsed = new Date(value)
  if (isNaN(parsed.getTime())) return 'TBD'
  return parsed.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

const formattedStartDate = computed(() => formatDateTime(campaign.value.startDate))
const formattedEndDate = computed(() => formatDateTime(campaign.value.endDate))

const formattedGoal = computed(() =>
  campaign.value.goalAmount ? `$${campaign.value.goalAmount.toLocaleString()}` : 'TBD'
)

const formattedRaised = computed(() => `$${campaign.value.raisedAmount.toLocaleString()}`)

const progress = ref({
  total: 0,
  currentMilestone: 0,
  nextMilestone: 10000
})

let pollHandle: ReturnType<typeof setInterval> | null = null

const refreshProgress = async () => {
  try {
    const data = await apiService.fetchCampaignProgress()
    progress.value = {
      total: data.total,
      currentMilestone: data.currentMilestone,
      nextMilestone: data.nextMilestone
    }
  } catch (err) {
    console.error('Failed to refresh campaign progress:', err)
  }
}

const loadCampaignInfo = async () => {
  try {
    campaign.value = await apiService.fetchCampaignInfo()
  } catch (err) {
    console.error('Failed to load campaign info:', err)
  }
}

onMounted(() => {
  loadCampaignInfo()
  refreshProgress()
  pollHandle = setInterval(refreshProgress, 20000)
})

onUnmounted(() => {
  if (pollHandle) clearInterval(pollHandle)
})
</script>