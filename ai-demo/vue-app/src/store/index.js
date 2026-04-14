import { createStore } from 'vuex'

export default createStore({
  state: {
    sidebarCollapsed: false,
    theme: 'light',
    feedbackPanelOpen: false
  },
  mutations: {
    TOGGLE_SIDEBAR(state) {
      state.sidebarCollapsed = !state.sidebarCollapsed
    },
    SET_SIDEBAR(state, collapsed) {
      state.sidebarCollapsed = collapsed
    },
    SET_THEME(state, theme) {
      state.theme = theme
      document.documentElement.setAttribute('data-theme', theme)
    },
    TOGGLE_THEME(state) {
      state.theme = state.theme === 'light' ? 'dark' : 'light'
      document.documentElement.setAttribute('data-theme', state.theme)
    },
    TOGGLE_FEEDBACK_PANEL(state) {
      state.feedbackPanelOpen = !state.feedbackPanelOpen
    },
    SET_FEEDBACK_PANEL(state, open) {
      state.feedbackPanelOpen = open
    }
  },
  actions: {
    toggleSidebar({ commit }) {
      commit('TOGGLE_SIDEBAR')
    },
    setSidebar({ commit }, collapsed) {
      commit('SET_SIDEBAR', collapsed)
    },
    toggleTheme({ commit }) {
      commit('TOGGLE_THEME')
    },
    toggleFeedbackPanel({ commit }) {
      commit('TOGGLE_FEEDBACK_PANEL')
    },
    setFeedbackPanel({ commit }, open) {
      commit('SET_FEEDBACK_PANEL', open)
    }
  },
  getters: {
    isSidebarCollapsed: state => state.sidebarCollapsed,
    currentTheme: state => state.theme,
    isFeedbackPanelOpen: state => state.feedbackPanelOpen
  }
})
