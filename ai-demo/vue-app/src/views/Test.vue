<template>
  <div class="container">
    <div class="header-row">
      <h1>Hello World App</h1>
      <a href="http://localhost:8000/docs" target="_blank" rel="noopener" class="docs-btn">API Docs ↗</a>
    </div>

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
        <textarea v-model="messagePayload" rows="5" placeholder='{"order_id": "ORD-001", "user": "john_doe", "total": "49.99"}'></textarea>
      </label>
    </div>

    <div class="section row">
      <button @click="createGroup">👥 Create Consumer Group</button>
      <label class="inline-check">
        <input type="checkbox" v-model="groupFromBeginning" />
        From beginning
      </label>
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

const message = ref('')
const error = ref('')
const dbResult = ref(null)
const redisResult = ref(null)

const streamName = ref('orders')
const groupName = ref('workers')
const consumerName = ref('worker-1')
const messagePayload = ref(JSON.stringify({ order_id: "ORD-001", user: "john_doe", item: "Widget Pro", total: "49.99", currency: "USD" }, null, 2))
const ackMessageId = ref('')
const groupFromBeginning = ref(true)
const streamOutput = ref('')
const streamOutputLabel = ref('')
const streamError = ref('')

const fetchMessage = async () => {
  try {
    error.value = ''
    const res = await fetch(`${BASE_URL}/api/hello`)
    const data = await res.json()
    message.value = data.message || data
  } catch (e) {
    error.value = e.message
  }
}

const testDB = async (type) => {
  try {
    error.value = ''
    dbResult.value = null
    const res = await fetch(`${BASE_URL}/api/${type}/test`)
    dbResult.value = await res.json()
  } catch (e) {
    dbResult.value = { status: 'error', message: e.message }
  }
}

const testRedis = async () => {
  try {
    error.value = ''
    redisResult.value = null
    const res = await fetch(`${BASE_URL}/api/redis/test`)
    redisResult.value = await res.json()
  } catch (e) {
    redisResult.value = { status: 'error', message: e.message }
  }
}

const streamAdd = async () => {
  try {
    streamError.value = ''
    let payload
    try {
      payload = JSON.parse(messagePayload.value || '{}')
    } catch {
      streamError.value = 'Invalid JSON in message payload'
      return
    }
    const res = await fetch(`${BASE_URL}/api/streams/${streamName.value}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    // Auto-populate ack field with the new message ID for convenience
    if (data.message_id) ackMessageId.value = data.message_id
    streamOutputLabel.value = 'Add Message'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const streamRead = async () => {
  try {
    streamError.value = ''
    const res = await fetch(`${BASE_URL}/api/streams/${streamName.value}/read?start_id=0`)
    const data = await res.json()
    streamOutputLabel.value = 'Read Messages'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const streamInfo = async () => {
  try {
    streamError.value = ''
    const res = await fetch(`${BASE_URL}/api/streams/${streamName.value}/info`)
    const data = await res.json()
    streamOutputLabel.value = 'Stream Info'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const createGroup = async () => {
  try {
    streamError.value = ''
    const res = await fetch(
      `${BASE_URL}/api/streams/${streamName.value}/consumer-group/${groupName.value}/create?start_from_beginning=${groupFromBeginning.value}`,
      { method: 'POST' }
    )
    const data = await res.json()
    streamOutputLabel.value = 'Create Group'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const groupRead = async () => {
  try {
    streamError.value = ''
    const res = await fetch(
      `${BASE_URL}/api/streams/${streamName.value}/consumer-group/${groupName.value}/read?consumer_name=${consumerName.value}`
    )
    const data = await res.json()
    streamOutputLabel.value = 'Read as Consumer'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const ackMessage = async () => {
  try {
    streamError.value = ''
    const res = await fetch(
      `${BASE_URL}/api/streams/${streamName.value}/consumer-group/${groupName.value}/ack/${ackMessageId.value}`,
      { method: 'POST' }
    )
    const data = await res.json()
    streamOutputLabel.value = 'Acknowledge'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const groupInfo = async () => {
  try {
    streamError.value = ''
    const res = await fetch(
      `${BASE_URL}/api/streams/${streamName.value}/consumer-group/${groupName.value}/info`
    )
    const data = await res.json()
    streamOutputLabel.value = 'Group Info'
    streamOutput.value = JSON.stringify(data, null, 2)
  } catch (e) {
    streamError.value = e.message
  }
}

const clearOutput = () => {
  streamOutput.value = ''
  streamOutputLabel.value = ''
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.docs-btn {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9rem;
}
.section {
  margin: 20px 0;
}
.section.row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: flex-end;
}
label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 0.9rem;
  color: #555;
}
input, textarea {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  width: 200px;
}
textarea {
  width: 100%;
  max-width: 480px;
  resize: vertical;
}
button {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
button:hover {
  background: #3aa876;
}
.success { color: #42b983; font-weight: 500; }
.error { color: #e74c3c; }
.result {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.clear-btn {
  padding: 4px 10px;
  background: #6c757d;
  font-size: 0.85rem;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 0.9rem;
}
.inline-check {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
}
.inline-check input {
  width: auto;
  cursor: pointer;
}
h2 {
  margin-top: 30px;
  margin-bottom: 15px;
}
</style>
