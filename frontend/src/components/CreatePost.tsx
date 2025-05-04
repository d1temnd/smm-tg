import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

interface Channel {
  id: number;
  name: string;
  tg_id: string;
  user_name: string;
}

interface CreatePostFormData {
  text: string;
  id: string;
  file?: File;
  time: string;
  send_autor: string;
}

export default function CreatePost() {
  const [text, setText] = useState('');
  const [channelId, setChannelId] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [time, setTime] = useState('0');
  const [sendAutor, setSendAutor] = useState(false);
  const [error, setError] = useState('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Получаем список каналов
  const { data: channels, isLoading: channelsLoading } = useQuery<Channel[]>({
    queryKey: ['telegram-channels'],
    queryFn: async () => {
      const response = await axios.get('/api/telegram/all');
      return response.data;
    }
  });

  const createPostMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await axios.post('/api/post/create', formData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      navigate('/posts');
    },
    onError: (error: any) => {
      setError(error.response?.data?.message || 'Failed to create post');
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const formData = new FormData();
    formData.append('text', text);
    formData.append('chanal_id', channelId);
    formData.append('time', time);
    formData.append('send_autor', sendAutor.toString());
    if (file) {
      formData.append('file', file);
    }

    createPostMutation.mutate(formData);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setFile(file);
      // Создаем URL для предпросмотра изображения
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  if (channelsLoading) {
    return <div className="text-center p-4">Loading channels...</div>;
  }

  const selectedChannel = channels?.find(channel => channel.id.toString() === channelId);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Create New Post</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="text" className="block text-sm font-medium text-gray-700">
              Post Text
            </label>
            <textarea
              id="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              rows={4}
              placeholder="Use Markdown for formatting: *bold*, _italic_, [link](url)"
            />
          </div>

          <div>
            <label htmlFor="channel" className="block text-sm font-medium text-gray-700">
              Channel
            </label>
            <select
              id="channel"
              value={channelId}
              onChange={(e) => setChannelId(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select a channel</option>
              {channels?.map((channel) => (
                <option key={channel.id} value={channel.id}>
                  {channel.name} (@{channel.user_name})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="time" className="block text-sm font-medium text-gray-700">
              Delay (seconds)
            </label>
            <input
              type="number"
              id="time"
              value={time}
              onChange={(e) => setTime(e.target.value)}
              min="0"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="file" className="block text-sm font-medium text-gray-700">
              Media File
            </label>
            <input
              type="file"
              id="file"
              onChange={handleFileChange}
              accept="image/*"
              className="mt-1 block w-full"
            />
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="send_autor"
              checked={sendAutor}
              onChange={(e) => setSendAutor(e.target.checked)}
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <label htmlFor="send_autor" className="ml-2 block text-sm text-gray-900">
              Add author name to post
            </label>
          </div>

          <button
            type="submit"
            disabled={createPostMutation.isPending}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {createPostMutation.isPending ? 'Creating...' : 'Create Post'}
          </button>
        </form>

        {/* Preview Section */}
        <div className="bg-white rounded-lg shadow-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Preview</h2>
          <div className="border rounded-lg p-4 bg-gray-50">
            {selectedChannel && (
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  {selectedChannel.name.charAt(0)}
                </div>
                <div className="ml-3">
                  <div className="font-semibold">{selectedChannel.name}</div>
                  <div className="text-sm text-gray-500">@{selectedChannel.user_name}</div>
                </div>
              </div>
            )}
            {previewUrl && (
              <div className="mb-4">
                <img src={previewUrl} alt="Preview" className="max-w-full rounded-lg" />
              </div>
            )}
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{text}</ReactMarkdown>
            </div>
            {sendAutor && (
              <div className="mt-4 text-sm text-gray-500">
                Posted by @{selectedChannel?.user_name}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 