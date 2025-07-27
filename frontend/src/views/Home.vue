<template>
  <div class="layout-container d-flex gap-3">
    <!-- Left Column -->
    <div class="left-column d-flex flex-column gap-3">
      <Search class="flex-shrink-1" />
      <Player class="flex-grow-1 h-100" style="min-height: 0" />
      <Playlist class="flex-grow-1 h-100" style="min-height: 0" />
    </div>
    <div class="right-column d-flex flex-column gap-3">
      <div class="flex-grow-1 h-100 d-flex flex-column gap-3" style="min-height: 0">
        <SelectionList class="flex-grow-1 h-100" style="min-height: 0" />
        <TabCard class="flex-grow-1 h-100" style="min-height: 0" />
        <!--<PreferencesForm class="flex-grow-1 h-100" style="min-height: 0" />-->

        <!--<Analytics class="flex-shrink-1" />-->
      </div>
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search.vue';
import SelectionList from '@/components/SelectionList.vue';
import PreferencesForm from '@/components/PreferencesForm.vue';
import TabCard from '@/components/TabCard.vue';
import Player from '@/components/Player.vue';
import Playlist from '@/components/Playlist.vue';
import Analytics from '@/components/Analytics.vue';

export default {
  components: { Search, SelectionList, PreferencesForm, TabCard, Player, Playlist, Analytics },
};
</script>

<style>
.container1 {
  max-width: 1200px;
  margin: auto;
}
</style>
