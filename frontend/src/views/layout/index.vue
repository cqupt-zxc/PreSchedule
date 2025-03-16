<script setup lang="ts" name="layout">
import { RouterView, useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useUserInfoStore } from '@/store'
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { fixPwdAPI } from '@/api/admin'
// import { getStatusAPI, fixStatusAPI } from '@/api/shop'
// import { ElNotification } from 'element-plus'

// ------ data ------
const dialogFormVisible = ref(false)
const dialogStatusVisible = ref(false)
const formLabelWidth = '80px'
const isCollapse = ref(false)

let menuList = [
  {
    title: '年内统计',
    path: '/yearly',
    icon: 'pieChart',
  },
  {
    title: '历史统计',
    path: '/history',
    icon: 'memo',
  },
  {
    title: '课程一览',
    path: '/overview',
    icon: 'collection',
  },
]

const form = reactive({
  oldPwd: '',
  newPwd: '',
  rePwd: '',
})
const pwdRef = ref()
const status = ref(1)
const status_active = ref(1) // 单选框绑定的动态值

// 自定义校验规则: 两次密码是否一致
const samePwd = (rules: any, value: any, callback: any) => {
  if (value !== form.newPwd) {
    // 如果验证失败，则调用 回调函数时，指定一个 Error 对象。
    callback(new Error('两次输入的密码不一致!'))
  } else {
    // 如果验证成功，则直接调用 callback 回调函数即可。
    callback()
  }
}
const rules = { // 表单的规则检验对象
  oldPwd: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
    {
      pattern: /^[a-zA-Z0-9]{1,10}$/,
      message: '原密码必须是1-10的大小写字母数字',
      trigger: 'blur'
    }
  ],
  newPwd: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { pattern: /^\S{6,15}$/, message: '新密码必须是6-15的非空字符', trigger: 'blur' }
  ],
  rePwd: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { pattern: /^\S{6,15}$/, message: '新密码必须是6-15的非空字符', trigger: 'blur' },
    { validator: samePwd, trigger: 'blur' }
  ]
}

// ------ method ------
const router = useRouter()
const userInfoStore = useUserInfoStore()
const route = useRoute();
// 根据当前路由的路径返回要激活的菜单项
const getActiveAside = () => {
  return route.path;
};
// 关闭修改密码对话框
const cancelForm = () => {
  ElMessage({
    type: 'info',
    message: '已取消修改',
  })
  dialogFormVisible.value = false
}
// 修改密码
const fixPwd = async () => {
  const valid = await pwdRef.value.validate()
  if (valid) {
    const submitForm = {
      old_password: form.oldPwd,
      new_password: form.newPwd,
    }
    console.log('要提交的表单信息')
    console.log(submitForm)
    const { data: res } = await fixPwdAPI(submitForm)
    if (res.status != 10000) return   // 密码错误信息会在相应拦截器中捕获并提示
    ElMessage({
      type: 'success',
      message: '修改成功',
    })
    dialogFormVisible.value = false
  } else {
    return false
  }
}

const quitFn = () => {
  // 为了让用户体验更好，来个确认提示框
  ElMessageBox.confirm(
    '是否确认退出管理员登陆?',
    '退出登录',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
      ElMessage({
        type: 'success',
        message: '退出成功',
      })
      // 清除用户信息，包括token
      userInfoStore.userInfo = null
      console.log(userInfoStore)
      router.push('/login')
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消退出',
      })
    })
}

</script>

<template>
  <div class="common-layout">
    <el-dialog v-model="dialogFormVisible" title="修改密码" width="500">
      <el-form :model="form" :rules="rules" ref="pwdRef">
        <el-form-item prop="oldPwd" label="原密码" :label-width="formLabelWidth">
          <el-input v-model="form.oldPwd" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="newPwd" label="新密码" :label-width="formLabelWidth">
          <el-input v-model="form.newPwd" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="rePwd" label="确认密码" :label-width="formLabelWidth">
          <el-input v-model="form.rePwd" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="cancelForm">取消</el-button>
          <el-button type="primary" @click="fixPwd">确定</el-button>
        </div>
      </template>
    </el-dialog>
    <el-container>
      <el-header>
        <img src="../../assets/image/cqupt_logo.png" class="logo" />
        <!-- 折叠/展开左侧边栏图标 -->
        <el-icon class="icon1" v-if="isCollapse">
          <Expand @click.stop="isCollapse = !isCollapse" />
        </el-icon>
        <el-icon class="icon1" v-else>
          <Fold @click.stop="isCollapse = !isCollapse" />
        </el-icon>
        <!-- 管理员登陆 -->
        <el-dropdown style="float: right">
          <el-button type="primary">
            {{ userInfoStore.userInfo ? userInfoStore.userInfo.account : '已登录' }}
            <el-icon class="arrow-down-icon"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="dialogFormVisible = true">修改密码</el-dropdown-item>
              <el-dropdown-item @click="quitFn">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-container class="box1">
        <!-- 左侧导航菜单区域 -->
        <el-menu :width="isCollapse ? '640px' : '200px'" :default-active="getActiveAside()" :collapse="isCollapse"
          background-color="#22aaee" text-color="#fff" unique-opened router>
          <!-- 加了router模式，就会在激活导航时以 :index 作为path进行路径跳转（nb!不用自己写路由了!） -->
          <!-- 根据不同情况选择menu-item/submenu进行遍历，所以外层套template遍历，里面组件做判断看是否该次遍历到自己 -->
          <template v-for="item in menuList" :key="item.path">
            <el-menu-item :index="item.path">
              <el-icon>
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.title }}</span>
            </el-menu-item>
          </template>
        </el-menu>

        <el-container class="mycontainer">
          <el-main>
            <router-view></router-view>
          </el-main>
          <el-footer>重庆邮电大学 智能预排课系统</el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<style lang="less" scoped>
