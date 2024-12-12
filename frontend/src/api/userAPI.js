import { API_USER } from "@/constants/API";
import axiosInstance from "./axiosInstance";
import loginInstance from "./loginInstance";

export const postRegister = (first_name, last_name, email, password) => {
  return loginInstance({
    url: API_USER.REGISTER,
    method: "POST",
    data: {
      first_name,
      last_name,
      email,
      password,
    },
  });
};

export const getUser = () => {
  return axiosInstance({
    url: API_USER.USER,
    method: "GET",
  });
};
