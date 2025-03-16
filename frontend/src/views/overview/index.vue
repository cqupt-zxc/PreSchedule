<script setup lang="ts">
import { deleteCourseAPI, updateCourseAPI } from '@/api/manage'
import { computed, onBeforeMount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCoursesAPI } from '@/api/yearly'
import { getCurrentSemester } from '@/utils/date'
import { useUserInfoStore } from '@/store'

const modifyTeachers = ref(false)

type Course = {
  index: number
  semester: string
  course_name: string
  hours: number
  teachers: string[]
  heads: number
  students: number
  teachers_str: string
}
const tableData = ref<Course[]>([])
const { year, semester } = getCurrentSemester();
const yearSemester = ref<string>(`${year}${semester}`)

const search_form = ref({
  course_name: '',
  semester: '',
  teacher: '',
})

const init = async () => {
  tableData.value = []
  search_form.value.semester = yearSemester.value
  let id = 1
  // 将search_form放入请求的query中
  const { data: res } = await getCoursesAPI({ ...search_form.value })

  res.data.forEach((ele: any) => {
    // 将ele.teacher中的中文括号改为英文括号
    ele.teacher = ele.teacher === 'nan' ? '' : ele.teacher
    ele.teacher = ele.teacher.replace(/（/g, '(').replace(/）/g, ')');

    const courseIndex = tableData.value.findIndex((course: Course) => course.course_name === ele.course_name);

    if (courseIndex === -1) {
      // 如果tableData没有该课程，则新增该课程，该条数据的老师作为该课程的老师数组的第一个元素
      tableData.value.push({
        index: id,
        semester: ele.semester,
        course_name: ele.course_name,
        hours: ele.hours,
        heads: ele.total_head,
        students: ele.students,
        teachers: [`${ele.teacher}`],
        teachers_str: '',
      });
      id += 1
    } else {
      // 如果tableData有该课程，则更新该课程的老师数组
      tableData.value[courseIndex].teachers.push(`${ele.teacher}`);
      // tableData.value[courseIndex].heads += ele.heads
    }
  })

  // 遍历数组，将老师数组组合成一个字符串
  tableData.value.forEach((ele: any) => {
    ele.teachers_str = ele.teachers.join('、');
  })

  // 按照tableData中的id进行排序
  tableData.value.sort((a, b) => {
    return a.index - b.index;
  })
}

const route = useRoute();
onMounted(() => {
  // 判断 route.query.status 是否为 'changed'
  if (route.query.status === 'changed') {
    // 调用异步函数
    const semester = Array.isArray(route.query.semester) ? route.query.semester[0] : route.query.semester;
    if (semester) {
      handleStatusChanged(semester as string);
    }
  }
})

const handleStatusChanged = async (semester: string) => {
  // 阻塞0.5秒
  await new Promise(resolve => setTimeout(resolve, 500));
  yearSemester.value = semester
  init();
  router.replace({ query: {} });
}


const oldTeachersList = ref<string[]>([]);

// 更新教师
const modify_teachers = () => {
  modifyTeachers.value = !modifyTeachers.value
  if (modifyTeachers.value === true) {
    // 按下修改教师按钮
    tableData.value.forEach((ele: any) => {
      oldTeachersList.value.push(ele.teachers_str)
    })
  } else {
    // 按下取消修改按钮
    tableData.value.forEach((ele: any, index: number) => {
      // 将tableDateachers_str恢复为oldTeachersList中的值
      ele.teachers_str = oldTeachersList.value[index];
    });
  }
}

interface UpdateForm {
  new_course_name: string;
  new_hours: number;
  new_students: number;
  new_semester: string;
  new_teachers: string[];
  new_total_head: number;
  old_total_head: number;
  old_course_name: string;
  old_hours: number;
  old_students: number;
  old_semester: string;
  old_teachers: string[];
}

// 提交修改教师
const update_new_teachers = () => {
  tableData.value.forEach((new_ele: Course, index: number) => {
    if (new_ele.teachers_str !== oldTeachersList.value[index]) {
      // 检查修改后的教师姓名是否符合格式要求
      // （包含老师姓名，用()表示头数，中英文括号内的数字是头数，用中英文顿号分隔，不能有其他的符号）
      const teacherRegex = /^([\u4e00-\u9fa5]+)((?:\(|（)([\u4e00-\u9fa52-9])(?:\)|）))?(?:、([\u4e00-\u9fa5]+(?:\(|（)([\u4e00-\u9fa52-9])(?:\)|）)))*$/;
      if (teacherRegex.test(new_ele.teachers_str)) {
        // 将修改后的教师姓名分割成数组
        const newTeachersStrArray = new_ele.teachers_str.split(/(，|,|\u3001)/);
        const newTeachersArray = newTeachersStrArray.filter((_, index) => index % 2 === 0);
        // 仅将teachersArray元素中的中文括号转化为英文
        newTeachersArray.forEach((teacher, index) => {
          if (teacher.includes('（') || teacher.includes('）')) {
            newTeachersArray[index] = newTeachersArray[index].replace(/（/g, '(').replace(/）/g, ')');
          }
        });

        // 将修改前的教师姓名分割成数组
        const oldTeachersStrArray = oldTeachersList.value[index].split(/(，|,|\u3001)/);
        const oldTeachersArray = oldTeachersStrArray.filter((_, index) => index % 2 === 0);

        const updateForm: UpdateForm = {
          new_course_name: new_ele.course_name,
          new_hours: new_ele.hours,
          new_students: new_ele.students,
          new_semester: new_ele.semester,
          new_teachers: newTeachersArray,
          new_total_head: new_ele.heads,
          old_total_head: new_ele.heads,
          old_course_name: new_ele.course_name,
          old_hours: new_ele.hours,
          old_students: new_ele.students,
          old_semester: new_ele.semester,
          old_teachers: oldTeachersArray,
        }
        // console.log('updateForm:', updateForm);

        updateCourse(updateForm);
      } else {
        ElMessage({
          message: '教师信息格式不正确，请检查后重试',
          type: 'error',
        });
        // 恢复为oldTeachersList.value[index]中的数据
        new_ele.teachers_str = oldTeachersList.value[index];
      }
    }
  })

  if (modifyTeachers.value === true) {
    modifyTeachers.value = !modifyTeachers.value
  }
}

