import { createStore } from 'vuex'

export default createStore({
  state: {
    sidebarCollapsed: false,
    theme: 'light'
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
    }
  },
  getters: {
    isSidebarCollapsed: state => state.sidebarCollapsed,
    currentTheme: state => state.theme
  }
})
