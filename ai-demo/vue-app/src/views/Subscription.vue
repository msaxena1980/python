<template>
  <div class="subscription-page">
    <!-- Current Plan Status -->
    <div class="current-plan-banner">
      <font-awesome-icon icon="circle-info" class="info-icon" />
      <span class="plan-status">
        <strong>{{ t('subscription.freePlan') }}</strong>
        <span class="separator">•</span>
        <span>15 {{ t('common.creditsRemaining') }}</span>
        <span class="separator">•</span>
        <span class="status-badge">{{ t('common.active') }}</span>
      </span>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <h1>{{ t('subscription.title') }}</h1>
      <p class="subtitle">{{ t('subscription.subtitle') }}</p>
    </div>

    <!-- Billing Cycle Toggle -->
    <div class="billing-toggle-section">
      <div class="billing-toggle">
        <button 
          :class="['toggle-btn', { active: billingCycle === 'monthly' }]"
          @click="billingCycle = 'monthly'"
        >
          {{ t('subscription.monthly') }}
        </button>
        <button 
          :class="['toggle-btn', { active: billingCycle === 'yearly' }]"
          @click="billingCycle = 'yearly'"
        >
          {{ t('subscription.yearly') }}
          <span class="save-label">{{ t('subscription.save') }} 8%</span>
        </button>
      </div>
    </div>

    <!-- Discount Options -->
    <div class="discount-section">
      <h3>{{ t('subscription.applyDiscount') }}</h3>
      <p class="discount-subtitle">{{ t('subscription.discountSubtitle') }}</p>
      <div class="discount-options">
        <button class="discount-btn">
          <font-awesome-icon icon="tag" />
          <span>{{ t('subscription.coupon') }}</span>
        </button>
        <button class="discount-btn">
          <font-awesome-icon icon="gift" />
          <span>{{ t('subscription.referral') }}</span>
        </button>
        <button class="discount-btn disabled">
          <font-awesome-icon icon="coins" />
          <span>{{ t('subscription.cashpoints') }}</span>
          <span class="badge-zero">0</span>
        </button>
      </div>
    </div>

    <!-- Pricing Plans -->
    <div class="pricing-grid">
      <!-- Free Plan -->
      <div class="pricing-card current">
        <div class="plan-badge current-badge">{{ t('subscription.currentPlan') }}</div>
        <h2 class="plan-name">{{ t('subscription.plans.free.name') }}</h2>
        <div class="plan-price">
          <span class="currency">₹</span>
          <span class="amount">0</span>
          <span class="period">{{ t('subscription.perMonth') }}</span>
        </div>
        <p class="plan-description">{{ t('subscription.plans.free.description') }}</p>
        <ul class="plan-features">
          <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.free.features.uploads') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.free.features.basicAI') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.free.features.limitedChat') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.free.features.library') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.free.features.mobile') }}</li>
        </ul>
        <button class="plan-button current-plan-btn" disabled>{{ t('subscription.currentPlan') }}</button>
      </div>

      <!-- Monthly/Yearly Plan -->
      <div class="pricing-card popular">
        <div class="plan-badge popular-badge">⭐ {{ t('subscription.mostPopular') }}</div>
        <h2 class="plan-name">{{ billingCycle === 'monthly' ? t('subscription.plans.monthly.name') : t('subscription.plans.yearly.name') }}</h2>
        <div class="plan-price">
          <span class="currency">₹</span>
          <span class="amount">{{ billingCycle === 'monthly' ? '500' : '5,000' }}</span>
          <span class="period">{{ billingCycle === 'monthly' ? t('subscription.perMonth') : t('subscription.perYear') }}</span>
        </div>
        <div v-if="billingCycle === 'yearly'" class="savings-note">
          {{ t('subscription.save') }} ₹1,000 (8% {{ t('subscription.off') }})
        </div>
        <p class="plan-description">{{ billingCycle === 'monthly' ? t('subscription.plans.monthly.description') : t('subscription.plans.yearly.description') }}</p>
        <ul class="plan-features">
          <template v-if="billingCycle === 'monthly'">
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.unlimitedUploads') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.advancedAI') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.unlimitedChat') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.groupStudy') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.hindiMode') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.instaCamera') }}</li>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.monthly.features.prioritySupport') }}</li>
          </template>
          <template v-else>
            <li><font-awesome-icon icon="check" class="check-icon" /> {{ t('subscription.plans.yearly.features.everything') }}</li>
            <li><font-awesome-icon icon="bolt" class="bolt-icon" /> {{ t('subscription.plans.yearly.features.priorityAI') }}</li>
            <li><font-awesome-icon icon="bolt" class="bolt-icon" /> {{ t('subscription.plans.yearly.features.analytics') }}</li>
            <li><font-awesome-icon icon="bolt" class="bolt-icon" /> {{ t('subscription.plans.yearly.features.customPlans') }}</li>
            <li><font-awesome-icon icon="bolt" class="bolt-icon" /> {{ t('subscription.plans.yearly.features.earlyAccess') }}</li>
            <li><font-awesome-icon icon="bolt" class="bolt-icon" /> {{ t('subscription.plans.yearly.features.dedicatedSupport') }}</li>
          </template>
        </ul>
        <button class="plan-button primary-btn">
          {{ t('subscription.startPlan', { plan: billingCycle === 'monthly' ? t('subscription.monthly') : t('subscription.yearly') }) }}
        </button>
      </div>

      <!-- Insta Pass -->
      <div class="pricing-card insta-pass">
        <h2 class="plan-name">{{ t('subscription.plans.instaPass.name') }}</h2>
        <div class="plan-price">
          <span class="currency">₹</span>
          <span class="amount">50</span>
          <span class="period">{{ t('subscription.perDays') }}</span>
        </div>
        <p class="plan-description">{{ t('subscription.plans.instaPass.description') }}</p>
        <ul class="plan-features">
          <li><font-awesome-icon icon="check" class="check-icon purple" /> {{ t('subscription.plans.instaPass.features.unlimited') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon purple" /> {{ t('subscription.plans.instaPass.features.allFeatures') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon purple" /> {{ t('subscription.plans.instaPass.features.camera') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon purple" /> {{ t('subscription.plans.instaPass.features.exams') }}</li>
          <li><font-awesome-icon icon="check" class="check-icon purple" /> {{ t('subscription.plans.instaPass.features.noCommitment') }}</li>
        </ul>
        <button class="plan-button insta-btn">{{ t('subscription.getPlan', { plan: t('subscription.instaPass') }) }}</button>
      </div>
    </div>

    <!-- Footer Note -->
    <div class="footer-note">
      <p>{{ t('subscription.creditsNote') }} <a href="#">{{ t('common.readMore') }}</a></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCircleInfo, faTag, faGift, faCoins, faCheck, faBolt } from '@fortawesome/free-solid-svg-icons'

library.add(faCircleInfo, faTag, faGift, faCoins, faCheck, faBolt)

const { t } = useI18n()
const billingCycle = ref('monthly')
</script>

<style scoped>
.subscription-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.current-plan-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 32px;
}

.info-icon {
  color: var(--accent-color);
  font-size: 1.2rem;
}

.plan-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.separator {
  color: var(--text-secondary);
}

.status-badge {
  background: #10b981;
  color: white;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.billing-toggle-section {
  display: flex;
  justify-content: center;
  margin-bottom: 48px;
}

.billing-toggle {
  display: inline-flex;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  padding: 6px;
  gap: 6px;
}

.toggle-btn {
  padding: 12px 32px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-btn.active {
  background: var(--accent-color);
  color: white;
  box-shadow: 0 2px 8px rgba(91, 95, 199, 0.3);
}

.save-label {
  font-size: 0.75rem;
  background: #10b981;
  color: white;
  padding: 2px 8px;
  border-radius: 8px;
  font-weight: 700;
}

.toggle-btn:not(.active) .save-label {
  background: var(--bg-secondary);
  color: #10b981;
}

.discount-section {
  text-align: center;
  margin-bottom: 48px;
}

.discount-section h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.discount-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.discount-options {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.discount-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.discount-btn:hover:not(.disabled) {
  border-color: var(--accent-color);
  background: var(--bg-secondary);
}

.discount-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.badge-zero {
  background: var(--bg-secondary);
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 0.85rem;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.pricing-card {
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: 16px;
  padding: 32px 24px;
  position: relative;
  transition: all 0.3s;
}

.pricing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.pricing-card.current {
  border-color: #10b981;
}

.pricing-card.popular {
  border-color: var(--accent-color);
  border-width: 3px;
}

.pricing-card.insta-pass {
  background: linear-gradient(135deg, #f3e7ff 0%, #e9d5ff 100%);
  border-color: #a855f7;
}

.plan-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.current-badge {
  background: #10b981;
  color: white;
}

.popular-badge {
  background: var(--accent-color);
  color: white;
}

.save-badge {
  background: #10b981;
  color: white;
}

.plan-name {
  font-size: 1.8rem;
  color: var(--text-primary);
  margin: 20px 0 16px;
  text-align: center;
}

.plan-price {
  text-align: center;
  margin-bottom: 16px;
}

.currency {
  font-size: 1.5rem;
  color: var(--text-secondary);
  font-weight: 600;
  vertical-align: top;
}

.amount {
  font-size: 3rem;
  color: var(--text-primary);
  font-weight: 700;
  line-height: 1;
}

.period {
  font-size: 1rem;
  color: var(--text-secondary);
}

.plan-description {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 24px;
  font-size: 0.95rem;
  min-height: 48px;
}

.savings-note {
  text-align: center;
  color: #10b981;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 12px;
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 6px;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.plan-features li {
  padding: 10px 0;
  color: var(--text-primary);
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-icon {
  color: #10b981;
  font-size: 1.1rem;
}

.check-icon.purple {
  color: #a855f7;
}

.bolt-icon {
  color: #f59e0b;
  font-size: 1.1rem;
}

.plan-button {
  width: 100%;
  padding: 14px 24px;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.current-plan-btn {
  background: #10b981;
  color: white;
  cursor: not-allowed;
  opacity: 0.7;
}

.primary-btn {
  background: #000;
  color: white;
}

.primary-btn:hover {
  background: #1f1f1f;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.secondary-btn {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 2px solid var(--text-primary);
}

.secondary-btn:hover {
  background: var(--text-primary);
  color: var(--bg-primary);
  transform: translateY(-2px);
}

.insta-btn {
  background: #a855f7;
  color: white;
}

.insta-btn:hover {
  background: #9333ea;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
}

.footer-note {
  text-align: center;
  padding: 20px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.footer-note a {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
}

.footer-note a:hover {
  text-decoration: underline;
}
</style>
