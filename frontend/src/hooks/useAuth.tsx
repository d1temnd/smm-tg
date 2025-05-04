import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: number;
  name: string;
  rule: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (name: string, password: string) => Promise<void>;
  register: (name: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Проверяем наличие сессии на бэкенде через POST запрос
    axios.post('/api/auth/login', {})
      .then(response => {
        if (response.data.message === 'Login successful') {
          // Если сессия существует, получаем данные пользователя
          axios.get('/api/auth/profile')
            .then(profileResponse => {
              setUser(profileResponse.data.user);
            })
            .catch(() => {
              setUser(null);
            });
        } else {
          setUser(null);
        }
      })
      .catch(() => {
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const login = async (name: string, password: string) => {
    const response = await axios.post('/api/auth/login', { name, password });
    if (response.data.message === 'Login successful') {
      // Получаем данные пользователя после успешного входа
      const profileResponse = await axios.get('/api/auth/profile');
      setUser(profileResponse.data.user);
    } else {
      throw new Error('Login failed');
    }
  };

  const register = async (name: string, password: string) => {
    const response = await axios.post('/api/auth/register', { name, password });
    if (response.data.message === 'User registered successfully') {
      // После успешной регистрации автоматически входим
      await login(name, password);
    } else {
      throw new Error('Registration failed');
    }
  };

  const logout = async () => {
    await axios.post('/api/auth/logout');
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 