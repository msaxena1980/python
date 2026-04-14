<template>
  <div class="page">
    <h1>{{ t('nav.settings') }}</h1>
    <div class="settings-section">
      <p class="empty-state">{{ t('settings.empty') }}</p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.settings-section {
  margin-top: 20px;
  background: var(--bg-primary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  padding: 40px;
  text-align: center;
}

.empty-state {
  color: var(--text-secondary);
  font-size: 1rem;
}
</style>
