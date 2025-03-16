export function getCurrentSemester(): { year: number, semester: number } {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1; // getMonth() 返回 0-11，需要加 1

  let year: number;
  let semester: number;

  if (currentMonth >= 3 && currentMonth <= 9) {
    // 当前学年的秋季学期
    year = currentYear;
    semester = 1;
  } else {
    // 上一个学年的春季学期
    year = currentYear - 1;
    semester = 2;
  }

  console.log(`当前学年: ${year} 学年, 学期: ${semester}`);
  return { year, semester };
}