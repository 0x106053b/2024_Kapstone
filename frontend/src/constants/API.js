export const API_AUTH = Object.freeze({
  LOGIN: "/auth/login", //로그인
  REFRESH: "/auth/refresh-token", //refresh-token
});

export const API_USER = Object.freeze({
  USER: "/user/", // 한 사람의 유저 정보 가져오기
  REGISTER: "/user/register", // 회원가입
});

export const API_CHATROOM = Object.freeze({
  CREATE_CHATROOM: "/chatroom/create", // 채팅방 생성
  GET_CHATROOMS: "/chatroom/", // 채팅방들 목록 모두 가져오기
  GET_CHATROOM: (chatroom_id) => `/chatroom/${chatroom_id}`, // 채팅방 정보 가져오기
  DELETE_CHATROOM: (chatroom_id) => `/chatroom/${chatroom_id}`, // 채팅방 삭제
});

export const API_MESSAGE = Object.freeze({
  SEND_MESSAGE: (chatroom_id) => `/message/${chatroom_id}`, //메시지 보내기
  GET_MESSAGE: (chatroom_id) => `/message/${chatroom_id}`, //메시지 기록 모두 받기
  DELETE_MESSAGE: (chatroom_id) => `/message/${chatroom_id}`, //채팅방 전체 메시지 삭제
});

export const API_DOCUMENT = Object.freeze({
  UPLOAD_DOCUMENT: (chatroom_id) => `/document/${chatroom_id}`, //자료 업로드
  GET_DOCUMENTS: (chatroom_id) => `/document/${chatroom_id}`, //자료 기록 받기
  DELETE_DOCUMENT: (chatroom_id, document_id) =>
    `/document/${chatroom_id}/${document_id}`, //자료 삭제
});
