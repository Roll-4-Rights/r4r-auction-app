<template>
  <v-container class="py-8" style="max-width: 480px;">
    <h1 class="mb-4">Sign in to bid</h1>

    <p v-if="sent" class="text-success">
      Check your email for a sign-in link. It expires in 15 minutes.
    </p>

    <v-form v-else @submit.prevent="submit">
      <v-text-field
        v-model="email"
        label="Email"
        type="email"
        required
      />

      <v-select
        v-if="showCountry"
        v-model="country"
        :items="countries"
        label="Country"
        class="mt-2"
        required
      />

      <p v-if="error" class="text-error mb-2">{{ error }}</p>

      <v-btn type="submit" color="primary" :loading="loading" block>
        Send sign-in link
      </v-btn>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { apiFetch } from '../api'

const email = ref('')
const country = ref('')
const showCountry = ref(false) // shown after a first attempt tells us they're new
const loading = ref(false)
const error = ref('')
const sent = ref(false)

const countries = ['United States', 'Canada', 'United Kingdom', 'Australia'] // TODO: replace with your real supported list

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const response = await apiFetch('/api/bidder/request-login', {
      method: 'POST',
      body: JSON.stringify({ email: email.value, country: country.value }),
    })
    const data = await response.json()

    if (!response.ok) {
      if (data.error === 'Country is required for first-time bidders') {
        showCountry.value = true
        error.value = 'Looks like this is your first time — please select your country too.'
      } else {
        error.value = data.error || 'Something went wrong.'
      }
      return
    }

    sent.value = true
  } catch (err) {
    error.value = 'Failed to send login link.'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>