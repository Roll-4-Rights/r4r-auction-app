import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../pages/Home.vue') },
  { path: '/auction', name: 'Auction', component: () => import('../pages/AuctionListings.vue') },
  { path: '/auction/:id', name: 'ItemDetail', component: () => import('../pages/ItemDetail.vue') },
  { path: '/account', name: 'Account', component: () => import('../pages/Account.vue') },
  { path: '/charity', name: 'CharityInfo', component: () => import('../pages/CharityInfo.vue') },
  { path: '/faq', name: 'Faq', component: () => import('../pages/Faq.vue') },
  { path: '/donators', name: 'DonatorInfo', component: () => import('../pages/DonatorInfo.vue') },
  { path: '/education', name: 'Education', component: () => import('../pages/EducationResources.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})