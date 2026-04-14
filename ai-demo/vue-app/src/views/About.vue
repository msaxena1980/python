<template>
  <div class="page">
    <h1>{{ t('nav.about') }}</h1>
    <p>This is the About Us page.</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
