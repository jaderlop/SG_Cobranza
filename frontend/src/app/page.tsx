'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function Home() {
    const router = useRouter();
    const { isAuthenticated, loading } = useAuth();

    useEffect(() => {
        if (!loading) {
            if (isAuthenticated) {
                router.push('/dashboard');
            } else {
                router.push('/auth/login');
            }
        }
    }, [isAuthenticated, loading, router]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <h2 className="text-xl font-semibold mt-4 text-gray-700">Cargando...</h2>
            </div>
        </div>
    );
}
