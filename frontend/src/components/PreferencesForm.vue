<template>
  <div class="mb-2">
    <multiselect v-model="preferences.genre" :options="GENRE_OPTIONS" :multiple="true" :close-on-select="false" placeholder="Select genre(s)" />
  </div>
  <div class="mb-2">
    <multiselect v-model="preferences.key" :options="KEY_OPTIONS" :multiple="true" :close-on-select="false" placeholder="Select key(s)" label="label" track-by="value" />
  </div>
  <div class="mb-2">
    <multiselect v-model="preferences.time_signature" :options="TIME_SIGNATURE_OPTIONS" :multiple="true" :close-on-select="false" placeholder="Select time signature(s)" />
  </div>

  <div class="d-flex align-items-center mb-2">
    <label class="form-label me-3 mb-0" style="min-width: 70px">Year</label>
    <vue-slider v-model="yearRange" :min="SLIDER_BOUNDS.year.min" :max="SLIDER_BOUNDS.year.max" :interval="1" class="vue-slider-custom flex-fill" />
  </div>
  <div class="d-flex align-items-center mb-2">
    <label class="form-label me-3 mb-0" style="min-width: 70px">Tempo</label>
    <vue-slider v-model="tempoRange" :min="SLIDER_BOUNDS.tempo.min" :max="SLIDER_BOUNDS.tempo.max" :interval="1" class="vue-slider-custom flex-fill" />
  </div>
  <div class="d-flex align-items-center mb-2">
    <label class="form-label me-3 mb-0" style="min-width: 70px">Duration</label>
    <vue-slider v-model="durationRange" :min="SLIDER_BOUNDS.duration.min" :max="SLIDER_BOUNDS.duration.max" :interval="1" class="vue-slider-custom flex-fill" />
  </div>
  <div class="d-flex align-items-center">
    <label class="form-label me-1 mb-0" style="min-width: 70px">Mode</label>
    <div class="d-flex">
      <div class="form-check me-2">
        <input class="form-check-input" type="radio" :value="null" v-model="preferences.mode" id="mode-any" />
        <label class="form-check-label" for="mode-any">Any</label>
      </div>
      <div class="form-check me-2">
        <input class="form-check-input" type="radio" :value="0" v-model="preferences.mode" id="mode-minor" />
        <label class="form-check-label" for="mode-minor">Minor</label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" :value="1" v-model="preferences.mode" id="mode-major" />
        <label class="form-check-label" for="mode-major">Major</label>
      </div>
    </div>
  </div>
</template>

<script setup>
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.css';
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/antd.css';
import { usePreferences } from '@/composables/usePreferences.js';
import { preferences } from '@/stores/preferencesStore.js';
import { GENRE_OPTIONS, KEY_OPTIONS, TIME_SIGNATURE_OPTIONS, SLIDER_BOUNDS } from '@/constants/musicOptions.js';

const { yearRange, tempoRange, durationRange } = usePreferences();
</script>
