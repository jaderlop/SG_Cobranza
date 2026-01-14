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
    (error) => {
        if (error.response?.status === 401) {
            console.warn("⚠️ 401 Unauthorized – limpiando sesión");

            if (typeof window !== "undefined") {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");

                // redirigir al login
                window.location.href = "/auth/login";
            }
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

// Sales API
export const salesAPI = {
    getAll: async () => {
        const response = await apiClient.get('/sales');
        return response.data;
    },

    create: async (data: { items: Array<{ product_id: number; quantity: number }> }) => {
        const response = await apiClient.post('/sales', data);
        return response.data;
    },
};

// Purchases API
export const purchasesAPI = {
    getAll: async () => {
        const response = await apiClient.get('/purchases');
        return response.data;
    },

    create: async (data: {
        supplier_id: number;
        items: Array<{ product_id: number; quantity: number; unit_cost: number }>
    }) => {
        const response = await apiClient.post('/purchases', data);
        return response.data;
    },
};

// Dashboard API
export const dashboardAPI = {
    getKPIs: async () => {
        const response = await apiClient.get('/dashboard/kpis');
        return response.data;
    },

    getSalesByDay: async () => {
        const response = await apiClient.get('/dashboard/sales-by-day');
        return response.data;
    },

    getPurchasesByDay: async () => {
        const response = await apiClient.get('/dashboard/purchases-by-day');
        return response.data;
    },

    getTopProducts: async () => {
        const response = await apiClient.get('/dashboard/top-products');
        return response.data;
    },
};

export default apiClient;
