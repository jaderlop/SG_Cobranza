/**
 * KPI Card Component
 * Reusable card component for displaying Key Performance Indicators
 */

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KPICardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: LucideIcon;
    colorScheme: 'blue' | 'green' | 'red' | 'purple' | 'orange' | 'yellow' | 'indigo';
    trend?: {
        value: number;
        isPositive: boolean;
    };
}

const colorClasses = {
    blue: {
        gradient: 'from-blue-500 to-blue-600',
        light: 'text-blue-100',
        bg: 'bg-blue-100',
        text: 'text-blue-600'
    },
    green: {
        gradient: 'from-green-500 to-green-600',
        light: 'text-green-100',
        bg: 'bg-green-100',
        text: 'text-green-600'
    },
    red: {
        gradient: 'from-red-500 to-red-600',
        light: 'text-red-100',
        bg: 'bg-red-100',
        text: 'text-red-600'
    },
    purple: {
        gradient: 'from-purple-500 to-purple-600',
        light: 'text-purple-100',
        bg: 'bg-purple-100',
        text: 'text-purple-600'
    },
    orange: {
        gradient: 'from-orange-500 to-orange-600',
        light: 'text-orange-100',
        bg: 'bg-orange-100',
        text: 'text-orange-600'
    },
    yellow: {
        gradient: 'from-yellow-500 to-yellow-600',
        light: 'text-yellow-100',
        bg: 'bg-yellow-100',
        text: 'text-yellow-700'
    },
    indigo: {
        gradient: 'from-indigo-500 to-indigo-600',
        light: 'text-indigo-100',
        bg: 'bg-indigo-100',
        text: 'text-indigo-600'
    }
};

export default function KPICard({
    title,
    value,
    subtitle,
    icon: Icon,
    colorScheme,
    trend
}: KPICardProps) {
    const colors = colorClasses[colorScheme];

    return (
        <div className={`bg-gradient-to-br ${colors.gradient} rounded-xl shadow-lg p-6 text-white transform hover:scale-105 transition-transform duration-200`}>
            <div className="flex items-center justify-between">
                <div className="flex-1">
                    <p className={`${colors.light} text-sm font-medium mb-2`}>
                        {title}
                    </p>
                    <p className="text-3xl font-bold mb-1">
                        {value}
                    </p>
                    {subtitle && (
                        <p className={`${colors.light} text-xs mt-2`}>
                            {subtitle}
                        </p>
                    )}
                    {trend && (
                        <div className={`flex items-center mt-2 text-xs ${colors.light}`}>
                            {trend.isPositive ? (
                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            ) : (
                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                                </svg>
                            )}
                            <span>{Math.abs(trend.value)}%</span>
                        </div>
                    )}
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-lg backdrop-blur-sm">
                    <Icon className="w-8 h-8" />
                </div>
            </div>
        </div>
    );
}
