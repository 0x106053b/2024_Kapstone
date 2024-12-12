import { API_USER } from "@/constants/API";
import axiosInstance from "./axiosInstance";

export const postRegister = (first_name, last_name, email, password) => {
  return axiosInstance({
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
