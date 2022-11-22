<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header-wrap"><Header /></el-header>
      <el-main><drag-panel /></el-main>
      <el-footer class="footer-wrap"><footer></footer></el-footer>
    </el-container>
  </div>
</template>
<script setup>
import dragPanel from "./components/dragPanel.vue";
import Header from "./components/Header.vue";
</script>

<style scoped>
div.common-layout {
  height: 100vh;
  overflow: hidden;
}
.header-wrap {
  background: #ccc;
  position: fixed;
  width: 100%;
  height: 49px;
  opacity: 0;
}
.header-wrap:hover {
  opacity: 1;
}

.footer-wrap {
  background: #ccc;
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 49px;
  opacity: 0;
}

.footer-wrap:hover {
  opacity: 1;
}
</style>
