<template>
  <div style="text-align: center">
    <div class="submissions-area">
      <el-tabs @tab-click="handleTabClick" stretch v-model="tabsValue">
        <el-tab-pane label="Machine Learning" name="Machine Learning">
          <div style="margin: 14px">
            <el-input placeholder="Search machine learning tasks by name" v-model="search_input" class="input-with-select">
              <el-select v-model="selected_status" slot="prepend" placeholder="Status" @change="onStatusSelected">
                <el-option label="Total" value=""></el-option>
                <el-option label="Submitted" value="Submitted"></el-option>
                <el-option label="Running" value="Running"></el-option>
                <el-option label="Finished" value="Finished"></el-option>
                <el-option label="Failed" value="Failed"></el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-search" @click="onSearch"></el-button>
            </el-input>
          </div>
          <div style="margin: 14px">
            <el-table
              class="submissions-table"
              :data="submissions_table"
              stripe
              border
              @selection-change="onSelectionChange"
              ref="multipleTable"
              type="selection"
              style="width: 100%; background-color: #E8E8E8; color: #282828">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="Task ID">
                      <span>{{ props.row.fields.task_id }}</span>
                    </el-form-item>
                    <el-form-item label="Proj. Name">
                      <span>{{ props.row.fields.proj_name }}</span>
                    </el-form-item>
                    <el-form-item label="Train Data">
                      <span>{{ props.row.fields.train_data }}</span>
                    </el-form-item>
                    <el-form-item label="Test Data">
                      <span>{{ props.row.fields.test_data }}</span>
                    </el-form-item>
                    <el-form-item label="Label">
                      <span>{{ props.row.fields.label }}</span>
                    </el-form-item>
                    <el-form-item label="Feat. Sel.">
                      <span>{{ props.row.fields.feat_sel }}</span>
                    </el-form-item>
                    <el-form-item label="Estimator">
                      <span>{{ props.row.fields.estimator }}</span>
                    </el-form-item>
                    <el-form-item label="CV Type">
                      <span>{{ props.row.fields.cv_type }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column
              label="Task Name"
              prop="fields.task_name">
              </el-table-column>
              <el-table-column
              label="Task Type"
              prop="fields.task_type"
              width="120">
              </el-table-column>
              <el-table-column
              label="Status"
              prop="fields.task_status"
              width="100">
                <template slot-scope="scope">
                  <el-tag
                    size="small"
                    :type="scope.row.fields.task_status === 'Finished' ? 'success' : (scope.row.fields.task_status === 'Failed' ? 'danger' : (scope.row.fields.task_status === 'Running' ? 'primary' : 'info'))">
                    {{ scope.row.fields.task_status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                type="selection"
                width="40">
              </el-table-column>
            </el-table>
          </div>
          <div style="margin: 14px; padding-bottom: 30px">
            <el-pagination
              background
              layout="sizes, prev, pager, next"
              :page-sizes="[10, 15, 20, 25, 30]"
              :page-size="pagesize"
              :total="totalsize"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              style="float: left">
            </el-pagination>
            <el-tooltip content="View the report(s) of selected task(s)" placement="top">
              <el-button style="float: right" size="large" type="primary" @click="clickToView">View</el-button>
            </el-tooltip>
          </div>
        </el-tab-pane>
        <el-tab-pane label="SchizoGraphNet" name="SchizoGraphNet">
          <div style="margin: 14px">
            <el-input placeholder="Search SchizoGraphNet tasks by name" v-model="search_input" class="input-with-select">
              <el-select v-model="selected_status" slot="prepend" placeholder="Status" @change="onStatusSelected">
                <el-option label="Total" value=""></el-option>
                <el-option label="Submitted" value="Submitted"></el-option>
                <el-option label="Running" value="Running"></el-option>
                <el-option label="Finished" value="Finished"></el-option>
                <el-option label="Failed" value="Failed"></el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-search" @click="onSearch"></el-button>
            </el-input>
          </div>
          <div style="margin: 14px">
            <el-table
              class="submissions-table"
              :data="submissions_table"
              stripe
              border
              @selection-change="onSelectionChange"
              ref="multipleTable"
              type="selection"
              style="width: 100%; background-color: #E8E8E8; color: #282828">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="Task ID">
                      <span>{{ props.row.fields.task_id }}</span>
                    </el-form-item>
                    <el-form-item label="Proj. Name">
                      <span>{{ props.row.fields.proj_name }}</span>
                    </el-form-item>
                    <el-form-item label="Train Data">
                      <span>{{ props.row.fields.train_data }}</span>
                    </el-form-item>
                    <el-form-item label="Test Data">
                      <span>{{ props.row.fields.test_data }}</span>
                    </el-form-item>
                    <el-form-item label="Label">
                      <span>{{ props.row.fields.label }}</span>
                    </el-form-item>
                    <el-form-item label="Feat. Sel.">
                      <span>{{ props.row.fields.feat_sel }}</span>
                    </el-form-item>
                    <el-form-item label="Estimator">
                      <span>{{ props.row.fields.estimator }}</span>
                    </el-form-item>
                    <el-form-item label="CV Type">
                      <span>{{ props.row.fields.cv_type }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column
              label="Task Name"
              prop="fields.task_name">
              </el-table-column>
              <el-table-column
              label="Task Type"
              prop="fields.task_type"
              width="120">
              </el-table-column>
              <el-table-column
              label="Status"
              prop="fields.task_status"
              width="100">
                <template slot-scope="scope">
                  <el-tag
                    size="small"
                    :type="scope.row.fields.task_status === 'Finished' ? 'success' : (scope.row.fields.task_status === 'Failed' ? 'danger' : (scope.row.fields.task_status === 'Running' ? 'primary' : 'info'))">
                    {{ scope.row.fields.task_status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                type="selection"
                width="40">
              </el-table-column>
            </el-table>
          </div>
          <div style="margin: 14px; padding-bottom: 30px">
            <el-pagination
              background
              layout="sizes, prev, pager, next"
              :page-sizes="[10, 15, 20, 25, 30]"
              :page-size="pagesize"
              :total="totalsize"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              style="float: left">
            </el-pagination>
            <el-tooltip content="View the report(s) of selected task(s)" placement="top">
              <el-button style="float: right" size="large" type="primary" @click="clickToView">View</el-button>
            </el-tooltip>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      search_input: '',
      selected_status: '',
      submissions_table: [],
      pagesize: 10,
      currpage: 1,
      totalsize: 0,
      multipleSelections: [],
      tabsValue: 'Machine Learning',
      analysisType: 'Machine Learning'
    }
  },
  mounted: function () {
    this.showSubmissions()
  },
  methods: {
    handleTabClick () {
      this.analysisType = this.tabsValue
      this.showSubmissions()
    },
    handleSizeChange (val) {
      this.pagesize = val
      this.showSubmissions()
    },
    onSearch () {
      this.showSubmissions()
    },
    onStatusSelected () {
      this.showSubmissions()
    },
    showSubmissions () {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      axios.get('/rest/api/v0/show_submissions?analysis_type=' + this.analysisType + '&page_num=' + this.currpage + '&page_size=' + this.pagesize + '&user_id=' + sessionStorage.getItem('UserID') + '&search=' + this.search_input.toLowerCase() + '&status=' + this.selected_status)
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.totalsize = res.total_size
            this.parseSubmissionsTable(res['list'])
            console.log(this.submissions_table)
            loading.close()
          } else {
            loading.close()
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    parseSubmissionsTable (submissions) {
      var parsedConfig
      if (this.analysisType === 'Machine Learning') {
        for (let submission of submissions) {
          parsedConfig = JSON.parse(submission.fields.task_config)
          submission.fields.proj_name = parsedConfig.proj_name
          submission.fields.train_data = parsedConfig.train_data
          submission.fields.test_data = parsedConfig.test_data
          submission.fields.label = parsedConfig.label
          submission.fields.feat_sel = parsedConfig.feat_sel
          submission.fields.estimator = parsedConfig.estimator
          submission.fields.cv_type = parsedConfig.cv_type
        }
      } else if (this.analysisType === 'SchizoGraphNet') {
        // for (let submission of submissions) {
        //   parsedConfig = JSON.parse(submission.fields.task_config)
        //   submission.fields.proj_name = parsedConfig.proj_name
        //   submission.fields.test_var_data_x = parsedConfig.group_var_data_y
        //   submission.fields.group_var_data_y = parsedConfig.group_var_data_y
        // }
      }
      this.submissions_table = submissions
      console.log(this.submissions_table)
    },
    onSelectionChange (val) {
      this.multipleSelections = val
    },
    clickToView () {
      console.log(this.multipleSelections.length)
      if (this.multipleSelections.length > 30) {
        this.$alert('You can only view 30 or less reports at the same time!', 'Error!', {
          confirmButtonText: 'Confirm',
          callback: action => {
            this.$refs.multipleTable.clearSelection()
          }
        })
      } else if (this.multipleSelections.length === 0) {
        this.$alert('There is no report to view!', 'Error!', {
          confirmButtonText: 'Confirm',
          callback: action => {}
        })
      } else {
        this.$router.push({
          name: 'viewer',
          params: {analysisType: this.analysisType, taskSelections: this.multipleSelections}
        })
      }
    },
    handleCurrentChange (cpage) {
      this.currpage = cpage
      this.showSubmissions()
    }
  }
}
</script>

<style lang="scss">
.submissions-area {
  width: 772px;
  margin: 14px auto;
  padding: 14px;
  text-align: left;
  background-color: #FFFFFF;
}
.input-with-select .el-input-group__prepend {
  background-color: #FFFFFF;
  .el-select .el-input {
    width: 130px;
}
}
.demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>
