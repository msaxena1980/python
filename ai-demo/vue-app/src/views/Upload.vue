<template>
  <div class="page">
    <div class="upload-card">
      <h1>Upload Document</h1>
      <p>Upload your study materials and documents here.</p>
      <div class="upload-area">
        <font-awesome-icon icon="cloud-upload-alt" class="upload-icon" />
        <p>Drag and drop files here or click to browse</p>
        <button class="upload-btn">Select Files</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons'

library.add(faCloudUploadAlt)
</script>

<style scoped>
.upload-card {
  background: var(--bg-primary);
  padding: 40px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  text-align: center;
}

.upload-card h1 {
  color: var(--text-primary);
  margin-bottom: 12px;
  font-size: 2rem;
}

.upload-card > p {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 32px;
}

.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 60px 40px;
  background: var(--bg-secondary);
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: var(--accent-color);
  background: var(--bg-primary);
}

.upload-icon {
  font-size: 4rem;
  color: var(--accent-color);
  margin-bottom: 20px;
}

.upload-area p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.upload-btn {
  background: var(--accent-color);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(91, 95, 199, 0.3);
}
</style>
