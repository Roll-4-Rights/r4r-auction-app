<template>
  <v-container>
    <p v-if="loading">Loading item...</p>
    <p v-else-if="error">{{ error }}</p>

    <v-row v-else>
      <v-col cols="12" md="6">
        <v-img
          src="https://placehold.co/600x400?text=Item+Image"
          height="400"
          cover
        />
      </v-col>

      <v-col cols="12" md="6">
        <h1>{{ item.title }}</h1>
        <p>{{ item.description }}</p>

        <v-divider class="my-4" />

        <p><strong>Current Bid:</strong> ${{ item.current_bid }}</p>
        <p><strong>Starting Bid:</strong> ${{ item.starting_bid }}</p>

        <v-btn color="primary" class="mt-2 mb-4">Place Bid</v-btn>

        <v-divider class="my-4" />

        <h3>Shipping & Donor Info</h3>
        <p><strong>Ships from:</strong> {{ item.ships_from }}</p>
        <p><strong>Ships to:</strong> {{ item.ships_to }}</p>
        <p><strong>Shipping paid by:</strong> {{ item.shipping_paid_by }}</p>
        <p><strong>Donor:</strong> {{ item.donator_handle }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const item = ref<any>(null)
const loading = ref(true)
const error = ref('')

async function fetchItem() {
  try {
    const id = route.params.id
    const url = `${import.meta.env.VITE_API_URL}/api/auction/items/${id}`
    const response = await fetch(url)
    item.value = await response.json()
  } catch (err) {
    error.value = 'Failed to load item.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchItem()
})
</script>