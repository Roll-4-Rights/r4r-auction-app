<template>
  <div class="home-page">

    <!-- Hero image -->
    <div class="hero-section">      <!-- The rigid  frame -->
      <div class="pan-container">  <!-- Fit the frame  -->
        <img :src="heroImage" alt="Panning photo" class="pan-image"> <!-- The sliding picture -->
      </div>
    </div>


    <!-- Welcome heading + intro -->
    <v-container class="text-center welcome-section">
      <h1 class="welcome-title">
        Welcome to the {{ campaignName }} Fundraiser!
      </h1>
      <p class="body-text mt-4">
        {{ introParagraph }}
      </p>
    </v-container>

    <!-- Body copy + CTA -->
    <v-container class="text-center body-section">
      <p v-for="(para, i) in bodyParagraphs" :key="i" class="body-text mb-4">
        {{ para }}
      </p>

      <v-btn
        class="cta-button mt-2"
        size="large"
        rounded="pill"
        @click="goToPastAuctions"
      >
        {{ ctaText }}
      </v-btn>

      <h2 class="quick-links-title mt-12">Quick Links</h2>
      <div class="quick-links">
        <router-link
          v-for="link in quickLinks"
          :key="link.label"
          :to="link.to"
          class="quick-link"
        >
          {{ link.label }}
        </router-link>
      </div>

      <div class="social-icons mt-4">
        <a :href="instagramUrl" target="_blank" rel="noopener" aria-label="Instagram">
          <v-icon size="22">mdi-instagram</v-icon>
        </a>
        <a :href="blueskyUrl" target="_blank" rel="noopener" aria-label="Bluesky">
          <v-icon size="22">mdi-butterfly-outline</v-icon>
        </a>
      </div>
    </v-container>

    <!-- Footer -->
    <v-divider />
    <footer class="site-footer">
      <div class="footer-country">
        <div class="footer-country-label">Country/region</div>
        <v-select
          v-model="country"
          :items="countryOptions"
          item-title="label"
          item-value="value"
          density="compact"
          variant="outlined"
          hide-details
          class="footer-country-select"
        />
      </div>
      <div class="footer-copy">
        {{ footerCopy || `© ${currentYear}, Roll4Rights · Privacy policy` }}
      </div>
    </footer>
  </div>
</template>





<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import fallbackHeroImage from '@/assets/Hero_Sized_big.jpg'

const router = useRouter()

const campaignName = ref('Roll4Rights')
const heroImage = ref(fallbackHeroImage)
const introParagraph = ref('intro paragraph')

const bodyParagraphs = ref([
  'body paragraph 1',
  'body paragraph 2',
])

const ctaText = ref('CTA button')
const instagramUrl = ref('https://instagram.com')
const blueskyUrl = ref('https://bsky.app')
const footerCopy = ref('')

const quickLinks = [
  { label: 'Search', to: '/search' },
  { label: 'FAQ', to: '/faq' },
  { label: 'Contact Us', to: '/contact' },
]

function goToPastAuctions() {
  router.push('/current-campaign')
}

const country = ref('us')
const countryOptions = [
  { label: 'United States | USD \$', value: 'us' },
]

const currentYear = computed(() => new Date().getFullYear())

