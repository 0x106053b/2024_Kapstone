import axiosInstance from "./axiosInstance";
import { API_MESSAGE } from "@/constants/API";

export const postSendMessage = (chatroom_id, content) => {
  return axiosInstance({
    url: API_MESSAGE.SEND_MESSAGE(chatroom_id),
    method: "POST",
    data: { content },
  });
};

/* response
{
  "message_id": 0,
  "content": "string",
  "send_time": "2024-11-30T12:50:57.428Z",
  "sender_type": "string", //user
  "chatroom_id": 0
}
*/

export const getMessage = (chatroom_id) => {
  return axiosInstance({
    url: API_MESSAGE.GET_MESSAGE(chatroom_id),
    method: "GET",
  });
};

/* response
  {
    "message_id": 0,
    "content": "string",
    "send_time": "2024-11-30T12:53:27.684Z",
    "sender_type": "string",  //user or bot
    "chatroom_id": 0
  }
*/

export const deleteMessage = (chatroom_id) => {
  return axiosInstance({
    url: API_MESSAGE.DELETE_MESSAGE(chatroom_id),
    method: "DELETE",
  });
};
