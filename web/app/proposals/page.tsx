'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useProposalStore, Proposal } from '@/lib/store';
import { proposalApi, opportunityApi } from '@/lib/api';
import { AlertCircle, FileText, Clock, CheckCircle, XCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Proposals() {
  const router = useRouter();
  const { user } = useAuthStore();
  const { proposals, setProposals } = useProposalStore();
  const [isLoading, setIsLoading] = useState(true);
  const [opportunityTitles, setOpportunityTitles] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [proposalsRes, opportunitiesRes] = await Promise.all([
          proposalApi.list(),
          opportunityApi.getTracked(),
        ]);

        setProposals(proposalsRes.data);

        const titles: Record<string, string> = {};
        opportunitiesRes.data.forEach((opp: any) => {
          titles[opp.opportunity_id] = opp.title;
        });
        setOpportunityTitles(titles);
      } catch (error) {
        toast.error('Failed to load proposals');
        console.error('Error fetching proposals:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [user, router, setProposals]);

  const handleCreateProposal = () => {
    router.push('/proposals/new');
  };

  const handleEditProposal = (proposal: Proposal) => {
    router.push(`/proposals/${proposal.proposal_id}/edit`);
  };

  const handleDeleteProposal = async (proposal: Proposal) => {
    if (!confirm('Are you sure you want to delete this proposal?')) return;

    try {
      await proposalApi.delete(proposal.proposal_id);
      setProposals(proposals.filter((p) => p.proposal_id !== proposal.proposal_id));
      toast.success('Proposal deleted');
    } catch (error) {
      toast.error('Failed to delete proposal');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'draft':
        return <FileText className="w-5 h-5 text-gray-600" />;
      case 'submitted':
        return <Clock className="w-5 h-5 text-blue-600" />;
      case 'accepted':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'rejected':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      case 'submitted':
        return 'bg-blue-100 text-blue-800';
      case 'accepted':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (!user) return null;

  return (
    <div>
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">My Proposals</h1>
          <p className="text-gray-600">
            Manage your drafts and submitted proposals ({proposals.length} total)
          </p>
        </div>
        <button
          onClick={handleCreateProposal}
          className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition font-medium"
        >
          Create New Proposal
        </button>
      </div>

      {/* Proposals List */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
          <p className="mt-4 text-gray-600">Loading proposals...</p>
        </div>
      ) : proposals.length === 0 ? (
        <div className="text-center py-12 bg-blue-50 rounded-lg border border-blue-200">
          <FileText className="w-12 h-12 text-blue-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No proposals yet</h3>
          <p className="text-gray-600 mb-6">
            Create your first proposal to start submitting to opportunities
          </p>
          <button
            onClick={handleCreateProposal}
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Create Proposal
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {proposals.map((proposal) => (
            <div key={proposal.proposal_id} className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden hover:shadow-lg transition">
              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 mb-1">
                      {proposal.title}
                    </h3>
                    <p className="text-sm text-gray-600">
                      for {opportunityTitles[proposal.opportunity_id] || 'Unknown Opportunity'}
                    </p>
                  </div>
                  <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(proposal.status)}`}>
                    {getStatusIcon(proposal.status)}
                    {proposal.status.charAt(0).toUpperCase() + proposal.status.slice(1)}
                  </span>
                </div>

                {/* Content Preview */}
                <div className="mb-4 p-3 bg-gray-50 rounded text-sm text-gray-700 line-clamp-3">
                  {proposal.content || 'No content yet'}
                </div>

                {/* Metadata */}
                <div className="grid grid-cols-2 gap-2 mb-4 text-xs text-gray-600 border-t border-b border-gray-200 py-3">
                  <div>
                    <p className="font-semibold">Created</p>
                    {new Date(proposal.created_at).toLocaleDateString()}
                  </div>
                  <div>
                    <p className="font-semibold">Updated</p>
                    {new Date(proposal.updated_at).toLocaleDateString()}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleEditProposal(proposal)}
                    className="flex-1 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition text-sm font-medium"
                  >
                    Edit
                  </button>
                  {proposal.status === 'draft' && (
                    <button
                      onClick={() => handleDeleteProposal(proposal)}
                      className="flex-1 px-4 py-2 border border-red-300 text-red-600 rounded hover:bg-red-50 transition text-sm font-medium"
                    >
                      Delete
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Stats */}
      {proposals.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            {
              label: 'Drafts',
              count: proposals.filter((p) => p.status === 'draft').length,
              color: 'text-gray-600',
            },
            {
              label: 'Submitted',
              count: proposals.filter((p) => p.status === 'submitted').length,
              color: 'text-blue-600',
            },
            {
              label: 'Accepted',
              count: proposals.filter((p) => p.status === 'accepted').length,
              color: 'text-green-600',
            },
            {
              label: 'Rejected',
              count: proposals.filter((p) => p.status === 'rejected').length,
              color: 'text-red-600',
            },
          ].map((stat, index) => (
            <div key={index} className="bg-white rounded-lg shadow p-4 border border-gray-200 text-center">
              <p className={`text-3xl font-bold ${stat.color}`}>{stat.count}</p>
              <p className="text-sm text-gray-600 mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
