'use client';

import React from 'react';
import { Opportunity } from '@/lib/store';
import { Calendar, MapPin, DollarSign, ExternalLink, Bookmark } from 'lucide-react';
import { format } from 'date-fns';

interface OpportunityCardProps {
  opportunity: Opportunity;
  onTrack?: (opportunity: Opportunity) => void;
  isTracked?: boolean;
}

export default function OpportunityCard({
  opportunity,
  onTrack,
  isTracked = false,
}: OpportunityCardProps) {
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'exhibition':
        return 'bg-purple-100 text-purple-800';
      case 'grant':
        return 'bg-green-100 text-green-800';
      case 'residency':
        return 'bg-blue-100 text-blue-800';
      case 'call':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRelevanceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-blue-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-gray-600';
  };

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition border border-gray-200 overflow-hidden">
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-start gap-4 mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(opportunity.opportunity_type)}`}>
                {opportunity.opportunity_type.charAt(0).toUpperCase() + opportunity.opportunity_type.slice(1)}
              </span>
              <span className={`text-sm font-semibold ${getRelevanceColor(opportunity.relevance_score)}`}>
                {Math.round(opportunity.relevance_score * 100)}% Match
              </span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">{opportunity.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{opportunity.description}</p>
          </div>
          {onTrack && (
            <button
              onClick={() => onTrack(opportunity)}
              className={`p-2 rounded-lg transition ${
                isTracked
                  ? 'bg-purple-100 text-purple-600'
                  : 'bg-gray-100 text-gray-600 hover:bg-purple-100 hover:text-purple-600'
              }`}
            >
              <Bookmark className="w-5 h-5" fill={isTracked ? 'currentColor' : 'none'} />
            </button>
          )}
        </div>

        {/* Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 py-4 border-t border-b border-gray-200">
          <div className="flex items-center gap-2 text-gray-600">
            <Calendar className="w-4 h-4" />
            <span className="text-sm">
              {format(new Date(opportunity.deadline), 'MMM dd, yyyy')}
            </span>
          </div>
          {opportunity.location && (
            <div className="flex items-center gap-2 text-gray-600">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">{opportunity.location}</span>
            </div>
          )}
          {opportunity.budget_range && (
            <div className="flex items-center gap-2 text-gray-600">
              <DollarSign className="w-4 h-4" />
              <span className="text-sm">{opportunity.budget_range}</span>
            </div>
          )}
        </div>

        {/* Source and Actions */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">via {opportunity.source}</span>
          {opportunity.url && (
            <a
              href={opportunity.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-purple-600 hover:text-purple-700 font-medium text-sm"
            >
              View Details
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
