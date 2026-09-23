<!-- filepath: c:\Users\gamer\Documents\Roll4Rights\r4r-auction-app\src\pages\AuctionListings.vue -->
<template>
  <div class="auction-hall">
    <header class="hall-header">
      <div>
        <h1>Live Lots</h1>
        <p class="hall-header__subtitle">Every bid updates instantly — no need to refresh.</p>
      </div>
      <span class="live-indicator"><span class="live-indicator__dot"></span>Live</span>
    </header>

    <div class="filter-row" role="tablist" aria-label="Filter by category">
      <button
        v-for="category in categories"
        :key="category"
        class="filter-pill"
        :class="{ 'filter-pill--active': selectedCategory === category }"
        @click="selectedCategory = category"
      >
        {{ category }}
      </button>
    </div>

    <p v-if="loading" class="state-message">Loading the auction…</p>
    <p v-else-if="error" class="state-message state-message--error">{{ error }}</p>

    <div v-else class="hall-layout">
      <section class="lot-grid">
        <p v-if="!filteredItems.length" class="state-message">No lots in this category yet.</p>

        <article
          v-for="item in filteredItems"
          :key="item.id"
          class="lot-card"
          :class="{ 'lot-card--ending': isEndingSoon(item), 'lot-card--ended': isEnded(item) }"
        >
          <router-link :to="`/auction/${item.id}`" class="lot-card__link">
            <div class="lot-card__image">
              <img v-if="item.photos && item.photos[0]" :src="item.photos[0]" :alt="item.item_name" loading="lazy" />
              <div v-else class="lot-card__image-placeholder">No photo yet</div>
              <span v-if="item.category" class="lot-card__category">{{ item.category }}</span>
            </div>

            <div class="lot-card__body">
              <h2 class="lot-card__name">{{ item.item_name }}</h2>
              <p v-if="item.donator_name" class="lot-card__donator">Donated by {{ item.donator_name }}</p>

              <div class="lot-card__bid-row">
                <div class="lot-card__bid-block">
                  <span class="lot-card__bid-label">Current bid</span>
                  <span class="lot-card__bid-amount">${{ item.current_bid ?? item.starting_bid }}</span>
                </div>
                <span class="lot-card__time" :class="{ 'lot-card__time--urgent': isEndingSoon(item) }">
                  {{ formatTimeLeft(item) }}
                </span>
              </div>

              <p v-if="item.can_bid === false" class="lot-card__ship-warning">Can't ship to your country</p>
              <p v-else-if="item.can_bid === null" class="lot-card__ship-warning lot-card__ship-warning--muted">
                Sign in to bid
              </p>
            </div>
          </router-link>
        </article>
      </section>

      <aside class="leaderboard">
        <h2 class="leaderboard__title">Top Bidders</h2>
        <p v-if="!leaderboard.length" class="leaderboard__empty">No bids yet — be the first.</p>
        <ol v-else class="leaderboard__list">
          <li v-for="(bidder, index) in leaderboard" :key="bidder.bidder_id" class="leaderboard__row">
            <span class="leaderboard__rank">{{ index + 1 }}</span>
            <span class="leaderboard__name">{{ bidder.display_name }}</span>
            <span class="leaderboard__total">${{ bidder.total.toFixed(2) }}</span>
          </li>
        </ol>
      </aside>
    </div>
  </div>
</template>






<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { apiFetch } from '../api'
import { socket } from '../socket'

interface AuctionItem {
  id: number
  item_name: string
  description: string
  category: string
  donator_name: string
  photos: any
  starting_bid: number
  current_bid: number
  highest_bidder: string | null
  auction_end_time: string | null
  shipping_from: string
  can_bid: boolean | null
}

interface LeaderboardEntry {
  bidder_id: number
  display_name: string
  total: number
  items_winning: number
}

const items = ref<AuctionItem[]>([])
const leaderboard = ref<LeaderboardEntry[]>([])
const loading = ref(true)
const error = ref('')
const selectedCategory = ref('All')
const now = ref(Date.now())

let tickTimer: ReturnType<typeof setInterval> | undefined

