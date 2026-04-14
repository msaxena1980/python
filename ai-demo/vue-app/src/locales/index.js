import { createI18n } from 'vue-i18n'
import en from './en.json'
import fr from './fr.json'
import hi from './hi.json'

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    fr,
    hi
  }
})

export default i18n
