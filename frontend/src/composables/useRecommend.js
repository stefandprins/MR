// import { reactive, ref, watch, onUnmounted } from 'vue';
// import debounce from 'lodash/debounce';

import { selectedTracks, recommendations, recommendState } from '@/stores/trackStore.js';

export function useRecommend() {
  const state = recommendState;

  const submitPreferences = async (filters) => {
    console.log('=== DEBUGGING SUBMISSION ===');
    console.log('selectedTracks:', selectedTracks);
    console.log('filters:', filters);
    const track_ids = selectedTracks.map((track) => track.id);
    console.log('track_ids:', track_ids);

    const payload = { track_ids, ...filters };
    console.log('Full payload:', JSON.stringify(payload, null, 2));

    const safeStringify = JSON.stringify;

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: safeStringify(payload),
    };

    state.loading = true;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/recommend`, requestOptions);

      const data = await response.json();
      console.log(data);
      recommendations.splice(0, recommendations.length, ...data);
    } catch (error) {
      console.error('Recommendation request failed', error);
    } finally {
      state.loading = false;
    }
  };

  return {
    state,
    submitPreferences,
  };
}