async function fetchSiteContent() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/site-content`
    const res = await fetch(url)
    const data = await res.json()
    console.log('site-content response:', data)

    if (data.error) {
      console.error('Site content error:', data.error)
      return
    }
  
    // Properly tracks index [0] of data.list or handles flat objects
    const content = Array.isArray(data.list) ? (data.list[0] ?? {}) : (data ?? {})

    const rawHeroImage = content['Hero Image']
    if (rawHeroImage) {
      if (Array.isArray(rawHeroImage) && rawHeroImage.length > 0) {
        const attachment = rawHeroImage[0]
        const rawUrl = attachment.url || attachment.signedUrl || attachment.path
        
        if (rawUrl) {
          if (rawUrl.startsWith('http')) {
            heroImage.value = rawUrl
          } else if (rawUrl.startsWith('/')) {
            heroImage.value = `http://localhost:8080${rawUrl}`
          } else {
            // Forces local NocoDB upload paths (like noco/...) to load via port 8080
            heroImage.value = `http://localhost:8080/${rawUrl}`
          }
        }
      } else if (typeof rawHeroImage === 'string') {
        const matchStr = rawHeroImage.match(/https?:\/\/[^\s)]+/)
        heroImage.value = matchStr ? matchStr[0] : fallbackHeroImage
      }
    }
  
    if (content['Intro Paragraph']) introParagraph.value = content['Intro Paragraph']
    if (content['Body Paragraph 1'] || content['Body Paragraph 2']) {
      bodyParagraphs.value = [content['Body Paragraph 1'], content['Body Paragraph 2']].filter(Boolean)
    }
    if (content['Cta Button Text']) ctaText.value = content['Cta Button Text']
    if (content['Social Instagram Url']) instagramUrl.value = content['Social Instagram Url']
    if (content['Social Bluesky Url']) blueskyUrl.value = content['Social Bluesky Url']
    if (content['Footer Copy']) footerCopy.value = content['Footer Copy']
  } catch (err) {
    console.error('Failed to load site content', err)
    heroImage.value = fallbackHeroImage
  }
}

async function fetchCampaignSettings() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/campaign`
    const res = await fetch(url)
    const data = await res.json()
    
    const content = Array.isArray(data.list) ? (data.list[0] ?? {}) : (data ?? {})
    
    if (content['Campaign Name']) {
      campaignName.value = content['Campaign Name']
    }
  } catch (err) {
    console.error('Failed to load campaign settings', err)
  }
}

onMounted(() => {
  fetchSiteContent()
  fetchCampaignSettings()
})
</script>







<style scoped>
.home-page {
  background: #f2ece1;
}

/* 🎥 Hero Section & Pan Animation Frame */
.hero-section {
  width: 100%;
  height: 500px;
  overflow: hidden;
  position: relative;
  isolation: isolate; 
}

.pan-container {
  width: 100%;
  height: 100%;
}

.pan-image {
  width: 115%; /* 15% extra width padding to slide across */
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  right: 0; /* Forces the animation to slide right first */
  
  animation: smoothPan 28s linear infinite alternate; 
  will-change: transform;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes smoothPan {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(13%, 0, 0); 
  }
}

/* Welcome section */
.welcome-section {
  max-width: 700px;
  padding: 48px 24px 32px;
}
.welcome-title {
  font-family: 'Georgia', serif;
  font-size: 2rem;
  color: #163a47;
  font-weight: 700;
  line-height: 1.3;
}

.body-text {
  color: #6d6257;
  font-size: 0.95rem;
  line-height: 1.7;
  max-width: 620px;
  margin-left: auto;
  margin-right: auto;
}

/* Body section */
.body-section {
  max-width: 700px;
  padding: 40px 24px 56px;
}

.cta-button {
  background: #0f2b36 !important;
  color: #fff !important;
  text-transform: none;
  font-size: 0.85rem;
  padding: 0 28px;
  height: auto;
  line-height: 1.4;
  min-height: 56px;
}

.quick-links-title {
  font-family: 'Georgia', serif;
  font-size: 1.3rem;
  color: #163a47;
}
.quick-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 8px;
  font-size: 0.85rem;
}
.quick-link {
  color: #6d6257;
  text-decoration: none;
}
.quick-link:hover {
  text-decoration: underline;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
}
.social-icons a {
  color: #163a47;
}

/* Footer Layout (Fixed the backslash typo) */
.site-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 32px 16px;
  font-size: 0.75rem;
  color: #6d6257;
}
.footer-country {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}
.footer-country-select {
  max-width: 220px;
}
</style>
