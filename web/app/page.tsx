'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, Sparkles, Target, Shield, Zap } from 'lucide-react';

export default function Home() {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Discovery',
      description: 'Our advanced agents discover opportunities perfectly matched to your artistic profile',
    },
    {
      icon: Target,
      title: 'Smart Matching',
      description: 'Relevance scoring helps you focus on the most suitable opportunities for your work',
    },
    {
      icon: Zap,
      title: 'Proposal Generation',
      description: 'Generate compelling proposals with AI assistance in multiple tones and styles',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your artistic work and submissions are protected with enterprise-grade security',
    },
  ];

  return (
    <div>
      {/* Hero Section */}
      <div className="mb-16">
        <div className="max-w-3xl mb-12">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Find Your Next Opportunity
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            CuratAI uses advanced AI agents to discover and match art opportunities, grants, exhibitions, and residencies tailored to your unique artistic vision.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/register"
              className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-lg hover:shadow-lg transition font-semibold"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center gap-2 border-2 border-purple-600 text-purple-600 px-8 py-3 rounded-lg hover:bg-purple-50 transition font-semibold"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Feature Preview */}
        <div className="bg-white rounded-lg shadow-xl p-8 border border-gray-200">
          <div className="aspect-video bg-gradient-to-br from-purple-100 to-blue-100 rounded-lg flex items-center justify-center">
            <Sparkles className="w-16 h-16 text-purple-400 animate-pulse" />
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
          Powered by Intelligent Agents
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-lg shadow p-8 border border-gray-200 hover:shadow-lg transition"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center mb-4">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* How It Works */}
      <div className="mb-16 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-12 border border-purple-200">
        <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {[
            { num: '1', title: 'Sign Up', desc: 'Create your artist profile' },
            { num: '2', title: 'Discover', desc: 'AI scouts opportunities for you' },
            { num: '3', title: 'Create', desc: 'Generate proposals with AI help' },
            { num: '4', title: 'Submit', desc: 'Track submissions and outcomes' },
          ].map((step, index) => (
            <div key={index} className="text-center">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                {step.num}
              </div>
              <h3 className="font-bold text-gray-900 mb-2">{step.title}</h3>
              <p className="text-gray-600 text-sm">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white rounded-lg shadow-lg p-12 border border-gray-200 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Ready to discover your next opportunity?
        </h2>
        <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
          Join hundreds of artists who are using CuratAI to find grants, exhibitions, and residencies tailored to their work.
        </p>
        <Link
          href="/register"
          className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-lg hover:shadow-lg transition font-semibold text-lg"
        >
          Get Started Free
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>
    </div>
  );
}
