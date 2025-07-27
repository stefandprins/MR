<template>
  <!-- Your Selection Card -->
  <div class="card custom-card shadow-sm text-bg-light d-flex flex-column">
    <!-- Card Title -->
    <!--<div class="text-start">-->
    <div class="text-start">
      <ul class="d-flex list-unstyled" role="tablist">
        <li class="flex-grow-1" role="presentation">
          <button :class="[activeTab === 'preferences' ? 'card-header' : 'card-header1', 'w-100']" @click="activeTab = 'preferences'">
            <i class="fas fa-cog me-2"></i>
            Preferences
          </button>
        </li>
        <li class="flex-grow-1" role="presentation">
          <button :class="[activeTab === 'analytics' ? 'card-header' : 'card-header1', 'w-100']" @click="activeTab = 'analytics'">
            <i class="fas fa-chart-bar me-2"></i>
            Analytics
          </button>
        </li>
      </ul>
    </div>

    <!--</div>-->

    <div class="card-body d-flex flex-column h-100" style="min-width: 0; min-height: 0">
      <div v-if="activeTab === 'preferences'">
        <!-- Preferences content goes here -->
        <PreferencesForm class="flex-grow-1 h-100" style="min-height: 0" />
      </div>
      <div v-if="activeTab === 'analytics'">
        <!-- Analytics content goes here -->
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import PreferencesForm from '@/components/PreferencesForm.vue';
import Analytics from '@/components/Analytics.vue';

const activeTab = ref('preferences');
</script>
