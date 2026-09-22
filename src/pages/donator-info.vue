<template>
  <v-container class="py-10 px-6" max-width="1400">
    <!-- Reserved for future hand-drawn fantasy banner artwork -->
    <div class="donator-banner-placeholder">
      <img
        src="/images/donator-info-banner.png"
        alt="Donator Profiles"
        class="donator-banner-image"
      />
    </div>

        <!-- Fantasy ivy divider -->
    <div class="ivy-divider" aria-hidden="true">
      <img
        src="/images/ivy-divider.svg"
        alt=""
        class="ivy-divider-image"
      />
    </div>

    <!-- Loading state -->
    <div v-if="loading && profiles.length === 0" class="d-flex justify-center py-12">
      <v-progress-circular indeterminate color="#0B4F6C" size="48"></v-progress-circular>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-12 text-medium-emphasis">
      <p class="text-body-1">Couldn't load donator profiles right now. Please try again shortly.</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="profiles.length === 0" class="text-center py-12 text-medium-emphasis">
      <p class="text-body-1">No donator profiles yet — check back soon!</p>
    </div>

    <template v-else>
      <v-row>
        <v-col
          v-for="profile in profiles"
          :key="profile.id"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card
            class="h-100 parchment-card elevation-hover"
            elevation="0"
          >
            <!-- parchment decoration -->

            <v-card-text class="parchment-content pa-6">
              <h3 class="donator-name mb-3">
                {{ profile.socialMediaName || 'Anonymous Donator' }}
              </h3>

              <p class="donator-description">
                {{ profile.waresDescription }}
              </p>

              <div class="card-footer">
                <div
                  v-if="profile.location"
                  class="donator-location"
                >
                  <v-icon icon="mdi-map-marker-outline" size="16"></v-icon>
                  <span>{{ profile.location }}</span>
                </div>

                <a
                  v-if="profile.website"
                  :href="withHttps(profile.website)"
                  target="_blank"
                  rel="noopener"
                  class="donator-website"
                >
                  <v-icon icon="mdi-open-in-new" size="14"></v-icon>
                  <span>Visit Website</span>
                </a>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Pagination -->
      <div class="d-flex align-center justify-center mt-10" style="gap: 16px;">
        <v-btn
          icon="mdi-chevron-left"
          variant="tonal"
          color="#0B4F6C"
          :disabled="page === 1 || loading"
          @click="goToPage(page - 1)"
        ></v-btn>

        <span class="text-body-2 font-weight-bold text-medium-emphasis">
          Page {{ page }}<span v-if="totalPages"> of {{ totalPages }}</span>
        </span>

        <v-btn
          icon="mdi-chevron-right"
          variant="tonal"
          color="#0B4F6C"
          :disabled="isLastPage || loading"
          @click="goToPage(page + 1)"
        ></v-btn>
      </div>
    </template>
  </v-container>
</template>




<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { apiService } from '@/services/api'

interface DonatorProfile {
  id: number
  socialMediaName: string
  waresDescription: string
  location: string
  website: string
}

const PAGE_SIZE = 9 // 3x3 grid

const profiles = ref<DonatorProfile[]>([])
const page = ref(1)
const totalRows = ref<number | null>(null)
const isLastPage = ref(false)
const loading = ref(false)
const error = ref(false)

const totalPages = computed(() =>
  totalRows.value !== null ? Math.max(1, Math.ceil(totalRows.value / PAGE_SIZE)) : null
)

// Adds https:// when someone forgets it in the NocoDB "Website" field
const withHttps = (value: string) => {
  const link = (value || '').trim()
  if (!link) return ''
  return /^https?:\/\//i.test(link) ? link : `https://${link}`
}

