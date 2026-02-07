'use client';

/**
 * Dashboard Main Page
 * Complete dashboard with 11 KPIs, 4 charts, and quick access links
 */

import { useEffect, useState } from 'react';
import { dashboardAPI } from '@/lib/api';
import { Line, Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import {
    DollarSign,
    ShoppingCart,
    TrendingUp,
    Users,
    Package,
    Calendar,
    AlertTriangle,
    CheckCircle,
    Clock,
    BarChart3,
    RefreshCw,
    ArrowRight,
} from 'lucide-react';
import KPICard from '@/components/dashboard/KPICard';
import TopProductsTable from '@/components/dashboard/TopProductsTable';
import SalesByStatusChart from '@/components/dashboard/SalesByStatusChart';
import { DashboardState } from '@/types/dashboard';
import Link from 'next/link';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export default function DashboardPage() {
    const [state, setState] = useState<DashboardState>({
        kpis: null,
        salesByDay: [],
        purchasesByDay: [],
        salesByStatus: [],
        topProducts: [],
        loading: true,
        error: null,
    });

    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        setRefreshing(true);
        try {
            const [kpis, salesByDay, purchasesByDay, salesByStatus, topProducts] =
                await Promise.all([
                    dashboardAPI.getKPIs(),
                    dashboardAPI.getSalesByDay(30),
                    dashboardAPI.getPurchasesByDay(30),
                    dashboardAPI.getSalesByStatus(),
                    dashboardAPI.getTopProducts(5),
                ]);

            setState({
                kpis,
                salesByDay,
                purchasesByDay,
                salesByStatus,
                topProducts,
                loading: false,
                error: null,
            });
        } catch (error: any) {
            console.error('Error loading dashboard:', error);
            setState(prev => ({
                ...prev,
                loading: false,
                error: error.response?.data?.detail || 'Error al cargar el dashboard',
            }));
        } finally {
            setRefreshing(false);
        }
    };

    if (state.loading) {
        return (
            <div className="flex items-center justify-center min-h-96">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>
                    <p className="mt-4 text-xl text-gray-600 font-medium">Cargando dashboard...</p>
                </div>
            </div>
        );
    }

    if (state.error) {
        return (
            <div className="flex items-center justify-center min-h-96">
                <div className="text-center max-w-md">
                    <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Error al cargar dashboard</h3>
                    <p className="text-gray-600 mb-4">{state.error}</p>
                    <button
                        onClick={loadDashboardData}
                        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    const { kpis, salesByDay, purchasesByDay, salesByStatus, topProducts } = state;

    // Chart configurations
    const salesChartData = {
        labels: salesByDay.map(d => new Date(d.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })),
        datasets: [
            {
                label: 'Ventas',
                data: salesByDay.map(d => d.total),
                borderColor: 'rgb(16, 185, 129)',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2,
            },
        ],
    };

    const purchasesChartData = {
        labels: purchasesByDay.map(d => new Date(d.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })),
        datasets: [
            {
                label: 'Compras',
                data: purchasesByDay.map(d => d.total),
                backgroundColor: 'rgba(239, 68, 68, 0.8)',
                borderColor: 'rgb(239, 68, 68)',
                borderWidth: 1,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            title: { display: false },
            tooltip: {
                callbacks: {
                    label: function (context: any) {
                        return `$${context.parsed.y.toLocaleString('es-ES', { minimumFractionDigits: 2 })}`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: 'rgba(0, 0, 0, 0.05)' },
                ticks: {
                    callback: function (value: any) {
                        return '$' + value.toLocaleString('es-ES');
                    }
                }
            },
            x: { grid: { display: false } },
        },
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-600 mt-1">Resumen general de operaciones del negocio</p>
                </div>
                <button
                    onClick={loadDashboardData}
                    disabled={refreshing}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
                    <span>{refreshing ? 'Actualizando...' : 'Actualizar'}</span>
                </button>
            </div>

            {/* Main KPIs - Row 1 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Ventas"
                    value={`$${kpis?.total_sales_amount.toLocaleString('es-ES', { minimumFractionDigits: 2 }) || '0.00'}`}
                    subtitle={`${kpis?.total_sales_count || 0} transacciones`}
                    icon={DollarSign}
                    colorScheme="green"
                />
                <KPICard
                    title="Total Compras"
                    value={`$${kpis?.total_purchases_amount.toLocaleString('es-ES', { minimumFractionDigits: 2 }) || '0.00'}`}
                    subtitle="Costos totales"
                    icon={ShoppingCart}
                    colorScheme="red"
                />
                <KPICard
                    title="Total Productos"
                    value={kpis?.total_products || 0}
                    subtitle="Productos activos"
                    icon={Package}
                    colorScheme="blue"
                />
                <KPICard
                    title="Total Clientes"
                    value={kpis?.total_clients || 0}
                    subtitle="Clientes activos"
                    icon={Users}
                    colorScheme="purple"
                />
            </div>

            {/* Timeliness KPIs - Row 2 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <KPICard
                    title="Ventas Hoy"
                    value={`$${kpis?.sales_today.toLocaleString('es-ES', { minimumFractionDigits: 2 }) || '0.00'}`}
                    subtitle="Ingresos del día"
                    icon={Calendar}
                    colorScheme="green"
                />
                <KPICard
                    title="Ventas este Mes"
                    value={`$${kpis?.sales_this_month.toLocaleString('es-ES', { minimumFractionDigits: 2 }) || '0.00'}`}
                    subtitle="Ingresos mensuales"
                    icon={TrendingUp}
                    colorScheme="indigo"
                />
                <KPICard
                    title="Compras este Mes"
                    value={`$${kpis?.purchases_this_month.toLocaleString('es-ES', { minimumFractionDigits: 2 }) || '0.00'}`}
                    subtitle="Gastos mensuales"
                    icon={ShoppingCart}
                    colorScheme="orange"
                />
            </div>

            {/* Status KPIs - Row 3 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <KPICard
                    title="Ventas Pagadas"
                    value={kpis?.paid_sales_count || 0}
                    subtitle="Estado: pagado"
                    icon={CheckCircle}
                    colorScheme="green"
                />
                <KPICard
                    title="Ventas Pendientes"
                    value={kpis?.pending_sales_count || 0}
                    subtitle="Estado: pendiente"
                    icon={Clock}
                    colorScheme="yellow"
                />
                <KPICard
                    title="Stock Bajo"
                    value={kpis?.low_stock_products_count || 0}
                    subtitle="Productos bajo mínimo"
                    icon={AlertTriangle}
                    colorScheme="red"
                />
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Sales Chart */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-800">Ventas por Día</h3>
                        <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">
                            Últimos 30 días
                        </span>
                    </div>
                    <div className="h-80">
                        {salesByDay.length > 0 ? (
                            <Line data={salesChartData} options={chartOptions} />
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-gray-400">
                                <BarChart3 className="w-16 h-16 mb-4 opacity-50" />
                                <p>No hay datos de ventas</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Purchases Chart */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-800">Compras por Día</h3>
                        <span className="px-3 py-1 bg-red-100 text-red-800 text-sm rounded-full font-medium">
                            Últimos 30 días
                        </span>
                    </div>
                    <div className="h-80">
                        {purchasesByDay.length > 0 ? (
                            <Bar data={purchasesChartData} options={chartOptions} />
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-gray-400">
                                <BarChart3 className="w-16 h-16 mb-4 opacity-50" />
                                <p>No hay datos de compras</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Bottom Section: Status Chart + Top Products */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <SalesByStatusChart data={salesByStatus} />
                <TopProductsTable products={topProducts} />
            </div>

            {/* Quick Access Links */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl shadow-lg p-6 text-white">
                <h3 className="text-lg font-semibold mb-4">Accesos Rápidos</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <Link
                        href="/dashboard/sales"
                        className="flex items-center justify-between p-4 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition backdrop-blur-sm group"
                    >
                        <span className="font-medium">Ventas</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <Link
                        href="/dashboard/purchases"
                        className="flex items-center justify-between p-4 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition backdrop-blur-sm group"
                    >
                        <span className="font-medium">Compras</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <Link
                        href="/dashboard/products"
                        className="flex items-center justify-between p-4 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition backdrop-blur-sm group"
                    >
                        <span className="font-medium">Productos</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <Link
                        href="/dashboard/clients"
                        className="flex items-center justify-between p-4 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition backdrop-blur-sm group"
                    >
                        <span className="font-medium">Clientes</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
