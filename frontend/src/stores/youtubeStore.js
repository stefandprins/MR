import { ref, reactive } from 'vue';

export const youtubeURL = ref(null);
export const youtubeState = reactive({
  loading: false,
  error: null,
});
