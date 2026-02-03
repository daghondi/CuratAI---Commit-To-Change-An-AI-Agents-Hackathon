'use client';

import React, { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Target, Award, Clock } from 'lucide-react';

interface DashboardMetrics {
  total_tracked: number;
  total_proposals: number;
  submissions_this_month: number;
  acceptance_rate: number;
  average_relevance_score: number;
}

interface ChartData {
  name: string;
  value: number;
  [key: string]: any;
}

const COLORS = ['#a855f7', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export default function DashboardCharts({ metrics }: { metrics: DashboardMetrics }) {
  const [monthlyData, setMonthlyData] = useState<ChartData[]>([]);
  const [opportunityBreakdown, setOpportunityBreakdown] = useState<ChartData[]>([]);

  useEffect(() => {
    // Mock data - replace with real API calls
    setMonthlyData([
      { name: 'Week 1', opportunities: 5, proposals: 2, submissions: 1 },
      { name: 'Week 2', opportunities: 8, proposals: 4, submissions: 1 },
      { name: 'Week 3', opportunities: 6, proposals: 3, submissions: 2 },
      { name: 'Week 4', opportunities: 12, proposals: 6, submissions: 3 },
    ]);

    setOpportunityBreakdown([
      { name: 'Exhibitions', value: 45 },
      { name: 'Grants', value: 30 },
      { name: 'Residencies', value: 15 },
      { name: 'Other', value: 10 },
    ]);
  }, []);

  const statCards = [
    {
      icon: Target,
      label: 'Opportunities Tracked',
      value: metrics.total_tracked,
      color: 'from-purple-500 to-purple-600',
    },
    {
      icon: TrendingUp,
      label: 'Proposals Created',
      value: metrics.total_proposals,
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: Award,
      label: 'Submissions This Month',
      value: metrics.submissions_this_month,
      color: 'from-green-500 to-green-600',
    },
    {
      icon: Clock,
      label: 'Acceptance Rate',
      value: `${(metrics.acceptance_rate * 100).toFixed(1)}%`,
      color: 'from-orange-500 to-orange-600',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={index}
              className={`bg-gradient-to-br ${stat.color} text-white p-6 rounded-lg shadow-lg`}
            >
              <div className="flex items-center justify-between mb-2">
                <Icon className="w-8 h-8 opacity-80" />
                <span className="text-sm font-semibold opacity-90">{stat.label}</span>
              </div>
              <p className="text-3xl font-bold">{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Activity Over Time */}
        <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Activity Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="opportunities"
                stroke="#a855f7"
                strokeWidth={2}
                dot={{ fill: '#a855f7' }}
              />
              <Line
                type="monotone"
                dataKey="proposals"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ fill: '#3b82f6' }}
              />
              <Line
                type="monotone"
                dataKey="submissions"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ fill: '#10b981' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Opportunity Breakdown */}
        <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Opportunity Types</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={opportunityBreakdown}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {opportunityBreakdown.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Relevance Score Trend */}
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Average Relevance Score</h3>
        <div className="flex items-end gap-4">
          <div className="flex-1">
            <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">
              {(metrics.average_relevance_score * 100).toFixed(0)}%
            </div>
            <p className="text-gray-600 text-sm mt-2">
              CuratAI found opportunities with {(metrics.average_relevance_score * 100).toFixed(0)}% match to your profile
            </p>
          </div>
          <div className="w-32 h-32">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={[
                    { value: metrics.average_relevance_score * 100, fill: '#a855f7' },
                    { value: (1 - metrics.average_relevance_score) * 100, fill: '#e5e7eb' },
                  ]}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={60}
                  dataKey="value"
                  startAngle={90}
                  endAngle={-270}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
