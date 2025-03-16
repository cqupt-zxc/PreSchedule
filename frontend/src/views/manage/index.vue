<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus';
import { addCourseAPI, updateCourseAPI } from '@/api/manage';
import { useRoute, useRouter } from 'vue-router';

// 表单验证规则
const rules = ref({
  semester: [{ required: true, message: '请输入课程学期', trigger: 'blur' }],
  course_name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  hours: [{ required: true, message: '请输入学时', trigger: 'blur' }],
  students: [{ required: true, message: '请输入学生人数', trigger: 'blur' }],
  teachers: [{ required: false, message: '请输入教师姓名', trigger: 'blur' }],
  total_head: [{ required: true, message: '请输入总头数', trigger: 'blur' }], // 新增字段验证规则
});

// 定义表单实例
const ruleForm = ref<InstanceType<typeof ElForm> | null>(null);

// 获取路由对象
const route = useRoute();
const router = useRouter();
const is_update = ref(Object.keys(route.query).length > 1);
// console.log(is_update.value)

interface Course {
  semester: string;
  course_name: string;
  hours: number;
  students: number;
  teachers: string;
  total_head: number; // 新增字段
}

let oldCourse: Course = {
  semester: '',
  course_name: '',
  hours: 0,
  students: 0,
  teachers: '',
  total_head: 0, // 新增字段
};
const form = ref<Course>(oldCourse);
const heads = ref(0);

// 根据查询参数初始化表单
const initForm = async () => {
  // console.log(is_update.value)
  const courseNameParam = route.query.course_name;
  const semesterParam = route.query.semester;
  const hoursParam = route.query.hours;
  const studentsParam = route.query.students;
  const teachersParam = route.query.teachers;
  const totalHeadParam = route.query.heads; // 新增字段

  form.value.semester = Array.isArray(semesterParam) ? (semesterParam[0] || '') : (semesterParam || '');
  form.value.course_name = Array.isArray(courseNameParam) ? (courseNameParam[0] || '') : (courseNameParam || '');
  form.value.hours = Array.isArray(hoursParam) ? Number(hoursParam[0] || 0) : Number(hoursParam || 0);
  form.value.students = Array.isArray(studentsParam) ? Number(studentsParam[0] || 0) : Number(studentsParam || 0);
  form.value.teachers = Array.isArray(teachersParam) ? (teachersParam[0] || '') : (teachersParam || '');
  form.value.total_head = Array.isArray(totalHeadParam) ? Number(totalHeadParam[0] || 0) : Number(totalHeadParam || 0); // 新增字段

  if (is_update.value === true) {
    oldCourse = {
      semester: form.value.semester,
      course_name: form.value.course_name,
      hours: form.value.hours,
      students: form.value.students,
      teachers: form.value.teachers,
      total_head: form.value.total_head, // 新增字段
    };
  }
};
onMounted(() => {
  initForm();
})

// 数据有变动时，更改heads的值
watch(() => form.value.teachers, (newValue) => {
  if (newValue.length === 0) {
    heads.value = 0;
  } else {
    heads.value = newValue.split(/(，|,|\u3001)/).filter((_, index) => index % 2 === 0).length;
    // 识别并计算括号内的数字
    if (newValue.includes('(') || newValue.includes('（')) {
      const regex = /[\(（](\d+)[\)）]/g;
      const match = newValue.match(regex);
      if (match) {
        match.forEach((item) => {
          const number = Number(item.replace(/[\(（]|[\)）]/g, ''));
          heads.value -= 1;
          heads.value += number;
        });
      }
    }
  }
})

// 提交表单
const submit = async () => {
  if (!ruleForm.value) return;
  await ruleForm.value.validate((valid: boolean) => {
    if (valid) {
      if (is_update.value === true) {
        updateCourse();
      } else {
        addCourse();
      }
      // 跳转到/manage 页面
      router.push({
        path: '/overview',
        query: {
          status: 'changed',
          semester: form.value.semester,
        },
      });
    } else {
      ElMessage({
        message: '表单验证失败',
        type: 'error',
      });
      return false;
    }
  });
};

// 修改课程的 API 调用
const updateCourse = async () => {
  try {
    const newTeachersStrArray = form.value.teachers.split(/(,|\u3001)/);
    const newTeachersArray = newTeachersStrArray.filter((_, index) => index % 2 === 0);
    const oldTeachersStrArray = oldCourse.teachers.split(/(,|\u3001)/);
    const oldTeachersArray = oldTeachersStrArray.filter((_, index) => index % 2 === 0);
    const submitForm = {
      new_course_name: form.value.course_name,
      new_hours: form.value.hours,
      new_students: form.value.students,
      new_semester: form.value.semester,
      new_teachers: newTeachersArray,
      new_total_head: form.value.total_head,
      old_total_head: oldCourse.total_head,
      old_course_name: oldCourse.course_name,
      old_hours: oldCourse.hours,
      old_students: oldCourse.students,
      old_semester: oldCourse.semester,
      old_teachers: oldTeachersArray,
    }
    const response = await updateCourseAPI(submitForm);
    if (response.data.status === 10000) {
      ElMessage({
        message: '课程修改成功',
        type: 'success',
      });
      // 清空表单
      form.value = {
        semester: '',
        course_name: '',
        hours: 0,
        total_head: 0,
        students: 0,
        teachers: '',
      };
    } else {
      ElMessage({
        message: '课程修改失败',
        type: 'error',
      });
    }
  } catch (error) {
    ElMessage({
      message: '网络错误，请重试',
      type: 'error',
    });
  }
}

// 添加课程的 API 调用
const addCourse = async () => {
  try {
    const response = await addCourseAPI(form.value);
    if (response.data.status === 10000) {
      ElMessage({
        message: '课程添加成功',
        type: 'success',
      });
      // 清空表单
      form.value = {
        semester: '',
        course_name: '',
        hours: 0,
        total_head: 0,
        students: 0,
        teachers: '',
      };
    } else {
      ElMessage({
        message: '课程添加失败',
        type: 'error',
      });
    }
  } catch (error) {
    ElMessage({
      message: '网络错误，请重试',
      type: 'error',
    });
  }
};

// 重置表单
const resetForm = () => {
  if (!ruleForm.value) return;
  ruleForm.value.resetFields();
};
</script>

<template>
  <el-form :model="form" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
    <el-form-item label="课程学期" prop="semester">
      <el-input v-model="form.semester"></el-input>
    </el-form-item>
    <el-form-item label="课程名称" prop="course_name">
      <el-input v-model="form.course_name"></el-input>
    </el-form-item>
    <el-form-item label="学时" prop="hours">
      <el-input v-model.number="form.hours"></el-input>
    </el-form-item>
    <el-form-item label="学生人数" prop="students">
      <el-input v-model.number="form.students"></el-input>
    </el-form-item>
    <el-form-item label="总头数" prop="total_head">
      <el-input v-model.number="form.total_head"></el-input>
    </el-form-item>
    <el-form-item label="教师姓名" prop="teachers" v-if="route.query.teachers">
      <el-input v-model="form.teachers"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit" color="#007A51">提交</el-button>
      <el-button @click="resetForm">重置</el-button>
      <div class="heads-container">
        <span>已排头数：{{ heads }}</span>
      </div>
    </el-form-item>
  </el-form>
</template>

<style lang="less" scoped>
.demo-ruleForm {
  width: 50%;
  margin: 0 auto;
}

.heads-container {
  font-size: 14px;
  margin-left: auto;
}
</style>
