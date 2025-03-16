<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserInfoStore } from '@/store'

const router = useRouter()
const userInfoStore = useUserInfoStore()

onMounted(() => {
  if (!userInfoStore.userInfo) {
    router.push('/login')
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>