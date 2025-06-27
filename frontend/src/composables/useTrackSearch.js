import { ref, watch, onUnmounted } from 'vue';
import debounce from 'lodash/debounce';
import { selectedTracks } from '@/stores/trackStore.js'; // shared store

export function useTrackSearch() {
  const query = ref('');
  const results = ref([]);
  const loading = ref(false);
  const cache = new Map(); // Cache storage
  const selectedFromResults = ref(false);
  const currentSelectedTrack = ref(null); // temporary holder

  const fetchTracks = async () => {
    if (!query.value.trim()) {
      results.value = [];
      loading.value = false;
      return;
    }

    if (cache.has(query.value)) {
      results.value = cache.get(query.value);
      return;
    }

    loading.value = true;
    try {
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query.value)}`);
      if (!response.ok) throw new Error('Failed to fetch tracks');
      const data = await response.json();
      const mappedData = data.map((track) => ({
        ...track,
        label: `${track.title} (${track.artist_name})`,
      }));

      results.value = mappedData;
      cache.set(query.value, mappedData);
    } catch (error) {
      console.error('Search failed:', error);
      results.value = [];
    } finally {
      loading.value = false;
    }
  };

  const debouncedFetch = debounce(fetchTracks, 400, { leading: false, trailing: true });

  watch(query, () => {
    if (selectedFromResults.value) {
      selectedFromResults.value = false;
      return;
    }

    if (query.value.trim() === '') {
      results.value = [];
      return;
    }

    debouncedFetch.cancel();
    debouncedFetch();
  });

  onUnmounted(() => {
    debouncedFetch.cancel();
  });

  const selectTrack = (track) => {
    query.value = `${track.title} (${track.artist_name})`;
    currentSelectedTrack.value = track;
    selectedFromResults.value = true;
    results.value = []; // 👈 This line closes the list
    cache.delete(query.value); // Optional
  };

  const addTrack = () => {
    if (currentSelectedTrack.value && !selectedTracks.value.some((t) => t.id === currentSelectedTrack.value.id)) {
      selectedTracks.value.push(currentSelectedTrack.value);
    }
    query.value = '';
    results.value = [];
    currentSelectedTrack.value = null;
  };

  return {
    query,
    results,
    loading,
    selectTrack,
    addTrack,
    selectedTrack: currentSelectedTrack,
    selectedTracks, // exposed from shared store
  };
}
