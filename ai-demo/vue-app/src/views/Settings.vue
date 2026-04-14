<template>
  <div class="page">
    <h1>{{ t('nav.settings') }}</h1>
    <div class="settings-section">
      <div class="setting-item">
        <span>{{ t('common.theme') }}</span>
        <button @click="toggleTheme" class="theme-btn">
          <font-awesome-icon :icon="currentTheme === 'light' ? 'moon' : 'sun'" />
          {{ currentTheme === 'light' ? t('common.darkMode') : t('common.lightMode') }}
        </button>
      </div>
      <div class="setting-item">
        <span>{{ t('common.language') }}</span>
        <select v-model="selectedLocale" @change="changeLocale">
          <option value="en">English</option>
          <option value="fr">Français</option>
          <option value="hi">हिन्दी</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons'

library.add(faSun, faMoon)

const { t, locale } = useI18n()
const store = useStore()
const selectedLocale = ref(locale.value)

const currentTheme = computed(() => store.getters.currentTheme)

const toggleTheme = () => {
  store.dispatch('toggleTheme')
}

const changeLocale = () => {
  locale.value = selectedLocale.value
}
</script>

<style scoped>
.settings-section {
  margin-top: 20px;
}
.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
}
.theme-btn {
  display: flex;
  align-items: center;
  gap: 8px;
}
select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-primary);
}
</style>
