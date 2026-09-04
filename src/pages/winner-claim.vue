<template>
  <v-container class="py-8" style="max-width: 560px;">
    <p v-if="loading">Loading...</p>
    <p v-else-if="loadError" class="text-error">{{ loadError }}</p>

    <div v-else-if="!submitted">
      <h1 class="mb-2">Congratulations, {{ claim.display_name }}!</h1>
      <p class="mb-4">
        You won <strong>{{ claim.item_name }}</strong> for
        <strong>${{ claim.amount }}</strong>.
      </p>
      <p class="mb-4">
        Please complete your donation to the charity, then upload a screenshot
        or receipt below as proof.
      </p>

      <v-form @submit.prevent="submit">
        <v-file-input
          v-model="proofFile"
          label="Proof of donation"
          accept="image/*,application/pdf"
          required
        />

        <p v-if="submitError" class="text-error mb-2">{{ submitError }}</p>

        <v-btn type="submit" color="primary" :loading="submitting" block>
          Submit for review
        </v-btn>
      </v-form>
    </div>

    <p v-else class="text-success">
      Thank you! Your submission has been sent to our team for review.
    </p>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const BASE_URL = import.meta.env.VITE_API_URL
const route = useRoute()
const token = route.params.token as string

const loading = ref(true)
const loadError = ref('')
const claim = ref<any>({})

const proofFile = ref<File[]>([])
const submitting = ref(false)
const submitError = ref('')
const submitted = ref(false)

onMounted(async () => {
  try {
    const response = await fetch(`${BASE_URL}/api/winner-claim/${token}`)
    const data = await response.json()
    if (!response.ok) {
      loadError.value = data.error || 'This link is invalid or expired.'
      return
    }
    claim.value = data
  } catch (err) {
    loadError.value = 'Something went wrong loading your claim.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

async function submit() {
  if (!proofFile.value?.length) {
    submitError.value = 'Please attach a proof file.'
    return
  }

  submitting.value = true
  submitError.value = ''
  try {
    const formData = new FormData()
    formData.append('proof', proofFile.value[0])

    // Note: no apiFetch helper here — file uploads must NOT set
    // Content-Type manually, the browser sets the multipart boundary itself.
    const response = await fetch(`${BASE_URL}/api/winner-claim/${token}`, {
      method: 'POST',
      body: formData,
    })
    const data = await response.json()

    if (!response.ok) {
      submitError.value = data.error || 'Submission failed.'
      return
    }

    submitted.value = true
  } catch (err) {
    submitError.value = 'Something went wrong submitting your proof.'
    console.error(err)
  } finally {
    submitting.value = false
  }
}
</script>