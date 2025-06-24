<template>
  <div class="container py-4 d-flex justify-content-between gap-3">
    <div class="d-flex flex-column flex-grow-1 gap-3">
      <PreferencesForm />
      <Playlist />
    </div>
    <div>
      <RecommendationData />
    </div>
  </div>
</template>

<script>
import PreferencesForm from '@/components/PreferencesForm.vue';
import Playlist from '@/components/Playlist.vue';
import RecommendationData from '@/components/RecommendationData.vue';

export default {
  components: { PreferencesForm, Playlist, RecommendationData },
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: auto;
}
</style>
