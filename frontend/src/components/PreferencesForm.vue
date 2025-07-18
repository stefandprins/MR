<template>
  <!-- Your Selection Card -->
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-cog me-2"></i>
        Preferences
      </h5>
    </div>
    <form @submit.prevent="submitPreferences" class="card-body d-flex flex-column h-100">
      <div class="d-flex flex-row flex-grow-1 justify-content-between gap-4" style="min-height: 0">
        <!-- Make Your Selection -->

        <!-- User Preferences -->
        <div class="d-flex flex-column flex-fill" style="min-width: 0">
          <div class="flex-grow-1"></div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { selectedTracks } from '@/stores/trackStore.js';
import { useRecommend } from '@/composables/useRecommend.js';

console.log('selectedTracks loaded:', selectedTracks.value);

const { state, submitPreferences } = useRecommend();
</script>
