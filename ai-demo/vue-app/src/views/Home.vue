<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">{{ t('home.hero.title') }}</h1>
        <p class="hero-subtitle">{{ t('home.hero.subtitle') }}</p>
        <button class="cta-button" @click="$router.push('/upload')">
          {{ t('home.hero.cta') }}
          <font-awesome-icon icon="arrow-right" />
        </button>
      </div>
      <div class="hero-image">
        <font-awesome-icon icon="graduation-cap" class="hero-icon" />
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">{{ t('home.features.title') }}</h2>
      <div class="features-grid">
        <div 
          v-for="feature in features" 
          :key="feature.id"
          class="feature-card"
          @click="$router.push(feature.route)"
        >
          <div class="feature-icon" :class="feature.colorClass">
            <font-awesome-icon :icon="feature.icon" />
          </div>
          <h3 class="feature-title">{{ t(`home.features.${feature.id}.title`) }}</h3>
          <p class="feature-description">{{ t(`home.features.${feature.id}.description`) }}</p>
          <div class="feature-arrow">
            <font-awesome-icon icon="arrow-right" />
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="stat-item">
        <div class="stat-number">1000+</div>
        <div class="stat-label">{{ t('home.stats.students') }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">50K+</div>
        <div class="stat-label">{{ t('home.stats.documents') }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">98%</div>
        <div class="stat-label">{{ t('home.stats.satisfaction') }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">24/7</div>
        <div class="stat-label">{{ t('home.stats.support') }}</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { 
  faGraduationCap, faArrowRight, faUpload, faBookOpen, 
  faUsers, faBookReader, faBrain, faChartLine
} from '@fortawesome/free-solid-svg-icons'

library.add(faGraduationCap, faArrowRight, faUpload, faBookOpen, faUsers, faBookReader, faBrain, faChartLine)

const { t } = useI18n()

const features = [
  {
    id: 'upload',
    icon: 'upload',
    colorClass: 'blue',
    route: '/upload'
  },
  {
    id: 'instaStudy',
    icon: 'book-open',
    colorClass: 'green',
    route: '/insta-study'
  },
  {
    id: 'groupStudy',
    icon: 'users',
    colorClass: 'purple',
    route: '/group-study'
  },
  {
    id: 'studyCenter',
    icon: 'book-reader',
    colorClass: 'orange',
    route: '/study-center'
  },
  {
    id: 'aiExplanations',
    icon: 'brain',
    colorClass: 'pink',
    route: '/test'
  },
  {
    id: 'trackProgress',
    icon: 'chart-line',
    colorClass: 'teal',
    route: '/profile'
  }
]
</script>

<style scoped>
.home-page {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  margin-bottom: 80px;
  padding: 40px 0;
}

.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 24px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 32px;
  line-height: 1.6;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 36px;
  background: var(--accent-color);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(91, 95, 199, 0.3);
}

.cta-button:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(91, 95, 199, 0.4);
}

.hero-image {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-color) 0%, #7c3aed 100%);
  border-radius: 24px;
  padding: 80px;
  box-shadow: 0 20px 60px rgba(91, 95, 199, 0.2);
}

.hero-icon {
  font-size: 12rem;
  color: white;
  opacity: 0.9;
}

/* Features Section */
.features-section {
  margin-bottom: 80px;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 48px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color), #7c3aed);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--accent-color);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: white;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-icon.blue { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.feature-icon.green { background: linear-gradient(135deg, #10b981, #059669); }
.feature-icon.purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
.feature-icon.orange { background: linear-gradient(135deg, #f59e0b, #d97706); }
.feature-icon.pink { background: linear-gradient(135deg, #ec4899, #db2777); }
.feature-icon.teal { background: linear-gradient(135deg, #14b8a6, #0d9488); }

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.feature-description {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.feature-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-secondary);
  color: var(--accent-color);
  transition: all 0.3s;
}

.feature-card:hover .feature-arrow {
  background: var(--accent-color);
  color: white;
  transform: translateX(4px);
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
  padding: 60px;
  background: linear-gradient(135deg, var(--accent-color) 0%, #7c3aed 100%);
  border-radius: 24px;
  margin-bottom: 40px;
}

.stat-item {
  text-align: center;
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero-section {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .hero-image {
    padding: 60px;
  }
  
  .hero-icon {
    font-size: 8rem;
  }
  
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
    padding: 40px 20px;
  }
  
  .stat-number {
    font-size: 2rem;
  }
}
</style>
