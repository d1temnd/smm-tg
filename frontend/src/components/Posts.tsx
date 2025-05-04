import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

interface Post {
  id: number;
  autor_name: string;
  text: string;
  image_data: string | null; // base64 encoded image data
  time_publication: number;
  chanal_id: string;
}

export default function Posts() {
  const { data: posts, isLoading, error } = useQuery<Post[]>({
    queryKey: ['posts'],
    queryFn: async () => {
      const response = await axios.get('/api/post/all');
      return response.data;
    }
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading posts</div>;

  return (
    <div className="space-y-4">
      {posts?.map((post) => (
        <div key={post.id} className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                <span className="text-gray-600 font-medium">
                  {post.autor_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-900">{post.autor_name}</p>
                <p className="text-sm text-gray-500">
                  {new Date(post.time_publication * 1000).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
          <div className="prose prose-sm max-w-none mb-4">
            <ReactMarkdown>{post.text}</ReactMarkdown>
          </div>
          {post.image_data && (
            <div className="mt-4 flex justify-center">
              <div className="relative w-[300px] h-[300px] bg-gray-100 rounded-lg shadow-sm">
                <img
                  src={`data:image/jpeg;base64,${post.image_data}`}
                  alt="Post media"
                  className="absolute inset-0 w-full h-full object-contain rounded-lg"
                />
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 