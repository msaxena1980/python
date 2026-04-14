<template>
  <header class="app-header">
    <div class="header-left">
      <button class="upgrade-btn" @click="$router.push('/subscription')">
        <font-awesome-icon icon="crown" />
        <span>{{ t('header.upgrade') }}</span>
      </button>
    </div>
    <div class="header-right">
      <span class="user-greeting">{{ t('header.greeting', { name: userName }) }}</span>
      <select v-model="selectedLocale" @change="changeLocale" class="language-select">
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="hi">हिन्दी</option>
      </select>
      <button class="theme-toggle" @click="toggleTheme" :title="currentTheme === 'light' ? t('common.darkMode') : t('common.lightMode')">
        <font-awesome-icon :icon="currentTheme === 'light' ? 'moon' : 'sun'" />
      </button>
      <button class="notification-btn" :title="t('header.notifications')" @click.stop="toggleNotifications">
        <font-awesome-icon icon="bell" />
        <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
      </button>
      <div v-if="showNotifications" class="notification-popup" @click.stop>
        <div class="notification-header">
          <h3>{{ t('header.notifications') }}</h3>
          <button v-if="notifications.length > 0" class="mark-read-btn" @click="markAllAsRead">
            {{ t('header.markAllRead') }}
          </button>
        </div>
        <div class="notification-list">
          <div v-if="notifications.length === 0" class="no-notifications">
            {{ t('header.noNotifications') }}
          </div>
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.read }"
            @click="markAsRead(notification.id)"
          >
            <div class="notification-icon" :class="notification.type">
              <font-awesome-icon :icon="getNotificationIcon(notification.type)" />
            </div>
            <div class="notification-content">
              <p class="notification-text">{{ notification.text }}</p>
              <span class="notification-time">{{ notification.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoon, faSun, faBell, faCrown, faInfoCircle, faCalendar, faCheckCircle, faClock } from '@fortawesome/free-solid-svg-icons'

library.add(faMoon, faSun, faBell, faCrown, faInfoCircle, faCalendar, faCheckCircle, faClock)

const store = useStore()
const { t, locale } = useI18n()

const userName = 'Manish'
const currentTheme = computed(() => store.getters.currentTheme)
const selectedLocale = ref(locale.value)
const showNotifications = ref(false)
const notifications = ref([
  { id: 1, text: 'New study materials added to Physics', time: '2 min ago', type: 'info', read: false },
  { id: 2, text: 'Your group study session starts in 30 minutes', time: '1 hour ago', type: 'event', read: false },
  { id: 3, text: 'Congratulations! You earned 50 credits', time: '3 hours ago', type: 'success', read: true },
  { id: 4, text: 'Reminder: Complete your daily practice quiz', time: '5 hours ago', type: 'reminder', read: true }
])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

const toggleTheme = () => {
  store.dispatch('toggleTheme')
}

const changeLocale = () => {
  locale.value = selectedLocale.value
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) notification.read = true
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

const getNotificationIcon = (type) => {
  const icons = {
    info: 'info-circle',
    event: 'calendar',
    success: 'check-circle',
    reminder: 'clock'
  }
  return icons[type] || 'bell'
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: var(--sidebar-width);
  right: 0;
  height: 70px;
  background: var(--bg-dark);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 90;
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Adjust header when sidebar is collapsed */
.sidebar.collapsed ~ .main-content .app-header {
  left: var(--sidebar-collapsed-width);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.upgrade-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.upgrade-btn:hover {
  background: linear-gradient(135deg, #d97706, #b45309);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.upgrade-btn svg {
  font-size: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.user-greeting {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.language-select {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.language-select:hover {
  border-color: var(--accent-color);
}

.language-select:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(91, 95, 199, 0.1);
}

.theme-toggle,
.notification-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s;
}

.theme-toggle:hover,
.notification-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.notification-btn {
  position: relative;
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

.notification-popup {
  position: absolute;
  top: 60px;
  right: 40px;
  width: 360px;
  max-height: 480px;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  z-index: 100;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.notification-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.mark-read-btn {
  background: none;
  border: none;
  color: var(--accent-color);
  font-size: 0.85rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.mark-read-btn:hover {
  background: rgba(91, 95, 199, 0.1);
}

.notification-list {
  max-height: 400px;
  overflow-y: auto;
}

.no-notifications {
  padding: 40px 20px;
  text-align: center;
  color: var(--text-secondary);
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 20px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.notification-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.notification-item.unread {
  background: rgba(91, 95, 199, 0.08);
  position: relative;
}

.notification-item.unread::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 6px;
  background: var(--accent-color);
  border-radius: 50%;
}

.notification-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.info {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.notification-icon.event {
  background: rgba(168, 85, 247, 0.2);
  color: #a855f7;
}

.notification-icon.success {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.notification-icon.reminder {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-text {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  color: var(--text-primary);
  line-height: 1.4;
}

.notification-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    padding: 0 20px;
  }
  
  .user-greeting {
    display: none;
  }
  
  .upgrade-btn span {
    display: none;
  }
  
  .upgrade-btn {
    padding: 10px 12px;
  }
}
</style>
