<template>
  <div class="card shadow-sm text-bg-light p-4">
    <h2>Playlist</h2>
    <ul>
      <li v-for="song in songs" :key="song.id">{{ song.title }} – {{ song.artist }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Playlist',
  props: {
    songs: {
      type: Array,
      default: () => [],
    },
  },
};
</script>

<style scoped>
.playlist {
  margin-top: 20px;
}
</style>
