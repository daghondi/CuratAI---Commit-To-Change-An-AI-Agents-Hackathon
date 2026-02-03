'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { authApi } from '@/lib/api';
import { AlertCircle, Eye, EyeOff, Check } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Register() {
  const router = useRouter();
  const { setUser, setLoading } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    artist_name: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const passwordStrength = {
    length: formData.password.length >= 8,
    hasNumber: /\d/.test(formData.password),
    hasUpperCase: /[A-Z]/.test(formData.password),
    hasSpecial: /[!@#$%^&*]/.test(formData.password),
  };

  const passwordsMatch = formData.password === formData.confirmPassword && formData.password;
  const isFormValid = 
    formData.email &&
    formData.artist_name &&
    formData.password &&
    passwordsMatch &&
    passwordStrength.length &&
    passwordStrength.hasNumber;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!isFormValid) {
      setError('Please ensure all password requirements are met');
      return;
    }

    setIsLoading(true);
    setLoading(true);

    try {
      const response = await authApi.register(
        formData.email,
        formData.artist_name,
        formData.password
      );

      localStorage.setItem('auth_token', response.data.access_token);
      setUser(response.data.user);

      toast.success('Account created successfully!');
      router.push('/dashboard');
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-xl">C</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Join CuratAI</h1>
          <p className="text-gray-600 mt-2">Create your artist account</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8 border border-gray-200">
          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          {/* Email */}
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              required
            />
          </div>

          {/* Artist Name */}
          <div className="mb-4">
            <label htmlFor="artist_name" className="block text-sm font-semibold text-gray-700 mb-2">
              Artist Name
            </label>
            <input
              id="artist_name"
              type="text"
              name="artist_name"
              value={formData.artist_name}
              onChange={handleChange}
              placeholder="Your professional name"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              required
            />
          </div>

          {/* Password */}
          <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
              Password
            </label>
            <div className="relative mb-3">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>

            {/* Password Strength */}
            <div className="space-y-2 mb-3">
              <div className={`flex items-center gap-2 text-xs ${passwordStrength.length ? 'text-green-600' : 'text-gray-400'}`}>
                <Check className="w-4 h-4" />
                At least 8 characters
              </div>
              <div className={`flex items-center gap-2 text-xs ${passwordStrength.hasNumber ? 'text-green-600' : 'text-gray-400'}`}>
                <Check className="w-4 h-4" />
                At least one number
              </div>
              <div className={`flex items-center gap-2 text-xs ${passwordStrength.hasUpperCase ? 'text-green-600' : 'text-gray-400'}`}>
                <Check className="w-4 h-4" />
                At least one uppercase letter
              </div>
            </div>
          </div>

          {/* Confirm Password */}
          <div className="mb-6">
            <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <input
                id="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'}
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${
                  formData.confirmPassword
                    ? passwordsMatch
                      ? 'border-green-300 focus:ring-green-600'
                      : 'border-red-300 focus:ring-red-600'
                    : 'border-gray-300 focus:ring-purple-600'
                }`}
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
              >
                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            {formData.confirmPassword && !passwordsMatch && (
              <p className="text-red-600 text-xs mt-1">Passwords do not match</p>
            )}
          </div>

          {/* Sign Up Button */}
          <button
            type="submit"
            disabled={isLoading || !isFormValid}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-2 rounded-lg hover:shadow-lg transition disabled:opacity-50 font-semibold"
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </button>

          {/* Sign In Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-purple-600 hover:text-purple-700 font-semibold">
                Sign in
              </Link>
            </p>
          </div>
        </form>

        {/* Footer Links */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            By signing up, you agree to our{' '}
            <a href="#" className="text-purple-600 hover:text-purple-700">
              Terms of Service
            </a>
            {' and '}
            <a href="#" className="text-purple-600 hover:text-purple-700">
              Privacy Policy
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
