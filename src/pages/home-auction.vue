<template>
  <div class="home-page">
    <!-- Hero image -->
    <div class="hero-section">
      <v-img :src="heroImage" height="500" cover class="hero-image" />
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
        {{ footerCopy || `© ${currentYear}, Roll4Rights Powered by Shopify · Privacy policy` }}
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
  { label: 'United States | USD $', value: 'us' },
]

const currentYear = computed(() => new Date().getFullYear())

async function fetchSiteContent() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/api/site-content`
    const res = await fetch(url)
    const data = await res.json()
    console.log('site-content response:', data) // TEMP - remove after verifying

    if (data['Hero Image']?.[0]?.url) heroImage.value = data['Hero Image'][0].url
    if (data['Intro Paragraph']) introParagraph.value = data['Intro Paragraph']
    if (data['Body Paragraph 1'] || data['Body Paragraph 2']) {
      bodyParagraphs.value = [data['Body Paragraph 1'], data['Body Paragraph 2']].filter(Boolean)
    }
    if (data['Cta Button Text']) ctaText.value = data['Cta Button Text']
    if (data['Social Instagram Url']) instagramUrl.value = data['Social Instagram Url']
    if (data['Social Bluesky Url']) blueskyUrl.value = data['Social Bluesky Url']
    if (data['Footer Copy']) footerCopy.value = data['Footer Copy']
  } catch (err) {
    console.error('Failed to load site content', err)
  }
}

onMounted(fetchSiteContent)
</script>

<style scoped>
.home-page {
  background: #f2ece1;
}

/* Hero */
.hero-section {
  width: 100%;
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

/* Footer */
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