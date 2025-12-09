# Frontend - Next.js Application

## Overview

Modern web frontend built with Next.js 14 and React 18 for the SMB Financial Management System.

## Features

- ✅ Server-side rendering (SSR) with Next.js
- ✅ TypeScript for type safety
- ✅ TailwindCSS for styling
- ✅ JWT authentication
- ✅ Protected routes
- ✅ Responsive sidebar navigation
- ✅ Dashboard with metrics
- ✅ Chart.js integration for data visualization
- ✅ Form handling with React Hook Form
- ✅ API client with axios
- ✅ Modern UI components

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **UI Library**: React 18
- **TypeScript**: Type-safe development
- **Styling**: TailwindCSS
- **Charts**: Chart.js + react-chartjs-2
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios with SWR for data fetching
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── auth/
│   │   │   └── login/             # Login page
│   │   ├── dashboard/             # Protected dashboard pages
│   │   │   ├── layout.tsx         # Dashboard layout with sidebar
│   │   │   ├── page.tsx           # Dashboard home
│   │   │   ├── clients/           # Clients pages
│   │   │   ├── products/          # Products pages
│   │   │   └── ...                # Other module pages
│   │   ├── globals.css            # Global styles
│   │   └── layout.tsx             # Root layout
│   ├── components/
│   │   ├── ui/                    # Reusable UI components
│   │   ├── forms/                 # Form components
│   │   ├── charts/                # Chart components
│   │   ├── tables/                # Table components
│   │   └── layout/                # Layout components
│   ├── lib/
│   │   └── api.ts                 # API client
│   ├── hooks/                     # Custom React hooks
│   ├── context/                   # React context providers
│   └── types/                     # TypeScript type definitions
├── public/                        # Static files
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit environment variables
nano .env.local
```

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Default Login

After backend seed data is loaded:

- **Admin**: username: `admin`, password: `admin123`
- **Accountant**: username: `contador`, password: `admin123`
- **Salesperson**: username: `vendedor`, password: `admin123`

## Pages

### Authentication
- `/auth/login` - Login page

### Dashboard (Protected)
- `/dashboard` - Dashboard home with metrics and charts
- `/dashboard/clients` - Client management
- `/dashboard/suppliers` - Supplier management
- `/dashboard/products` - Product management
- `/dashboard/sales` - Sales orders
- `/dashboard/purchases` - Purchase orders
- `/dashboard/invoices` - Invoice management with OCR
- `/dashboard/inventory` - Inventory tracking
- `/dashboard/reports` - Financial reports

## Components

### Layout Components
- `DashboardLayout` - Main dashboard layout with sidebar and header
- Sidebar navigation with active state
- Header with user info and logout

### UI Components (to be implemented)
- Button
- Input
- Card
- Table
- Modal
- Dropdown
- Badge
- Alert

### Form Components (to be implemented)
- ClientForm
- ProductForm
- InvoiceForm
- etc.

### Chart Components (to be implemented)
- SalesChart - Line chart for sales over time
- ExpensesChart - Pie chart for expense categories
- CashFlowChart - Bar chart for cash flow

## API Integration

The `lib/api.ts` file provides a centralized API client:

```typescript
import { authAPI, clientsAPI, productsAPI } from '@/lib/api';

// Login
const tokens = await authAPI.login('username', 'password');

// Get clients
const clients = await clientsAPI.getAll();

// Create product
const product = await productsAPI.create(productData);
```

## Styling

### TailwindCSS

Custom utility classes are defined in `globals.css`:

- `.btn` - Base button styles
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.btn-danger` - Danger button
- `.card` - Card container
- `.input` - Input field
- `.label` - Form label

### Color Palette

- **Primary**: Blue tones (brand color)
- **Success**: Green (#10b981)
- **Danger**: Red (#ef4444)
- **Warning**: Amber (#f59e0b)

## Authentication Flow

1. User enters credentials on login page
2. Frontend sends request to `/api/auth/login`
3. Backend returns JWT access and refresh tokens
4. Tokens stored in localStorage
5. API client automatically adds token to requests
6. Protected routes check for token and redirect if missing

## Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch
```

## Frontend Agent Deliverable Status

✅ Implemented:
- Next.js 14 project structure
- Authentication system
- API client with interceptors
- Login page
- Dashboard layout with sidebar
- Dashboard home with metrics
- TailwindCSS configuration
- TypeScript configuration

🚧 To implement:
- Client management pages (CRUD)
- Product management pages (CRUD)
- Sales, Purchases, Invoices pages
- Chart components with real data
- Invoice photo upload interface
- OCR data editor
- Report generation and export
- Form validation with Zod
- Data tables with sorting/filtering
- Additional UI components

## Best Practices

- Use TypeScript for all components
- Follow Next.js App Router conventions
- Use server components where possible
- Client components only when interactivity needed
- Keep components small and focused
- Use custom hooks for reusable logic
- Validate all forms with Zod
- Handle loading and error states
- Implement optimistic UI updates
- Use SWR for data fetching and caching

## Next Steps

1. Implement remaining CRUD pages
2. Add Chart.js components with real data
3. Create invoice upload and OCR interface
4. Build report generation UI
5. Add form validation
6. Create reusable UI components
7. Implement data tables
8. Add loading skeletons
9. Error boundary components
10. Responsive mobile design
