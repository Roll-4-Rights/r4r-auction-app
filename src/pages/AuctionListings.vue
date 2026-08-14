<!-- filepath: c:\Users\gamer\Documents\Roll4Rights\r4r-auction-app\src\pages\AuctionListings.vue -->
<template>
<v-container class="py-8">
    <h1 class="mb-6">Auction Items</h1>

    <p v-if="loading">Loading items...</p>
    <p v-else-if="error">{{ error }}</p>

    <v-row v-else>
      <v-col
        v-for="item in items"
        :key="item.Id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card :to="`/auction/${item.Id}`" elevation="2" class="pa-2">
          <v-img
            src="https://placehold.co/400x300?text=Item+Image"
            height="200"
            cover
            class="rounded"
          />
          <v-card-text class="text-center">
            <div class="text-h6" style="color: #103948;">
              ${{ item.current_bid }}
            </div>
            <div class="text-caption text-medium-emphasis">
              Current Bid
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-pagination
      v-if="!loading && !error"
      v-model="currentPage"
      :length="totalPages"
      class="mt-6"
    />
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

const items = ref<any[]>([])
const loading = ref(true)
const error = ref('')

const currentPage = ref(1)
const pageSize = 12
const totalRows = ref(0)

const totalPages = computed(() =>
  Math.ceil(totalRows.value / pageSize)
)

async function fetchItems() {
  loading.value = true
  try {
    const offset = (currentPage.value - 1) * pageSize
    const url = `${import.meta.env.VITE_API_URL}/api/auction/items?limit=${pageSize}&offset=${offset}`
    const response = await fetch(url)
    const data = await response.json()

    items.value = data.list
    totalRows.value = data.pageInfo.totalRows
  } catch (err) {
    error.value = 'Failed to load items.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

watch(currentPage, () => {
  fetchItems()
})

onMounted(() => {
  fetchItems()
})
</script>
