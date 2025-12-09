'use client';

export default function DashboardPage() {
    return (
        <div>
            <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {/* Metric Cards */}
                <div className="card">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Total Sales</h3>
                    <p className="text-3xl font-bold text-gray-900">$124,580</p>
                    <p className="text-sm text-success-600 mt-2">+12.5% from last month</p>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Total Expenses</h3>
                    <p className="text-3xl font-bold text-gray-900">$54,230</p>
                    <p className="text-sm text-danger-600 mt-2">+5.2% from last month</p>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Net Profit</h3>
                    <p className="text-3xl font-bold text-gray-900">$70,350</p>
                    <p className="text-sm text-success-600 mt-2">+18.3% from last month</p>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Active Clients</h3>
                    <p className="text-3xl font-bold text-gray-900">245</p>
                    <p className="text-sm text-gray-600 mt-2">+8 new this month</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Sales Chart Placeholder */}
                <div className="card">
                    <h3 className="text-lg font-semibold mb-4">Monthly Sales</h3>
                    <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                        <p className="text-gray-500">Chart will be rendered here</p>
                    </div>
                </div>

                {/* Expenses Chart Placeholder */}
                <div className="card">
                    <h3 className="text-lg font-semibold mb-4">Expenses by Category</h3>
                    <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                        <p className="text-gray-500">Chart will be rendered here</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
