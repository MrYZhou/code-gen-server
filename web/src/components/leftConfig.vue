<template>
  <el-drawer v-model="drawer" :direction="direction">
    <template #header>
      <h4>配置面板</h4>
    </template>
    <template #default>
      <div>
        <el-form :model="config" label-width="100px" :label-position="'left'">
          <el-form-item label="版本">
            <el-radio-group v-model="config.vueType" class="ml-4">
              <el-radio label="1" size="large">vue2</el-radio>
              <el-radio label="2" size="large">vue3</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="平台">
            <el-radio-group v-model="config.codeForm" class="ml-4">
              <el-radio label="1" size="large">uniapp</el-radio>
              <el-radio label="2" size="large">web</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="输出路径">
            <el-input v-model="config.output" placeholder="输出路径"></el-input>
          </el-form-item>
          <el-form-item label="过滤字段前缀">
            <el-input v-model="config.fieldPre" placeholder="前缀"></el-input>
          </el-form-item>
        </el-form>

        <el-row>
          <el-tag class="ml-2" type="success">数据库配置</el-tag>
        </el-row>

        <div class="mt10">
          <el-form
            :model="datbaseInfo"
            label-width="100px"
            :label-position="'left'"
          >
            <el-form-item label="连接地址">
              <el-input
                v-model="datbaseInfo.ip"
                placeholder="请输入"
              ></el-input>
            </el-form-item>
            <el-form-item label="连接端口">
              <el-input
                v-model="datbaseInfo.port"
                placeholder="请输入"
              ></el-input>
            </el-form-item>

            <el-form-item label="用户名">
              <el-input
                v-model="datbaseInfo.account"
                placeholder="请输入"
              ></el-input>
            </el-form-item>

            <el-form-item label="密码">
              <el-input
                v-model="datbaseInfo.password"
                placeholder="请输入"
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">关闭</el-button>
        <el-button type="primary" @click="confirmClick">确定</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { ElMessageBox } from 'element-plus'

const drawer = ref(true)
defineExpose({
  drawer,
})
const direction = ref('rtl')
const radio1 = ref('Option 1')
let config = reactive({ vueType: '1', codeForm: '1', output: '', fieldPre: '' })
let datbaseInfo = reactive({
  ip: '127.0.0.1',
  port: '3306',
  account: 'admin',
  password: '',
})
const handleClose = (done) => {
  ElMessageBox.confirm('Are you sure you want to close this?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}
function cancelClick() {
  drawer.value = false
}
function showPanel() {
  console.log(111)
  drawer.value = true
}
function confirmClick() {
  ElMessageBox.confirm(`Are you confirm to chose ${radio1.value} ?`)
    .then(() => {
      drawer.value = false
    })
    .catch(() => {
      // catch error
    })
}
// return {drawer}
</script>
