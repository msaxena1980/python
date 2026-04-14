<template>
  <div class="page">
    <h1>{{ t('nav.profile') }}</h1>
    <p>User profile information goes here.</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
