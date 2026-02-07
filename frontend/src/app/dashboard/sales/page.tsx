'use client';

import { useEffect, useState } from 'react';
import { salesAPI, productsAPI } from '@/lib/api';

interface Product {
    id: number;
    name: string;
    price: number;
    stock_quantity: number;
}

interface SaleItem {
    product_id: number;
    quantity: number;
    unit_price: number;
}

export default function SalesPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [sales, setSales] = useState<any[]>([]);
    const [selectedItems, setSelectedItems] = useState<SaleItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [productsRes, salesRes] = await Promise.all([
                productsAPI.getAll(),
                salesAPI.getAll(),
            ]);
            setProducts(productsRes);
            setSales(salesRes);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const addItem = () => {
        if (products.length > 0) {
            setSelectedItems([...selectedItems, { product_id: products[0].id, quantity: 1, unit_price: products[0].price }]);
        }
    };

    const removeItem = (index: number) => {
        setSelectedItems(selectedItems.filter((_, i) => i !== index));
    };

    const updateItem = (
        index: number,
        field: 'product_id' | 'quantity',
        value: number
    ) => {
        const newItems = [...selectedItems];

        if (field === 'product_id') {
            const product = products.find(p => p.id === value);
            newItems[index].product_id = value;
            newItems[index].unit_price = product?.price || 0;
        }

        if (field === 'quantity') {
            newItems[index].quantity = value;
        }

        setSelectedItems(newItems);
    };


    const calculateTotal = () => {
        return selectedItems.reduce((sum, item) => {
            const product = products.find((p) => p.id === item.product_id);
            return sum + (product ? product.price * item.quantity : 0);
        }, 0);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (selectedItems.length === 0) {
            alert('Debe agregar al menos un producto');
            return;
        }

        const payload = {
            sale_number: `S-${Date.now()}`,
            client_id: 1, // luego lo haces seleccionable
            sale_date: new Date().toISOString().slice(0, 10),
            due_date: new Date().toISOString().slice(0, 10),
            status: 'pending',
            payment_status: 'unpaid',
            notes: '',
            items: selectedItems,
        };

        setLoading(true);
        try {
            await salesAPI.create(payload);
            setSuccess(true);
            setSelectedItems([]);
            await loadData();
            setTimeout(() => setSuccess(false), 3000);
        } catch (error: any) {
            console.error(error.response?.data);
            alert(error.response?.data?.detail || 'Error al crear venta');
        } finally {
            setLoading(false);
        }
    };


    return (
        <div>
            <h1 className="text-3xl font-bold mb-8 text-gray-800">Ventas</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Form */}
                <div className="card">
                    <h2 className="text-xl font-semibold mb-4 text-gray-800">Registrar Venta</h2>

                    {success && (
                        <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                            ✓ Venta registrada exitosamente
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <div className="flex justify-between items-center mb-3">
                                <label className="label">Productos</label>
                                <button
                                    type="button"
                                    onClick={addItem}
                                    className="text-sm btn btn-secondary"
                                >
                                    + Agregar Producto
                                </button>
                            </div>

                            {selectedItems.map((item, index) => {
                                const product = products.find((p) => p.id === item.product_id);
                                return (
                                    <div key={index} className="grid grid-cols-12 gap-2 mb-2">
                                        <div className="col-span-7">
                                            <select
                                                className="input text-sm"
                                                value={item.product_id}
                                                onChange={(e) => updateItem(index, 'product_id', parseInt(e.target.value))}
                                            >
                                                {products.map((p) => (
                                                    <option key={p.id} value={p.id}>
                                                        {p.name} (${p.price}) - Stock: {p.stock_quantity}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="col-span-3">
                                            <input
                                                type="number"
                                                min="1"
                                                className="input text-sm"
                                                value={item.quantity}
                                                onChange={(e) => updateItem(index, 'quantity', parseInt(e.target.value))}
                                                placeholder="Cant."
                                            />
                                        </div>
                                        <div className="col-span-2">
                                            <button
                                                type="button"
                                                onClick={() => removeItem(index)}
                                                className="w-full btn bg-red-100 hover:bg-red-200 text-red-700 text-sm"
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    </div>
                                );
                            })}

                            {selectedItems.length === 0 && (
                                <p className="text-sm text-gray-500 italic">No hay productos agregados</p>
                            )}
                        </div>

                        <div className="border-t pt-4 mb-4">
                            <div className="flex justify-between text-xl font-bold">
                                <span>Total:</span>
                                <span>${calculateTotal().toFixed(2)}</span>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading || selectedItems.length === 0}
                            className="w-full btn btn-primary"
                        >
                            {loading ? 'Guardando...' : 'Registrar Venta'}
                        </button>
                    </form>
                </div>

                {/* Sales List */}
                <div className="card">
                    <h2 className="text-xl font-semibold mb-4 text-gray-800">Historial de Ventas</h2>
                    <div className="max-h-96 overflow-y-auto">
                        {sales.length === 0 ? (
                            <p className="text-gray-500 italic text-sm">No hay ventas registradas</p>
                        ) : (
                            <div className="space-y-3">
                                {sales.map((sale) => (
                                    <div key={sale.id} className="p-3 bg-gray-50 rounded border">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <p className="font-semibold">Venta #{sale.id}</p>
                                                <p className="text-sm text-gray-600">
                                                    {new Date(sale.created_at).toLocaleString('es-ES')}
                                                </p>
                                                <p className="text-xs text-gray-500 mt-1">
                                                    {sale.items?.length || 0} producto(s)
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-lg font-bold text-green-600">
                                                    ${parseFloat(sale.total_amount).toFixed(2)}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
