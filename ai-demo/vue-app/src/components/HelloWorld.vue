<template>
  <div>
    <h1>{{ msg }}</h1>
    <p>Edit <code>src/App.vue</code> to get started.</p>
  </div>
</template>

<script setup>
defineProps({
  msg: String,
})
</script>
