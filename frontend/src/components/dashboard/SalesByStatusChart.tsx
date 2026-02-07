/**
 * Sales by Status Chart Component
 * Doughnut chart showing distribution of sales by payment status
 */

import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { SalesByStatus } from '@/types/dashboard';
import { PieChart } from 'lucide-react';

ChartJS.register(ArcElement, Tooltip, Legend);

interface SalesByStatusChartProps {
    data: SalesByStatus[];
    loading?: boolean;
}

export default function SalesByStatusChart({ data, loading }: SalesByStatusChartProps) {
    if (loading) {
        return (
            <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Ventas por Estado</h3>
                <div className="h-80 flex items-center justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Ventas por Estado</h3>
                <div className="h-80 flex flex-col items-center justify-center text-gray-400">
                    <PieChart className="w-16 h-16 mb-4 opacity-50" />
                    <p>No hay datos de ventas</p>
                </div>
            </div>
        );
    }

    const statusColors: Record<string, string> = {
        'paid': '#10b981',      // green-500
        'unpaid': '#ef4444',    // red-500
        'partial': '#f59e0b',   // amber-500
        'pending': '#6b7280',   // gray-500
        'completed': '#3b82f6', // blue-500
    };

    const chartData = {
        labels: data.map(item =>
            item.status.charAt(0).toUpperCase() + item.status.slice(1)
        ),
        datasets: [
            {
                data: data.map(item => item.total_amount),
                backgroundColor: data.map(item =>
                    statusColors[item.status.toLowerCase()] || '#6b7280'
                ),
                borderColor: '#ffffff',
                borderWidth: 2,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom' as const,
                labels: {
                    padding: 15,
                    font: {
                        size: 12,
                    },
                },
            },
            tooltip: {
                callbacks: {
                    label: function (context: any) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const index = context.dataIndex;
                        const count = data[index].count;
                        return [
                            `${label}: $${value.toLocaleString('es-ES', { minimumFractionDigits: 2 })}`,
                            `${count} ventas`
                        ];
                    }
                }
            }
        },
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-800">Ventas por Estado</h3>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-medium">
                    {data.reduce((sum, item) => sum + item.count, 0)} ventas
                </span>
            </div>
            <div className="h-80">
                <Doughnut data={chartData} options={chartOptions} />
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3">
                {data.map(item => (
                    <div
                        key={item.status}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                        <div className="flex items-center space-x-2">
                            <div
                                className="w-3 h-3 rounded-full"
                                style={{
                                    backgroundColor: statusColors[item.status.toLowerCase()] || '#6b7280'
                                }}
                            />
                            <span className="text-sm font-medium text-gray-700 capitalize">
                                {item.status}
                            </span>
                        </div>
                        <span className="text-sm font-semibold text-gray-900">
                            {item.count}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
