import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserRole } from '../types';

export interface UserProfile {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
  department_id?: string;
  ward_number?: string;
}

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  role: UserRole;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  switchDemoRole: (role: UserRole) => Promise<void>;
}

const defaultUser: UserProfile = {
  id: 'u0000000-0000-0000-0000-000000000001',
  full_name: 'Aarav Mehta',
  email: 'citizen@civicflow.gov',
  role: 'CITIZEN',
  ward_number: 'Ward 3',
};

const AuthContext = createContext<AuthContextType>({
  user: defaultUser,
  token: 'demo-token',
  role: 'CITIZEN',
  login: async () => {},
  logout: () => {},
  switchDemoRole: async () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(() => {
    const saved = localStorage.getItem('civicflow_user');
    return saved ? JSON.parse(saved) : defaultUser;
  });
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('civicflow_token') || 'demo-token';
  });

  const role: UserRole = user?.role || 'CITIZEN';

  const login = async (email: string, password: string) => {
    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error('Invalid credentials');
      const data = await res.json();
      setUser(data.profile);
      setToken(data.access_token);
      localStorage.setItem('civicflow_user', JSON.stringify(data.profile));
      localStorage.setItem('civicflow_token', data.access_token);
    } catch (e) {
      console.error('Login error', e);
      throw e;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('civicflow_user');
    localStorage.removeItem('civicflow_token');
  };

  const switchDemoRole = async (targetRole: UserRole) => {
    try {
      const res = await fetch('/api/v1/auth/demo-switch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: targetRole }),
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data.profile);
        setToken(data.access_token);
        localStorage.setItem('civicflow_user', JSON.stringify(data.profile));
        localStorage.setItem('civicflow_token', data.access_token);
      }
    } catch (e) {
      console.error('Demo switch error', e);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, role, login, logout, switchDemoRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
