export const API_AUTH = Object.freeze({
  LOGIN: "/auth/login", //로그인
});

export const API_USER = Object.freeze({
  USER: "/user/", // 유저 목록 가져오기
  USER_BY_ID: (userId) => `/user/${userId}`, // 한 사람의 유저 정보 가져오기
  REGISTER: "/user/register", // 회원가입
});
