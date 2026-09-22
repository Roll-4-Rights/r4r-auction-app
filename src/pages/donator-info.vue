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
      <v-row justify="center">
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
            <div class="parchment-decoration" aria-hidden="true">
              <span class="parchment-curl parchment-curl-top-left"></span>
              <span class="parchment-curl parchment-curl-top-right"></span>

              <span class="ivy-vine ivy-vine-left"></span>
              <span class="ivy-vine ivy-vine-bottom"></span>
              <span class="ivy-leaf leaf-1"></span>
              <span class="ivy-leaf leaf-2"></span>
              <span class="ivy-leaf leaf-3"></span>
              <span class="ivy-leaf leaf-4"></span>
              <span class="ivy-leaf leaf-5"></span>
            </div>

            <v-card-text class="parchment-content pa-6 d-flex flex-column">
              <div class="d-flex align-center mb-3">
                <span class="wax-seal" aria-hidden="true">
                  {{ (profile.socialMediaName || 'A').charAt(0).toUpperCase() }}
                </span>
                <h3 class="donator-name mb-0">
                  {{ profile.socialMediaName || 'Anonymous Donator' }}
                </h3>
              </div>

              <div class="name-rule" aria-hidden="true"></div>

              <div
                v-if="profile.location"
                class="d-flex align-center mb-3 mt-3 donator-location"
              >
                <v-icon icon="mdi-map-marker-outline" size="15" class="mr-1"></v-icon>
                {{ profile.location }}
              </div>

              <p
                class="donator-wares mb-4"
                style="flex-grow: 1; white-space: normal; overflow-wrap: break-word;"
              >
                {{ profile.waresDescription }}
              </p>

              <a
                v-if="profile.website"
                :href="withHttps(profile.website)"
                target="_blank"
                rel="noopener"
                class="visit-link d-flex align-center"
              >
                <v-icon icon="mdi-feather" size="14" class="mr-1"></v-icon>
                Visit Website
              </a>
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
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap');

.donator-name {
  font-family: 'Cinzel', 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #3d2413;
  line-height: 1.3;
}

.name-rule {
  height: 2px;
  width: 56px;
  margin-left: 46px;
  background: linear-gradient(90deg, #a8792f, transparent);
}

.donator-location {
  font-family: 'EB Garamond', serif;
  font-size: 0.9rem;
  font-style: italic;
  color: #6e5433;
}

.donator-wares {
  font-family: 'EB Garamond', serif;
  font-size: 1.02rem;
  line-height: 1.55;
  color: #4b2b17;
}

.visit-link {
  font-family: 'EB Garamond', serif;
  font-size: 0.92rem;
  font-weight: 600;
  color: #6e1f2b;
  text-decoration: none;
  width: fit-content;
  border-bottom: 1px solid rgba(110, 31, 43, 0.35);
  padding-bottom: 1px;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.visit-link:hover {
  color: #8a2836;
  border-color: rgba(110, 31, 43, 0.7);
}

.wax-seal {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  margin-right: 12px;
  font-family: 'Cinzel', serif;
  font-weight: 700;
  font-size: 0.95rem;
  color: #f4e6c2;
  background: radial-gradient(circle at 32% 28%, #9c2f3d, #6e1f2b 65%, #4c141f 100%);
  box-shadow:
    0 2px 4px rgba(60, 10, 15, 0.4),
    inset 0 0 3px rgba(255, 220, 180, 0.35);
}

.parchment-card {
  position: relative;
  overflow: hidden;
  min-height: 260px;
  border: 1px solid #a8792f !important;
  border-radius: 3px !important;
  background:
    radial-gradient(
      ellipse at 20% 15%,
      rgba(255, 250, 222, 0.55),
      transparent 45%
    ),
    linear-gradient(
      135deg,
      rgba(112, 70, 28, 0.18),
      transparent 20%,
      transparent 76%,
      rgba(112, 70, 28, 0.16)
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
    0 7px 14px rgba(67, 39, 15, 0.22),
    inset 0 0 22px rgba(111, 64, 19, 0.22),
    inset 0 0 3px rgba(255, 244, 192, 0.85) !important;
  transform: rotate(-0.35deg);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

/* Alternating slight rotations make the cards feel handmade. */
.parchment-card:nth-child(even) {
  transform: rotate(0.35deg);
}

.parchment-card:hover {
  transform: translateY(-5px) rotate(0deg);
  box-shadow:
    0 16px 26px rgba(67, 39, 15, 0.28),
    0 0 18px rgba(184, 118, 44, 0.25),
    inset 0 0 22px rgba(111, 64, 19, 0.22),
    inset 0 0 3px rgba(255, 244, 192, 0.85) !important;
}

.parchment-content {
  position: relative;
  z-index: 3;
  min-height: 260px;
  color: #4b2b17;
}

/* Soft, uneven-looking parchment corners. */
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

/* Decorative rolled/curl marks at the top corners. */
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

/* Base vine shape. */
.ivy-vine {
  position: absolute;
  display: block;
  height: 3px;
  border-radius: 50%;
  background: #3f5d2d;
  opacity: 0.9;
  transform-origin: left center;
}

/* Ivy climbing the left edge. */
.ivy-vine-left {
  left: 5px;
  bottom: 28px;
  width: 92px;
  transform: rotate(-64deg);
}

/* Ivy trailing along the bottom edge. */
.ivy-vine-bottom {
  right: 12px;
  bottom: 9px;
  width: 132px;
  transform: rotate(-4deg);
}

/* Individual leaves. */
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

@media (max-width: 600px) {
  .donator-banner-placeholder {
    min-height: 100px;
    margin-bottom: 2rem;
    padding: 0;
  }

  .donator-banner-image {
    min-height: 90px;
  }
}

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
</style>