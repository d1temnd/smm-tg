import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Posts from './components/Posts';
import CreatePost from './components/CreatePost';
import Profile from './pages/Profile';
import AdminPanel from './pages/AdminPanel';
import ProtectedRoute from './components/ProtectedRoute';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<Layout />}>
            <Route path="/" element={
              <ProtectedRoute requiredRole="user">
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/posts" element={
              <ProtectedRoute requiredRole="user">
                <Posts />
              </ProtectedRoute>
            } />
            <Route path="/posts/create" element={
              <ProtectedRoute requiredRole="editor">
                <CreatePost />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute requiredRole="user">
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/admin" element={
              <ProtectedRoute requiredRole="admin">
                <AdminPanel />
              </ProtectedRoute>
            } />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App; 