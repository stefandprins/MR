<template>
  <!-- Your Selection Card -->
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column h-100">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-list me-2"></i>
        Your Selection
      </h5>
    </div>

    <!-- Make Your Selection -->
    <div class="card-body d-flex flex-column h-100" style="min-width: 0; min-height: 0">
      <!-- Scrollable list -->
      <div class="flex-grow-1 overflow-auto" style="min-height: 0">
        <div v-for="(track, index) in selectedTracks" :key="track.id" class="selected-track p-1 mb-2">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <div class="fw-medium">{{ track.title }}</div>
              <small class="text-muted">{{ track.artist_name }}</small>
            </div>
            <button class="btn btn-sm btn-outline-danger" @click="removeTrack(track.id)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
      <button type="submit" class="flex-shrink-0 btn btn-dark w-100 mt-3" :disabled="selectedTracks.length === 0" @click="submitPreferences">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { selectedTracks } from '@/stores/trackStore.js';
import { useRecommend } from '@/composables/useRecommend.js';
import { useTrackSearch } from '@/composables/useTrackSearch.js';

console.log('selectedTracks loaded:', selectedTracks.value);

const { state, submitPreferences } = useRecommend();
const { removeTrack } = useTrackSearch();
</script>
