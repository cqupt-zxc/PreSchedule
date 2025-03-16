<template>
  <div style="display: flex; align-items: center;">
    统计学年:<el-input-number v-model="year" :min="1900" :max="2999" class="input" />
    <el-button type="primary" color="#007A51" @click="search" small>统计</el-button>
  </div>

  <table style="width: 100%; margin-top: 10px;" v-if="tableData.length">
    <thead class="table_grey table_head">
      <tr>
        <th rowspan="2" style="width: 10px;">序号</th> <!-- 添加序号列 -->
        <th rowspan="2">姓名</th>
        <th colspan="3">秋季学期</th>
        <th colspan="3">春季学期</th>
        <th rowspan="2">学年学时合计</th>
        <th rowspan="2">学年总门数</th>
      </tr>
      <tr>
        <th>单课程学时和</th>
        <th>学期学时合计：{{ autumn_average_hours }}</th>
        <th>课程门数</th>
        <th>单课程学时和</th>
        <th>学期学时合计：{{ spring_average_hours }}</th>
        <th>课程门数</th>
      </tr>
    </thead>
    <tbody class="table_white">
      <tr v-for="(item, index) in filterTableData" :key="index">
        <td>{{ index + 1 }}</td> <!-- 显示序号 -->
        <td>{{ item.name }}</td>
        <td>{{ item.single_hours_autumn }}</td>
        <td>{{ item.total_hours_autumn }}</td>
        <td>{{ item.course_amount_autumn }}</td>
        <td>{{ item.single_hours_spring }}</td>
        <td>{{ item.total_hours_spring }}</td>
        <td>{{ item.course_amount_spring }}</td>
        <td>{{ item.year_total_hours }}</td>
        <td @click="handleDetail(item.name)">
          <el-popover placement="right" :width="400" trigger="click">
            <template #reference>
              <span class="course-amount">{{ item.total_course_amount }}</span>
            </template>
            <el-table :data="details">
              <el-table-column prop="hours" label="课时" />
              <el-table-column prop="heads" label="头数" />
              <el-table-column prop="semester" label="学期" />
              <el-table-column prop="course_name" label="课程名称" />
            </el-table>
          </el-popover>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { getCoursesAPI } from '@/api/yearly'
import { getTeachersAPI } from '@/api/history'

// 获取今年年份
const year = new Date().getFullYear() - 1
const form = ref({
  course_name: '',
  semester: `${year}1`,
  teacher: '',
})

// 表格数据
const tableData = ref<blockData[]>([])
interface blockData {
  name: string,
  single_hours_autumn: number,
  total_hours_autumn: number,
  course_amount_autumn: number,
  single_hours_spring: number,
  total_hours_spring: number,
  course_amount_spring: number,
  year_total_hours: number,
  total_course_amount: number,
}

const teacherFilter = ref('')
const filterTableData = computed(() =>
  tableData.value.filter(
    (data) =>
      !teacherFilter.value ||
      data.name.toLowerCase().includes(teacherFilter.value.toLowerCase())
  )
)

const TableVisible = ref(false)
const details = ref<detailData[]>([])
interface detailData {
  heads: number,
  hours: number,
  semester: string,
  course_name: string,
}
const handleDetail = async (name: string) => {
  details.value = []
  form.value.teacher = name

  form.value.semester = `${year}1`
  const { data: res1 } = await getCoursesAPI({ ...form.value })
  // 新建一个弹窗，展示查询到的信息
  res1.data.forEach((ele: any) => {
    let newDetail: detailData = {
      heads: ele.heads,
      hours: ele.hours,
      semester: `${year}1`,
      course_name: ele.course_name,
    }
    details.value.push(newDetail)
  })

  form.value.semester = `${year}2`
  const { data: res2 } = await getCoursesAPI({ ...form.value })
  // 新建一个弹窗，展示查询到的信息
  res2.data.forEach((ele: any) => {
    let newDetail: detailData = {
      heads: ele.heads,
      hours: ele.hours,
      semester: `${year}2`,
      course_name: ele.course_name,
    }
    details.value.push(newDetail)
  })

  TableVisible.value = true
}

const spring_average_hours = ref(0)
const autumn_average_hours = ref(0)

