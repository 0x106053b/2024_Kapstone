import axios from "axios";
import Cookies from "js-cookie";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = Cookies.get("access_token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = Cookies.get("refresh_token");
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/refresh-token`,
          {
            refresh_token: refreshToken,
          }
        );
        const { access_token } = response.data;
        Cookies.set("access_token", access_token, {
          expires: new Date(Date.now() + 60 * 60 * 1000),
          path: "/",
          secure: false,
          sameSite: "Lax",
        });
        originalRequest.headers["Authorization"] = `Bearer ${access_token}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        Cookies.remove("access_token");
        Cookies.remove("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
