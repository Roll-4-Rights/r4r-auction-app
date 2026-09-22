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
        src="/images/ivy-divider.png"
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
.elevation-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.06) !important;
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

.elevation-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06) !important;
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