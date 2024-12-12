import { API_AUTH } from "@/constants/API";
import axiosInstance from "./axiosInstance";

export const postLogin = (email, password) => {
  return axiosInstance({
    url: API_AUTH.LOGIN,
    method: "POST",
    data: {
      email,
      password,
    },
  });
};
