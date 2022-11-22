<template>
  <!-- 左侧配置面板 -->
  <leftConfig ref="leftconfig"></leftConfig>

  <!-- 拖拽主布局 -->

  <div class="larry">
    <div class="btn-group">
      <div><el-button @click="doConfig" :icon="Tools"></el-button></div>
      <div><el-button @click="doView" :icon="View"></el-button></div>
      <div><el-button @click="doDownload" :icon="Download"></el-button></div>
    </div>
    <div class="group group-con-show">
      <draggable
        :sort="false"
        itemKey="k1"
        :list="state.modules.arr1"
        ghost-class="ghost"
        handle=".move"
        filter=".forbid"
        :force-fallback="true"
        chosen-class="chosenClass"
        animation="300"
        :group="{ name: 'larry', pull: 'clone', put: 'false' }"
        :move="onMove"
        @onSort="onSortA"
      >
        <template #item="{ element }">
          <div @click="addItem(element)" class="item item-control move">
            <label>{{ element.name }}</label>
          </div>
        </template>
      </draggable>
    </div>
    <div class="group group-show">
      <draggable
        style="height: 100%"
        :list="state.modules.arr2"
        ghost-class="ghost"
        itemKey="k2"
        handle=".move"
        filter=".forbid"
        :force-fallback="true"
        chosen-class="chosenClass"
        animation="300"
        group="larry"
        :onSort="onSortB"
        :move="onMove"
      >
        <template #item="{ element }">
          <div style="position: relative; margin-bottom: 10px">
            <div class="item move">
              <label>{{ element.name }} </label>
            </div>
            <div>
              <el-icon
                class="delete-icon"
                @click.prevent="deleateControl(element)"
              >
                <Delete />
              </el-icon>
            </div>
          </div>
        </template>
      </draggable>
    </div>
    <div class="group group-form">
      <div class="wrap-form">
        <rightCom
          :data="state.modules.arr2"
          :indexKey="state.indexKey"
        ></rightCom>
      </div>
    </div>
  </div>
  <!-- 日志输出和表单属性配置,可在配置面板开启 -->
  <!-- <div class="config-info">
    <el-row>
    :group="{ name: 'larry', put: 'true' }"
      <el-col :span="12">日志</el-col>
      <el-col :span="12">表单</el-col>
    </el-row>
  </div> -->
</template>
<script setup>
import draggable from 'vuedraggable'
import leftConfig from './leftConfig.vue'
import rightCom from './rightCom/index.vue'
import { useMainStore } from '@/store'

import { View, Tools, Download } from '@element-plus/icons-vue'

const store = useMainStore()

onMounted(() => {
  
})

const state = reactive({
  indexKey: -1,
  configModel: {},
  modules: {
    arr1: [
      { name: '输入框', id: 1 },
      { name: '下拉框', id: 2 },
      { name: '按钮', id: 3 },
      { name: '时间选择', id: 4 },
    ],
    arr2: [
      // { name: "B组", id: 5 ,itemKey:5},
      // { name: "员工", id: 6 ,itemKey:6},
      // { name: "报表", id: 7 ,itemKey:7},
      // { name: "库存", id: 8 ,itemKey:8},
    ],
  },
})

// 显示控制面板
const leftconfig = ref()
const doConfig = () => {
  leftconfig.value.drawer = true
}
//预览
const doView = () => {
  tableInfo()
}
// 下载
const doDownload = () => {
  tableInfo()
}

let tableInfo = () => {
  store.insertTableInfo(11)
  console.log(store.state, store)
}
// 控件操作
let deleateControl = (element) => {
  if (!element) element = { id: -1 }

  let array = state.modules.arr2
  for (let index = 0; index < array.length; index++) {
    const item = array[index]
    if (item.id == element.id) {
      state.modules.arr2.splice(index, 1)
      break
    }
  }
}

let addItem = (control) => {
  // if (control.name === "输入框") {
  // }
  // control.id = +new Date()
  state.modules.arr2.push(control)

  control.configModel = {
    value: '',
    field: '',
    label: '字段',
    disabled: true,
    placeholder: '输入值',
    required: false,
    relationOptions: [],
    adptorFun: () => {},
  }
  state.indexKey = state.modules.arr2.length - 1
  console.log(state.indexKey)
}

// 拖拽方法
const onSortA = (e, originalEvent) => {}
//当插入、移除、改变位置时会触发该事件
const onSortB = (e) => {
  console.log(e)
  // focus();
  state.message = JSON.stringify(state.modules.arr2)
}

const onMove = (e, originalEvent) => {
  console.log(e)
  //不允许停靠到A组的第一个元素
  if (e.relatedContext.element?.disabledPark == true) {
    state.message = '不允许停靠到A组的第一个元素'
    return false
  }

  return true
}
</script>
<style type="scss">
.larry {
  background-color: #f1f1f1;
  display: flex;
  margin-top: 10px;
  justify-content: space-between;
  padding: 20px;
  min-width: 990px;
}
.wrap-form {
  display: inline-block;
}
.btn-group div {
  margin-bottom: 5px;
}
.group {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-content: center;
  width: 46%;
}
.group-con-show {
  border: 1px solid #51c4d3;
  padding: 20px 0;
  display: flex;
  /* justify-content: space-between; */
  text-align: center;
  /* align-items: center; */
  width: 300px;
  height: 80vh;
  background-color: #fff;
  margin: 0 10px;
}

.group-form {
  border: 1px solid #51c4d3;
  padding: 20px;
  width: 50%;
  height: 80vh;
  background-color: #fff;
}
.config-info {
  border: 1px solid red;
  margin: 20px;
  padding: 20px;
  height: 30vh;
}
.group-show {
  border: 1px solid #51c4d3;
  padding: 20px;
  width: 50%;
  height: 80vh;
  overflow-y: scroll;
  background-color: #fff;
  margin: 0 10px;
}
.group-show::-webkit-scrollbar {
  display: none;
}
.delete-icon {
  position: absolute;
  /* width: 24px; */
  font-size: 22px;
  padding: 10px;
  /* background-color: aliceblue; */
  right: 6px;
  /* right: -39px; */
  top: -16px;
  z-index: 9999;
  border-radius: 50%;
  /* border: 1px solid #ccc; */
  /* border: 1px solid red; */
}
.delete-icon:hover {
  color: rgb(206, 103, 103);
  background-color: #f1f1f1;
}
.item {
  border: solid 1px #ddd;
  padding: 0px;
  text-align: left;
  background-color: #fff;
  display: flex;
  align-items: center;
  height: 36px;
  /* line-height: 38px; */
  /* user-select: none; */
}
.item-control {
  display: inline-block;
  width: 100px;
  height: 45px;
  line-height: 45px;
  margin: 3px;
  text-align: center;
}

.item > label {
  padding: 6px 10px;
  color: #333;
}
.item > label:hover {
  cursor: move;
}
.item > span {
  padding: 6px 10px;
  color: #666;
}
.ghost {
  border: solid 1px pink !important;
}
.chosenClass {
  opacity: 1;
  border: solid 1px #ccc;
}
.fallbackClass {
  background-color: aquamarine;
}
</style>
