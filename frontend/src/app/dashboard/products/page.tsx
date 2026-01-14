'use client';

import { useEffect, useState } from 'react';
import { productsAPI } from '@/lib/api';

interface Product {
    id: number;
    name: string;
    sku?: string;
    price: number;
    cost?: number;
    stock_quantity: number;
    unit: string;
    category?: string;
    is_active: boolean;
}

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [editingProduct, setEditingProduct] = useState<Product | null>(null);
    const [formData, setFormData] = useState({
        name: '',
        sku: '',
        price: '',
        cost: '',
        stock_quantity: '0',
        unit: 'unit',
        category: '',
    });

    useEffect(() => {
        loadProducts();
    }, []);

    const loadProducts = async () => {
        try {
            const data = await productsAPI.getAll();
            setProducts(data);
        } catch (error) {
            console.error('Error loading products:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const payload = {
                ...formData,
                price: parseFloat(formData.price),
                cost: formData.cost ? parseFloat(formData.cost) : undefined,
                stock_quantity: parseInt(formData.stock_quantity),
            };

            if (editingProduct) {
                await productsAPI.update(editingProduct.id, payload);
            } else {
                await productsAPI.create(payload);
            }
            await loadProducts();
            resetForm();
        } catch (error: any) {
            alert(error.response?.data?.detail || 'Error al guardar producto');
        }
    };

    const handleEdit = (product: Product) => {
        setEditingProduct(product);
        setFormData({
            name: product.name,
            sku: product.sku || '',
            price: product.price.toString(),
            cost: product.cost?.toString() || '',
            stock_quantity: product.stock_quantity.toString(),
            unit: product.unit || 'unit',
            category: product.category || '',
        });
        setShowForm(true);
    };

    const handleDelete = async (id: number) => {
        if (!confirm('¿Eliminar este producto?')) return;
        try {
            await productsAPI.delete(id);
            await loadProducts();
        } catch (error: any) {
            alert(error.response?.data?.detail || 'Error al eliminar producto');
        }
    };

    const resetForm = () => {
        setFormData({
            name: '',
            sku: '',
            price: '',
            cost: '',
            stock_quantity: '0',
            unit: 'unit',
            category: '',
        });
        setEditingProduct(null);
        setShowForm(false);
    };

    if (loading) {
        return <div className="flex justify-center p-8">Cargando...</div>;
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Productos</h1>
                <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
                    {showForm ? 'Cancelar' : '+ Nuevo Producto'}
                </button>
            </div>

            {showForm && (
                <div className="card mb-6">
                    <h2 className="text-xl font-semibold mb-4">
                        {editingProduct ? 'Editar Producto' : 'Nuevo Producto'}
                    </h2>
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="label">Nombre *</label>
                            <input
                                type="text"
                                className="input"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label className="label">SKU</label>
                            <input
                                type="text"
                                className="input"
                                value={formData.sku}
                                onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">Categoría</label>
                            <input
                                type="text"
                                className="input"
                                value={formData.category}
                                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">Precio Venta *</label>
                            <input
                                type="number"
                                step="0.01"
                                className="input"
                                value={formData.price}
                                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label className="label">Costo</label>
                            <input
                                type="number"
                                step="0.01"
                                className="input"
                                value={formData.cost}
                                onChange={(e) => setFormData({ ...formData, cost: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">Stock Inicial</label>
                            <input
                                type="number"
                                className="input"
                                value={formData.stock_quantity}
                                onChange={(e) => setFormData({ ...formData, stock_quantity: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">Unidad</label>
                            <select
                                className="input"
                                value={formData.unit}
                                onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                            >
                                <option value="unit">Unidad</option>
                                <option value="kg">Kilogramo</option>
                                <option value="ltr">Litro</option>
                                <option value="m">Metro</option>
                                <option value="pack">Paquete</option>
                            </select>
                        </div>
                        <div className="md:col-span-3 flex gap-2">
                            <button type="submit" className="btn btn-primary">
                                {editingProduct ? 'Actualizar' : 'Crear'}
                            </button>
                            <button type="button" onClick={resetForm} className="btn btn-secondary">
                                Cancelar
                            </button>
                        </div>
                    </form>
                </div>
            )}

            <div className="card">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Producto</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">SKU</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Categoría</th>
                                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Precio</th>
                                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Stock</th>
                                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">Estado</th>
                                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {products.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                                        No hay productos registrados
                                    </td>
                                </tr>
                            ) : (
                                products.map((product) => (
                                    <tr key={product.id} className="hover:bg-gray-50">
                                        <td className="px-4 py-3 font-medium">{product.name}</td>
                                        <td className="px-4 py-3 text-sm text-gray-600">{product.sku || '-'}</td>
                                        <td className="px-4 py-3 text-sm text-gray-600">{product.category || '-'}</td>
                                        <td className="px-4 py-3 text-right font-medium">${product.price.toFixed(2)}</td>
                                        <td className="px-4 py-3 text-right">
                                            <span
                                                className={`px-2 py-1 text-xs rounded-full ${product.stock_quantity > 10
                                                        ? 'bg-green-100 text-green-800'
                                                        : product.stock_quantity > 0
                                                            ? 'bg-yellow-100 text-yellow-800'
                                                            : 'bg-red-100 text-red-800'
                                                    }`}
                                            >
                                                {product.stock_quantity} {product.unit}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-center">
                                            <span
                                                className={`px-2 py-1 text-xs rounded-full ${product.is_active
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-red-100 text-red-800'
                                                    }`}
                                            >
                                                {product.is_active ? 'Activo' : 'Inactivo'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-right space-x-2">
                                            <button
                                                onClick={() => handleEdit(product)}
                                                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                                            >
                                                Editar
                                            </button>
                                            <button
                                                onClick={() => handleDelete(product.id)}
                                                className="text-red-600 hover:text-red-800 text-sm font-medium"
                                            >
                                                Eliminar
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