const fetchProfiles = async () => {
  loading.value = true
  error.value = false
  try {
    const data = await apiService.fetchDonatorProfiles({
      limit: PAGE_SIZE,
      offset: (page.value - 1) * PAGE_SIZE
    })
    profiles.value = (data.list || []).map((row: any) => ({
      id: row.Id,
      socialMediaName: row['Social Media Name'] || '',
      waresDescription: row['Wares Description'] || '',
      location: row['Location'] || '',
      website: row['Website'] || ''
    }))
    totalRows.value = data.pageInfo?.totalRows ?? null
    isLastPage.value = data.pageInfo?.isLastPage ?? profiles.value.length < PAGE_SIZE
  } catch (err) {
    console.error('Failed to fetch donator profiles:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const goToPage = (target: number) => {
  if (target < 1 || loading.value) return
  page.value = target
  fetchProfiles()
}

onMounted(fetchProfiles)
</script>







<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Eagle+Lake&family=IM+Fell+English:ital@0;1&display=swap');

.elevation-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.06) !important;
}

/* Banner image at top */
.donator-banner-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 150px;
  margin: 0 auto 2.5rem;
  padding: 0 1rem;
}

.donator-banner-image {
  display: block;
  width: min(100%, 400px);
  height: auto;
  min-height: 120px;
  object-fit: contain;
}

/* Ivy divider */
.ivy-divider {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 0 auto 2.5rem;
  padding: 0 0.5rem;
}

.ivy-divider-image {
  display: block;
  width: 100%;
  max-width: 1200px;
  height: auto;
  max-height: 100px;
  object-fit: contain;
}

