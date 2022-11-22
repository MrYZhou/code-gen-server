import { RouteRecordRaw } from 'vue-router'

export const useSystemStore = defineStore({
  //仓库标识
  id: 'system',
  // 仓库资源
  state: () => ({
    dynamicRoute: [],
  }),
  // 快捷获取
  getters: {
    // 可以自己定义新的key,进行改造
  },
  // 行为
  actions: {
    getDynamicRoute(data?: string): RouteRecordRaw[] {
      return [
        {
          path: '/Login2',
          name: 'Login2',
          component: () => import('@/pages/login/Login.vue'),
        },
      ]
    },
  },
})