const search = async () => {
  // 获取课程数据
  spring_average_hours.value = 0
  autumn_average_hours.value = 0
  const year = new Date().getFullYear() - 1
  tableData.value = []
  let flag = false // 标志老师是否该课程老师是否存在于普通教师表中

  // 获取教师名单，创建表单数据
  const { data: teachers_data } = await getTeachersAPI()
  teachers_data.data[0].teacher.forEach((ele: any) => {
    let newRow: blockData = {
      name: ele,
      single_hours_autumn: 0,
      total_hours_autumn: 0,
      course_amount_autumn: 0,
      single_hours_spring: 0,
      total_hours_spring: 0,
      course_amount_spring: 0,
      year_total_hours: 0,
      total_course_amount: 0,
    }
    tableData.value.push(newRow)
  })

  // 消除tableData.value中teacher中的空格
  tableData.value.forEach((ele) => {
    ele.name = ele.name.replace(' ', '')
  })

  form.value.semester = `${year}1`
  const { data: res_autumn } = await getCoursesAPI({ ...form.value })
  res_autumn.data.forEach((ele: any) => {
    ele.teacher = ele.teacher.replace(/[\s]*[（(][^）)]*[）)]/g, '').replace(' ', '').trim();
    tableData.value.forEach((row: any) => {
      // 保留ele.teacher中/英文括号前的内容
      if (row.name === ele.teacher) {
        row.single_hours_autumn += ele.hours
        row.total_hours_autumn += ele.hours * ele.heads
        row.course_amount_autumn += 1
        row.year_total_hours += ele.hours * ele.heads
        row.total_course_amount += 1

        autumn_average_hours.value += ele.hours * ele.heads
        flag = true
      }
    })
    if (!flag) {
      let newRow: blockData = {
        name: ele.teacher,
        single_hours_autumn: ele.hours,
        total_hours_autumn: ele.hours * ele.heads,
        course_amount_autumn: 1,
        single_hours_spring: 0,
        total_hours_spring: 0,
        course_amount_spring: 0,
        year_total_hours: ele.hours * ele.heads,
        total_course_amount: 1,
      }

      tableData.value.push(newRow)
      autumn_average_hours.value += ele.hours * ele.heads
    }
    flag = false
  })

  form.value.semester = `${year}2`
  const { data: res_spring } = await getCoursesAPI({ ...form.value })
  res_spring.data.forEach((ele: any) => {
    ele.teacher = ele.teacher.replace(/[\s]*[（(][^）)]*[）)]/g, '').replace(' ', '').trim();
    tableData.value.forEach((row: any) => {
      if (row.name === ele.teacher) {
        row.single_hours_spring += ele.hours
        row.total_hours_spring += ele.hours * ele.heads
        row.course_amount_spring += 1
        row.year_total_hours += ele.hours * ele.heads
        row.total_course_amount += 1

        spring_average_hours.value += ele.hours * ele.heads
        flag = true
      }
    })
    if (!flag) {
      let newRow: blockData = {
        name: ele.teacher,
        single_hours_autumn: 0,
        total_hours_autumn: 0,
        course_amount_autumn: 0,
        single_hours_spring: ele.hours,
        total_hours_spring: ele.hours * ele.heads,
        course_amount_spring: 1,
        year_total_hours: ele.hours * ele.heads,
        total_course_amount: 1,
      }

      tableData.value.push(newRow)
      spring_average_hours.value += ele.hours * ele.heads
    }
    flag = false
  })

  // 排除ele.teacher==='nan'的数据
  tableData.value = tableData.value.filter(
    (ele) => ele.name !== 'nan' && ele.name !== '无'
  )
}
</script>

<style scoped>
.input {
  width: 150px;
  margin: 0 10px;
}

.checkbox {
  margin: 0 10px;
}

.el-checkbox__input.is-checked+.el-checkbox__label {
  color: #007A51;
}

table {
  width: 100%;
  border-collapse: separate;
  /* 修改此处 */
  border-spacing: 0;
  /* 避免单元格间距 */
  margin: 20px 0;
  font-size: 14px;
  text-align: left;
}

th,
td {
  text-align: center;
  padding: 5px;
  border: 1px solid #ddd;
  min-width: 40px;
}

.table_grey {
  background-color: #f5f7fa;
}

.table_white {
  background-color: white;
}

.course-amount {
  padding: 0 15px;
  /* 增加内边距 */
  display: inline-block;
  /* 确保内边距生效 */
}

.table_head {
  position: sticky;
  top: -20px;
  /* background-color: white; */
  border: 1px solid #ddd;
  z-index: 1;
}
</style>