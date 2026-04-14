<template>
  <div class="layout">
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <router-link to="/" class="logo-wrapper" v-if="!isCollapsed">
          <font-awesome-icon icon="graduation-cap" class="logo-icon" />
          <span class="logo-text">AI Tutor</span>
        </router-link>
        <div v-if="isCollapsed" class="logo-wrapper-collapsed" @click="navigateHome">
          <font-awesome-icon icon="graduation-cap" class="logo-icon" />
        </div>
        <button class="toggle-btn" @click="toggleSidebar">
          <font-awesome-icon :icon="isCollapsed ? 'angles-right' : 'times'" />
        </button>
      </div>

      <nav class="sidebar-nav">
        <!-- Main Navigation Section -->
        <div class="nav-section">
          <div v-if="!isCollapsed" class="section-header" @click="toggleSection('library')">
            <div class="section-title">
              <font-awesome-icon icon="book" class="section-icon" />
              <span>{{ t('sidebar.documentLibrary') }}</span>
            </div>
            <font-awesome-icon 
              :icon="expandedSections.library ? 'chevron-down' : 'chevron-right'" 
              class="toggle-icon" 
            />
          </div>
          <div v-if="expandedSections.library || isCollapsed" class="section-content">
            <p v-if="!isCollapsed" class="no-items">{{ t('sidebar.noDocuments') }}</p>
          </div>
        </div>

        <div class="nav-section">
          <div v-if="!isCollapsed" class="section-header" @click="toggleSection('topics')">
            <div class="section-title">
              <font-awesome-icon icon="circle" class="section-icon" />
              <span>{{ t('sidebar.topics') }} (0)</span>
            </div>
            <font-awesome-icon 
              :icon="expandedSections.topics ? 'chevron-down' : 'chevron-right'" 
              class="toggle-icon" 
            />
          </div>
        </div>

        <!-- Main Menu Items -->
        <div class="main-menu">
          <router-link to="/test" class="menu-item">
            <font-awesome-icon icon="flask" />
            <span v-if="!isCollapsed">{{ t('nav.test') }}</span>
          </router-link>
          <router-link to="/subscription" class="menu-item">
            <font-awesome-icon icon="crown" />
            <span v-if="!isCollapsed">{{ t('nav.upgrade') }}</span>
          </router-link>
          <button class="menu-item" @click="openFeedback">
            <font-awesome-icon icon="comment-dots" />
            <span v-if="!isCollapsed">{{ t('nav.feedback') }}</span>
          </button>
          <router-link to="/upload" class="menu-item">
            <font-awesome-icon icon="upload" />
            <span v-if="!isCollapsed">{{ t('nav.upload') }}</span>
          </router-link>
          <router-link to="/insta-study" class="menu-item">
            <font-awesome-icon icon="book-open" />
            <span v-if="!isCollapsed">{{ t('nav.instaStudy') }}</span>
          </router-link>
          <router-link to="/group-study" class="menu-item">
            <font-awesome-icon icon="users" />
            <span v-if="!isCollapsed">{{ t('nav.groupStudy') }}</span>
          </router-link>
          <router-link to="/study-center" class="menu-item">
            <font-awesome-icon icon="book-reader" />
            <span v-if="!isCollapsed">{{ t('nav.studyCenter') }}</span>
          </router-link>
        </div>

      </nav>

      <!-- Bottom Navigation -->
      <div class="sidebar-footer">
        <!-- User Profile at Top of Footer -->
        <div v-if="!isCollapsed" class="user-profile" @click="toggleUserSection">
          <div class="user-avatar">
            <font-awesome-icon icon="user-circle" />
          </div>
          <div class="user-info">
            <div class="user-name">Manish Saxena</div>
            <div class="user-plan">{{ t('user.freePlan') }}</div>
          </div>
          <button class="expand-btn">
            <font-awesome-icon :icon="expandedSections.userSection ? 'chevron-down' : 'chevron-up'" />
          </button>
        </div>

        <!-- Collapsible Content -->
        <div v-if="!isCollapsed && expandedSections.userSection" class="user-section-content">
          <!-- Menu Items -->
          <div class="footer-nav">
            <router-link to="/profile" class="footer-item">
              <font-awesome-icon icon="user" />
              <span>{{ t('nav.profile') }}</span>
            </router-link>
            <router-link to="/settings" class="footer-item">
              <font-awesome-icon icon="cog" />
              <span>{{ t('nav.settings') }}</span>
            </router-link>
            <button class="footer-item logout">
              <font-awesome-icon icon="sign-out-alt" />
              <span>{{ t('nav.logout') }}</span>
            </button>
          </div>
        </div>

        <!-- Collapsed Sidebar Icons -->
        <div v-if="isCollapsed" class="collapsed-footer-nav">
          <router-link to="/profile" class="footer-item" :title="t('nav.profile')">
            <font-awesome-icon icon="user" />
          </router-link>
          <router-link to="/settings" class="footer-item" :title="t('nav.settings')">
            <font-awesome-icon icon="cog" />
          </router-link>
          <button class="footer-item logout" :title="t('nav.logout')">
            <font-awesome-icon icon="sign-out-alt" />
          </button>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <AppHeader />
      <div class="main-content-wrapper">
        <router-view />
      </div>
    </main>

    <!-- Feedback Trigger Button -->
    <!-- <button class="feedback-trigger" @click="openFeedback" title="Send Feedback">
      <font-awesome-icon icon="comment-dots" />
      <span>Feedback</span>
    </button> -->

    <!-- Feedback Panel -->
    <FeedbackPanel />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { 
  faGraduationCap, faTimes, faBook, faCircle, faChevronDown, faChevronRight,
  faUpload, faBookOpen, faUsers, faUser, faCog, faCommentDots, 
  faSignOutAlt, faUserCircle, faChevronUp, faBookReader, faCrown, faFlask,
  faAnglesRight
} from '@fortawesome/free-solid-svg-icons'
import FeedbackPanel from './FeedbackPanel.vue'
import AppHeader from './AppHeader.vue'

