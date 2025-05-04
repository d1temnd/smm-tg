import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import ErrorPage from './ErrorPage';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'admin' | 'editor' | 'user';
}

export default function ProtectedRoute({ children, requiredRole = 'user' }: ProtectedRouteProps) {
  const { user, isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole === 'admin' && user?.rule !== 'admin') {
    return (
      <ErrorPage
        title="Access Denied"
        message="You don't have permission to access this page. Only administrators can view this content."
        code={403}
      />
    );
  }

  if (requiredRole === 'editor' && !['admin', 'editor'].includes(user?.rule || '')) {
    return (
      <ErrorPage
        title="Access Denied"
        message="You don't have permission to access this page. Only editors and administrators can view this content."
        code={403}
      />
    );
  }

  return <>{children}</>;
} 