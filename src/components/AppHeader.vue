<template>
  <v-app-bar color="primary" style="position: relative;">
    <div class="header-grid">
      <div class="header-left">
        <v-btn icon="mdi-magnify" variant="text" class="text-white" @click="onSearchClick" />
      </div>

      <div class="header-center">
        <v-btn to="/" variant="text" class="text-white">Home</v-btn>
        <v-btn to="/auction" variant="text" class="text-white">Auction</v-btn>
        <v-btn to="/charity" variant="text" class="text-white">Charity Info</v-btn>
        <v-btn to="/donators" variant="text" class="text-white">Donators</v-btn>
        <v-btn to="/education" variant="text" class="text-white">Education & Resources</v-btn>
      </div>

      <div class="header-right">
        <v-btn to="/account" icon="mdi-account" variant="text" class="text-white" />
        <v-btn href="#" variant="tonal" color="white" class="text-primary">Donate</v-btn>
      </div>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function onSearchClick() {
  router.push('/auction')
}
</script>

<style scoped>
.header-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  width: 100%;
  padding: 0 var(--header-side-padding, 32px);
}

.header-left {
  justify-self: start;
}

.header-center {
  justify-self: center;
  display: flex;
  gap: var(--nav-gap, 8px);
}

.header-right {
  justify-self: end;
  padding-right: var(--login-padding-right, 16px);
}
</style>