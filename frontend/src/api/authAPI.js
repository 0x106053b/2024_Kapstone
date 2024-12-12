import { API_AUTH } from "@/constants/API";
import axiosInstance from "./axiosInstance";
import loginInstance from "./loginInstance";

export const postLogin = (email, password) => {
  return loginInstance({
    url: API_AUTH.LOGIN,
    method: "POST",
    data: {
      email,
      password,
    },
  });
};

export const postRefreshToken = () => {
  return axiosInstance({
    url: API_AUTH.REFRESH,
    method: "POST",
  });
};
