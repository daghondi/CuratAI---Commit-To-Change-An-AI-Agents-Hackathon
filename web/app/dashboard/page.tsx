'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useOpportunityStore } from '@/lib/store';
import { dashboardApi, opportunityApi } from '@/lib/api';
import DashboardCharts from '@/components/DashboardCharts';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface DashboardMetrics {
  total_tracked: number;
  total_proposals: number;
  submissions_this_month: number;
  acceptance_rate: number;
  average_relevance_score: number;
}

export default function Dashboard() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchMetrics = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await dashboardApi.getMetrics();
        setMetrics(response.data);
      } catch (err) {
        setError('Failed to load dashboard metrics');
        console.error('Error fetching metrics:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMetrics();
  }, [user, router]);

  const handleRefresh = async () => {
    try {
      setIsLoading(true);
      const response = await dashboardApi.getMetrics();
      setMetrics(response.data);
    } catch (err) {
      setError('Failed to refresh metrics');
    } finally {
      setIsLoading(false);
    }
  };

  const handleScoutOpportunities = async () => {
    try {
      setIsLoading(true);
      await opportunityApi.scout();
      await handleRefresh();
    } catch (err) {
      setError('Failed to scout opportunities');
    }
  };

  if (!user) return null;

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Welcome back, {user.artist_name}!
        </h1>
        <p className="text-gray-600 mb-6">
          Here's your opportunity dashboard powered by CuratAI agents
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleScoutOpportunities}
            disabled={isLoading}
            className="flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition disabled:opacity-50 font-medium"
          >
            <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
            Scout New Opportunities
          </button>
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="flex items-center justify-center gap-2 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:border-gray-400 transition disabled:opacity-50 font-medium"
          >
            <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
          <div>
            <p className="text-red-800 font-medium">{error}</p>
            <p className="text-red-700 text-sm">Try refreshing the page or contact support</p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !metrics ? (
        <div className="text-center py-12">
          <div className="inline-block">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      ) : metrics ? (
        <DashboardCharts metrics={metrics} />
      ) : null}

      {/* Quick Links */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <a
          href="/opportunities"
          className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition border border-gray-200"
        >
          <h3 className="font-bold text-gray-900 mb-2">Browse Opportunities</h3>
          <p className="text-gray-600 text-sm">Explore all discovered opportunities</p>
        </a>
        <a
          href="/proposals"
          className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition border border-gray-200"
        >
          <h3 className="font-bold text-gray-900 mb-2">My Proposals</h3>
          <p className="text-gray-600 text-sm">View and manage your proposals</p>
        </a>
        <a
          href="/profile"
          className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition border border-gray-200"
        >
          <h3 className="font-bold text-gray-900 mb-2">My Profile</h3>
          <p className="text-gray-600 text-sm">Update your artist information</p>
        </a>
      </div>
    </div>
  );
}
