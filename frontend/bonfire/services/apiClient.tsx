import axios from "axios";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;
const apiPort = process.env.NEXT_PUBLIC_API_PORT;

export const ApiClient = axios.create({
    baseURL: `${apiUrl}:${apiPort}/`,
    // baseURL: "http://127.0.0.1:5000/autoInfracao/",
    timeout: 180000,
    headers: {
        'X-Custom-Header': 'foobar',
    }
});