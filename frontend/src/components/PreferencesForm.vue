<template>
  <div class="card shadow-sm text-bg-light p-4 min-height-card">
    <form @submit.prevent="submitPreferences" class="d-flex flex-column h-100">
      <div class="d-flex flex-row justify-content-between flex-wrap gap-4 flex-grow-1">
        <!-- Make Your Selection -->
        <div class="d-flex flex-column flex-fill">
          <h2>Make Your Selection</h2>
          <table class="table table-striped table-hover">
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

        <!-- User Preferences -->
        <div class="d-flex flex-column flex-fill">
          <h2>User Preferences</h2>
        </div>
      </div>
      <button type="submit" class="btn btn-dark align-self-start w-100" :disabled="selectedTracks.length === 0">Submit</button>
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
</style>
