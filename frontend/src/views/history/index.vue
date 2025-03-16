<template>
  <div style="margin-bottom: 10px;">
    矩阵统计学年:<el-input-number v-model="year" :min="1900" :max="2999" class="input" />
    历史统计起始学年:<el-input-number v-model="history_year" :min="1900" :max="2999" class="input" />
    <el-button type="primary" class="btn_search" color="#007A51" @click="search" small>统计</el-button>
  </div>

  <!-- 年度课时矩阵 -->
  <table v-if="courseMatrix[0].length > 0">
    <thead class="table_grey fixed fixed_head">
      <tr>
        <th style="width: 10px;" rowspan="3" class="fixed left_col_1">序号</th> <!-- 添加序号列 -->
        <th class="fixed left_col_2"></th>
        <th class="fixed left_col_3"></th>
        <th class="fixed left_col_4"></th>
        <th class="fixed left_col_5"></th>
        <th class="fixed left_col_6"></th>
        <th class="fixed left_col_7"></th>
        <th v-for="(teacher, index) in teachers" :key="index" @click="handleDetail(teacher)"
          style="writing-mode: vertical-lr;">
          <el-popover placement="right" :width="400" trigger="click">
            <template #reference>
              <span class="course-amount">{{ teacher }}</span>
            </template>
            <el-table :data="details" height="250">
              <el-table-column prop="semester" label="学期" />
              <el-table-column prop="course_name" label="课程名称" />
            </el-table>
          </el-popover>
        </th>
      </tr>
      <tr>
        <th class="fixed left_col_2"></th>
        <th colspan="5" class="fixed left_col_3">年内总学时</th>
        <th v-for="(teacher, index) in teachers" :key="index">{{ total_hours.get(teacher) }}</th>
      </tr>
      <tr>
        <th class="fixed left_col_2"></th> <!-- 删除: <th></th> -->
        <th style="writing-mode: vertical-lr;" class="fixed left_col_3">上课学时</th>
        <th style="writing-mode: vertical-lr;" class="fixed left_col_4">开课学期</th>
        <th style="writing-mode: vertical-lr;" class="fixed left_col_5">学生人数</th>
        <th style="writing-mode: vertical-lr;" class="fixed left_col_6">总头数</th>
        <th style="writing-mode: vertical-lr;" class="fixed left_col_7">已排头数</th>
        <th :colspan="teachers.length">年度课程矩阵：头数.学时</th>
      </tr>
    </thead>
    <tr v-for="(course, index) in courses" :key="index" :class="{ 'shade_border': index === selectedRow }"
      @click="select_row(index)">
      <th class="table_grey fixed left_col_1" style="width: 10px;">{{ index + 1 }}</th> <!-- 添加序号列 -->
      <th class="table_grey fixed left_col_2" style="width: 200px; cursor: pointer;">{{ course }}</th>
      <th class="table_white fixed left_col_3">{{ CourseBasicInfoMap.get(course)?.hours }}</th>
      <th class="table_white fixed left_col_4">{{ CourseBasicInfoMap.get(course)?.semester }}</th>
      <th class="table_white fixed left_col_5">{{ CourseBasicInfoMap.get(course)?.students }}</th>
      <th class="table_white fixed left_col_6">{{ CourseBasicInfoMap.get(course)?.total_heads }}</th>
      <th class="table_white fixed left_col_7">{{ CourseBasicInfoMap.get(course)?.ordered_heads }}</th>
      <td v-for="(value, colIndex) in courseMatrix[index]" :key="colIndex"
        :class="['table_white', value !== '0.0' ? 'highlight' : '']">
        {{ value !== '0.0' ? value : '' }}
      </td>
    </tr>
  </table>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { getCoursesAPI } from '@/api/yearly'
import { getHistoryCoursesAPI, getTeachersAPI } from '@/api/history'

// 获取今年年份
const form = ref({
  course_name: '',
  semester: '',
  teacher: '',
})
const semester = ref<string>('1')
const year = ref<number>(new Date().getFullYear() - 1)
const history_year = ref<number>(new Date().getFullYear() - 3)

const courseMatrix = ref<string[][]>([[]])
const total_hours = ref(new Map<string, number>)
const teachers = ref<string[]>([])
const courses = ref<string[]>([])

type BasicInfo = {
  course_name: string
  semester: string
  hours: number
  students: number
  total_heads: number
  ordered_heads: number
}
const CourseBasicInfoMap = ref(new Map<string, BasicInfo>())

// 表格数据
const details = ref<detailData[]>([])
interface detailData {
  semester: string,
  course_name: string,
}

// 查询教师历史课程
const handleDetail = async (teacher: string) => {
  details.value = []
  form.value.teacher = teacher
  form.value.semester = `${history_year.value}1`

  let { data: res } = await getHistoryCoursesAPI({ ...form.value })
  // 新建一个弹窗，展示查询到的信息
  res.data.forEach((ele: any) => {
    const newDetail: detailData = {
      semester: ele.semester,
      course_name: ele.course_name,
    }
    details.value.push(newDetail)
  })
  details.value.sort((a, b) => {
    const aSemester = a.semester
    const bSemester = b.semester
    return aSemester.localeCompare(bSemester)
  })
}

