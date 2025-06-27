<template>
  <div class="card shadow-sm text-bg-light p-4">
    <form @submit.prevent="submitPreferences" class="d-flex flex-column">
      <div class="d-flex flex-row justify-content-between flex-wrap gap-4">
        <!-- Make Your Selection -->
        <div class="d-flex flex-column flex-fill">
          <h2>Make Your Selection</h2>
          <ul>
            <li v-for="(track, index) in selectedTracks" :key="index">{{ track.title }} ({{ track.artist_name }})</li>
          </ul>
        </div>

        <!-- User Preferences -->
        <div class="d-flex flex-column flex-fill">
          <h2>User Preferences</h2>
          <label for="genre">Genre:</label>
          <input v-model="preferences.genre" id="genre" type="text" class="form-control mb-2" />

          <label for="mood">Mood:</label>
          <input v-model="preferences.mood" id="mood" type="text" class="form-control mb-3" />
        </div>
      </div>
      <button type="submit" class="btn btn-dark align-self-start w-100">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { selectedTracks } from '@/stores/trackStore.js';

const preferences = reactive({
  genre: '',
  mood: '',
});

const submitPreferences = () => {
  console.log('Selected:', selectedTracks.value);
  console.log('Prefs:', preferences);
};
</script>

<style scoped>
.preferences-form {
  max-width: 400px;
  margin: auto;
}
</style>
