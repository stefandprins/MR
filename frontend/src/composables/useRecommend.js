import { reactive, ref, watch, onUnmounted } from 'vue';
import debounce from 'lodash/debounce';
import { selectedTracks } from '@/stores/trackStore.js'; // shared store
import { recommendations } from '@/stores/trackStore.js';

export function useRecommend() {
  const state = reactive({
    // recommendations: [],
    loading: false,
    error: null,
  });

  const submitPreferences = async () => {
    console.log('Hello');
    const track_ids = selectedTracks.value.map((track) => track.id);
    const payload = { track_ids };

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
      recommendations.value = data;
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
