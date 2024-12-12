import axiosInstance from "./axiosInstance";
import { API_CHATROOM } from "@/constants/API";

export const postCreateChatroom = (
  chatroom_name,
  instructor_name,
  course_code
) => {
  return axiosInstance({
    url: API_CHATROOM.CREATE_CHATROOM,
    method: "POST",
    data: { chatroom_name, instructor_name, course_code },
  });
};

export const getChatrooms = () => {
  return axiosInstance({
    url: API_CHATROOM.GET_CHATROOMS,
    method: "GET",
  });
};

export const getChatroom = (chatroom_id) => {
  return axiosInstance({
    url: API_CHATROOM.GET_CHATROOM(chatroom_id),
    method: "GET",
  });
};

export const deleteChatroom = (chatroom_id) => {
  return axiosInstance({
    url: API_CHATROOM.DELETE_CHATROOM(chatroom_id),
    method: "DELETE",
  });
};
