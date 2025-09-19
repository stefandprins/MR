// import { reactive, ref, watch, onUnmounted } from 'vue';
// import debounce from 'lodash/debounce';

import { selectedTracks, recommendations, analytics, recommendState } from '@/stores/trackStore.js';

export function useRecommend() {
  const state = recommendState;

  const submitPreferences = async (filters) => {
    const track_ids = selectedTracks.map((track) => track.id);
    const payload = { track_ids, ...filters };
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
      recommendations.splice(0, recommendations.length, ...(data.recommendations || []));
      Object.assign(analytics, data.analytics);
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
