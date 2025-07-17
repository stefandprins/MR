<template>
  <div class="container py-4 d-flex justify-content-between gap-3" style="height: calc(100vh - 56px)">
    <div class="d-flex flex-column flex-grow-1 gap-3" style="min-width: 0; height: 100%">
      <Search class="flex-shrink-1" />
      <PreferencesForm class="flex-grow-1" style="min-height: 0" />
      <Playlist class="flex-grow-1" style="min-height: 0" />
    </div>
    <div class="flex-shrink-1">
      <RecommendationData />
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search.vue';
import PreferencesForm from '@/components/PreferencesForm.vue';
import Playlist from '@/components/Playlist.vue';
import RecommendationData from '@/components/RecommendationData.vue';

export default {
  components: { Search, PreferencesForm, Playlist, RecommendationData },
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: auto;
}
</style>
