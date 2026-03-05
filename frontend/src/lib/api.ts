import axios from 'axios';
import axiosRetry from 'axios-retry';
import { ChatRequestPayload, ChatResponsePayload, MetricsPayload } from '@/types';

// Trong môi trường dev, trỏ về Server uvicorn địa phương
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Tự động retry nếu backend bị timeout / rate limit nhẹ
axiosRetry(apiClient, { retries: 2, retryDelay: axiosRetry.exponentialDelay });

export const chatApi = {
    sendMessage: async (payload: ChatRequestPayload): Promise<ChatResponsePayload> => {
        const response = await apiClient.post<ChatResponsePayload>('/chat', payload);
        return response.data;
    },

    getSession: async (sessionId: string) => {
        const response = await apiClient.get(`/session/${sessionId}`);
        return response.data;
    },

    getMetrics: async (sessionId: string): Promise<MetricsPayload> => {
        const response = await apiClient.get<MetricsPayload>(`/metrics/${sessionId}`);
        return response.data;
    }
};