const nameCompare = (a: string, b: string) => {
  const aName = a.split(' ')[0]
  const bName = b.split(' ')[0]
  return aName.localeCompare(bName)
}

const search = async () => {
  courseMatrix.value = [[]]
  total_hours.value.clear()
  teachers.value = []
  courses.value = []

  form.value.teacher = ''
  form.value.semester = `${year.value}1`
  const { data: res1 } = await getCoursesAPI({ ...form.value })
  form.value.semester = `${year.value}2`
  const { data: res2 } = await getCoursesAPI({ ...form.value })
  const res = [...res1.data, ...res2.data]

  const { data: teachers_data } = await getTeachersAPI()

  // 记录所有老师，按办公室分组
  teachers_data.data[0].teacher.forEach((ele: any) => {
    teachers.value.push(ele.replace(/\s+/g, '')) // 修改: 去除字符串中的空格
  })

  // 初始化年内总学时
  teachers.value.forEach((ele: string) => {
    total_hours.value.set(ele, 0)
  })

  res.forEach((ele: any) => {
    // 将ele.teacher中的中英文括号及其内容去除
    ele.teacher = ele.teacher.replace(/[\s]*[（(][^）)]*[）)]/g, '').trim();

    // 如果课程教师不包含在teachers中，则在末尾添加
    if (!teachers.value.includes(ele.teacher) && ele.teacher !== 'nan' && ele.teacher !== '无') {
      teachers.value.push(ele.teacher)
    }

    // 记录所有课程
    if (!courses.value.includes(ele.course_name)) {
      courses.value.push(ele.course_name)
    }
    courses.value.sort(nameCompare)

    // 记录课程基础信息到CourseBasicInfoMap
    if (!CourseBasicInfoMap.value.has(ele.course_name)) {
      CourseBasicInfoMap.value.set(ele.course_name, {
        course_name: ele.course_name,
        semester: ele.semester[4],
        students: ele.students,
        hours: ele.hours,
        total_heads: ele.total_head,
        ordered_heads: ele.heads,
      })
    } else {
      const existingInfo = CourseBasicInfoMap.value.get(ele.course_name);
      if (existingInfo) {
        existingInfo.ordered_heads += ele.heads;
      }
    }

    // 计算教师总课时
    const teacher = ele.teacher;
    const currentHours = total_hours.value.get(teacher) || 0;
    total_hours.value.set(teacher, currentHours + ele.hours * ele.heads);
  })

  // 初始化 courseMatrix
  for (let row = 0; row < courses.value.length; row++) {
    // 确保每一行都被初始化
    courseMatrix.value[row] = []
    for (let col = 0; col < teachers.value.length; col++) {
      courseMatrix.value[row][col] = `0.0`
    }
  }

  res.forEach((ele: any) => {
    // 创建年度课程矩阵
    for (let row = 0; row < courses.value.length; row++) {
      if (ele.course_name === courses.value[row]) {
        for (let col = 0; col < teachers.value.length; col++) {
          if (ele.teacher === teachers.value[col]) {
            courseMatrix.value[row][col] = `${ele.heads}.${ele.hours}`
          }
        }
      }
    }
  })
}

const selectedRow = ref<null | number>(null)

const select_row = (row: number) => {
  selectedRow.value = row
}
</script>

<style scoped>
.input {
  width: 150px;
  margin: 0 10px;
}

.radio {
  margin: 0 10px;
}

.el-checkbox__input.is-checked+.el-checkbox__label {
  color: #007A51;
}

table {
  width: max-content;
  border-collapse: separate;
  /* 修改此处 */
  border-spacing: 0;
  /* 避免单元格间距 */
  /* border-collapse: collapse; */
  margin: 20px 0;
  font-size: 14px;
  text-align: left;
  table-layout: fixed;
}

th,
td {
  text-align: center;
  padding: 2px;
  border: 1px solid #ddd;
}

.table_grey {
  background-color: #f5f7fa;
}

.shade_border>th:nth-child(n),
.shade_border>td:nth-child(n) {
  /* 加粗上下边框，添加阴影 */
  border-top: 2px solid #ddd;
  border-bottom: 2px solid #ddd;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.table_white {
  background-color: white;
}

.course-amount {
  display: inline-block;
}

.highlight {
  background-color: yellow;
}

.first_block {
  min-width: 150px;
}

.btn_search {
  margin-left: auto;
}

/* .table_head {
  position: sticky;
  top: -20px;
  z-index: 2;
} */

.fixed {
  position: sticky;
  background-color: #f5f7fa;
}

.fixed_head {
  top: -20px;
  z-index: 1;
}

.left_col_1 {
  left: -20px;
}

.left_col_2 {
  left: 2.5px;
}

.left_col_3 {
  left: 202.5px;
}

.left_col_4 {
  left: 228.5px;
}

.left_col_5 {
  left: 254.5px;
}

.left_col_6 {
  left: 285.25px;
}

.left_col_7 {
  left: 311.25px;
}
</style>
