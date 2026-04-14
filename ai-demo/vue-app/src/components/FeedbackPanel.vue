<template>
  <transition name="slide-fade">
    <div v-if="isOpen" class="feedback-panel-overlay" @click="closePanel">
      <div class="feedback-panel" @click.stop>
        <div class="panel-header">
          <button class="back-btn" @click="closePanel">
            <font-awesome-icon icon="arrow-left" />
          </button>
          <h2>{{ t('feedback.newRequest') }}</h2>
          <button class="close-btn" @click="closePanel">
            <font-awesome-icon icon="times" />
          </button>
        </div>

        <div class="panel-content">
          <form @submit.prevent="submitFeedback">
            <div class="form-group">
              <label for="feedback-type">{{ t('feedback.nature') }} <span class="required">*</span></label>
              <div class="select-wrapper">
                <select id="feedback-type" v-model="feedbackType" required>
                  <option value="" disabled>{{ t('feedback.selectType') }}</option>
                  <option value="issue">Issue</option>
                  <option value="enhancement">Enhancement</option>
                  <option value="feature">New Feature</option>
                  <option value="app-feedback">App Feedback</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="details">{{ t('feedback.details') }} <span class="required">*</span></label>
              <textarea 
                id="details" 
                v-model="details" 
                rows="8"
                placeholder="{{ t('feedback.detailsPlaceholder') }}"
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label for="image-upload">{{ t('feedback.attachImage') }}</label>
              <div class="upload-area" @click="triggerFileInput">
                <input 
                  ref="fileInput"
                  type="file" 
                  id="image-upload"
                  accept="image/png, image/jpeg"
                  @change="handleFileUpload"
                  hidden
                />
                <font-awesome-icon icon="image" class="upload-icon" />
                <p v-if="!uploadedFile">{{ t('feedback.imageHint') }}</p>
                <p v-else class="file-name">{{ uploadedFile.name }}</p>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="closePanel">{{ t('common.cancel') }}</button>
              <button type="submit" class="btn-submit">{{ t('feedback.submitRequest') }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowLeft, faTimes, faImage } from '@fortawesome/free-solid-svg-icons'

library.add(faArrowLeft, faTimes, faImage)

const store = useStore()
const { t } = useI18n()
const isOpen = computed(() => store.getters.isFeedbackPanelOpen)

const feedbackType = ref('')
const details = ref('')
const uploadedFile = ref(null)
const fileInput = ref(null)

const closePanel = () => {
  store.dispatch('setFeedbackPanel', false)
  // Reset form
  feedbackType.value = ''
  details.value = ''
  uploadedFile.value = null
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files?.[0]
  if (file && file.size <= 5 * 1024 * 1024) { // 5MB limit
    uploadedFile.value = file
  } else if (file) {
    alert('File size must be less than 5MB')
  }
}

const submitFeedback = () => {
  // Here you would send the feedback to your backend
  const feedback = {
    type: feedbackType.value,
    details: details.value,
    file: uploadedFile.value
  }
  
  console.log('Feedback submitted:', feedback)
  alert('Thank you for your feedback!')
  closePanel()
}
</script>

<style scoped>
.feedback-panel-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
}

.feedback-panel {
  width: 100%;
  max-width: 500px;
  background: var(--bg-primary);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  gap: 16px;
  background: var(--bg-primary);
}

.panel-header h2 {
  flex: 1;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.back-btn,
.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: var(--text-secondary);
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.back-btn:hover,
.close-btn:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: var(--bg-secondary);
}

.panel-content::-webkit-scrollbar {
  width: 8px;
}

.panel-content::-webkit-scrollbar-track {
  background: transparent;
}

.panel-content::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.required {
  color: #ef4444;
}

.select-wrapper {
  position: relative;
}

select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

select:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(91, 95, 199, 0.1);
}

select option {
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: 8px;
}

textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.95rem;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s;
}

textarea:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(91, 95, 199, 0.1);
}

textarea::placeholder {
  color: var(--text-secondary);
}

.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--bg-primary);
}

.upload-area:hover {
  border-color: var(--accent-color);
  background: var(--bg-secondary);
}

.upload-icon {
  font-size: 2rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.upload-area p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

.file-name {
  color: var(--accent-color) !important;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-cancel:hover {
  background: var(--bg-secondary);
}

.btn-submit {
  background: var(--accent-color);
  color: white;
}

.btn-submit:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(91, 95, 199, 0.3);
}

/* Animations */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-from .feedback-panel,
.slide-fade-leave-to .feedback-panel {
  transform: translateX(100%);
}
</style>
