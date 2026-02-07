# Dashboard Frontend - Guía de Uso

Dashboard completo para el sistema de gestión financiera. Consume todos los endpoints del backend y presenta KPIs, gráficos y accesos rápidos.

## 🚀 Características Implementadas

### KPIs (11 Total)
1. **Total Ventas** - Monto total de ventas y número de transacciones
2. **Total Compras** - Costos totales de compras
3. **Total Productos** - Número de productos activos en inventario
4. **Total Clientes** - Número de clientes activos
5. **Ventas Hoy** - Ingresos del día actual
6. **Ventas este Mes** - Ingresos del mes en curso
7. **Compras este Mes** - Gastos del mes en curso
8. **Ventas Pagadas** - Número de ventas con estado "pagado"
9. **Ventas Pendientes** - Número de ventas con estado "pendiente"
10. **Stock Bajo** - Productos con stock por debajo del nivel mínimo

### Gráficos (4 Total)
1. **Ventas por Día** - Gráfico de línea mostrando ventas de los últimos 30 días
2. **Compras por Día** - Gráfico de barras mostrando compras de los últimos 30 días
3. **Ventas por Estado** - Gráfico circular (doughnut) mostrando distribución de ventas por payment_status
4. **Top 5 Productos** - Tabla rankeada de productos más vendidos con medallas

### Accesos Rápidos
- Enlace a Ventas
- Enlace a Compras
- Enlace a Productos
- Enlace a Clientes

## 📁 Estructura de Archivos Creados

```
frontend/src/
├── types/
│   └── dashboard.ts                    # TypeScript types para datos del dashboard
├── components/
│   └── dashboard/
│       ├── KPICard.tsx                 # Componente reutilizable para KPI cards
│       ├── TopProductsTable.tsx        # Tabla de top productos con ranking
│       └── SalesByStatusChart.tsx      # Gráfico de ventas por estado
├── app/
│   └── dashboard/
│       └── page.tsx                    # Página principal del dashboard (MODIFICADO)
└── lib/
    └── api.ts                          # API client (MODIFICADO - agregados query params)
```

## 🎨 Componentes Reutilizables

### KPICard
Card con gradientes de color, iconos de Lucide React, y opcionalmente indicadores de tendencia.

**Props:**
- `title`: string - Título del KPI
- `value`: string | number - Valor principal a mostrar
- `subtitle`: string (opcional) - Texto descriptivo
- `icon`: LucideIcon - Icono de Lucide React
- `colorScheme`: Color del gradiente (blue, green, red, purple, orange, yellow, indigo)
- `trend`: Objeto con valor y dirección (opcional)

**Ejemplo:**
```tsx
<KPICard
    title="Total Ventas"
    value="$12,345.67"
    subtitle="125 transacciones"
    icon={DollarSign}
    colorScheme="green"
/>
```

### TopProductsTable
Tabla con ranking de productos más vendidos, incluyendo medallas para  los primeros 3 lugares.

**Props:**
- `products`: TopProduct[] - Array de productos
- `loading`: boolean (opcional) - Estado de carga

**Características:**
- Medallas doradas/plateadas/bronce para top 3
- Formato de moneda y cantidades
- Estado de vacío y loading
- Hover effects

### SalesByStatusChart
Gráfico circular (doughnut) mostrando distribución de ventas por estado de pago.

**Props:**
- `data`: SalesByStatus[] - Datos de ventas por estado
- `loading`: boolean (opcional) - Estado de carga

**Características:**
- Colores personalizados por estado
- Tooltips con detalles
- Leyenda en la parte inferior
- Resumen de conteos debajo del gráfico

## 🔧 Configuración y Ejecución

### Requisitos Previos
- Node.js 18+
- Backend corriendo en `http://localhost:8000`
- Variables de entorno configuradas

### Instalación
```bash
cd frontend
npm install
```

### Desarrollo
```bash
npm run dev
```
Abre [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

### Build de Producción
```bash
npm run build
npm run start
```

## 🔌 Endpoints Consumidos

Todos los endpoints son llamados desde `src/lib/api.ts`:

- `GET /api/dashboard/kpis` - Obtiene los 11 KPIs
- `GET /api/dashboard/sales-by-day?days=30` - Ventas últimos 30 días
- `GET /api/dashboard/purchases-by-day?days=30` - Compras últimos 30 días
- `GET /api/dashboard/sales-by-status` - Distribución de ventas por estado
- `GET /api/dashboard/top-products?limit=5` - Top 5 productos

## 🎯 Estados Manejados

### Loading State
Muestra spinner animado mientras se cargan los datos iniciales.

### Error State
Muestra mensaje de error con botón para reintentar si falla la carga de datos.

### Empty State
Cada gráfico/tabla muestra un estado vacío apropiado si no hay datos.

### Refreshing State
El botón "Actualizar" muestra estado de carga durante refresh.

## 🎨 Diseño Visual

### Paleta de Colores
- **Verde** (Green-500/600): Ventas, ingresos, positivo
- **Rojo** (Red-500/600): Compras, gastos, alertas
- **Azul** (Blue-500/600): Productos, información general
- **Púrpura** (Purple-500/600): Clientes
- **Naranja** (Orange-500/600): Compras mensuales
- **Amarillo** (Yellow-500/600): Pendientes, advertencias
- **Índigo** (Indigo-500/600): Ventas mensuales

### Animaciones
- Hover scale en KPI cards (scale-105)
- Spin en botón de actualizar durante refresh
- Slide en quick access links
- Pulse loading para skeletons

## 🧪 Testing

Para probar el dashboard con datos reales:

1. **Asegúrate que el backend esté corriendo:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Verifica que tengas datos de prueba en la base de datos**
   - Al menos algunas ventas con diferentes estados
   - Algunos productos vendidos
   - Compras recientes

3. **Inicia el frontend y navega al dashboard:**
   ```bash
   cd frontend
   npm run dev
   ```
   Visita: http://localhost:3000/dashboard

## 📝 Notas Técnicas

- **Framework**: Next.js 14 con App Router
- **Lenguaje**: TypeScript estricto
- **Estilos**: TailwindCSS con custom gradients
- **Gráficos**: react-chartjs-2 (Chart.js 4.x)
- **Iconos**: Lucide React
- **State Management**: React useState + useEffect (no necesita estado global)
- **Data Fetching**: Axios con interceptores para auth

## 🐛 Troubleshooting

### Los gráficos no se muestran
- Verifica que Chart.js esté registrado correctamente
- Revisa la consola del navegador
- Asegúrate que los datos tienen el formato correcto

### Error 404 en endpoints
- Verifica que el backend esté corriendo
- Confirma la variable `NEXT_PUBLIC_API_URL` en `.env.local`
- Revisa que los endpoints en el backend tengan el prefix correcto

### Datos aparecen como $0.00
- Verifica que haya datos en la base de datos
- Revisa los logs del backend para errores
- Confirma que el backend está retornando datos correctamente

## 🚀 Próximas Mejoras (Opcionales)

- [ ] Selector de rango de fechas personalizado
- [ ] Exportar datos a PDF/Excel
- [ ] Comparación con período anterior
- [ ] Real-time updates con WebSockets
- [ ] Filtros por cliente/producto
- [ ] Dashboard personalizable (drag & drop)

---

**Dashboard listo para producción** ✅
