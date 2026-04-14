<template>
  <div class="layout">
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <span v-if="!isCollapsed" class="logo">Vue App</span>
        <button class="toggle-btn" @click="toggleSidebar">
          <font-awesome-icon :icon="isCollapsed ? 'chevron-right' : 'chevron-left'" />
        </button>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          <font-awesome-icon icon="home" />
          <span v-if="!isCollapsed">{{ t('nav.home') }}</span>
        </router-link>
        <router-link to="/test" class="nav-item">
          <font-awesome-icon icon="flask" />
          <span v-if="!isCollapsed">{{ t('nav.test') }}</span>
        </router-link>
        <router-link to="/about" class="nav-item">
          <font-awesome-icon icon="info-circle" />
          <span v-if="!isCollapsed">{{ t('nav.about') }}</span>
        </router-link>
        <router-link to="/profile" class="nav-item">
          <font-awesome-icon icon="user" />
          <span v-if="!isCollapsed">{{ t('nav.profile') }}</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <font-awesome-icon icon="cog" />
          <span v-if="!isCollapsed">{{ t('nav.settings') }}</span>
        </router-link>
      </nav>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faHome, faFlask, faInfoCircle, faUser, faCog, faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons'

library.add(faHome, faFlask, faInfoCircle, faUser, faCog, faChevronLeft, faChevronRight)

const { t } = useI18n()
const store = useStore()

const isCollapsed = computed(() => store.getters.isSidebarCollapsed)

const toggleSidebar = () => {
  store.dispatch('toggleSidebar')
}
</script>

<style>
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
  --text-primary: #2c3e50;
  --text-secondary: #7f8c8d;
  --accent-color: #42b983;
  --border-color: #e1e4e8;
  --sidebar-width: 240px;
  --sidebar-collapsed-width: 60px;
}

[data-theme="dark"] {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #e4e4e7;
  --text-secondary: #a1a1aa;
  --accent-color: #42b983;
  --border-color: #3d3d5c;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.logo {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--accent-color);
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: var(--text-secondary);
  border-radius: 6px;
  transition: background 0.2s;
}

.toggle-btn:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.nav-item.router-link-active {
  background: var(--accent-color);
  color: white;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 8px;
}

.sidebar.collapsed .nav-item span {
  display: none;
}

.main-content {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
}

.page {
  max-width: 800px;
}

.page h1 {
  margin-bottom: 20px;
  color: var(--text-primary);
}
</style>
