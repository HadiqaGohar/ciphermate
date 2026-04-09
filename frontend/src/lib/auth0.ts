// Auth0 configuration - re-export available functions

import { Auth0Client } from "@auth0/nextjs-auth0/server";

// Client-side exports
export {
  getAccessToken,
  useUser,
  withPageAuthRequired,
} from "@auth0/nextjs-auth0";

// Server-side exports
export { Auth0Client } from "@auth0/nextjs-auth0/server";

// Create a simple auth client instance
export const auth0Client = new Auth0Client();
