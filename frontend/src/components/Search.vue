<template>
  <div class="card shadow-sm text-bg-light p-3">
    <h5>Select Tracks</h5>

    <div class="d-flex flex-row gap-3">
      <div class="flex-fill position-relative">
        <input type="text" class="form-control" placeholder="Type a track name" v-model="state.query" />
        <ul class="list-group position-absolute w-100 z-3">
          <li v-for="track in state.results" :key="track.id" class="list-group-item" @click="selectTrack(track)">{{ track.label }}</li>
        </ul>
      </div>

      <button class="btn btn-primary align-self-center" :disabled="!state.selectedTrack" @click="addTrack">Add Track</button>
    </div>
  </div>
</template>

<script setup>
import { useTrackSearch } from '@/composables/useTrackSearch.js';

const { state, selectTrack, addTrack, selectedTracks } = useTrackSearch();
</script>
