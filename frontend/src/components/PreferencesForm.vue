<template>
  <div class="card shadow-sm text-bg-light p-4">
    <form @submit.prevent="submitPreferences" class="d-flex flex-column">
      <div class="d-flex flex-row justify-content-between flex-wrap gap-4">
        <!-- Make Your Selection -->
        <div class="d-flex flex-column flex-fill">
          <h2>Make Your Selection</h2>
          <label for="track1">Track 1:</label>
          <input v-model="preferences.track1" id="track1" type="text" class="form-control mb-2" />

          <label for="track2">Track 2:</label>
          <input v-model="preferences.track2" id="track2" type="text" class="form-control" />

          <label for="track3">Track 3:</label>
          <input v-model="preferences.track3" id="track3" type="text" class="form-control" />

          <label for="track4">Track 4:</label>
          <input v-model="preferences.track4" id="track4" type="text" class="form-control" />

          <label for="track5">Track 5:</label>
          <input v-model="preferences.track5" id="track5" type="text" class="form-control" />
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

<script>
export default {
  name: 'PreferencesForm',
  data() {
    return {
      preferences: {
        genre: '',
        mood: '',
      },
    };
  },
  methods: {
    submitPreferences() {
      this.$emit('submit', this.preferences);
    },
  },
};
</script>

<style scoped>
.preferences-form {
  max-width: 400px;
  margin: auto;
}
</style>