library.add(
  faGraduationCap, faTimes, faBook, faCircle, faChevronDown, faChevronRight,
  faUpload, faBookOpen, faUsers, faUser, faCog, faCommentDots, 
  faSignOutAlt, faUserCircle, faChevronUp, faBookReader, faCrown, faFlask,
  faAnglesRight
)

const { t } = useI18n()
const store = useStore()
const router = useRouter()

const isCollapsed = computed(() => store.getters.isSidebarCollapsed)
const expandedSections = ref({
  library: true,
  topics: false,
  userSection: false
})

const toggleSidebar = () => {
  store.dispatch('toggleSidebar')
}

const toggleSection = (section) => {
  expandedSections.value[section] = !expandedSections.value[section]
}

const toggleUserSection = () => {
  expandedSections.value.userSection = !expandedSections.value.userSection
}

const openFeedback = () => {
  store.dispatch('setFeedbackPanel', true)
}

const navigateHome = () => {
  router.push('/')
}
</script>

<style>
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
  --bg-dark: #1a1a2e;
  --bg-darker: #0f0f1e;
  --text-primary: #2c3e50;
  --text-secondary: #7f8c8d;
  --text-muted: #a0aec0;
  --accent-color: #5b5fc7;
  --accent-hover: #4a4eb8;
  --border-color: #e1e4e8;
  --sidebar-width: 240px;
  --sidebar-collapsed-width: 60px;
  --danger-color: #ef4444;
}

[data-theme="dark"] {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --bg-dark: #0f0f1e;
  --bg-darker: #0a0a14;
  --text-primary: #e4e4e7;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;
  --accent-color: #5b5fc7;
  --accent-hover: #4a4eb8;
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
  position: relative;
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-dark);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 100;
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 64px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s;
}

.logo-wrapper:hover {
  opacity: 0.8;
}

.logo-wrapper-collapsed {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  cursor: pointer;
  transition: transform 0.2s;
}

.logo-wrapper-collapsed:hover {
  transform: scale(1.1);
}

.logo-icon {
  font-size: 1.5rem;
  color: var(--accent-color);
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 1rem;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px 12px;
}

.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.nav-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s;
}

.section-header:hover {
  background: rgba(255, 255, 255, 0.05);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.5px;
}

.section-icon {
  font-size: 0.85rem;
}

.toggle-icon {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

.section-content {
  padding: 8px 12px;
}

.no-items {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
  padding: 8px 0;
}

.main-menu {
  margin-top: 24px;
  padding: 0 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  margin-bottom: 4px;
  font-size: 0.9rem;
  border: none;
  background: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
  font-family: inherit;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.menu-item.router-link-active {
  background: var(--accent-color);
  color: white;
}

.sidebar.collapsed .menu-item {
  justify-content: center;
  padding: 12px 8px;
}

.sidebar.collapsed .menu-item span {
  display: none;
}

.quick-actions {
  margin-top: 16px;
  padding: 0 4px;
  margin-bottom: 16px;
}

.quick-actions-header {
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.5px;
  padding: 10px 12px;
  margin-bottom: 4px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  text-align: left;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 16px;
  margin-bottom: 16px;
  padding: 0 4px;
}

.stat-card {
  background: var(--bg-darker);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.sidebar-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px 8px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-darker);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 8px;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.05);
}

.user-section-content {
  animation: slideDown 0.3s ease-out;
  overflow: hidden;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
}

.footer-nav {
  margin-top: 16px;
  padding: 0 4px;
}

.collapsed-footer-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: left;
}

.footer-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.footer-item.logout {
  color: var(--danger-color);
}

.footer-item.logout:hover {
  background: rgba(239, 68, 68, 0.1);
}

.user-avatar {
  font-size: 2rem;
  color: var(--accent-color);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-plan {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.expand-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
}

.expand-btn:hover {
  color: #ffffff;
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  padding: 0;
  overflow-y: auto;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed ~ .main-content {
  margin-left: var(--sidebar-collapsed-width);
}

.main-content-wrapper {
  flex: 1;
  padding: 90px 40px 40px 40px;
  overflow-y: auto;
}

/* Feedback Trigger Button */
.feedback-trigger {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: #ef4444;
  color: white;
  border: none;
  padding: 16px 12px;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  z-index: 99;
  box-shadow: -2px 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.feedback-trigger:hover {
  background: #dc2626;
  padding-right: 16px;
}

.page {
  max-width: 1200px;
}

.page h1 {
  margin-bottom: 20px;
  color: var(--text-primary);
}
</style>
