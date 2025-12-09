'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
    const router = useRouter();

    useEffect(() => {
        // Redirect to dashboard or login based on auth status
        const token = localStorage.getItem('access_token');
        if (token) {
            router.push('/dashboard');
        } else {
            router.push('/auth/login');
        }
    }, [router]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <h1 className="text-2xl font-bold">Loading...</h1>
            </div>
        </div>
    );
}
