import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('./views/layout/index.vue'),
      redirect: '/yearly', // 将history设为首页home
      children: [
        {
          path: 'yearly',
          name: 'yearly',
          component: () => import('./views/yearly/index.vue')
        },
        {
          path: 'history',
          name: 'history',
          component: () => import('./views/history/index.vue')
        },
        {
          path: 'manage',
          name: 'manage',
          component: () => import('./views/manage/index.vue'),
        },
        {
          path: 'overview',
          name: 'overview',
          component: () => import('./views/overview/index.vue')
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      // lazy loading
      component: () => import('./views/login/index.vue')
    },
    {
      path: '/404',
      name: '404',
      // lazy loading
      component: () => import('./components/Page404.vue')
    },
    // 添加通配符路由，匹配所有未定义的路径
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    }
  ]
})

export default router