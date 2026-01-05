import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import DesertersPage from '../pages/DesertersPage.vue'
import DeserterDetailPage from '../pages/DeserterDetailPage.vue'
import LotteryPage from '../pages/LotteryPage.vue'
import MilitaryPage from '../pages/MilitaryPage.vue'
import NewSoldierGuidePage from '../pages/NewSoldierGuidePage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/deserters',
    name: 'Deserters',
    component: DesertersPage
  },
  {
    path: '/deserters/:id',
    name: 'DeserterDetail',
    component: DeserterDetailPage
  },
  {
    path: '/lottery',
    name: 'Lottery',
    component: LotteryPage
  },
  {
    path: '/military',
    name: 'Military',
    component: MilitaryPage
  },
  {
    path: '/new-soldier-guide',
    name: 'NewSoldierGuide',
    component: NewSoldierGuidePage
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../pages/AboutPage.vue')  
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
