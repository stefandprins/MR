<template>
  <div class="card shadow-sm text-bg-light p-4 h-100 d-flex flex-column">
    <h2 class="flex-shrink-0 mb-3">Playlist</h2>
    <div class="flex-grow-1 overflow-auto" style="min-height: 0">
      <table class="table table-striped table-hover mb-0">
        <thead class="table-dark">
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
