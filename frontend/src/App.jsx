import React, { useState } from 'react';
import { Link2, Clipboard, AlertCircle } from 'lucide-react';

const URLShortener = () => {
  const [url, setUrl] = useState('');
  const [customPath, setCustomPath] = useState('');
  const [shortenedUrl, setShortenedUrl] = useState('');
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setShortenedUrl('');
    
    try {
      const response = await fetch('http://localhost:8000/shorten', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          custom_path: customPath || undefined
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to shorten URL');
      }
      
      setShortenedUrl(`http://localhost:8000/${data.short_url}`);
    } catch (err) {
      setError(err.message);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shortenedUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen w-full bg-black flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-8 w-96">
        <div className="text-center">
          <div className="flex justify-center">
            <Link2 className="h-12 w-12 text-blue-500" />
          </div>
          <h2 className="mt-4 text-3xl font-bold text-gray-900">
            URL Shortener
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div>
            <input
              id="url"
              name="url"
              type="url"
              required
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter URL to shorten"
            />
          </div>
          
          <div>
            <input
              id="custom-path"
              name="custom-path"
              type="text"
              value={customPath}
              onChange={(e) => setCustomPath(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Custom path (optional)"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Shorten URL
          </button>
        </form>

        {error && (
          <div className="mt-4 flex items-center space-x-2 text-red-600">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        )}

        {shortenedUrl && (
          <div className="mt-4">
            <div className="flex items-center justify-between rounded-md bg-gray-50 px-4 py-3 border border-gray-200">
              <a 
                href={shortenedUrl}
                target="_blank"
                rel="noopener noreferrer" 
                className="text-sm text-blue-600 hover:text-blue-800 truncate underline"
              >
                {shortenedUrl}
              </a>
              <button
                onClick={copyToClipboard}
                className="ml-2 p-2 text-gray-500 hover:text-gray-700 focus:outline-none"
              >
                <Clipboard className="h-5 w-5" />
              </button>
            </div>
            {copied && (
              <p className="mt-2 text-sm text-green-600 text-center">
                Copied to clipboard!
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default URLShortener;