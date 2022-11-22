// 默认的仓库
export const useMainStore = defineStore({
  //仓库标识
  id: 'main',
  // 仓库资源
  state: () => ({
    name: 'hello larry',
    tableInfo: [],
  }),
  // 快捷获取
  getters: {
    // 可以自己定义新的key,进行改造
    me: (state) => state.name.replace('hello', ''),
  },
  // 行为
  actions: {
    // async insertPost(data) {
    //   // 可以做异步
    //   // await doAjaxRequest(data);
    //   this.name = data
    // },

    insertTableInfo(data) {
      // await doAjaxRequest(data);
      this.tableInfo = [
        {
          lable: '字段1',
          field: 'key1',
        },
        {
          lable: '字段2',
          field: 'key2',
        },
      ]
      console.log(this.tableInfo, 11)
    },
  },
})
