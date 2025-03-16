import request from '@/utils/request' // 引入自定义的axios函数

/**
 * 登录接口（这是JSDoc注释）
 * @param {*} param0 {course_name: 课程名称, semester: 学期, teacher: 教师姓名}
 * @returns Promise对象
 */
export const getHistoryCoursesAPI = (params: any) => {
  return request({
    url: `/history_courses`,
    method: 'get',
    params: params,
  })
}

export const getTeachersAPI = () => {
  return request({
    url: `/teacher`,
    method: 'get'
  })
}