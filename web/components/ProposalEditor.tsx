'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Proposal } from '@/lib/store';
import { Sparkles, Save, Send, Trash2, Copy } from 'lucide-react';

interface ProposalEditorProps {
  proposal?: Proposal;
  opportunityTitle: string;
  onSave: (content: string, tone: string) => Promise<void>;
  onGenerate?: (tone: string) => Promise<string>;
  onSubmit?: () => Promise<void>;
  isLoading?: boolean;
}

const tones = [
  { value: 'formal', label: 'Formal & Professional' },
  { value: 'engaging', label: 'Engaging & Creative' },
  { value: 'impact-driven', label: 'Impact-Driven' },
];

export default function ProposalEditor({
  proposal,
  opportunityTitle,
  onSave,
  onGenerate,
  onSubmit,
  isLoading = false,
}: ProposalEditorProps) {
  const [content, setContent] = useState(proposal?.content || '');
  const [selectedTone, setSelectedTone] = useState(proposal?.tone || 'engaging');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [charCount, setCharCount] = useState(content.length);

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = e.target.value;
    setContent(newContent);
    setCharCount(newContent.length);
  };

  const handleGenerate = async () => {
    if (!onGenerate) return;
    try {
      setIsGenerating(true);
      const generated = await onGenerate(selectedTone);
      setContent(generated);
      setCharCount(generated.length);
    } catch (error) {
      console.error('Generation failed:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      await onSave(content, selectedTone);
    } catch (error) {
      console.error('Save failed:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Proposal Editor</h2>
        <p className="text-gray-600">for {opportunityTitle}</p>
      </div>

      {/* Tone Selection */}
      <div className="mb-6">
        <label className="block text-sm font-semibold text-gray-700 mb-3">
          Select Writing Tone
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {tones.map((tone) => (
            <button
              key={tone.value}
              onClick={() => setSelectedTone(tone.value)}
              className={`p-3 rounded-lg border-2 transition font-medium ${
                selectedTone === tone.value
                  ? 'border-purple-600 bg-purple-50 text-purple-900'
                  : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-purple-300'
              }`}
            >
              {tone.label}
            </button>
          ))}
        </div>
      </div>

      {/* AI Generation */}
      {onGenerate && (
        <div className="mb-6 p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200">
          <button
            onClick={handleGenerate}
            disabled={isGenerating || isLoading}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-3 rounded-lg hover:shadow-lg transition disabled:opacity-50 font-medium"
          >
            <Sparkles className="w-5 h-5" />
            {isGenerating ? 'Generating...' : 'Generate with AI'}
          </button>
          <p className="text-xs text-gray-600 mt-2">
            💡 Tip: Click to generate a proposal using OpenAI GPT-4 with your selected tone
          </p>
        </div>
      )}

      {/* Editor */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-semibold text-gray-700">
            Proposal Content
          </label>
          <span className="text-xs text-gray-500">{charCount} characters</span>
        </div>
        <textarea
          value={content}
          onChange={handleContentChange}
          placeholder="Write your proposal here... or use AI generation above"
          className="w-full h-96 p-4 border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:outline-none resize-none"
        />
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <button
            onClick={handleCopyToClipboard}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:text-purple-600 border border-gray-300 rounded-lg transition"
            title="Copy to clipboard"
          >
            <Copy className="w-4 h-4" />
          </button>
          <button
            className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 border border-red-300 rounded-lg transition"
            title="Delete proposal"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSave}
            disabled={isSaving || isLoading || !content}
            className="flex items-center gap-2 px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition disabled:opacity-50 font-medium"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'Saving...' : 'Save Draft'}
          </button>
          {onSubmit && (
            <button
              onClick={onSubmit}
              disabled={isLoading || !content}
              className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:shadow-lg transition disabled:opacity-50 font-medium"
            >
              <Send className="w-4 h-4" />
              {isLoading ? 'Submitting...' : 'Submit Proposal'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
