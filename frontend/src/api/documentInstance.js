import axios from "axios";
import Cookies from "js-cookie";

const documentInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  headers: {
    Authorization: `Bearer ${Cookies.get("access_token")}`,
  },
});

export default documentInstance;
