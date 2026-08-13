<template>
  <v-app-bar>
    <div class="header-grid">
      <div class="header-left">
        <v-toolbar-title>Roll4Rights Auction</v-toolbar-title>
      </div>

      <div class="header-center">
        <v-btn to="/">Home</v-btn>
        <v-btn to="/auction">Auction</v-btn>
        <v-btn to="/charity">Charity Info</v-btn>
        <v-btn to="/faq">FAQ</v-btn>
        <v-btn to="/donators">Donator Information</v-btn>
      </div>

      <div class="header-right">
        <v-btn to="/account">Login</v-btn>
      </div>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
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