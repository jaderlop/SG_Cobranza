/**
 * Dashboard Type Definitions
 * Types for all dashboard data structures matching backend schemas
 */

export interface KPIData {
    total_sales_count: number;
    total_sales_amount: number;
    total_purchases_amount: number;
    total_products: number;
    total_clients: number;
    sales_today: number;
    sales_this_month: number;
    purchases_this_month: number;
    pending_sales_count: number;
    paid_sales_count: number;
    low_stock_products_count: number;
}

export interface DailyAmount {
    date: string; // ISO format YYYY-MM-DD
    total: number;
}

export interface SalesByStatus {
    status: string; // 'paid', 'unpaid', 'partial', etc.
    count: number;
    total_amount: number;
}

export interface TopProduct {
    product_id: number;
    product_name: string;
    total_quantity: number;
    total_amount: number;
}

export interface DashboardData {
    kpis: KPIData | null;
    salesByDay: DailyAmount[];
    purchasesByDay: DailyAmount[];
    salesByStatus: SalesByStatus[];
    topProducts: TopProduct[];
}

export interface DashboardState extends DashboardData {
    loading: boolean;
    error: string | null;
}