/* Outer parchment card */
.parchment-card {
  position: relative;
  overflow: hidden;
  min-height: 260px;
  height: 100%;
  border: 1px solid #b98b4d !important;
  border-radius: 4px !important;
  background:
    linear-gradient(
      135deg,
      rgba(112, 70, 28, 0.16),
      transparent 18%,
      transparent 78%,
      rgba(112, 70, 28, 0.14)
    ),
    linear-gradient(
      90deg,
      rgba(255, 247, 205, 0.3),
      transparent 22%,
      rgba(121, 74, 28, 0.08) 70%,
      rgba(255, 247, 205, 0.2)
    ),
    #e4c98f !important;
  box-shadow:
    0 7px 12px rgba(67, 39, 15, 0.2),
    inset 0 0 18px rgba(111, 64, 19, 0.2),
    inset 0 0 3px rgba(255, 244, 192, 0.8) !important;
  transform: rotate(-0.35deg);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

/* Alternate rotation for hand-made feel */
.parchment-card:nth-child(even) {
  transform: rotate(0.35deg);
}

.parchment-card:hover {
  transform: translateY(-4px) rotate(0deg);
  box-shadow:
    0 13px 22px rgba(67, 39, 15, 0.25),
    inset 0 0 18px rgba(111, 64, 19, 0.2),
    inset 0 0 3px rgba(255, 244, 192, 0.8) !important;
}

/* Parchment corners and decorative curls */
.parchment-card::before,
.parchment-card::after {
  content: "";
  position: absolute;
  z-index: 1;
  width: 42px;
  height: 42px;
  background: rgba(125, 76, 27, 0.18);
  pointer-events: none;
}

.parchment-card::before {
  top: -22px;
  left: -22px;
  border-radius: 50%;
  box-shadow: 7px 7px 0 rgba(255, 239, 174, 0.25);
}

.parchment-card::after {
  right: -22px;
  bottom: -22px;
  border-radius: 50%;
  box-shadow: -7px -7px 0 rgba(255, 239, 174, 0.22);
}

.parchment-decoration {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
}

.parchment-curl {
  position: absolute;
  width: 34px;
  height: 12px;
  border: 2px solid rgba(112, 65, 21, 0.48);
  border-radius: 50%;
  opacity: 0.8;
}

.parchment-curl-top-left {
  top: 12px;
  left: 12px;
  transform: rotate(-35deg);
}

.parchment-curl-top-right {
  top: 12px;
  right: 12px;
  transform: rotate(35deg);
}

/* Ivy vines and leaves */
.ivy-vine {
  position: absolute;
  display: block;
  height: 3px;
  border-radius: 50%;
  background: #3f5d2d;
  opacity: 0.9;
  transform-origin: left center;
}

.ivy-vine-left {
  left: 5px;
  bottom: 28px;
  width: 92px;
  transform: rotate(-64deg);
}

.ivy-vine-bottom {
  right: 12px;
  bottom: 9px;
  width: 132px;
  transform: rotate(-4deg);
}

.ivy-leaf {
  position: absolute;
  z-index: 3;
  width: 13px;
  height: 19px;
  border-radius: 13px 2px 13px 2px;
  background: linear-gradient(135deg, #6f8e45, #304b25);
  box-shadow: 1px 1px 2px rgba(45, 56, 24, 0.35);
  opacity: 0.95;
}

.leaf-1 {
  left: 18px;
  bottom: 73px;
  transform: rotate(-42deg);
}

.leaf-2 {
  left: 40px;
  bottom: 54px;
  transform: rotate(28deg);
}

.leaf-3 {
  left: 61px;
  bottom: 32px;
  transform: rotate(-38deg);
}

.leaf-4 {
  right: 94px;
  bottom: 14px;
  transform: rotate(38deg);
}

.leaf-5 {
  right: 57px;
  bottom: 10px;
  transform: rotate(-42deg);
}

/* Main card content */
.parchment-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  min-height: 260px;
  height: 100%;
  box-sizing: border-box;
  padding-bottom: 4.5rem !important;
  color: #4b2b17;
  text-align: center;
}

.donator-name {
  margin: 0;
  color: #4b2b17;
  font-family: "Eagle Lake", Georgia, serif;
  font-size: clamp(1.15rem, 2vw, 1.4rem);
  font-weight: 400;
  line-height: 1.35;
  letter-spacing: 0.02em;
  text-align: center;
}

.donator-description {
  flex: 1;
  margin: 0;
  color: #5b4025;
  font-family: "IM Fell English", Georgia, serif;
  font-size: 1.08rem;
  line-height: 1.5;
  text-align: center;
}

.card-footer {
  position: absolute;
  right: 1.5rem;
  bottom: 1.25rem;
  left: 1.5rem;

  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  min-height: 26px;
  width: auto;
}

.donator-location,
.donator-website {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  max-width: 48%;
  line-height: 1.3;
  white-space: normal;
}

.donator-location {
  justify-content: flex-start;
  color: #73512c;
  font-family: Georgia, serif;
  font-size: 0.8rem;
  text-align: left;
}

.donator-website {
  justify-content: flex-end;
  margin-left: auto;
  color: #345b38 !important;
  font-family: Georgia, serif;
  font-size: 0.75rem;
  text-align: right;
  text-decoration: none;
  text-transform: uppercase;
}

.donator-website:hover {
  color: #1f3d26 !important;
  text-decoration: underline;
}

.donator-location span,
.donator-website span {
  overflow-wrap: anywhere;
}

/* Optional PNG-override styles for a future art image */
.parchment-image-layer {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
}

.parchment-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
}

@media (max-width: 600px) {
  .donator-banner-placeholder {
    min-height: 100px;
    margin-bottom: 2rem;
    padding: 0;
  }

  .donator-banner-image {
    min-height: 90px;
  }

  .ivy-divider {
    padding: 0 0.25rem;
  }

  .parchment-card {
    min-height: 250px;
  }

  .parchment-content {
    min-height: 250px;
    padding: 1.25rem 1.25rem 4.25rem !important;
  }

  .card-footer {
    right: 1.25rem;
    bottom: 1rem;
    left: 1.25rem;
    gap: 0.5rem;
  }

  .donator-location,
  .donator-website {
    max-width: 46%;
    font-size: 0.7rem;
  }

  .donator-website {
    text-transform: none;
  }

  .donator-description {
    font-size: 1rem;
    line-height: 1.45;
  }
}
</style>