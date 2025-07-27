<template>
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-play me-2"></i>
        Your Playlist
      </h5>
    </div>

    <div class="card-body flex-grow-1 overflow-auto mb-3" style="min-height: 0">
      <div v-if="state.loading" class="d-flex justify-content-center align-items-center h-100">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <div v-else>
        <div class="playlist-row align-items-center p-1 mb-2">
          <div class="text-start">
            <div class="fw-medium">Title</div>
            <div class="text-muted">Artist</div>
          </div>
          <div>
            <div class="fw-medium">Duration</div>
            <div class="text-muted">Genre</div>
          </div>
          <div class="text-muted">bpm</div>
          <div class="text-muted">key</div>
          <div class="text-muted">Mode</div>
          <div class="text-muted">Time Signature</div>
          <div class="text-muted">URL</div>
        </div>
        <div v-for="(track, index) in recommendations" :key="index" class="playlist-row align-items-center p-1 mb-2">
          <div class="text-start">
            <div class="fw-medium">{{ track.title }}</div>
            <div class="text-muted">{{ track.artist_name }}</div>
          </div>
          <div>
            <div class="fw-medium">({{ formatDuration(track.duration) }})</div>
            <div class="text-muted">{{ track.genre }}</div>
          </div>
          <div class="text-muted">{{ track.tempo }}</div>
          <div class="text-muted">{{ track.key }}</div>
          <div class="text-muted">{{ track.mode }}</div>
          <div class="text-muted">{{ track.time_signature }}</div>
          <div>
            <button class="btn btn-primary btn-sm" @click="getVideoURL(track.title, track.artist_name)"><i class="fas fa-play me-2"></i>Play</button>
          </div>
        </div>
      </div>

      <!-- <table v-else class="table table-striped table-hover playlist-table mb-0">
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
            <td>
              {{ track.title }}
            </td>
            <td>{{ track.artist_name }}</td>
            <td>{{ track.genre }}</td>
            <td>
              <button class="btn btn-primary btn-sm" @click="getVideoURL(track.title, track.artist_name)"><i class="fas fa-play me-2"></i>Play</button>
            </td>
          </tr>
        </tbody>
      </table> -->
    </div>
  </div>
</template>

<script setup>
import { recommendations, recommendState } from '@/stores/trackStore.js';
import { useRecommend } from '@/composables/useRecommend.js';
import { useVideoURL } from '@/composables/useVideoURL.js';

const { getVideoURL } = useVideoURL();
const state = recommendState;

function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}
</script>
