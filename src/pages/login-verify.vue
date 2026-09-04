<template>
  <v-container class="py-8" style="max-width: 480px;">
    <p v-if="loading">Signing you in...</p>
    <p v-else-if="error" class="text-error">{{ error }}</p>
    <div v-else>
      <p>You're signed in as <strong>{{ displayName }}</strong>.</p>
      <v-btn color="primary" :to="'/auction'">Go to auction</v-btn>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../api'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const displayName = ref('')

onMounted(async () => {
  const token = route.query.token as string
  if (!token) {
    error.value = 'Missing login token.'
    loading.value = false
    return
  }

  try {
    const response = await apiFetch('/api/bidder/verify-login', {
      method: 'POST',
      body: JSON.stringify({ token }),
    })
    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'This link is invalid or expired.'
      return
    }

    displayName.value = data.display_name
  } catch (err) {
    error.value = 'Something went wrong verifying your login.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>