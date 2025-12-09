'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { authAPI } from '@/lib/api';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const router = useRouter();
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) {
                router.push('/auth/login');
                return;
            }

            try {
                const userData = await authAPI.getCurrentUser();
                setUser(userData);
            } catch (error) {
                localStorage.removeItem('access_token');
                router.push('/auth/login');
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, [router]);

    const handleLogout = async () => {
        try {
            await authAPI.logout();
        } catch (error) {
            // Ignore logout errors
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            router.push('/auth/login');
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <h2 className="text-xl font-semibold">Loading...</h2>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-900 text-white">
                <div className="p-6">
                    <h1 className="text-2xl font-bold">SMB Financial</h1>
                </div>

                <nav className="mt-6">
                    <a href="/dashboard" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Dashboard
                    </a>
                    <a href="/dashboard/clients" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Clients
                    </a>
                    <a href="/dashboard/suppliers" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Suppliers
                    </a>
                    <a href="/dashboard/products" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Products
                    </a>
                    <a href="/dashboard/sales" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Sales
                    </a>
                    <a href="/dashboard/purchases" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Purchases
                    </a>
                    <a href="/dashboard/invoices" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Invoices
                    </a>
                    <a href="/dashboard/inventory" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Inventory
                    </a>
                    <a href="/dashboard/reports" className="block px-6 py-3 hover:bg-gray-800 transition-colors">
                        Reports
                    </a>
                </nav>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <header className="bg-white border-b border-gray-200 px-8 py-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xl font-semibold text-gray-800">Welcome, {user?.username}</h2>
                        <button
                            onClick={handleLogout}
                            className="btn btn-secondary"
                        >
                            Logout
                        </button>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 p-8 bg-gray-50">
                    {children}
                </main>
            </div>
        </div>
    );
}