async function loadItems() {
  const res = await apiFetch('/api/auction/items?limit=1000')
  if (!res.ok) throw new Error('items')
  const data = await res.json()
  items.value = data.list
}

async function loadLeaderboard() {
  const res = await apiFetch('/api/auction/leaderboard?limit=8')
  if (!res.ok) throw new Error('leaderboard')
  leaderboard.value = await res.json()
}

async function loadAll() {
  loading.value = true
  error.value = ''
  try {
    await Promise.all([loadItems(), loadLeaderboard()])
  } catch (err) {
    error.value = 'Could not load the auction right now.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// When a bid comes in anywhere on the site, the server pushes the
// updated item — we just swap it into place, no refetch needed.
function handleItemUpdated(updated: AuctionItem) {
  const index = items.value.findIndex((i) => i.id === updated.id)
  if (index !== -1) items.value[index] = updated
}

function handleLeaderboardUpdated(updated: LeaderboardEntry[]) {
  leaderboard.value = updated
}

onMounted(() => {
  loadAll()
  socket.on('item_updated', handleItemUpdated)
  socket.on('leaderboard_updated', handleLeaderboardUpdated)
  // Ticks once a second so the "time left" labels count down live,
  // not just whenever something else happens to re-render the page.
  tickTimer = setInterval(() => { now.value = Date.now() }, 1000)
})

onUnmounted(() => {
  // Without this, leaving and coming back to this page would stack up
  // a second listener, and you'd get every update applied twice.
  socket.off('item_updated', handleItemUpdated)
  socket.off('leaderboard_updated', handleLeaderboardUpdated)
  if (tickTimer) clearInterval(tickTimer)
})

const categories = computed(() => {
  const set = new Set(items.value.map((i) => i.category).filter(Boolean))
  return ['All', ...Array.from(set).sort()]
})

const filteredItems = computed(() => {
  if (selectedCategory.value === 'All') return items.value
  return items.value.filter((i) => i.category === selectedCategory.value)
})

const ANTI_SNIPE_MS = 4 * 60 * 1000 // keep in sync with the backend's ANTI_SNIPE_WINDOW

function msRemaining(item: AuctionItem) {
  if (!item.auction_end_time) return null
  return new Date(item.auction_end_time).getTime() - now.value
}

function isEndingSoon(item: AuctionItem) {
  const remaining = msRemaining(item)
  return remaining !== null && remaining > 0 && remaining <= ANTI_SNIPE_MS
}

function isEnded(item: AuctionItem) {
  const remaining = msRemaining(item)
  return remaining !== null && remaining <= 0
}

function formatTimeLeft(item: AuctionItem) {
  const remaining = msRemaining(item)
  if (remaining === null) return ''
  if (remaining <= 0) return 'Ended'

  const totalSeconds = Math.floor(remaining / 1000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60

  if (hours > 0) return `${hours}h ${minutes}m left`
  if (minutes > 0) return `${minutes}m ${seconds}s left`
  return `${seconds}s left`
}
</script>





<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Spectral:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

.auction-hall {
  --teal-900: #103948;
  --teal-950: #0a262f;
  --parchment: #f3e8d2;
  --parchment-dim: #eadfc4;
  --gold: #c08a28;
  --brick: #9c3b2e;
  --ink: #1d2b2e;

  font-family: 'Inter', sans-serif;
  color: var(--ink);
  background: var(--parchment);
  min-height: 100vh;
  padding: 2.5rem clamp(1rem, 4vw, 3rem) 4rem;
}

.hall-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(16, 57, 72, 0.25);
  margin-bottom: 1.5rem;
}

.hall-header h1 {
  font-family: 'Spectral', serif;
  font-weight: 700;
  font-size: clamp(2rem, 4vw, 2.75rem);
  color: var(--teal-950);
  margin: 0;
}

.hall-header__subtitle {
  margin: 0.35rem 0 0;
  color: rgba(29, 43, 46, 0.65);
  font-size: 0.95rem;
}

.live-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--teal-900);
  padding: 0.35rem 0.75rem;
  border: 1px solid rgba(16, 57, 72, 0.3);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.4);
}

.live-indicator__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brick);
  animation: pulse 1.8s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.75); }
}

