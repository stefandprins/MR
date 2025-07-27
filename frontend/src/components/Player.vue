<template>
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-music me-2"></i>
        Player
      </h5>
    </div>
    <div class="card-body flex-grow-1 overflow-auto" style="min-height: 0">
      <div v-if="state.loading" class="d-flex justify-content-center align-items-center h-100">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <div v-if="youtubeURL && !state.loading" class="h-100">
        <iframe style="width: 100%; height: 100%; border: none" :src="embedUrl" frameborder="0" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { youtubeURL, youtubeState } from '@/stores/youtubeStore.js';

const state = youtubeState;

const embedUrl = computed(() => (youtubeURL.value ? 'https://www.youtube.com/embed/' + youtubeURL.value.split('v=')[1] : ''));
</script>
