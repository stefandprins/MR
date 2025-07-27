import { reactive } from 'vue';
import { SLIDER_BOUNDS } from '@/constants/musicOptions.js';

export const preferences = reactive({
  genre: [],
  min_year: SLIDER_BOUNDS.year.min,
  max_year: SLIDER_BOUNDS.year.max,
  min_tempo: SLIDER_BOUNDS.tempo.min,
  max_tempo: SLIDER_BOUNDS.tempo.max,
  min_duration: SLIDER_BOUNDS.duration.min,
  max_duration: SLIDER_BOUNDS.duration.max,
  key: [],
  mode: null,
  time_signature: [],
});
