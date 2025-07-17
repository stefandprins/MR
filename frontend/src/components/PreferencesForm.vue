<template>
  <div class="card shadow-sm text-bg-light p-4 h-100 d-flex flex-column">
    <form @submit.prevent="submitPreferences" class="d-flex flex-column h-100">
      <div class="d-flex flex-row flex-grow-1 justify-content-between gap-4" style="min-height: 0">
        <!-- Make Your Selection -->
        <div class="d-flex flex-column flex-fill" style="min-width: 0">
          <h2 class="flex-shrink-0 mb-3">Make Your Selection</h2>
          <div class="flex-grow-1 overflow-auto" style="min-height: 0">
            <table class="table table-striped table-hover mb-0">
              <thead class="table-dark">
                <tr>
                  <th scope="col">Title</th>
                  <th scope="col">Artist</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(track, index) in selectedTracks" :key="index">
                  <td>{{ track.title }}</td>
                  <td>{{ track.artist_name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- User Preferences -->
        <div class="d-flex flex-column flex-fill" style="min-width: 0">
          <h2 class="flex-shrink-0 mb-3">User Preferences</h2>
          <div class="flex-grow-1"></div>
        </div>
      </div>
      <button type="submit" class="flex-shrink-0 btn btn-dark w-100 mt-3" :disabled="selectedTracks.length === 0">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { selectedTracks } from '@/stores/trackStore.js';
import { useRecommend } from '@/composables/useRecommend.js';

console.log('selectedTracks loaded:', selectedTracks.value);

const { state, submitPreferences } = useRecommend();
</script>

<style scoped>
.preferences-form {
  max-width: 400px;
  margin: auto;
}

.table-container {
  min-height: 0;
}

.min-width-0 {
  min-width: 0;
}
</style>
