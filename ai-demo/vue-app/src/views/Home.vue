<template>
  <div class="page">
    <h1>{{ t('nav.home') }}</h1>
    <p>{{ t('common.welcome') }}</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
