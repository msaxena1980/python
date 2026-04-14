<template>
  <div class="container">
    <h1>Hello World App</h1>

    <!-- ── Core API ── -->
    <div class="section">
      <button @click="fetchMessage">Call API</button>
      <p v-if="message" class="success">{{ message }}</p>
    </div>

    <div class="section">
      <button @click="testDB('mysql')">Test MySQL</button>
      <button @click="testDB('postgres')">Test PostgreSQL</button>
      <button @click="testRedis">Test Redis</button>
      <p v-if="dbResult" :class="dbResult.status === 'connected' ? 'success' : 'error'">
        {{ dbResult.status === 'connected'
          ? `Connected to: ${dbResult.database}`
          : `Error: ${dbResult.message}` }}
      </p>
      <p v-if="redisResult" :class="redisResult.status === 'connected' ? 'success' : 'error'">
        {{ redisResult.status === 'connected'
          ? `Redis connected — test value: ${redisResult.test_value}`
          : `Redis error: ${redisResult.message}` }}
      </p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <hr />

    <!-- ── Redis Streams ── -->
    <h2>Redis Streams</h2>

    <!-- Config row -->
    <div class="section row">
      <label>Stream name
        <input v-model="streamName" placeholder="e.g. orders" />
      </label>
      <label>Group name
        <input v-model="groupName" placeholder="e.g. workers" />
      </label>
      <label>Consumer name
        <input v-model="consumerName" placeholder="e.g. worker-1" />
      </label>
    </div>

    <!-- Actions -->
    <div class="section row">
      <button @click="streamAdd">➕ Add Message</button>
      <button @click="streamRead">📖 Read Messages</button>
      <button @click="streamInfo">ℹ️ Stream Info</button>
    </div>

    <!-- Message payload for Add -->
    <div class="section">
      <label style="width:100%;max-width:480px">
        Message payload (JSON)
        <textarea v-model="messagePayload" rows="3" placeholder='{"key": "value"}'></textarea>
      </label>
    </div>

    <div class="section row">
      <button @click="createGroup">👥 Create Consumer Group</button>
      <button @click="groupRead">📥 Read as Consumer</button>
    </div>

    <!-- Ack row -->
    <div class="section row">
      <label>Message ID to acknowledge
        <input v-model="ackMessageId" placeholder="e.g. 1713091200000-0" />
      </label>
      <button @click="ackMessage">✅ Acknowledge</button>
      <button @click="groupInfo">📊 Group Info</button>
    </div>

    <!-- Stream output -->
    <div v-if="streamError" class="result error">{{ streamError }}</div>

    <div v-if="streamOutput" class="result">
      <div class="result-header">
        <strong>{{ streamOutputLabel }}</strong>
        <button class="clear-btn" @click="clearOutput">✕ Clear</button>
      </div>
      <pre>{{ streamOutput }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const BASE_URL = 'http://localhost:8000'

// ── Core state ──
const message = ref('')
const error = ref('')
const dbResult = ref(null)
const redisResult = ref(null)

// ── Streams state ──
const streamName = ref('orders')
const groupName = ref('workers')
const consumerName = ref('worker-1')
const messagePayload = ref('{"order_id": "123", "user": "Manish", "total": "99.99"}')
const ackMessageId = ref('')
const streamOutput = ref('')
const streamOutputLabel = ref('')
const streamError = ref('')

// ── Core helpers ──
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
  redisResult.value = null
  error.value = ''
  try {
    const res = await fetch(`${BASE_URL}/api/${type}/test`)
    dbResult.value = await res.json()
  } catch (e) {
    error.value = `Failed to reach ${type} endpoint.`
  }
}

async function testRedis() {
  redisResult.value = null
  dbResult.value = null
  error.value = ''
  try {
    const res = await fetch(`${BASE_URL}/api/redis/test`)
    redisResult.value = await res.json()
  } catch (e) {
    error.value = 'Failed to reach Redis endpoint.'
  }
}

// ── Streams helpers ──
function showResult(label, data) {
  streamOutputLabel.value = label
  streamOutput.value = JSON.stringify(data, null, 2)
  streamError.value = ''
}

function showStreamError(msg) {
  streamError.value = msg
  streamOutput.value = ''
}

