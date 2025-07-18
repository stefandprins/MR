<template>
  <div class="card custom-card shadow-sm text-bg-light">
    <!-- Card Title -->
    <div class="card-header text-start">
      <h5 class="mb-0">
        <i class="fas fa-lightbulb me-2"></i>
        Analytics
      </h5>
    </div>
    <div class="card-body" v-if="data">
      <p><strong>Algorithm:</strong> {{ data.algorithm }}</p>
      <p><strong>Score:</strong> {{ data.score }}</p>
      <p><strong>Reason:</strong> {{ data.reason }}</p>
    </div>
    <div class="card-body" v-else>
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
