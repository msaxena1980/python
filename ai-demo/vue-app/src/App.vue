<template>
  <div class="container">
    <h1>Hello World App</h1>

    <div class="section">
      <button @click="fetchMessage">Call API</button>
      <p v-if="message" class="success">{{ message }}</p>
    </div>

    <div class="section">
      <button @click="testDB('mysql')">Test MySQL</button>
      <button @click="testDB('postgres')">Test PostgreSQL</button>
      <p v-if="dbResult" :class="dbResult.status === 'connected' ? 'success' : 'error'">
        {{ dbResult.status === 'connected'
          ? `Connected to: ${dbResult.database}`
          : `Error: ${dbResult.message}` }}
      </p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const BASE_URL = 'http://localhost:8000'

const message = ref('')
const error = ref('')
const dbResult = ref(null)

async function fetchMessage() {
  try {
    const res = await fetch(`${BASE_URL}/api/hello`)
    const data = await res.json()
    message.value = data.message
    error.value = ''
  } catch (e) {
    error.value = 'Failed to reach API. Is the server running?'
    message.value = ''
  }
}

async function testDB(type) {
  dbResult.value = null
  error.value = ''
  try {
    const res = await fetch(`${BASE_URL}/api/${type}/test`)
    dbResult.value = await res.json()
  } catch (e) {
    error.value = `Failed to reach ${type} endpoint.`
  }
}
</script>

<style scoped>
.container {
  font-family: sans-serif;
  text-align: center;
  margin-top: 80px;
}
.section {
  margin: 24px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
button {
  padding: 10px 24px;
  font-size: 16px;
  cursor: pointer;
  margin: 0 8px;
}
.success {
  font-size: 18px;
  color: green;
}
.error {
  color: red;
}
</style>
