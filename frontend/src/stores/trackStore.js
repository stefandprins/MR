import { reactive } from 'vue';

export const selectedTracks = reactive([]);
export const recommendations = reactive([]);
export const recommendState = reactive({
  loading: false,
  error: null,
});
