/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL || "http://localhost:5000",
  },
  images: {
    domains: ["avatars.githubusercontent.com", "media.licdn.com"],
  },
};

module.exports = nextConfig;
