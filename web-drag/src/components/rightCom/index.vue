<script setup lang="ts">
import { onMounted } from 'vue'

import { useMainStore } from '../../store'
const store = useMainStore()

// props定义
type Props = {
  data
  indexKey
}
defineProps<Props>()
// 生命周期
onMounted(() => {})
</script>

<template>
  <div v-for="(item, index) in data">
    <div v-if="index == indexKey">
      <el-row>
        <el-col :span="5">字段</el-col>
        <el-col :span="19">
          <el-select v-model="item.configModel.value" placeholder="Select">
            <el-option
              v-for="item in store.tableInfo"
              :key="item.field"
              :label="item.label"
              :value="item.field"
            />
          </el-select>
        </el-col>
      </el-row>
      <el-row v-if="item.configModel.hasOwnProperty('placeholder')">
        <el-col :span="5">默认值</el-col>
        <el-col :span="19">
          <el-input v-model="item.configModel.placeholder"></el-input>
        </el-col>
      </el-row>

      <el-row v-if="item.configModel.hasOwnProperty('disabled')">
        <el-col :span="5">可编辑</el-col>
        <el-col :span="8">
          <el-radio-group v-model="item.configModel.disabled" class="ml-4">
            <el-radio :label="true" size="large">是</el-radio>
            <el-radio :label="false" size="large">否</el-radio>
          </el-radio-group>
        </el-col>
      </el-row>

      <el-row v-if="item.configModel.hasOwnProperty('required')">
        <el-col :span="5">必填</el-col>
        <el-col :span="8">
          <el-radio-group v-model="item.configModel.required" class="ml-4">
            <el-radio :label="true" size="large">是</el-radio>
            <el-radio :label="false" size="large">否</el-radio>
          </el-radio-group>
        </el-col>
      </el-row>

      <!-- <el-row>
          <el-col>{{item.configModel}}</el-col>
          <el-col></el-col>
        </el-row>

        <el-row>
          <el-col>{{item.configModel}}</el-col>
          <el-col></el-col>
        </el-row>

        <el-row>
          <el-col>{{item.configModel}}</el-col>
          <el-col></el-col>
        </el-row> -->
    </div>
  </div>
</template>

<style scoped>
.el-row {
  line-height: 50px;
  height: 50px;
}
.el-select {
  width: 100%;
}
</style>
