<template>
  <v-container fluid class="pa-0">
    <div class="hero-section">
      <v-img
        src="https://placehold.co/1600x500?text=Campaign+Artwork"
        height="500"
        cover
        class="hero-image"
      >
        <div class="hero-overlay">
          <div class="hero-title-box">
            {{ campaignTitle }}
          </div>
        </div>
      </v-img>
    </div>

    <v-container class="text-center py-8">
      <h1 class="text-h4" style="color: #103948;">
        Welcome to the {{ campaignName }} Charity Auction by Roll4Rights!
      </h1>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">



</script>

<style scoped>
.hero-section {
  position: relative;
  width: 100%;
}

.hero-overlay {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
}

.hero-title-box {
  background: white;
  padding: 12px 24px;
  font-size: 1.2rem;
  font-style: italic;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>