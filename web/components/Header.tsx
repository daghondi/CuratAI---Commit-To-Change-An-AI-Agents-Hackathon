'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuthStore } from '@/lib/store';
import { authApi } from '@/lib/api';
import { Bell, LogOut, User, Menu, X } from 'lucide-react';

export default function Header() {
  const { user, setUser } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (user) {
      // Fetch unread notification count
      // TODO: Implement notification count fetching
    }
  }, [user]);

  const handleLogout = async () => {
    try {
      await authApi.logout();
      setUser(null);
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <header className="bg-white shadow">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              CuratAI
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {user ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-purple-600 font-medium">
                  Dashboard
                </Link>
                <Link href="/opportunities" className="text-gray-700 hover:text-purple-600 font-medium">
                  Opportunities
                </Link>
                <Link href="/proposals" className="text-gray-700 hover:text-purple-600 font-medium">
                  Proposals
                </Link>

                <div className="flex items-center gap-4 border-l pl-8">
                  <Link href="/notifications" className="relative">
                    <Bell className="w-5 h-5 text-gray-700 hover:text-purple-600" />
                    {unreadCount > 0 && (
                      <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {unreadCount}
                      </span>
                    )}
                  </Link>

                  <div className="relative group">
                    <button className="flex items-center gap-2 text-gray-700 hover:text-purple-600">
                      <User className="w-5 h-5" />
                      <span className="font-medium">{user.artist_name}</span>
                    </button>
                    <div className="hidden group-hover:block absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
                      <Link href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                        Profile
                      </Link>
                      <Link href="/settings" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                        Settings
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-gray-700 hover:bg-red-50 flex items-center gap-2"
                      >
                        <LogOut className="w-4 h-4" />
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex items-center gap-4">
                <Link href="/login" className="text-gray-700 hover:text-purple-600 font-medium">
                  Login
                </Link>
                <Link
                  href="/register"
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg hover:shadow-lg transition"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-gray-700"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4 border-t">
            {user ? (
              <>
                <Link href="/dashboard" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Dashboard
                </Link>
                <Link href="/opportunities" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Opportunities
                </Link>
                <Link href="/proposals" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Proposals
                </Link>
                <Link href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-gray-700 hover:bg-red-50"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Login
                </Link>
                <Link href="/register" className="block px-4 py-2 text-gray-700 hover:bg-purple-50">
                  Get Started
                </Link>
              </>
            )}
          </div>
        )}
      </nav>
    </header>
  );
}
