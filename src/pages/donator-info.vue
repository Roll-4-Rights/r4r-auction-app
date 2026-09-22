<template>
  <v-container class="py-10 px-6" max-width="1400">
    <div class="cloth-banner-wrap">
      <div class="cloth-banner">
        <div class="banner-roll banner-roll-left"></div>

        <h1>Donator Profiles</h1>

        <div class="banner-roll banner-roll-right"></div>
      </div>
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
            class="h-100 rounded-2xl border-0 elevation-hover"
            style="background-color: #FFFFFF !important; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03) !important; transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;"
            elevation="0"
          >
            <v-card-text class="pa-6 d-flex flex-column" style="min-height: 230px;">
              <h3 class="text-h6 font-weight-black text-black mb-2">
                {{ profile.socialMediaName || 'Anonymous Donator' }}
              </h3>

              <div v-if="profile.location" class="d-flex align-center mb-3 text-medium-emphasis text-body-2">
                <v-icon icon="mdi-map-marker-outline" size="16" class="mr-1"></v-icon>
                {{ profile.location }}
              </div>

              <p
                class="text-body-2 text-medium-emphasis leading-relaxed mb-4"
                style="flex-grow: 1; white-space: normal; overflow-wrap: break-word;"
              >
                {{ profile.waresDescription }}
              </p>

              <a
                v-if="profile.website"
                :href="withHttps(profile.website)"
                target="_blank"
                rel="noopener"
                class="text-caption font-weight-bold d-flex align-center"
                style="color: #0B4F6C; text-decoration: none;"
              >
                <v-icon icon="mdi-open-in-new" size="14" class="mr-1"></v-icon>
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
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&display=swap');

.cloth-banner-wrap {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 2.5rem;
  padding: 0 2.5rem;
}

.cloth-banner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: min(100%, 760px);
  min-height: 112px;
  padding: 1.25rem 4rem;
  color: #4b2b17;
  text-align: center;
  background:
    linear-gradient(
      90deg,
      rgba(112, 69, 29, 0.22) 0%,
      transparent 8%,
      rgba(255, 241, 190, 0.3) 22%,
      transparent 42%,
      rgba(113, 70, 30, 0.12) 68%,
      transparent 88%,
      rgba(92, 52, 20, 0.22) 100%
    ),
    #d8b477;
  border-top: 3px solid #9a692f;
  border-bottom: 4px solid #8b5b28;
  box-shadow:
    0 8px 12px rgba(66, 38, 15, 0.28),
    inset 0 5px 7px rgba(255, 245, 202, 0.35),
    inset 0 -8px 10px rgba(91, 48, 13, 0.2);
  transform: rotate(-0.5deg);
}

/* Subtle cloth folds */
.cloth-banner::before,
.cloth-banner::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 18%;
  pointer-events: none;
}

.cloth-banner::before {
  left: 12%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 245, 202, 0.25),
    transparent
  );
}

.cloth-banner::after {
  right: 12%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(92, 48, 14, 0.13),
    transparent
  );
}

.cloth-banner h1 {
  position: relative;
  z-index: 1;
  margin: 0;
  font-family: "Cinzel", Georgia, serif;
  font-size: clamp(1.45rem, 3vw, 2.5rem);
  font-weight: 800;
  letter-spacing: 0.08em;
  line-height: 1.2;
  text-transform: uppercase;
  text-shadow:
    1px 1px 0 rgba(255, 238, 175, 0.55),
    2px 2px 2px rgba(70, 38, 14, 0.25);
}

/* Rolled wooden/fabric ends */
.banner-roll {
  position: absolute;
  top: -7px;
  width: 30px;
  height: calc(100% + 14px);
  border: 2px solid #82501f;
  border-radius: 8px;
  background: linear-gradient(
    90deg,
    #704118,
    #c28c43 35%,
    #e0b66b 55%,
    #87541f
  );
  box-shadow:
    2px 4px 5px rgba(64, 34, 10, 0.3),
    inset 2px 0 3px rgba(255, 222, 140, 0.35);
}

.banner-roll-left {
  left: -20px;
  transform: rotate(2deg);
}

.banner-roll-right {
  right: -20px;
  transform: rotate(-2deg);
}

/* Hanging pointed cloth ends */
.banner-roll-left::after,
.banner-roll-right::after {
  content: "";
  position: absolute;
  top: 100%;
  width: 44px;
  height: 45px;
  background: #b68543;
  border-bottom: 3px solid #82501f;
  clip-path: polygon(0 0, 100% 0, 72% 100%, 50% 78%, 28% 100%);
}

.banner-roll-left::after {
  left: -9px;
  transform: rotate(2deg);
}

.banner-roll-right::after {
  right: -9px;
  transform: rotate(-2deg);
}

@media (max-width: 600px) {
  .cloth-banner-wrap {
    padding: 0 1.5rem;
  }

  .cloth-banner {
    min-height: 92px;
    padding: 1rem 2.5rem;
  }

  .banner-roll {
    width: 22px;
  }

  .banner-roll-left {
    left: -14px;
  }

  .banner-roll-right {
    right: -14px;
  }

  .cloth-banner h1 {
    letter-spacing: 0.04em;
  }
}

.elevation-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06) !important;
}
</style>