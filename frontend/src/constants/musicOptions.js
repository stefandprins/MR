export const GENRE_OPTIONS = ['Pop', 'Electronic', 'Rock', 'Folk', 'Metal', 'Jazz', 'Hip-Hop', 'Blues', 'Country', 'Reggae', 'R&B', 'Classical'];

export const KEY_OPTIONS = [
  { value: 0, label: 'C' },
  { value: 1, label: 'C#' },
  { value: 2, label: 'D' },
  { value: 3, label: 'D#' },
  { value: 4, label: 'E' },
  { value: 5, label: 'F' },
  { value: 6, label: 'F#' },
  { value: 7, label: 'G' },
  { value: 8, label: 'G#' },
  { value: 9, label: 'A' },
  { value: 10, label: 'A#' },
  { value: 11, label: 'B' },
];

export const TIME_SIGNATURE_OPTIONS = [0, 1, 3, 4, 5, 7];


export const SLIDER_BOUNDS = {
  year: { min: 1950, max: 2024 },
  tempo: { min: 60, max: 200 },
  duration: { min: 1, max: 1000 },
};