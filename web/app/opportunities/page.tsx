'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useOpportunityStore, Opportunity } from '@/lib/store';
import { opportunityApi } from '@/lib/api';
import OpportunityCard from '@/components/OpportunityCard';
import { Search, Filter, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const opportunityTypes = [
  { value: '', label: 'All Types' },
  { value: 'exhibition', label: 'Exhibitions' },
  { value: 'grant', label: 'Grants' },
  { value: 'residency', label: 'Residencies' },
  { value: 'call', label: 'Open Calls' },
];

export default function Opportunities() {
  const router = useRouter();
  const { user } = useAuthStore();
  const { opportunities, setOpportunities, filters, setFilters } = useOpportunityStore();
  const [isLoading, setIsLoading] = useState(true);
  const [trackedIds, setTrackedIds] = useState<Set<string>>(new Set());
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchOpportunities = async () => {
      try {
        setIsLoading(true);
        const response = await opportunityApi.list();
        setOpportunities(response.data);

        // Load tracked opportunities
        const trackedResponse = await opportunityApi.getTracked();
        setTrackedIds(new Set(trackedResponse.data.map((opp: Opportunity) => opp.opportunity_id)));
      } catch (error) {
        toast.error('Failed to load opportunities');
        console.error('Error fetching opportunities:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOpportunities();
  }, [user, router, setOpportunities]);

  const handleTrackOpportunity = async (opportunity: Opportunity) => {
    try {
      if (trackedIds.has(opportunity.opportunity_id)) {
        setTrackedIds((prev) => {
          const newSet = new Set(prev);
          newSet.delete(opportunity.opportunity_id);
          return newSet;
        });
        toast.success('Opportunity removed from tracked');
      } else {
        await opportunityApi.track(opportunity.opportunity_id);
        setTrackedIds((prev) => new Set([...prev, opportunity.opportunity_id]));
        toast.success('Opportunity tracked!');
      }
    } catch (error) {
      toast.error('Failed to update opportunity');
      console.error('Error tracking opportunity:', error);
    }
  };

  const handleTypeFilter = (type: string) => {
    setFilters({ type: type || undefined });
  };

  const handleRelevanceFilter = (minScore: number) => {
    setFilters({ minScore: minScore > 0 ? minScore : undefined });
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ searchTerm: e.target.value || undefined });
  };

  if (!user) return null;

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Opportunities</h1>
        <p className="text-gray-600">
          Discover {opportunities.length} opportunities curated just for you
        </p>
      </div>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4 mb-8 border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          {/* Search */}
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search opportunities..."
                onChange={handleSearch}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              />
            </div>
          </div>

          {/* Type Filter */}
          <select
            value={filters.type || ''}
            onChange={(e) => handleTypeFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
          >
            {opportunityTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>

          {/* Toggle Advanced Filters */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center justify-center gap-2 border-2 border-gray-300 rounded-lg px-4 py-2 text-gray-700 hover:border-purple-600 transition"
          >
            <Filter className="w-5 h-5" />
            More
          </button>
        </div>

        {/* Advanced Filters */}
        {showFilters && (
          <div className="pt-4 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Relevance Score
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="10"
                  value={(filters.minScore || 0) * 100}
                  onChange={(e) => handleRelevanceFilter(parseInt(e.target.value) / 100)}
                  className="w-full"
                />
                <div className="text-xs text-gray-600 mt-1">
                  {((filters.minScore || 0) * 100).toFixed(0)}% or higher
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
          <p className="mt-4 text-gray-600">Loading opportunities...</p>
        </div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12 bg-blue-50 rounded-lg border border-blue-200">
          <AlertCircle className="w-12 h-12 text-blue-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No opportunities yet</h3>
          <p className="text-gray-600 mb-6">
            Go to your dashboard and click "Scout New Opportunities" to discover matched opportunities
          </p>
          <a
            href="/dashboard"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Go to Dashboard
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {opportunities.map((opportunity) => (
            <OpportunityCard
              key={opportunity.opportunity_id}
              opportunity={opportunity}
              onTrack={handleTrackOpportunity}
              isTracked={trackedIds.has(opportunity.opportunity_id)}
            />
          ))}
        </div>
      )}

      {/* Summary */}
      {opportunities.length > 0 && (
        <div className="mt-8 p-6 bg-purple-50 rounded-lg border border-purple-200">
          <h3 className="font-semibold text-gray-900 mb-2">
            Showing {opportunities.length} opportunities
          </h3>
          <p className="text-gray-600 text-sm">
            Track opportunities by clicking the bookmark icon to save them to your profile
          </p>
        </div>
      )}
    </div>
  );
}
