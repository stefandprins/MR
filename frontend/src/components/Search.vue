<template>
  <!-- Search Tracks Card -->
  <div class="card custom-card shadow-sm text-bg-light">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-search me-2"></i>
        Search Tracks
      </h5>
    </div>

    <div class="card-body d-flex flex-row gap-3">
      <div class="flex-fill position-relative">
        <div class="search-box">
          <i class="fas fa-search search-icon"></i>
          <input type="text" class="form-control" placeholder="Type a track name" v-model="state.query" />
          <ul class="list-group position-absolute w-100 z-3">
            <li v-for="track in state.results" :key="track.id" class="list-group-item" @click="selectTrack(track)">{{ track.label }}</li>
          </ul>
        </div>
      </div>

      <button class="btn btn-dark align-self-center" :disabled="!state.selectedTrack" @click="addTrack">Add Track</button>
    </div>
  </div>
</template>

<script setup>
import { useTrackSearch } from '@/composables/useTrackSearch.js';

const { state, selectTrack, addTrack, selectedTracks } = useTrackSearch();
</script>
