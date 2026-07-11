import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            E-Store
          </Link>
          <div className="flex gap-6">
            <Link to="/" className="text-gray-600 hover:text-blue-600 transition">
              Dashboard
            </Link>
            <Link to="/products" className="text-gray-600 hover:text-blue-600 transition">
              Products
            </Link>
            <Link to="/categories" className="text-gray-600 hover:text-blue-600 transition">
              Categories
            </Link>
            <Link to="/orders" className="text-gray-600 hover:text-blue-600 transition">
              Orders
            </Link>
            <Link to="/users" className="text-gray-600 hover:text-blue-600 transition">
              Users
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