.common-layout {
  height: 100%;
  background-color: #eee;
}

.el-header {
  background-color: #007A51;
  color: #ffffff;
  line-height: 60px;

  .logo {
    display: inline-block;
    margin: 10px 20px;
    width: 180px;
    height: 40px;
  }

  .icon1 {
    position: absolute;
    top: 18px;
    margin: 5px 10px 0 0;
  }

  .status {
    display: inline-block;
    align-items: center;
    vertical-align: top;
    line-height: 30px;
    margin: 15px 50px;
    padding: 0 10px;
    border-radius: 5px;
    background-color: #eebb00;
    color: #fff;
  }
}

.rightAudio {
  float: right;
  // margin: 14px 20px;
}

.status-change {
  float: right;
  margin: 14px 20px;
  background-color: rgba(255, 255, 255, 0.3);
  border: none;
  color: #fff;
}

.user {
  float: right;
  margin-right: 20px;
}

.el-dropdown .el-button {
  float: right;
  width: 80px;
  margin: 14px 20px;
  background-color: #eebb00;
  border-color: #eebb00;
  color: #fff;

  .arrow-down-icon {
    margin-left: 5px;
  }
}

.box1 {
  display: flex;
  height: 92vh;
}

.mycontainer {
  display: flex;
  flex: 6;
  flex-direction: column;
}

.el-main {
  flex: 1;
  background-color: #e9f5ff;
  color: #333;
  /* text-align: center; */
  /* line-height: 80px; */
}

a {
  display: block;
  height: 4rem;
  color: #334455;
  font-size: 20px;
  font-weight: bold;
  text-decoration: none;
}

a:hover {
  background-color: #445566;
  color: #eee;
}

.el-footer {
  --el-footer-height: 35px;
  background-color: #445566;
  font-size: 12px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>



<style lang="less">
.el-dialog {
  border-radius: 2%;
}

.el-dialog__header {
  height: 60px;
  line-height: 60px;
  padding: 0 30px;
  font-weight: bold;
}

.el-dialog__body {
  padding: 10px 30px 30px;

  .el-radio,
  .el-radio__input {
    white-space: normal; // 设置其自动换行，别撑不下还挤在一起...
  }

  .el-radio__label {
    padding-top: 15px;
    color: #445588;
    font-weight: 700;

    span {
      display: block;
      line-height: 20px;
      padding: 12px 0 20px 0;
      color: #666;
      font-weight: normal;
    }
  }

  .el-radio-group {
    &>.is-checked {
      border: 1px solid #007A51;
    }
  }

  .el-radio {
    width: 410px; // 本来想设置100%的，但是设置成固定值能去除el-radio-last-child的样式影响
    height: 100px;
    background: #fbfbfa;
    border: 1px solid #e5e4e4;
    border-radius: 4px;
    padding: 14px 22px;
    margin-top: 20px;
  }

  // .el-radio__input.is-checked+.el-radio__label {
  //   span {}
  // }
}

.el-badge__content.is-fixed {
  top: 24px;
  right: 2px;
  width: 18px;
  height: 18px;
  font-size: 10px;
  line-height: 16px;
  font-size: 10px;
  border-radius: 50%;
  padding: 0;
}

.badgeW {
  .el-badge__content.is-fixed {
    width: 30px;
    border-radius: 20px;
  }
}

.el-menu {
  padding: 30px 0 0 0;
  background-color: #445566;
}

.el-menu-item {
  margin: 10px;
  padding-right: 30px;
  border-radius: 10px;
  --el-menu-hover-bg-color: rgba(0, 122, 81, 0.5);
}

.el-menu-item.is-active {
  background-color: #007A51;
  color: #fff;
}

.el-menu--collapse {
  width: 85px;
}
</style>