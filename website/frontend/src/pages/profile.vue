<template>
  <div style="text-align: center">
    <div class="projects-area">
      <div>
        <h1 style="padding-left: 20px; font-family: Arial; font-weight: 150; font-size: 30px; color: #505050">
          <i class="el-icon-folder-checked"></i> Joined Projects | <strong style="font-size: 24px; color: #505050">Logged in as <strong style="font-size: 24px; color: #00CCFF">{{ username }}</strong></strong>
        </h1>
      </div>
      <div style="margin: 14px">
        <el-table
          class="projects-table"
          :data="projects_table"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828; ">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" in-line class="projects-table-expand">
                <el-form-item label="Project ID">
                  <span>{{ props.row.fields.proj_id }}</span>
                </el-form-item>
                <el-form-item label="Introduction">
                  <span>{{ props.row.fields.introduction }}</span>
                </el-form-item>
                <el-form-item label="Methods">
                  <span>{{ props.row.fields.methods }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
          label="Project Title"
          prop="fields.title">
          </el-table-column>
          <el-table-column
          label="Project Label"
          prop="fields.label"
          width="150px">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="Action"
            width="100px">
            <template slot-scope="scope" style="font-size: 20px">
              <el-button @click="handleView(scope.row)" size="small" icon="el-icon-view" circle></el-button>
              <el-button @click="handleQuit(scope.row)" type="danger" size="small" icon="el-icon-minus" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div class="projects-area">
      <div>
        <h1 style="float: left; padding-left: 20px; font-family: Arial; font-weight: 150; font-size: 30px; color: #505050">
          <i class="el-icon-folder-opened"></i> All Projects
        </h1>
      </div>
      <div style="margin: 14px">
        <el-input placeholder="Search projects by title or label" v-model="search_input" class="input-with-select" style="float: right; width: 50%">
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
      </div>
      <div style="margin: 14px">
        <el-table
          class="projects-table"
          :data="all_projects_table.filter(data => (!search_input || data.fields.title.toLowerCase().includes(search_input.toLowerCase()) || data.fields.label.toLowerCase().includes(search_input.toLowerCase()))).slice((currpage - 1) * pagesize, currpage * pagesize)"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828; ">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" in-line class="projects-table-expand">
                <el-form-item label="Project ID">
                  <span>{{ props.row.fields.proj_id }}</span>
                </el-form-item>
                <el-form-item label="Introduction">
                  <span>{{ props.row.fields.introduction }}</span>
                </el-form-item>
                <el-form-item label="Methods">
                  <span>{{ props.row.fields.methods }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
          label="Project Title"
          prop="fields.title">
          </el-table-column>
          <el-table-column
          label="Project Label"
          prop="fields.label"
          width="150px">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="Action"
            width="100px">
            <template slot-scope="scope" style="font-size: 20px">
              <el-button @click="handleJoin(scope.row)" size="small" icon="el-icon-plus" circle></el-button>
              <el-button @click="handleDelete(scope.row)" type="danger" size="small" icon="el-icon-delete" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="margin: 14px; padding-bottom: 30px">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="pagesize"
          :total="all_projects_table.length"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          style="float: left">
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  mounted () {
    this.username = sessionStorage.getItem('Username')
    this.user_id = sessionStorage.getItem('UserID')
    this.showJoinedProjects()
    this.showAllProjects()
  },
  data () {
    return {
      search_input: '',
      pagesize: 4,
      currpage: 1,
      username: '',
      user_id: '',
      projects_table: [],
      all_projects_table: []
    }
  },
  methods: {
    showJoinedProjects () {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      axios.get('/rest/api/v0/show_project_overview?user_id=' + sessionStorage.getItem('UserID'))
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.projects_table = res['list']
            console.log(this.projects_table)
            loading.close()
          } else {
            loading.close()
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    showAllProjects () {
      const loadingall = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      axios.get('/rest/api/v0/show_all_projects')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.all_projects_table = res['list']
            console.log(this.all_projects_table)
            loadingall.close()
          } else {
            loadingall.close()
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handleJoin (row) {
      axios.get('/rest/api/v0/join_project?proj_id=' + row.fields.proj_id + '&user_id=' + sessionStorage.getItem('UserID'))
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.$message({showClose: true, message: 'Successfully joined ' + row.fields.proj_id, type: 'success'})
            this.showJoinedProjects()
          } else {
            this.$message.warning(res['msg'])
            console.log(res['msg'])
          }
        })
    },
    handleDelete (row) {
      console.log(row.fields.proj_id)
      this.$confirm('Are you sure?', 'DELETE PROJECT!', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
      }).then(() => {
        axios.get('/rest/api/v0/delete_project?proj_id=' + row.fields.proj_id + '&user_id=' + sessionStorage.getItem('UserID'))
          .then(response => {
            var res = response.data
            if (res.error_num === 0) {
              console.log(res)
              this.showAllProjects()
              this.showJoinedProjects()
            } else {
              this.$message.error(res['msg'])
              console.log(res['msg'])
            }
          })
      }).catch(() => {})
    },
    handleQuit (row) {
      this.$confirm('Are you sure?', 'QUIT PROJECT!', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
      }).then(() => {
        axios.get('/rest/api/v0/quit_project?proj_id=' + row.fields.proj_id + '&user_id=' + sessionStorage.getItem('UserID'))
          .then(response => {
            var res = response.data
            if (res.error_num === 0) {
              console.log(res)
              this.$message({showClose: true, message: 'Successfully quitted ' + row.fields.proj_id, type: 'success'})
              this.showJoinedProjects()
            } else {
              this.$message.warning(res['msg'])
              console.log(res['msg'])
            }
          })
      }).catch(() => {})
    },
    handleCurrentChange (cpage) {
      this.currpage = cpage
    },
    handleSizeChange (psize) {
      this.pagesize = psize
    },
    handleView (row) {
      this.$router.push({
        name: 'project-overview',
        params: {projid: row.fields.proj_id, label: row.fields.label}
      })
    }
  }
}
</script>

<style lang="scss">
.profile-area {
  width: 772px;
  margin: 14px auto;
  text-align: left;
  padding: 14px;
  background-color: #FFFFFF;
  .profile-detail {
    padding: 14px;
    min-height: 200px;
    .github-link {
      padding-left: 20px;
      font-family: monospace;
      font-weight: 10;
      font-size: 20px;
      color: #282828;
      &:hover {
      color: #00CCFF;
      }
    }
  }
}
.projects-area {
  width: 772px;
  margin: 14px auto;
  padding: 14px;
  text-align: left;
  background-color: #FFFFFF;
}
.projects-table-expand {
  font-size: 0;
  width: 100%;
  }
  .projects-table-expand label {
    width: 140px;
    color: #505050;
  }
  .projects-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>
