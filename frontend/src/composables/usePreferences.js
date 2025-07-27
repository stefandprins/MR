import { computed } from 'vue';
import { preferences } from '@/stores/preferencesStore.js';

export function usePreferences() {
  const yearRange = computed({
    get: () => [preferences.min_year, preferences.max_year],
    set: ([min, max]) => {
      preferences.min_year = min;
      preferences.max_year = max;
    },
  });

  const tempoRange = computed({
    get: () => [preferences.min_tempo, preferences.max_tempo],
    set: ([min, max]) => {
      preferences.min_tempo = min;
      preferences.max_tempo = max;
    },
  });

  const durationRange = computed({
    get: () => [preferences.min_duration, preferences.max_duration],
    set: ([min, max]) => {
      preferences.min_duration = min;
      preferences.max_duration = max;
    },
  });

  return { yearRange, tempoRange, durationRange };
}
