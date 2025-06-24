<template>
  <div class="card shadow-sm text-bg-light p-4">
    <h2>Recommendation Details</h2>
    <div v-if="data">
      <p><strong>Algorithm:</strong> {{ data.algorithm }}</p>
      <p><strong>Score:</strong> {{ data.score }}</p>
      <p><strong>Reason:</strong> {{ data.reason }}</p>
    </div>
    <div v-else>
      <p>No recommendation data available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendationData',
  props: {
    data: {
      type: Object,
      default: null,
    },
  },
};
</script>

<style scoped>
.recommendation-data {
  margin-top: 20px;
}
</style>
