'use client';

import { useEffect, useState } from 'react';
import { clientsAPI } from '@/lib/api';

interface Client {
    id: number;
    name: string;
    email?: string;
    phone?: string;
    tax_id?: string;
    is_active: boolean;
}

export default function ClientsPage() {
    const [clients, setClients] = useState<Client[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [editingClient, setEditingClient] = useState<Client | null>(null);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        tax_id: '',
    });

    useEffect(() => {
        loadClients();
    }, []);

    const loadClients = async () => {
        try {
            const data = await clientsAPI.getAll();
            setClients(data);
        } catch (error) {
            console.error('Error loading clients:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (editingClient) {
                await clientsAPI.update(editingClient.id, formData);
            } else {
                await clientsAPI.create(formData);
            }
            await loadClients();
            resetForm();
        } catch (error: any) {
            alert(error.response?.data?.detail || 'Error al guardar cliente');
        }
    };

    const handleEdit = (client: Client) => {
        setEditingClient(client);
        setFormData({
            name: client.name,
            email: client.email || '',
            phone: client.phone || '',
            tax_id: client.tax_id || '',
        });
        setShowForm(true);
    };

    const handleDelete = async (id: number) => {
        if (!confirm('¿Eliminar este cliente?')) return;
        try {
            await clientsAPI.delete(id);
            await loadClients();
        } catch (error: any) {
            alert(error.response?.data?.detail || 'Error al eliminar cliente');
        }
    };

    const resetForm = () => {
        setFormData({ name: '', email: '', phone: '', tax_id: '' });
        setEditingClient(null);
        setShowForm(false);
    };

    if (loading) {
        return <div className="flex justify-center p-8">Cargando...</div>;
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Clientes</h1>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="btn btn-primary"
                >
                    {showForm ? 'Cancelar' : '+ Nuevo Cliente'}
                </button>
            </div>

            {showForm && (
                <div className="card mb-6">
                    <h2 className="text-xl font-semibold mb-4">
                        {editingClient ? 'Editar Cliente' : 'Nuevo Cliente'}
                    </h2>
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                            <label className="label">Email</label>
                            <input
                                type="email"
                                className="input"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">Teléfono</label>
                            <input
                                type="tel"
                                className="input"
                                value={formData.phone}
                                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="label">RUC/NIT</label>
                            <input
                                type="text"
                                className="input"
                                value={formData.tax_id}
                                onChange={(e) => setFormData({ ...formData, tax_id: e.target.value })}
                            />
                        </div>
                        <div className="md:col-span-2 flex gap-2">
                            <button type="submit" className="btn btn-primary">
                                {editingClient ? 'Actualizar' : 'Crear'}
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
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Nombre</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Teléfono</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">RUC/NIT</th>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Estado</th>
                                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {clients.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                                        No hay clientes registrados
                                    </td>
                                </tr>
                            ) : (
                                clients.map((client) => (
                                    <tr key={client.id} className="hover:bg-gray-50">
                                        <td className="px-4 py-3 font-medium">{client.name}</td>
                                        <td className="px-4 py-3 text-sm text-gray-600">{client.email || '-'}</td>
                                        <td className="px-4 py-3 text-sm text-gray-600">{client.phone || '-'}</td>
                                        <td className="px-4 py-3 text-sm text-gray-600">{client.tax_id || '-'}</td>
                                        <td className="px-4 py-3">
                                            <span
                                                className={`px-2 py-1 text-xs rounded-full ${client.is_active
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-red-100 text-red-800'
                                                    }`}
                                            >
                                                {client.is_active ? 'Activo' : 'Inactivo'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-right space-x-2">
                                            <button
                                                onClick={() => handleEdit(client)}
                                                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                                            >
                                                Editar
                                            </button>
                                            <button
                                                onClick={() => handleDelete(client.id)}
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
