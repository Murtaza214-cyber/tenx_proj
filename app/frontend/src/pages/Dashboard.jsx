import { useState, useEffect } from 'react'
import { productAPI, categoryAPI, orderAPI, userAPI } from '../services/api'

function Dashboard() {
  const [stats, setStats] = useState({
    products: 0,
    categories: 0,
    orders: 0,
    users: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const [productsRes, categoriesRes, ordersRes, usersRes] = await Promise.all([
        productAPI.getAll(),
        categoryAPI.getAll(),
        orderAPI.getAll(),
        userAPI.getAll(),
      ])

      setStats({
        products: productsRes.data.length,
        categories: categoriesRes.data.length,
        orders: ordersRes.data.length,
        users: usersRes.data.length,
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Products" count={stats.products} color="bg-blue-500" />
        <StatCard title="Categories" count={stats.categories} color="bg-green-500" />
        <StatCard title="Orders" count={stats.orders} color="bg-purple-500" />
        <StatCard title="Users" count={stats.users} color="bg-orange-500" />
      </div>
    </div>
  )
}

function StatCard({ title, count, color }) {
  return (
    <div className={`${color} text-white rounded-lg shadow p-6`}>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-4xl font-bold">{count}</p>
    </div>
  )
}

export default Dashboard
