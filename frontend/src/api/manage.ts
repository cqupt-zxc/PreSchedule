import request from '@/utils/request' // 引入自定义的axios函数

/**
 * 
 * @param {*} param0 {course_name: 课程名称, semester: 学期, teacher: 教师姓名}
 * @returns Promise对象
 */
export const deleteCourseAPI = (course_name: string) => {
    return request({
        url: `/courses`,
        method: 'delete',
        params: { 'course_name': course_name },
    });
};

export const addCourseAPI = (data: any) => {
    return request({
        url: `/courses`,
        method: 'post',
        data: data,
    });
};

export const updateCourseAPI = (data: any) => {
    return request({
        url: `/courses`,
        method: 'put',
        data: data,
    });
};