function clearOutput() {
  streamOutput.value = ''
  streamOutputLabel.value = ''
  streamError.value = ''
}

function stream() {
  return streamName.value.trim() || 'orders'
}

function group() {
  return groupName.value.trim() || 'workers'
}

async function streamAdd() {
  let payload
  try {
    payload = JSON.parse(messagePayload.value)
  } catch {
    showStreamError('Invalid JSON in message payload.')
    return
  }
  try {
    const res = await fetch(`${BASE_URL}/api/streams/${stream()}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    showResult('Add Message', await res.json())
  } catch (e) {
    showStreamError(`Add failed: ${e.message}`)
  }
}

async function streamRead() {
  try {
    const res = await fetch(`${BASE_URL}/api/streams/${stream()}/read?start_id=0&count=20`)
    showResult('Read Messages', await res.json())
  } catch (e) {
    showStreamError(`Read failed: ${e.message}`)
  }
}

async function streamInfo() {
  try {
    const res = await fetch(`${BASE_URL}/api/streams/${stream()}/info`)
    showResult('Stream Info', await res.json())
  } catch (e) {
    showStreamError(`Info failed: ${e.message}`)
  }
}

async function createGroup() {
  try {
    const res = await fetch(
      `${BASE_URL}/api/streams/${stream()}/consumer-group/${group()}/create`,
      { method: 'POST' }
    )
    showResult('Create Consumer Group', await res.json())
  } catch (e) {
    showStreamError(`Create group failed: ${e.message}`)
  }
}

async function groupRead() {
  const consumer = consumerName.value.trim() || 'worker-1'
  try {
    const res = await fetch(
      `${BASE_URL}/api/streams/${stream()}/consumer-group/${group()}/read?consumer_name=${consumer}&count=5`
    )
    const data = await res.json()
    // Auto-fill ack field with first message ID for convenience
    if (data.messages?.length > 0) {
      ackMessageId.value = data.messages[0].id
    }
    showResult('Read as Consumer', data)
  } catch (e) {
    showStreamError(`Group read failed: ${e.message}`)
  }
}

async function ackMessage() {
  const msgId = ackMessageId.value.trim()
  if (!msgId) {
    showStreamError('Enter a message ID to acknowledge.')
    return
  }
  try {
    const res = await fetch(
      `${BASE_URL}/api/streams/${stream()}/consumer-group/${group()}/ack/${msgId}`,
      { method: 'POST' }
    )
    showResult('Acknowledge Message', await res.json())
  } catch (e) {
    showStreamError(`Ack failed: ${e.message}`)
  }
}

async function groupInfo() {
  try {
    const res = await fetch(
      `${BASE_URL}/api/streams/${stream()}/consumer-group/${group()}/info`
    )
    showResult('Group Info', await res.json())
  } catch (e) {
    showStreamError(`Group info failed: ${e.message}`)
  }
}
</script>

<style scoped>
.container {
  font-family: sans-serif;
  text-align: center;
  margin-top: 60px;
  padding: 0 16px 60px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

h2 {
  margin-top: 32px;
  margin-bottom: 8px;
}

hr {
  margin: 32px 0;
  border: none;
  border-top: 1px solid #ddd;
}

.section {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.section.row {
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}

label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 13px;
  color: #555;
  gap: 4px;
}

input {
  padding: 7px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 160px;
}

textarea {
  padding: 7px 10px;
  font-size: 13px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  font-family: monospace;
  resize: vertical;
}

button {
  padding: 9px 18px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid #bbb;
  border-radius: 4px;
  background: #f5f5f5;
  transition: background 0.15s;
}

button:hover {
  background: #e8e8e8;
}

.success {
  font-size: 16px;
  color: green;
}

.error {
  color: red;
}

.result {
  margin-top: 20px;
  text-align: left;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #efefef;
  border-bottom: 1px solid #ddd;
  font-size: 13px;
}

.clear-btn {
  padding: 3px 8px;
  font-size: 12px;
  border: 1px solid #ccc;
  border-radius: 3px;
  background: #fff;
  cursor: pointer;
}

pre {
  margin: 0;
  padding: 14px;
  font-size: 12px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
