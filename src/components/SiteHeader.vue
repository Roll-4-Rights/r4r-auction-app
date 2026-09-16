<template>
  <nav class="site-nav">
    <div class="nav-top-row">
      <button class="nav-icon-btn" aria-label="Search">
        <v-icon>mdi-magnify</v-icon>
      </button>
      <router-link to="/" class="nav-title">Roll4Rights</router-link>
      <div class="nav-right">
        <router-link to="/login" class="nav-icon-btn" aria-label="Account">
          <v-icon>mdi-account-outline</v-icon>
        </router-link>
        <!-- TODO: replace with real donate/logo badge asset -->
        <v-avatar size="28" color="secondary" class="nav-badge">
          <v-icon size="18">mdi-heart</v-icon>
        </v-avatar>
      </div>
    </div>
    <div class="nav-bottom-row">
      <router-link
        v-for="link in navLinks"
        :key="link.label"
        :to="link.to"
        class="nav-link"
        exact-active-class="nav-link-active"
      >
        {{ link.label }}
      </router-link>
    </div>
  </nav>
</template>

<script setup lang="ts">
// TODO: keep this list in sync with src/router/index.ts
const navLinks = [
  { label: 'Home', to: '/' },
  { label: 'Auction', to: '/auction' },
  { label: 'Current Campaign', to: '/current-campaign' },
  { label: 'Donators', to: '/donators' },
  { label: 'Education & Resources', to: '/education' },
  { label: 'Charity Info', to: '/charity' },
]
</script>

<style scoped>
.site-nav {
  background: #0f2b36;
  color: #fff;
}
.nav-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px 4px;
}
.nav-title {
  font-family: 'Georgia', serif;
  font-size: 1.3rem;
  letter-spacing: 0.02em;
  color: #fff;
  text-decoration: none;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.nav-icon-btn {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  display: inline-flex;
}
.nav-bottom-row {
  display: flex;
  justify-content: center;
  gap: 28px;
  flex-wrap: wrap;
  padding: 0 16px 12px;
  font-size: 0.8rem;
}
.nav-link {
  color: #fff;
  text-decoration: none;
  opacity: 0.9;
}
.nav-link:hover {
  opacity: 1;
}
.nav-link-active {
  text-decoration: underline;
  opacity: 1;
}
</style>