// 修改课程教师API
const updateCourse = async (form: UpdateForm) => {
  console.log('修改课程教师', form);
  const response = await updateCourseAPI(form);
  if (response.data.status === 10000) {
    ElMessage({
      message: '课程修改成功',
      type: 'success',
    });
  } else {
    ElMessage({
      message: '课程修改失败',
      type: 'error',
    });
  }
}

const delete_course = async (row: Course) => {
  ElMessageBox.confirm(
    '是否删除该课程',
    '警告',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      console.log('delete_course: ', row);
      const response = await deleteCourseAPI(row.course_name);
      if (response.data.status === 10000) {
        tableData.value = tableData.value.filter((item) => item.course_name !== row.course_name);
        ElMessage({
          message: '课程删除成功',
          type: 'success',
        });
      } else {
        ElMessage({
          message: '课程删除失败',
          type: 'error',
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      });
    });
};

const userInfoStore = useUserInfoStore()
const role = userInfoStore.userInfo ? userInfoStore.userInfo.role : null;

// 新增和修改课程都是同一个页面，不过要根据路径传参的方式来区分
const router = useRouter()
const to_add_update = (row?: any) => {
  // console.log('看有没有传过来，来判断要add还是update', row)
  if (row) {
    router.push({
      path: '/manage',
      query: {
        // course_id: row.course_id,
        semester: row.semester,
        students: row.students,
        course_name: row.course_name,
        hours: row.hours,
        teachers: row.teachers_str,
        heads: row.heads,
      }
    })
  } else {
    router.push({
      path: '/manage',
      query: {
        semester: yearSemester.value,
      }
    })
  }
}
</script>

<template>
  <div class="horizontal">
    排课学期:<el-input v-model="yearSemester" size="small" class="input" />
    <el-button class="btn" type="primary" @click="init()" color="#007A51">
      一览
    </el-button>

    <div class="btn-group" v-if="role === 'admin'">
      <el-button size="large" class="btn" type="primary" @click="modify_teachers()">
        {{ modifyTeachers === false ? '修改教师' : '取消修改' }}
      </el-button>
      <el-button size="large" class="btn" type="success" @click="update_new_teachers()">
        提交修改
      </el-button>

      <el-button size="large" class="btn" type="primary" @click="to_add_update()">
        <el-icon style="font-size: 15px; margin-right: 10px;">
          <Plus />
        </el-icon>添加课程
      </el-button>
    </div>
  </div>

  <el-table :data="tableData" v-if="tableData.length" height="550">
    <el-table-column prop="index" label="序号" width="80px" />
    <el-table-column prop="semester" label="学期" width="100px" />
    <el-table-column prop="course_name" label="课程名称" width="250px" />
    <el-table-column prop="students" label="人数" width="80px" />
    <el-table-column prop="heads" label="头数" width="80px" />
    <el-table-column prop="hours" label="任课学时" width="150px" />
    <el-table-column prop="teachers_str" label="任课老师" v-if="modifyTeachers !== true">
      <template #default="scope">
        {{ scope.row.teachers_str }}
      </template>
    </el-table-column>
    <el-table-column prop="teachers_str" label="任课老师" v-if="modifyTeachers === true">
      <template #default="scope">
        <el-input v-model="scope.row.teachers_str" style="width: 240px" placeholder={{scope.row.teachers_str}} />
      </template>
    </el-table-column>
    <el-table-column label="操作" min-width="120" width="300px" v-if="role === 'admin'">
      <template #default="scope">
        <el-button link type="danger" @click="delete_course(scope.row)">
          删除
        </el-button>
        <el-button link type="primary" @click="to_add_update(scope.row)">
          修改
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<style lang="less" scoped>
// element-plus的样式修改
.el-table {
  width: 100%;
  // height: 500px;
  margin: 1rem auto;
  text-align: center;
  border: 1px solid #e4e4e4;
}

:deep(.el-table tr) {
  font-size: 14px;
}

.horizontal {
  display: flex;
  align-items: center;
  // margin: 0 40px;

  .input {
    font-size: 15px;
    width: 150px;
    margin-left: 10px;
    margin-right: 20px;
  }

  .btn {
    font-size: 14px;
  }

  .btn-group {
    margin-left: auto; // 使按钮组靠右对齐
    display: flex;
    gap: 10px; // 按钮之间的间距
  }
}

img {
  width: 50px;
  height: 50px;
  border-radius: 10px;
}

.add_btn {
  width: 100px;
  height: 40px;
  margin-left: 900px;
}
</style>