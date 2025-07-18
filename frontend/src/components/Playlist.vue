<template>
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-play me-2"></i>
        Your Playlist
      </h5>
    </div>
    <div class="card-body flex-grow-1 overflow-auto" style="min-height: 0">
      <table class="table table-striped table-hover playlist-table mb-0">
        <thead class="">
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Artist</th>
            <th scope="col">Genre</th>
            <th scope="col">URL</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(track, index) in recommendations" :key="index">
            <td>{{ track.title }}</td>
            <td>{{ track.artist_name }}</td>
            <td>{{ track.genre }}</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { recommendations } from '@/stores/trackStore.js';

console.log('Playlist loaded:', recommendations.value);
</script>
