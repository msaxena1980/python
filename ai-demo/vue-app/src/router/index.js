import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('../views/Test.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue')
  },
  {
    path: '/subscription',
    name: 'Subscription',
    component: () => import('../views/Subscription.vue')
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('../views/Upload.vue')
  },
  {
    path: '/insta-study',
    name: 'InstaStudy',
    component: () => import('../views/InstaStudy.vue')
  },
  {
    path: '/group-study',
    name: 'GroupStudy',
    component: () => import('../views/GroupStudy.vue')
  },
  {
    path: '/study-center',
    name: 'StudyCenter',
    component: () => import('../views/StudyCenter.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
