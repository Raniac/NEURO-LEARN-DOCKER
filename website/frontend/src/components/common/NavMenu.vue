<template>
  <div>
    <el-menu default-active="1" id="nav-menu" :default-openeds="['2', '3', '3-2']">
      <div class="logo">
        <router-link to="/home" class="nav-title">
          NEURO-LEARN
        </router-link>
      </div>
      <el-menu-item index="1"><router-link to="/profile" class="nav-link"><i class="el-icon-user"></i> User Profile</router-link></el-menu-item>
      <el-submenu index="2">
        <template slot="title">
          <div>
            <i class="el-icon-folder-opened"></i>
            <span style="font-size: 16px; color: #E8E8E8">Projects</span>
          </div>
        </template>
        <el-menu-item index="2-1"><router-link to="/projects/overview" class="nav-link"><i class="el-icon-files"></i> Overview</router-link></el-menu-item>
        <el-menu-item index="2-2"><router-link to="/projects/data" class="nav-link"><i class="el-icon-upload"></i> Data</router-link></el-menu-item>
        <el-submenu index="2-3">
          <template slot="title">
            <div>
              <i class="el-icon-document-add"></i>
              <span style="font-size: 16px; color: #E8E8E8">New Project</span>
            </div>
          </template>
          <el-menu-item index="2-3-1"><router-link to="/projects/newproj/beta" class="nav-link"><i class="el-icon-edit-outline"></i> Beta</router-link></el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">
          <div>
            <i class="el-icon-pie-chart"></i>
            <span style="font-size: 16px; color: #E8E8E8">Analysis</span>
          </div>
        </template>
        <el-menu-item index="3-1"><router-link to="/analysis/overview" class="nav-link"><i class="el-icon-menu"></i> Overview</router-link></el-menu-item>
        <el-submenu index="3-2">
          <template slot="title">
            <div>
              <i class="el-icon-s-order"></i>
              <span style="font-size: 16px; color: #E8E8E8">New Task</span>
            </div>
          </template>
          <el-menu-item index="3-2-1"><router-link to="/analysis/newtask/newsa" class="nav-link"><i class="el-icon-sugar"></i> Statistical Analysis</router-link></el-menu-item>
          <el-menu-item index="3-2-2"><router-link to="/analysis/newtask/newml" class="nav-link"><i class="el-icon-lollipop"></i> Machine Learning</router-link></el-menu-item>
          <el-menu-item index="3-2-3"><router-link to="/analysis/newtask/newsgn" class="nav-link"><i class="el-icon-ice-cream-round"></i> SchizoGraphNet</router-link></el-menu-item>
        </el-submenu>
        <el-menu-item index="3-3"><router-link to="/analysis/submissions" class="nav-link"><i class="el-icon-document-copy"></i> Submissions</router-link></el-menu-item>
        <el-menu-item index="3-4"><router-link to="/analysis/viewer" class="nav-link"><i class="el-icon-view"></i> Viewer</router-link></el-menu-item>
      </el-submenu>
      <el-menu-item index="4"><a target="_blank" href="https://github.com/Raniac/NEURO-LEARN-DOCKER/" class="nav-link"><i class="el-icon-notebook-2"></i> GitHub Repository</a></el-menu-item>
    </el-menu>
  </div>
</template>

<style lang='scss'>
#nav-menu {
  width: 250px;
  min-width: 250px;
  height: 100%;
  background-color: #282828;
  border-right-color: #282828;
  box-shadow: 5px 0 20px rgba(0,0,0,.3);
  position: fixed;
  z-index: 10;
  .logo {
    width: 250px;
    height: 65px;
    text-align: center;
    background-color: #282828;
  }
  .nav-title {
    display: block;
    padding-top: 20px;
    font-size: 25px;
    font-weight: 600;
    color: #00CCFF;
  }
  .nav-link {
    display: block;
    font-size: 16px;
  }
  .el-menu {
    background-color: #282828;
  }
  .el-menu-item,
  .el-submenu .el-submenu__title {
    height: 44px;
    line-height: 44px;
    color: #E8E8E8;
    &:hover {
      background-color: #505050;
    }
  }
  .router-link-active {
    color: #00CCFF;
  }
}
</style>

<script>
export default {
}
</script>
