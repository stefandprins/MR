<template>
  <div id="app">
    <Header />
    <main class="container-fluid px-4">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Header from './components/Header.vue';
</script>

<style>
html,
body,
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
