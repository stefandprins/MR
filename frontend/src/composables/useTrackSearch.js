import { reactive, ref, watch, onUnmounted } from 'vue';
import debounce from 'lodash/debounce';
import { selectedTracks } from '@/stores/trackStore.js'; // shared store

export function useTrackSearch() {
  const cache = new Map(); // Cache storage

  const state = reactive({
    query: '',
    results: [],
    loading: false,
    selectedFromResults: false,
    selectedTrack: null,
    error: null,
  });

  const fetchTracks = async () => {
    if (!state.query.trim()) {
      state.results = [];
      state.loading = false;
      state.error = null;
      return;
    }
    state.loading = true;

    if (cache.has(state.query)) {
      state.results = cache.get(state.query);
      state.loading = false; // Ensure loading is false when using cache
      return;
    }

    // loading.value = true;
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/search?query=${encodeURIComponent(state.query)}`);
      if (!response.ok) throw new Error('Failed to fetch tracks');
      const data = await response.json();
      // const mappedData = data.map((track) => ({
      state.results = data.map((track) => ({
        ...track,
        label: `${track.title} (${track.artist_name})`,
      }));

      cache.set(state.query, state.results);
      state.error = null;
    } catch (error) {
      console.error('Search failed:', error);
      state.error = error.message;
      state.results = [];
    } finally {
      state.loading = false;
    }
  };

  const debouncedFetch = debounce(fetchTracks, 400, { leading: true, trailing: true });

  watch(
    () => state.query,
    () => {
      if (state.selectedFromResults) {
        state.selectedFromResults = false;
        return;
      }

      if (state.query.trim() === '') {
        state.results = [];
        state.error = null;
        return;
      }

      debouncedFetch.cancel();
      debouncedFetch();
    }
  );

  onUnmounted(() => {
    debouncedFetch.cancel();
  });

  const selectTrack = (track) => {
    state.query = `${track.title} (${track.artist_name})`;
    state.selectedTrack = track;
    state.selectedFromResults = true;
    state.results = [];
    state.error = null;
    cache.delete(state.query);
  };

  const addTrack = () => {
    if (state.selectedTrack && !selectedTracks.value.some((t) => t.id === state.selectedTrack.id)) {
      selectedTracks.value.push(state.selectedTrack);
    }
    state.query = '';
    state.results = [];
    state.selectedTrack = null;
    state.error = null;
  };

  const removeTrack = (trackId) => {
    const index = selectedTracks.value.findIndex((t) => t.id === trackId);
    if (index !== -1) {
      selectedTracks.value.splice(index, 1);
    }
  };

  return {
    state,
    selectTrack,
    addTrack,
    removeTrack,
    selectedTracks, // exposed from shared store
  };
}
