/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`
          : 'http://localhost:8080/api/v1/:path*',
      },
    ];
  },
  images: {
    domains: ['via.placeholder.com', 'lh3.googleusercontent.com'],
  },
};

module.exports = nextConfig;