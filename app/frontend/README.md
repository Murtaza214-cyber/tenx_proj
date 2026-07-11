# E-Commerce Frontend

A modern React frontend for managing an e-commerce store with products, categories, orders, and users.

## Features

- **Dashboard**: Overview of products, categories, orders, and users
- **Products Management**: Create, read, update, and delete products
- **Categories Management**: Manage product categories
- **Orders Management**: View and manage customer orders
- **Users Management**: Manage customer information
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Tech Stack

- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn installed

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist` folder.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/         # Reusable React components
│   └── Navbar.jsx
├── pages/             # Page components
│   ├── Dashboard.jsx
│   ├── ProductsPage.jsx
│   ├── CategoriesPage.jsx
│   ├── OrdersPage.jsx
│   └── UsersPage.jsx
├── services/          # API service layer
│   └── api.js
├── App.jsx            # Main app component with routing
├── main.jsx           # React entry point
└── index.css          # Global styles
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000`. The API endpoints are configured in `src/services/api.js`.

Make sure your FastAPI backend is running before starting the frontend development server.

### Proxy Configuration

The Vite dev server is configured to proxy API requests from `/api` to `http://localhost:8000` for easier development.

## Available Routes

- `/` - Dashboard
- `/products` - Products management
- `/categories` - Categories management
- `/orders` - Orders management
- `/users` - Users management

## Development Tips

- Hot Module Replacement (HMR) is enabled by default in Vite
- Changes to components will reflect instantly in the browser
- Console errors and warnings are displayed in the browser dev tools
- Network requests can be monitored in the Network tab

## Troubleshooting

If you encounter CORS issues:
1. Make sure the backend is running on `http://localhost:8000`
2. Check that CORS is properly configured in your FastAPI backend

For styling issues:
- Tailwind CSS classes might need a rebuild
- Try clearing the cache: `rm -rf node_modules .vite` and reinstall
