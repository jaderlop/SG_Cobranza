'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const router = useRouter();
    const { user, loading, logout, isAuthenticated } = useAuth();

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            router.push('/auth/login');
        }
    }, [isAuthenticated, loading, router]);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <h2 className="text-xl font-semibold mt-4">Cargando...</h2>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    const navItems = [
        { href: '/dashboard', icon: '📊', label: 'Dashboard' },
        { href: '/dashboard/sales', icon: '💰', label: 'Ventas' },
        { href: '/dashboard/purchases', icon: '🛒', label: 'Compras' },
        { href: '/dashboard/clients', icon: '👥', label: 'Clientes' },
        { href: '/dashboard/products', icon: '📦', label: 'Productos' },
    ];

    return (
        <div className="min-h-screen flex bg-gray-50">
            {/* Sidebar */}
            <aside className="w-64 bg-gradient-to-b from-gray-900 to-gray-800 text-white shadow-xl">
                <div className="p-6 border-b border-gray-700">
                    <div className="flex items-center space-x-3">
                        <div className="p-2 bg-blue-600 rounded-lg">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold">Sistema Gestión</h1>
                            <p className="text-xs text-gray-400">ERP Modular</p>
                        </div>
                    </div>
                </div>

                <nav className="mt-6 px-3">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className="flex items-center space-x-3 px-4 py-3 mb-1 rounded-lg hover:bg-gray-700 transition-all duration-200 group"
                        >
                            <span className="text-2xl group-hover:scale-110 transition-transform">{item.icon}</span>
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    ))}
                </nav>

                <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700">
                    <div className="px-4 py-3 bg-gray-700 rounded-lg mb-3">
                        <p className="text-xs text-gray-400">Usuario activo</p>
                        <p className="font-semibold truncate">{user?.username}</p>
                        <p className="text-xs text-gray-400 truncate">{user?.email}</p>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <header className="bg-white border-b border-gray-200 shadow-sm">
                    <div className="px-8 py-4 flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <h2 className="text-2xl font-bold text-gray-800">
                                Bienvenido, {user?.username}
                            </h2>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="text-sm text-gray-600">
                                {new Date().toLocaleDateString('es-ES', {
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </div>
                            <button
                                onClick={() => logout()}
                                className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition font-medium text-gray-700"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                </svg>
                                <span>Salir</span>
                            </button>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 p-8 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}
