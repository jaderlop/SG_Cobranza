import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
    baseURL: `${API_URL}/api`,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Unauthorized - clear token and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/auth/login';
        }
        return Promise.reject(error);
    }
);

// Authentication API
export const authAPI = {
    login: async (username: string, password: string) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post('/auth/login', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    logout: async () => {
        const response = await apiClient.post('/auth/logout');
        return response.data;
    },

    getCurrentUser: async () => {
        const response = await apiClient.get('/auth/me');
        return response.data;
    },
};

// Clients API
export const clientsAPI = {
    getAll: async (skip = 0, limit = 100) => {
        const response = await apiClient.get(`/clients?skip=${skip}&limit=${limit}`);
        return response.data;
    },

    getById: async (id: number) => {
        const response = await apiClient.get(`/clients/${id}`);
        return response.data;
    },

    create: async (data: any) => {
        const response = await apiClient.post('/clients', data);
        return response.data;
    },

    update: async (id: number, data: any) => {
        const response = await apiClient.put(`/clients/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await apiClient.delete(`/clients/${id}`);
        return response.data;
    },
};

// Products API
export const productsAPI = {
    getAll: async (skip = 0, limit = 100, category?: string) => {
        let url = `/products?skip=${skip}&limit=${limit}`;
        if (category) url += `&category=${category}`;
        const response = await apiClient.get(url);
        return response.data;
    },

    getById: async (id: number) => {
        const response = await apiClient.get(`/products/${id}`);
        return response.data;
    },

    create: async (data: any) => {
        const response = await apiClient.post('/products', data);
        return response.data;
    },

    update: async (id: number, data: any) => {
        const response = await apiClient.put(`/products/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await apiClient.delete(`/products/${id}`);
        return response.data;
    },
};

export default apiClient;
