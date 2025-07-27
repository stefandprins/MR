<template>
  <div v-if="analytics" class="flex-grow-1 overflow-auto" style="min-height: 0">
    <div class="analytics-row align-items-center p-1 mb-2">
      <div class="fw-medium">Average Similarity</div>
      <div class="text-muted">{{ analytics.average_similarity }}</div>
    </div>

    <!-- Genre Distribution -->
    <div class="genre-grid align-items-center p-1 mb-2">
      <div class="fw-medium" :style="{ gridRow: `span ${genre_numRows}` }">Genre Distribution</div>
      <div v-for="(block, idx) in genre_blocks" :key="idx">
        <div class="analytics-block text-muted">{{ block }}</div>
      </div>
    </div>

    <!-- Key Distribution -->
    <div class="genre-grid align-items-center p-1 mb-2">
      <div class="fw-medium" :style="{ gridRow: `span ${key_numRows}` }">Key Distribution</div>
      <div v-for="(block, idx) in key_blocks" :key="idx">
        <div class="analytics-block text-muted">{{ block }}</div>
      </div>
    </div>

    <!-- Mode Distribution -->
    <div class="genre-grid align-items-center p-1 mb-2">
      <div class="fw-medium" :style="{ gridRow: `span ${mode_numRows}` }">Mode Distribution</div>
      <div v-for="(block, idx) in mode_blocks" :key="idx">
        <div class="analytics-block text-muted">{{ block }}</div>
      </div>
    </div>

    <!-- Tempo Distribution -->
    <div class="tempo-grid align-items-center p-1 mb-2">
      <div class="fw-medium" :style="{ gridRow: `span ${tempo_numRows}` }">Tempo Distribution</div>
      <div v-for="(block, idx) in tempo_blocks" :key="idx">
        <div class="analytics-block text-muted">{{ block }}</div>
      </div>
    </div>

    <!-- Time Signature Distribution -->
    <div class="genre-grid align-items-center p-1 mb-2">
      <div class="fw-medium" :style="{ gridRow: `span ${timeSig_numRows}` }">Time Signature Distribution</div>
      <div v-for="(block, idx) in timeSig_blocks" :key="idx">
        <div class="analytics-block text-muted">{{ block }}</div>
      </div>
    </div>
  </div>
  <div class="" v-else>
    <p>No recommendation data available.</p>
  </div>
</template>

<script setup>
import { analytics } from '@/stores/trackStore.js';
import { KEY_OPTIONS } from '@/constants/musicOptions.js';
import { computed } from 'vue';

const keyLabelMap = Object.fromEntries(KEY_OPTIONS.map((opt) => [opt.value, opt.label]));

// How many columns you want for genre/key blocks (not counting aside)
const columns = 2;
const columns2 = 1;

const genre_blocks = computed(() => Object.entries(analytics.genre_distribution ?? {}).map(([genre, count]) => `${genre}: ${count}`));
const key_blocks = computed(() => Object.entries(analytics.key_distribution ?? {}).map(([key, count]) => `${keyLabelMap[key] ?? key}: ${count}`));
const mode_blocks = computed(() => Object.entries(analytics.mode_distribution ?? {}).map(([mode, count]) => `${mode}: ${count}`));
const tempo_blocks = computed(() => Object.entries(analytics.tempo_distribution ?? {}).map(([range, count]) => `${range}: ${count}`));
const timeSig_blocks = computed(() => Object.entries(analytics.time_signature_distribution ?? {}).map(([sig, count]) => `${sig}: ${count}`));

const genre_numRows = computed(() => Math.ceil(genre_blocks.value.length / columns));
const key_numRows = computed(() => Math.ceil(key_blocks.value.length / columns));
const mode_numRows = computed(() => Math.ceil(mode_blocks.value.length / columns));
const tempo_numRows = computed(() => Math.ceil(tempo_blocks.value.length / columns2));
const timeSig_numRows = computed(() => Math.ceil(timeSig_blocks.value.length / columns));
</script>
