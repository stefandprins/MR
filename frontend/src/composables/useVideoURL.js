import { reactive } from 'vue';
import { youtubeURL, youtubeState } from '@/stores/youtubeStore.js';

export function useVideoURL() {
  const state = youtubeState;

  const getVideoURL = async (title, artist_name) => {
    // Store the arguments as a payload
    const payload = { title, artist_name };

    const safeStringify = JSON.stringify;

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: safeStringify(payload),
    };

    // Set the loading state to true before the endpoint request
    state.loading = true;

    try {
      // video endpoint
      const response = await fetch(`${import.meta.env.VITE_API_URL}/youtube`, requestOptions);
      const data = await response.json();
      console.log(data);
      youtubeURL.value = data.url;
    } catch (error) {
      console.error('Youtube URL request failed', error);
    } finally {
      // Set the loading state to false after the endpoint request
      state.loading = false;
    }
  };

  return {
    state,
    getVideoURL,
  };
}
