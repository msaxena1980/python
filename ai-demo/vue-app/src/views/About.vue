<template>
  <div class="page">
    <div class="about-card">
      <h1>{{ t('nav.about') }}</h1>
      <p>This is the About Us page.</p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<style scoped>
.about-card {
  background: var(--bg-primary);
  padding: 40px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.about-card h1 {
  color: var(--text-primary);
  margin-bottom: 20px;
  font-size: 2rem;
}

.about-card p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.6;
}
</style>