@media (prefers-reduced-motion: reduce) {
  .live-indicator__dot { animation: none; }
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 2rem;
}

.filter-pill {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  padding: 0.45rem 1.1rem;
  border-radius: 999px;
  border: 1px solid rgba(16, 57, 72, 0.35);
  background: transparent;
  color: var(--teal-900);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.filter-pill:hover {
  background: rgba(16, 57, 72, 0.08);
}

.filter-pill--active {
  background: var(--teal-900);
  border-color: var(--teal-900);
  color: var(--parchment);
}

.state-message {
  color: rgba(29, 43, 46, 0.65);
  padding: 2rem 0;
}

.state-message--error {
  color: var(--brick);
}

.hall-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2.5rem;
  align-items: start;
}

.lot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.lot-card {
  background: #fff;
  border: 1px solid rgba(16, 57, 72, 0.15);
  border-radius: 6px;
  overflow: hidden;
  transition: border-color 0.15s ease, transform 0.15s ease;
}

.lot-card:hover {
  border-color: var(--teal-900);
  transform: translateY(-2px);
}

.lot-card--ending {
  border-color: var(--brick);
}

.lot-card--ended {
  opacity: 0.55;
}

.lot-card__link {
  display: block;
  color: inherit;
  text-decoration: none;
}

.lot-card__image {
  position: relative;
  aspect-ratio: 4 / 3;
  background: var(--parchment-dim);
}

.lot-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.lot-card__image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(16, 57, 72, 0.4);
  font-size: 0.85rem;
}

.lot-card__category {
  position: absolute;
  top: 0.6rem;
  left: 0.6rem;
  background: rgba(10, 38, 47, 0.85);
  color: var(--parchment);
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
}

.lot-card__body {
  padding: 1rem 1.1rem 1.2rem;
}

.lot-card__name {
  font-family: 'Spectral', serif;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.3rem;
  color: var(--teal-950);
}

.lot-card__donator {
  font-size: 0.82rem;
  color: rgba(29, 43, 46, 0.6);
  margin: 0 0 0.9rem;
}

.lot-card__bid-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.5rem;
}

.lot-card__bid-block {
  display: flex;
  flex-direction: column;
}

.lot-card__bid-label {
  font-size: 0.72rem;
  color: rgba(29, 43, 46, 0.55);
}

.lot-card__bid-amount {
  font-family: 'Spectral', serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--gold);
  line-height: 1.1;
}

.lot-card__time {
  font-size: 0.8rem;
  color: rgba(29, 43, 46, 0.6);
  white-space: nowrap;
}

.lot-card__time--urgent {
  color: var(--brick);
  font-weight: 600;
}

.lot-card__ship-warning {
  margin: 0.7rem 0 0;
  font-size: 0.78rem;
  color: var(--brick);
}

.lot-card__ship-warning--muted {
  color: rgba(29, 43, 46, 0.55);
}

.leaderboard {
  position: sticky;
  top: 1.5rem;
  background: var(--teal-950);
  color: var(--parchment);
  border-radius: 6px;
  padding: 1.4rem 1.3rem;
}

.leaderboard__title {
  font-family: 'Spectral', serif;
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0 0 1rem;
}

.leaderboard__empty {
  font-size: 0.85rem;
  color: rgba(243, 232, 210, 0.6);
}

.leaderboard__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.leaderboard__row {
  display: grid;
  grid-template-columns: 1.5rem 1fr auto;
  align-items: center;
  gap: 0.6rem;
  padding-bottom: 0.65rem;
  border-bottom: 1px solid rgba(243, 232, 210, 0.12);
}

.leaderboard__row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.leaderboard__rank {
  font-family: 'Spectral', serif;
  font-weight: 600;
  color: var(--gold);
  font-size: 0.95rem;
}

.leaderboard__name {
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.leaderboard__total {
  font-family: 'Spectral', serif;
  font-weight: 600;
  font-size: 0.92rem;
}

@media (max-width: 860px) {
  .hall-layout {
    grid-template-columns: 1fr;
  }

  .leaderboard {
    position: static;
    order: -1;
  }
}
</style>