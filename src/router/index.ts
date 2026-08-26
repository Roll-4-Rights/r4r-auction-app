import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../pages/home-auction.vue') },
  { path: '/auction', name: 'Auction', component: () => import('../pages/auction-listings.vue') },
  { path: '/auction/:id', name: 'ItemDetail', component: () => import('../pages/item-detail.vue') },
  { path: '/account', name: 'Account', component: () => import('../pages/account.vue') },
  { path: '/charity', name: 'CharityInfo', component: () => import('../pages/charity-info.vue') },
  { path: '/current-campaign', name: 'CurrentCampaign', component: () => import('../pages/current-campaign-auction.vue') },
  { path: '/faq', name: 'Faq', component: () => import('../pages/faq.vue') },
  { path: '/donators', name: 'DonatorInfo', component: () => import('../pages/donator-info.vue') },
  { path: '/education', name: 'Education', component: () => import('../pages/education-resources.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})