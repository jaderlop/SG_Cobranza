'use client';

import { useEffect, useState } from 'react';
import { purchasesAPI, productsAPI } from '@/lib/api';

interface Product {
    id: number;
    name: string;
    price: number;
    cost?: number;
}

interface Supplier {
    id: number;
    name: string;
}

interface PurchaseItem {
    product_id: number;
    quantity: number;
    unit_price: number;
}

export default function PurchasesPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [purchases, setPurchases] = useState<any[]>([]);
    const [suppliers, setSuppliers] = useState<Supplier[]>([
        { id: 1, name: 'Proveedor 1' },
        { id: 2, name: 'Proveedor 2' },
    ]);
    const [selectedSupplierId, setSelectedSupplierId] = useState(1);
    const [selectedItems, setSelectedItems] = useState<PurchaseItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [productsRes, purchasesRes] = await Promise.all([
                productsAPI.getAll(),
                purchasesAPI.getAll(),
            ]);
            setProducts(productsRes);
            setPurchases(purchasesRes);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const addItem = () => {
        if (products.length > 0) {
            setSelectedItems([
                ...selectedItems,
                {
                    product_id: products[0].id,
                    quantity: 1,
                    unit_price: products[0].cost || products[0].price * 0.7,
                },
            ]);
        }
    };

    const removeItem = (index: number) => {
        setSelectedItems(selectedItems.filter((_, i) => i !== index));
    };

    const updateItem = (
        index: number,
        field: 'product_id' | 'quantity' | 'unit_price',
        value: number
    ) => {
        const newItems = [...selectedItems];
        newItems[index][field] = value;
        setSelectedItems(newItems);
    };

    const calculateTotal = () => {
        return selectedItems.reduce((sum, item) => sum + item.quantity * item.unit_price, 0);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (selectedItems.length === 0) {
            alert('Debe agregar al menos un producto');
            return;
        }

        setLoading(true);
        try {
            await purchasesAPI.create({
                purchase_number: `PO-${Date.now()}`, // o lo que quieras como formato
                supplier_id: selectedSupplierId,
                purchase_date: new Date().toISOString().slice(0, 10),
                due_date: new Date().toISOString().slice(0, 10),
                status: 'pending',
                notes: '',
                items: selectedItems.map(item => ({
                    product_id: item.product_id,
                    quantity: item.quantity,
                    unit_price: item.unit_price,
                })),
            });

            setSuccess(true);
            setSelectedItems([]);
            await loadData();
            setTimeout(() => setSuccess(false), 3000);
        } catch (error: any) {
            console.error(error.response?.data);
            alert(JSON.stringify(error.response?.data, null, 2) || 'Error al crear compra');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1 className="text-3xl font-bold mb-8 text-gray-800">Compras</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Form */}
                <div className="card">
                    <h2 className="text-xl font-semibold mb-4 text-gray-800">Registrar Compra</h2>

                    {success && (
                        <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                            ✓ Compra registrada exitosamente
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label className="label">Proveedor</label>
                            <select
                                className="input"
                                value={selectedSupplierId}
                                onChange={(e) => setSelectedSupplierId(parseInt(e.target.value))}
                            >
                                {suppliers.map((s) => (
                                    <option key={s.id} value={s.id}>
                                        {s.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-4">
                            <div className="flex justify-between items-center mb-3">
                                <label className="label">Productos</label>
                                <button type="button" onClick={addItem} className="text-sm btn btn-secondary">
                                    + Agregar Producto
                                </button>
                            </div>

                            {selectedItems.map((item, index) => {
                                const product = products.find((p) => p.id === item.product_id);
                                return (
                                    <div key={index} className="grid grid-cols-12 gap-2 mb-2">
                                        <div className="col-span-5">
                                            <select
                                                className="input text-sm"
                                                value={item.product_id}
                                                onChange={(e) => updateItem(index, 'product_id', parseInt(e.target.value))}
                                            >
                                                {products.map((p) => (
                                                    <option key={p.id} value={p.id}>
                                                        {p.name}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="col-span-2">
                                            <input
                                                type="number"
                                                min="1"
                                                className="input text-sm"
                                                value={item.quantity}
                                                onChange={(e) => updateItem(index, 'quantity', parseInt(e.target.value))}
                                                placeholder="Cant."
                                            />
                                        </div>
                                        <div className="col-span-3">
                                            <input
                                                type="number"
                                                step="0.01"
                                                min="0"
                                                className="input text-sm"
                                                value={item.unit_price}
                                                onChange={(e) =>
                                                    updateItem(index, 'unit_price', parseFloat(e.target.value))
                                                }
                                                placeholder="Costo"
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
                            {loading ? 'Guardando...' : 'Registrar Compra'}
                        </button>
                    </form>
                </div>

                {/* Purchases List */}
                <div className="card">
                    <h2 className="text-xl font-semibold mb-4 text-gray-800">Historial de Compras</h2>
                    <div className="max-h-96 overflow-y-auto">
                        {purchases.length === 0 ? (
                            <p className="text-gray-500 italic text-sm">No hay compras registradas</p>
                        ) : (
                            <div className="space-y-3">
                                {purchases.map((purchase) => (
                                    <div key={purchase.id} className="p-3 bg-gray-50 rounded border">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <p className="font-semibold">Compra #{purchase.id}</p>
                                                <p className="text-sm text-gray-600">
                                                    {new Date(purchase.created_at).toLocaleString('es-ES')}
                                                </p>
                                                <p className="text-xs text-gray-500 mt-1">
                                                    Proveedor ID: {purchase.supplier_id}
                                                </p>
                                                <p className="text-xs text-gray-500">
                                                    {purchase.items?.length || 0} producto(s)
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-lg font-bold text-red-600">
                                                    ${parseFloat(purchase.total_amount).toFixed(2)}
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
