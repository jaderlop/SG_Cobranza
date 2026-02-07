/**
 * Top Products Table Component
 * Displays ranking of best-selling products
 */

import React from 'react';
import { TopProduct } from '@/types/dashboard';
import { TrendingUp, Package } from 'lucide-react';

interface TopProductsTableProps {
    products: TopProduct[];
    loading?: boolean;
}

export default function TopProductsTable({ products, loading }: TopProductsTableProps) {
    if (loading) {
        return (
            <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Productos</h3>
                <div className="animate-pulse space-y-3">
                    {[...Array(5)].map((_, i) => (
                        <div key={i} className="h-12 bg-gray-200 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    if (products.length === 0) {
        return (
            <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Productos</h3>
                <div className="h-64 flex flex-col items-center justify-center text-gray-400">
                    <Package className="w-16 h-16 mb-4 opacity-50" />
                    <p>No hay datos de productos</p>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                    Top Productos
                </h3>
                <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">
                    {products.length} productos
                </span>
            </div>

            <div className="space-y-3">
                {products.map((product, index) => (
                    <div
                        key={product.product_id}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <div className="flex items-center space-x-4 flex-1">
                            <div className={`flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm ${index === 0 ? 'bg-yellow-400 text-yellow-900' :
                                index === 1 ? 'bg-gray-300 text-gray-700' :
                                    index === 2 ? 'bg-orange-300 text-orange-900' :
                                        'bg-blue-100 text-blue-700'
                                }`}>
                                {index + 1}
                            </div>
                            <div className="flex-1">
                                <p className="font-semibold text-gray-900">{product.product_name}</p>
                                <p className="text-sm text-gray-500">
                                    {product.total_quantity.toLocaleString()} unidades vendidas
                                </p>
                            </div>
                        </div>
                        <div className="text-right">
                            <p className="text-lg font-bold text-gray-900">
                                ${product.total_amount.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                            </p>
                            <p className="text-xs text-gray-500">
                                Total ventas
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
