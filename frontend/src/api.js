import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

const api = axios.create({
    // use this baseURL for every request made
    baseURL: import.meta.env.VITE_API_URL
})

// Intercepter: adds the correct headers to any requests we send
api.interceptors.request.use(
    (config) => {
        // if we have a token add it to the Authorization header
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api