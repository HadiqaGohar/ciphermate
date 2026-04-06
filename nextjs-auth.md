### Install Dependencies with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/CONTRIBUTING.md

Installs project dependencies using the pnpm package manager. This is a standard step for setting up a Node.js project.

```bash
pnpm install
```

--------------------------------

### Generate and Serve Docs with pnpm and npx

Source: https://github.com/auth0/nextjs-auth0/blob/main/CONTRIBUTING.md

Commands to generate API documentation and serve it locally. Requires the http-server package to be installed globally or via npx.

```bash
pnpm run docs
```

```bash
npx http-server docs
```

--------------------------------

### Run Next.js Development Server

Source: https://github.com/auth0/nextjs-auth0/blob/main/examples/with-mrrt/README.md

Commands to start the development server for a Next.js application. These commands utilize different package managers like npm, yarn, pnpm, and bun. The server typically runs on http://localhost:3000.

```bash
npm run dev
```

```bash
yarn dev
```

```bash
pnpm dev
```

```bash
bun dev
```

--------------------------------

### Create New Handlers with Default Configuration (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

This example shows how to create new authentication routes, such as `/api/auth/signup`, by configuring the default `handleLogin` handler with specific parameters like `screen_hint: "signup"`.

```javascript
export default handleAuth({
  // Creates /api/auth/signup
  signup: handleLogin({
    authorizationParams: { screen_hint: "signup" },
  }),
})
```

--------------------------------

### Run Next.js Development Server (Bash)

Source: https://github.com/auth0/nextjs-auth0/blob/main/e2e/test-app/README.md

Commands to start the Next.js development server using different package managers. Ensure Node.js and the respective package manager are installed. The server typically runs on http://localhost:3000.

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

--------------------------------

### Start Interactive Login Programmatically (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Initiates the interactive login process by programmatically calling the `startInteractiveLogin` method. This is an alternative to redirecting to the built-in `/auth/login` endpoint. It requires importing the auth0 client and returns a redirect response.

```typescript
import { NextRequest } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export const GET = async (req: NextRequest) => {
  return auth0.startInteractiveLogin();
};
```

--------------------------------

### Install Auth0 Next.js SDK

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Installs the Auth0 Next.js SDK using npm. This command requires Node.js version 20 LTS or newer.

```shell
npm i @auth0/nextjs-auth0
```

--------------------------------

### v3 Custom Auth Handler Example (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

Illustrates the v3 approach to customizing individual authentication handlers (like `logout` and `login`) by providing custom implementations to the `handleAuth` function.

```typescript
// v3 approach (no longer available in v4)
export const GET = handleAuth({
  async logout(req: NextApiRequest, res: NextApiResponse) {
    // Custom logout logic
    console.log('User is logging out');
    
    return await handleLogout(req, res);
  },
  async login(req: NextApiRequest, res: NextApiResponse) {
    // Custom login logic
    return await handleLogin(req, res, {
      authorizationParams: {
        audience: 'https://my-api.com'
      }
    });
  }
});
```

--------------------------------

### Watch for Changes and Rebuild with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Starts a watcher that automatically rebuilds the project whenever source files change. This is useful for active development.

```bash
pnpm run build:watch
```

--------------------------------

### Serve Documentation Locally with http-server

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Serves the generated documentation locally using the http-server package. This allows you to preview the documentation in a web browser.

```bash
npx http-server docs
```

--------------------------------

### Configure Auth0 Client with Database Sessions

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to configure the Auth0 client to use a custom session store for persisting user sessions in a database. This involves providing an implementation of the `SessionStore` interface with methods for getting, setting, deleting, and optionally handling backchannel logout.

```typescript
import { Auth0Client } from '@auth0/auth0-spa-js';

export const auth0 = new Auth0Client({
  sessionStore: {
    async get(id) {
      // query and return a session by its ID
    },
    async set(id, sessionData) {
      // upsert the session given its ID and sessionData
    },
    async delete(id) {
      // delete the session using its ID
    },
    async deleteByLogoutToken({ sid, sub }: { sid?: string; sub?: string }) {
      // optional method to be implemented when using Back-Channel Logout
    }
  }
});
```

--------------------------------

### Get Access Token in Browser (React Client Component)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Provides an example of how to use the `getAccessToken` helper within a React client component to fetch an access token for calling external APIs. It includes basic error handling for cases where the token cannot be obtained and mentions the importance of refresh token rotation configuration.

```tsx
"use client";

import { getAccessToken } from "@auth0/nextjs-auth0";

export default function Component() {
  async function fetchData() {
    try {
      const token = await getAccessToken();
      // call external API with token...
    } catch (err) {
      // err will be an instance of AccessTokenError if an access token could not be obtained
    }
  }

  return (
    <main>
      <button onClick={fetchData}>Fetch Data</button>
    </main>
  );
}
```

--------------------------------

### Run Unit Tests with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Executes the unit tests for the project using the pnpm package manager.

```bash
pnpm test:unit
```

--------------------------------

### Configure Auth0Client with Authorization Parameters

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to statically configure authorization parameters like scope and audience when initializing the Auth0Client. This is useful for setting default authorization settings for your application.

```typescript
export const auth0 = new Auth0Client({
  authorizationParameters: {
    scope: "openid profile email",
    audience: "urn:custom:api"
  }
});
```

--------------------------------

### Initiate Backchannel Authentication with Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Shows how to use the `getTokenByBackchannelAuth` method to initiate Client-Initiated Backchannel Authentication. This method requires a `bindingMessage` and `loginHint` which includes the user's `sub` claim.

```typescript
import { auth0 } from '@/lib/auth0';

const tokenResponse = await auth0.getTokenByBackchannelAuth({
  bindingMessage: "",
  loginHint: {
    sub: "auth0|123456789"
  }
});
```

--------------------------------

### V3 Route Handler for Auth0 in App Router

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This TypeScript code demonstrates the previous method of setting up authentication endpoints in v3 using a dynamic Route Handler in the App Router. It imports `handleAuth` from `@auth0/nextjs-auth0` and exports a GET function to manage authentication requests.

```typescript
import { handleAuth } from "@auth0/nextjs-auth0"

export const GET = handleAuth()
```

--------------------------------

### Build Project with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Builds the project using the pnpm package manager. This command compiles the source code into a distributable format.

```bash
pnpm run build
```

--------------------------------

### Build Project with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/CONTRIBUTING.md

Builds the project using pnpm. This command compiles the source code into a distributable format. Includes a watch mode for continuous building.

```bash
pnpm run build
```

```bash
pnpm run build:watch
```

--------------------------------

### Run Unit Test Coverage with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Runs the unit tests and generates a code coverage report using the pnpm package manager.

```bash
pnpm run test:coverage
```

--------------------------------

### Generate API Documentation

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Generates the API documentation for the project. This command typically uses a documentation generation tool.

```bash
pnpm run docs
```

--------------------------------

### Get Access Token for Connection on Server (Pages Router - TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Obtains an access token for a given connection in the Pages Router using the `getAccessTokenForConnection` helper. This method is suitable for use in `getServerSideProps` and API routes, and requires passing the request (`req`) and response (`res`) objects.

```typescript
import type { NextApiRequest, NextApiResponse } from "next";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ message: string }>
) {
  try {
    const token = await auth0.getAccessTokenForConnection(
      { connection: "google-oauth2" },
      req,
      res
    );
  } catch (err) {
    // err will be an instance of AccessTokenError if an access token could not be obtained
  }

  res.status(200).json({ message: "Success!" });
}
```

--------------------------------

### v4 Auth0 Client Initialization with Dynamic Base URL (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

Initializes the `Auth0Client` in v4, utilizing the dynamically configured `APP_BASE_URL` for the `appBaseUrl` and `redirect_uri` properties.

```typescript
export const auth0 = new Auth0Client({
  appBaseUrl: process.env.APP_BASE_URL,
  authorizationParameters: {
    redirect_uri: `${process.env.APP_BASE_URL}/auth/callback`,
    audience: "YOUR_API_AUDIENCE_HERE", // optional
  },
});
```

--------------------------------

### Get Access Token in Next.js Middleware (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example shows how to obtain an access token within Next.js middleware using `auth0.getAccessToken`. It's crucial to pass both `request` and `response` objects to ensure token refresh capabilities. This method is useful for protecting routes or adding authenticated headers to requests originating from the middleware. Dependencies include `next/server` and `@auth0/nextjs-auth0`.

```typescript
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  const accessToken = await auth0.getAccessToken(request, authRes);

  // the headers from the auth middleware should always be returned
  return authRes;
}
```

--------------------------------

### Session Cookie Options via Auth0ClientOptions

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Configure session cookie options directly when initializing the Auth0Client. Options provided here take precedence over environment variables.

```APIDOC
## Session Cookie Options via Auth0ClientOptions

### Description
Configure session cookie attributes directly when initializing the `Auth0Client`. Options provided directly in `Auth0ClientOptions` take precedence over environment variables. The `httpOnly` attribute is always `true` regardless of configuration.

### Method
```typescript
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  session: {
    cookie: {
      domain: ".example.com",
      path: "/app",
      transient: true,
      // httpOnly is always true and cannot be configured
      secure: process.env.NODE_ENV === "production",
      sameSite: "Lax",
      name: "appSession" // Optional: custom cookie name, defaults to '__session'
    },
    // ... other session options like absoluteDuration ...
  }
  // ... other client options ...
});
```

### Session Cookie Options

- **domain** (String): Specifies the `Domain` attribute. Overrides `AUTH0_COOKIE_DOMAIN`.
- **path** (String): Specifies the `Path` attribute. Defaults to `/`. Overrides `AUTH0_COOKIE_PATH`.
- **transient** (Boolean): If `true`, the `maxAge` attribute is omitted, making it a session cookie. Defaults to `false`. Overrides `AUTH0_COOKIE_TRANSIENT`.
- **secure** (Boolean): Specifies the `Secure` attribute. Defaults to `false` (or `true` if `AUTH0_COOKIE_SECURE=true` is set). Overrides `AUTH0_COOKIE_SECURE`.
- **sameSite** ('Lax' | 'Strict' | 'None'): Specifies the `SameSite` attribute. Defaults to `Lax` (or the value of `AUTH0_COOKIE_SAME_SITE`). Overrides `AUTH0_COOKIE_SAME_SITE`.
- **name** (String): The name of the session cookie. Defaults to `__session`.
```

--------------------------------

### Initialize Auth0Provider with Server-Side User

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Wraps components with Auth0Provider and passes an initial user object obtained from the server. This makes the user data available via the useUser() hook. Ensure the 'auth0' client path is correctly configured.

```tsx
import { Auth0Provider } from "@auth0/nextjs-auth0";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export default async function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await auth0.getSession();

  return (
    <html lang="en">
      <body>
        <Auth0Provider user={session?.user}>{children}</Auth0Provider>
      </body>
    </html>
  );
}
```

--------------------------------

### Minimize Dynamic Scope Requests with getAccessToken (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example contrasts the preferred method of using default scopes with `getAccessToken` against the less preferred method of requesting dynamic scopes. It highlights how avoiding explicit scope parameters in `getAccessToken` calls helps in managing session size by minimizing the number of distinct tokens stored.

```typescript
// Preferred: Use default scopes
const token = await auth0.getAccessToken({
  audience: "https://api.example.com"
});

// Avoid unless necessary: Dynamic scopes increase session size
const token = await auth0.getAccessToken({
  audience: "https://api.example.com",
  scope: "openid profile email read:products write:products admin:all"
});
```

--------------------------------

### Retrieve Access Tokens for Different Audiences (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example demonstrates how to use the `getAccessToken` method within a Next.js API route to fetch tokens for various audiences. It covers retrieving the default token, a token for a specific audience, and a token with additional scopes, showcasing flexibility in token acquisition.

```typescript
import { NextResponse } from "next/server";
import { auth0 } from "@/lib/auth0";

export async function GET() {
  try {
    // Get token for default audience
    const defaultToken = await auth0.getAccessToken();

    // Get token for different audience
    const dataToken = await auth0.getAccessToken({
      audience: "https://data-api.example.com"
    });

    // Get token with additional scopes
    const adminToken = await auth0.getAccessToken({
      audience: "https://admin.example.com",
      scope: "write:admin"
    });

    // Call external API with token
    const response = await fetch("https://data-api.example.com/data", {
      headers: { Authorization: `Bearer ${dataToken.token}` }
    });

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch data" },
      { status: 500 }
    );
  }
}
```

--------------------------------

### Combine Next.js Middleware with Auth0 Middleware

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example demonstrates how to combine custom Next.js middleware with the Auth0 middleware. It ensures that the Auth0 middleware handles authentication routes while allowing other middleware to process requests, carefully managing the 'x-middleware-next' header to prevent unintended request forwarding.

```typescript
export async function middleware(request: NextRequest) {
  const authResponse = await auth0.middleware(request);

  // if path starts with /auth, let the auth middleware handle it
  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authResponse;
  }

  // call any other middleware here
  const someOtherResponse = await someOtherMiddleware(request);
  const shouldProceed = someOtherResponse.headers.get("x-middleware-next");

  // add any headers from the auth middleware to the response
  for (const [key, value] of authResponse.headers) {
    // Only copy 'x-middleware-next' if the custom middleware response intends to proceed.
    if (key.toLowerCase() === "x-middleware-next" && !shouldProceed) {
      continue; // Skip copying this header if we are blocking/redirecting
    }
    someOtherResponse.headers.set(key, value);
  }

  return someOtherResponse;
}
```

--------------------------------

### Run Tests with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/CONTRIBUTING.md

Executes various test suites for the project using pnpm. Supports unit tests, unit test coverage, and end-to-end (E2E) tests.

```bash
pnpm test:unit
```

```bash
pnpm run test:coverage
```

```bash
pnpm run test:e2e
```

--------------------------------

### Run E2E Tests with pnpm

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/media/CONTRIBUTING.md

Executes the end-to-end (E2E) tests for the project and watches for changes. Requires the TEST_USER_PASSWORD environment variable to be set.

```bash
pnpm run test:e2e
```

--------------------------------

### Propagate Headers for API Routes/getServerSideProps (Next.js)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example demonstrates how to propagate headers from the Auth0 middleware to ensure consistency when calling `getAccessTokenForConnection` in API Routes or `getServerSideProps` within the Pages Router. It creates a new `NextResponse` that includes the original request headers and sets the necessary cookie headers from the `authRes`.

```ts
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  const accessToken = await auth0.getAccessTokenForConnection(
    { connection: "google-oauth2" },
    request,
    authRes
  );

  // create a new response with the updated request headers
  const resWithCombinedHeaders = NextResponse.next({
    request: {
      headers: request.headers
    }
  });

  // set the response headers (set-cookie) from the auth response
  authRes.headers.forEach((value, key) => {
    resWithCombinedHeaders.headers.set(key, value);
  });

  // the headers from the auth middleware should always be returned
  return resWithCombinedHeaders;
}
```

--------------------------------

### Configuring Logout Strategy

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Control the logout mechanism used by the SDK. Options include 'auto' (default), 'oidc', and 'v2'.

```APIDOC
## Auth0Client Configuration

### Description
Configure the `logoutStrategy` option during Auth0Client initialization to control the logout behavior.

### Method
Client Initialization

### Parameters
#### Configuration Options
- **logoutStrategy** (string) - Optional - Specifies the logout strategy. Available options:
  - **"auto"** (default): Uses OIDC logout when `end_session_endpoint` is available, falls back to `/v2/logout`.
  - **"oidc"**: Always uses OIDC RP-Initiated Logout. Returns an error if not supported.
  - **"v2"**: Always uses Auth0's `/v2/logout` endpoint, supporting wildcard URLs.

### Request Example
```ts
import { Auth0Client } from '@auth0/auth0-spa-js';

const auth0 = new Auth0Client({
  domain: 'YOUR_DOMAIN',
  client_id: 'YOUR_CLIENT_ID',
  logoutStrategy: 'v2' // or 'auto', 'oidc'
  // ... other config
});
```

### Use Cases for "v2" Strategy
The "v2" strategy is useful for:
- Applications needing wildcard URL support in logout redirects (e.g., `https://localhost:3000/*/about`).
- Supporting multiple languages or environments with dynamic URLs.
- Migrating from v3 to maintain existing logout URL patterns.
- Complex logout URL requirements incompatible with OIDC logout.

### Note on "v2" Strategy
When using the "v2" strategy, ensure your logout URLs, including wildcards, are registered in your Auth0 application's **Allowed Logout URLs** settings.
```

--------------------------------

### v3 Custom Authorization Parameters (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

In v3 of the Auth0 Next.js SDK, custom authorization parameters required specifying a custom handler within `handleAuth`. This example demonstrates passing an `audience` parameter during login.

```typescript
import { handleAuth, handleLogin } from "@auth0/nextjs-auth0"

export default handleAuth({
  login: handleLogin({
    authorizationParams: { audience: "urn:my-api" },
  }),
})
```

--------------------------------

### Client Component User Authentication Check with `useUser` Hook

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This React client component example demonstrates how to check for user authentication in the browser using the `useUser` hook from the Auth0 SDK. It displays a loading state, a message for unauthenticated users, or the user's profile information if authenticated.

```tsx
"use client"

import { useUser } from "@auth0/nextjs-auth0"

export default function Profile() {
  const { user, isLoading, error } = useUser()

  if (isLoading) return <div>Loading...</div>
  if (!user) return <div>Not authenticated!</div>

  return (
    <main>
      <h1>Profile</h1>
      <div>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>
    </main>
  )
}
```

--------------------------------

### Get Access Token in Next.js API Route (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet demonstrates how to use `auth0.getAccessToken` within a Next.js API route handler to retrieve an access token for calling external services. It includes basic error handling for token acquisition. Dependencies include `next` and `@auth0/nextjs-auth0`.

```typescript
import type { NextApiRequest, NextApiResponse } from "next";

import { auth0 } from "@/lib/auth0";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ message: string }>
) {
  try {
    const token = await auth0.getAccessToken(req, res);
    // call external API with token...
  } catch (err) {
    // err will be an instance of AccessTokenError if an access token could not be obtained
  }

  res.status(200).json({ message: "Success!" });
}
```

--------------------------------

### Update User Session on Server (Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Provides an example of updating the user's session on the server for the Pages Router, specifically within `getServerSideProps` or API routes. It uses the `auth0.updateSession(req, res, session)` helper to modify the session object.

```ts
import type { NextApiRequest, NextApiResponse } from "next";

import { auth0 } from "@/lib/auth0";

type ResponseData =
  | {}
  | {
      error: string;
    };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  const session = await auth0.getSession(req);

  if (!session) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  await auth0.updateSession(req, res, {
    ...session,
    updatedAt: Date.now()
  });

  res.status(200).json({});
}

```

--------------------------------

### Dynamically Specify Audience in Login URL

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Shows how to dynamically specify authorization parameters, such as the 'audience', by appending them as query parameters to the '/auth/login' endpoint. This allows for flexible authentication flows based on specific needs.

```html
<a href="/auth/login?audience=urn:my-api">Login</a>
```

--------------------------------

### Get Access Token for Connection on Server (App Router - TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Retrieves an access token for a specified connection (e.g., 'google-oauth2') using the `getAccessTokenForConnection` method within the App Router. This method can be used in Server Routes, Server Actions, and Server Components. Server Components cannot persist token refreshes; use middleware for that.

```typescript
import { NextResponse } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function GET() {
  try {
    const token = await auth0.getAccessTokenForConnection({
      connection: "google-oauth2"
    });
    // call external API with token...
  } catch (err) {
    // err will be an instance of AccessTokenError if an access token could not be obtained
  }

  return NextResponse.json({
    message: "Success!"
  });
}
```

--------------------------------

### Middleware for Authentication Protection (Next.js)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example illustrates how to implement middleware in Next.js to protect routes using Auth0. It utilizes `auth0.middleware(request)` and `auth0.getSession(request)` to check for a valid session and redirect unauthenticated users to the login page. The `request` object must be passed to `getSession` in middleware for session updates.

```ts
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "@/lib/auth0";

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  // the headers from the auth middleware should always be returned
  return authRes;
}

```

--------------------------------

### Get Session in Server Components (Next.js App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This code demonstrates how to retrieve the authenticated user's session within Server Components in the Next.js App Router. It uses the `getSession()` helper function to access user details and protect server-side resources. The `getSession()` method provides the full session object, including user profile and tokens.

```tsx
import { auth0 } from "@/lib/auth0";

export default async function Home() {
  const session = await auth0.getSession();

  if (!session) {
    return <div>Not authenticated</div>;
  }

  return (
    <main>
      <h1>Welcome, {session.user.name}!</h1>
    </main>
  );
}

```

--------------------------------

### Specify ReturnTo URL After Authentication

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Illustrates how to use the 'returnTo' query parameter in the login URL to redirect the user to a specific route after successful authentication. The specified URL must be registered in the application's Allowed Callback URLs.

```html
/auth/login?returnTo=/dashboard
```

--------------------------------

### Get Access Token in Middleware (Next.js)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet shows how to use `getAccessTokenForConnection` within Next.js middleware to obtain an access token for a specified connection. It requires the `auth0` client and handles session checks and redirects for unauthenticated users. The `authRes` object from `auth0.middleware` is crucial for passing request and response context.

```tsx
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  const accessToken = await auth0.getAccessTokenForConnection(
    { connection: "google-oauth2" },
    request,
    authRes
  );

  // the headers from the auth middleware should always be returned
  return authRes;
}
```

--------------------------------

### Generate Session Cookie for Testing with Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This example shows how to use the `generateSessionCookie` helper function from the `@auth0/nextjs-auth0/testing` module to create a session cookie value for use in integration tests, including defining user and token set information.

```typescript
import { generateSessionCookie } from "@auth0/nextjs-auth0/testing";

const sessionCookieValue = await generateSessionCookie(
  {
    user: {
      sub: "user_123"
    },
    tokenSet: {
      accessToken: "at_123",
      refreshToken: "rt_123",
      expiresAt: 123456789
    }
  },
  {
    secret: process.env.AUTH0_SECRET!
  }
);
```

--------------------------------

### Get Access Token on Server (Next.js App Router Route Handler)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Shows how to retrieve an access token on the server-side using the `getAccessToken` helper within a Next.js App Router route handler. This method automatically handles token refreshing if expired and a refresh token is available. It notes that Server Components cannot set cookies and recommends using middleware for token persistence in such cases.

```typescript
import { NextResponse } from "next/server";

import { auth0 } from "@/lib/auth0";

export async function GET() {
  try {
    const token = await auth0.getAccessToken();
    // call external API with token...
  } catch (err) {
    // err will be an instance of AccessTokenError if an access token could not be obtained
  }

  return NextResponse.json({
    message: "Success!"
  });
}
```

--------------------------------

### Configure Return URL for Post-Login Redirect (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Specifies the `returnTo` parameter when calling `startInteractiveLogin` to define the URL the user will be redirected to after completing authentication. The specified URL must be registered in the application's Allowed Callback URLs.

```typescript
import { NextRequest } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export const GET = async (req: NextRequest) => {
  return auth0.startInteractiveLogin({
    returnTo: "/dashboard"
  });
};
```

--------------------------------

### Add Custom Logic After Authentication with onCallback Hook

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This code example shows how to use the `onCallback` hook provided by Auth0Client in nextjs-auth0. This hook allows you to execute custom logic after a user has successfully authenticated, such as logging user information or redirecting the user based on custom conditions.

```typescript
import { NextResponse } from 'next/server';
import { Auth0Client } from '@auth0/nextjs-auth0/server';

export const auth0 = new Auth0Client({
  async onCallback(error, context, session) {
    if (error) {
      console.error('Authentication error:', error);
      return NextResponse.redirect(
        new URL('/error', process.env.APP_BASE_URL)
      );
    }

    // Custom logic after successful authentication
    if (session) {
      console.log(`User ${session.user.sub} logged in successfully`);
    }

    return NextResponse.redirect(
      new URL(context.returnTo || "/", process.env.APP_BASE_URL)
    );
  }
});
```

--------------------------------

### Set Custom Profile and Access Token Routes via Environment Variables

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to configure custom routes for the user profile and access token endpoints in a Next.js application using environment variables. This is necessary for features like `withPageAuthRequired` to function correctly with custom routes.

```ini
# .env.local
# required environment variables...

NEXT_PUBLIC_PROFILE_ROUTE=/api/me
NEXT_PUBLIC_ACCESS_TOKEN_ROUTE=/api/auth/token
```

--------------------------------

### Transaction Cookie Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Configure transaction cookie expiration and management modes.

```APIDOC
## Transaction Cookie Configuration

### Description
Transaction cookies are used to maintain state during authentication flows. The SDK provides several configuration options to manage transaction cookie behavior and prevent cookie accumulation issues.

### Customizing Transaction Cookie Expiration

Configure transaction cookies expiration by providing a `maxAge` property for `transactionCookie`.

### Method
```typescript
export const auth0 = new Auth0Client({
  transactionCookie: {
    maxAge: 1800, // 30 minutes (in seconds)
    // ... other options
  },
});
```

### Transaction Management Modes

#### Parallel Transactions (Default)

```typescript
const authClient = new Auth0Client({
  enableParallelTransactions: true // Default: allows multiple concurrent logins
  // ... other options
});
```

**Use When:**
- Users might open multiple tabs and attempt to log in simultaneously
- You want maximum compatibility with typical user behavior
- Your application supports multiple concurrent authentication flows

#### Single Transaction Mode

```typescript
const authClient = new Auth0Client({
  enableParallelTransactions: false // Only one active transaction at a time
  // ... other options
});
```

**Use When:**
- You want to prevent cookie accumulation issues in applications with frequent login attempts
- You prefer simpler transaction management
- Users typically don't need multiple concurrent login flows
- You're experiencing cookie header size limits due to abandoned transaction cookies edge cases
```

--------------------------------

### Remove getServerSidePropsWrapper in Next.js API routes (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

With the explicit session update mechanism in v2.x, the `getServerSidePropsWrapper` is no longer necessary. You can directly define `getServerSideProps` and handle session retrieval within it. This simplifies the server-side data fetching setup.

```javascript
export const getServerSideProps = (ctx) => {
  const session = getSession(ctx.req, ctx.res)
  if (session) {
    // User is authenticated
  } else {
    // User is not authenticated
  }
}
```

--------------------------------

### StartInteractiveLoginOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.StartInteractiveLoginOptions.html

Defines the options available when starting an interactive login flow.

```APIDOC
## StartInteractiveLoginOptions Interface

### Description

This interface represents the configuration options for initiating an interactive login process using the Auth0 Next.js SDK.

### Properties

#### `authorizationParameters` (AuthorizationParameters) - Optional

An object containing authorization parameters to be passed to the authorization server.

#### `returnTo` (string) - Optional

The URL to which the user will be redirected after a successful login.

### Interface Definition

```typescript
interface StartInteractiveLoginOptions {
    authorizationParameters?: AuthorizationParameters;
    returnTo?: string;
}
```

### Source

[src/types/index.ts:105](https://github.com/auth0/nextjs-auth0/blob/88edf0e2f7c1f113c01064c7a3856870baa646bc/src/types/index.ts#L105)
```

--------------------------------

### v4 Auth0 Client Initialization with Static Authorization Parameters (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

Statically configures authorization parameters, such as `scope` and `audience`, during the initialization of the `Auth0Client` in v4.

```typescript
export const auth0 = new Auth0Client({
  authorizationParameters: {
    scope: "openid profile email",
    audience: "urn:custom:api",
  },
});
```

--------------------------------

### App Router Server Component Authentication Check

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This example shows how to protect an App Router Server Component in Next.js using the `auth0.getSession()` method. If no session is found, the user is redirected to the login page with a specified return URL. Otherwise, it displays a welcome message with the user's name.

```tsx
// Example for an App Router Server Component
import { redirect } from 'next/navigation'
import { auth0 } from './lib/auth0' // Adjust path if your auth0 client is elsewhere

export default async function Page() {
  const session = await auth0.getSession()

  if (!session) {
    // The user will be redirected to authenticate and then taken to the
    // /dashboard route after successfully being authenticated.
    return redirect('/auth/login?returnTo=/dashboard')
  }

  return <h1>Hello, {session.user.name}</h1>
}
```

--------------------------------

### Override Default Error Handler for Auth Routes (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

This example shows how to implement a centralized error handler for authentication routes. The `onError` function within `handleAuth` allows customization of error logging and response handling, replacing the previous per-route try-catch blocks.

```javascript
export default handleAuth({
  onError(req, res, error) {
    errorLogger(error)
    // You can finish the response yourself if you want to customize
    // the status code or redirect the user
    // res.writeHead(302, {
    //     Location: '/custom-error-page'
    // });
    // res.end();
  },
})
```

--------------------------------

### Update Auth0 SDK Configuration (Before V1 - JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

Illustrates the configuration structure for initializing Auth0 in a Next.js application using v0.x of the SDK. This serves as a comparison to highlight the changes required for v1 migration, showing older configuration properties like `domain`, `clientId`, `redirectUri`, `postLogoutRedirectUri`, and the older session configuration.

```javascript
import { initAuth0 } from "@auth0/nextjs-auth0"

export default initAuth0({
  domain: "my-tenant.auth0.com",
  clientId: "MY_CLIENT_ID",
  clientSecret: "MY_CLIENT_SECRET",
  scope: "openid profile",
  audience: "MY_AUDIENCE",
  redirectUri: "http://localhost:3000/api/callback",
  postLogoutRedirectUri: "http://localhost:3000/",
  session: {
    cookieSecret: "some_very_long_secret_string",
    cookieLifetime: 60 * 60 * 8,
    storeIdToken: false,
    storeRefreshToken: false,
    storeAccessToken: false,
  },
  oidcClient: {
    clockTolerance: 10000,
    httpTimeout: 2500,
  },
})
```

--------------------------------

### OIDC Logout Privacy Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Control whether the `id_token_hint` parameter is included in OIDC logout URLs for privacy considerations.

```APIDOC
## Auth0Client Configuration: OIDC Logout Privacy

### Description
Configure the `includeIdTokenHintInOIDCLogoutUrl` option to manage the inclusion of `id_token_hint` in OIDC logout requests, balancing security and privacy.

### Method
Client Initialization

### Parameters
#### Configuration Options
- **includeIdTokenHintInOIDCLogoutUrl** (boolean) - Optional - Determines whether to include the `id_token_hint` parameter in OIDC logout URLs.
  - **`true`** (default): Includes `id_token_hint` for enhanced security. This is the recommended setting.
  - **`false`**: Excludes `id_token_hint` for privacy. This may expose PII in logs or browser history.

### Request Example (Default Behavior)
```ts
import { Auth0Client } from '@auth0/auth0-spa-js';

const auth0 = new Auth0Client({
  domain: 'YOUR_DOMAIN',
  client_id: 'YOUR_CLIENT_ID',
  logoutStrategy: 'auto', // or 'oidc'
  includeIdTokenHintInOIDCLogoutUrl: true // default value
  // ... other config
});
```

### Request Example (Privacy-Focused)
```ts
import { Auth0Client } from '@auth0/auth0-spa-js';

const auth0 = new Auth0Client({
  domain: 'YOUR_DOMAIN',
  client_id: 'YOUR_CLIENT_ID',
  logoutStrategy: 'auto', // or 'oidc'
  includeIdTokenHintInOIDCLogoutUrl: false // exclude id_token_hint for privacy
  // ... other config
});
```

### Important Considerations
- Setting `includeIdTokenHintInOIDCLogoutUrl` to `false` is only effective with `oidc` or `auto` (when OIDC is used) logout strategies. It has no effect on the `v2` strategy.
- When `id_token_hint` is excluded, logout requests lose cryptographic verification, potentially increasing the risk of denial-of-service attacks, as warned by the OpenID Connect specification.
```

--------------------------------

### Implement Federated Logout with Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Enable federated logout to log the user out from both Auth0 and their connected identity provider. This can be combined with custom return URLs.

```html
<!-- Regular logout (Auth0 session only) -->
<a href="/auth/logout">Logout</a>

<!-- Federated logout (Auth0 + Identity Provider) -->
<a href="/auth/logout?federated">Logout from IdP</a>

<!-- Federated logout with custom returnTo -->
<a href="/auth/logout?federated&returnTo=https://example.com/goodbye">Logout from IdP</a>

```

--------------------------------

### Get Session in getServerSideProps (Next.js Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet shows how to fetch the authenticated user's session within `getServerSideProps` in the Next.js Pages Router. It uses the `getSession(req)` helper to obtain session data and conditionally render content based on authentication status. This is suitable for applications needing session data without external API calls.

```tsx
import type { GetServerSideProps, InferGetServerSidePropsType } from "next";

import { auth0 } from "@/lib/auth0";

export const getServerSideProps = (async (ctx) => {
  const session = await auth0.getSession(ctx.req);

  if (!session) return { props: { user: null } };

  return { props: { user: session.user ?? null } };
}) satisfies GetServerSideProps<{ user: any | null }>;

export default function Page({
  user
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  if (!user) {
    return (
      <main>
        <p>Not authenticated!</p>
      </main>
    );
  }

  return (
    <main>
      <p>Welcome, {user.name}!</p>
    </main>
  );
}

```

--------------------------------

### Customize Authorization Parameters for Login (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to customize authorization parameters like scope and audience when initiating an interactive login programmatically. This can be done either statically during client instantiation or dynamically when calling `startInteractiveLogin`.

```typescript
import { NextRequest } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export const GET = async (req: NextRequest) => {
  // Call startInteractiveLogin with optional parameters
  return auth0.startInteractiveLogin({
    authorizationParameters: {
      scope: "openid profile email",
      audience: "urn:custom:api"
    }
  });
};
```

--------------------------------

### v4 Dynamic Base URL Configuration (next.config.js - TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

Configures the `APP_BASE_URL` environment variable dynamically in `next.config.js` for platforms like Vercel, ensuring correct URLs for preview deployments.

```typescript
// next.config.js
module.exports = {
  env: {
    APP_BASE_URL:
      process.env.VERCEL_ENV === "preview"
        ? `https://${process.env.VERCEL_BRANCH_URL}`
        : process.env.APP_BASE_URL,
  },
};
```

--------------------------------

### Logout with Custom Return URL

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Specify a custom URL to redirect the user to after they have logged out by appending the `returnTo` parameter to the logout endpoint.

```APIDOC
## GET /auth/logout

### Description
Initiates the logout process and redirects the user to a specified URL upon completion.

### Method
GET

### Endpoint
/auth/logout

### Query Parameters
- **returnTo** (string) - Optional - The URL to redirect the user to after logout. This URL must be registered in your client's Allowed Logout URLs.

### Request Example
```
/auth/logout?returnTo=https://example.com/some-page
```

### Response
#### Success Response (302 Found)
- **Location** (string) - The URL to redirect the user to.

#### Response Example
```
Location: https://example.com/some-page
```
```

--------------------------------

### Session Cookie Options via Environment Variables

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Configure session cookie attributes using environment variables. The SDK automatically picks up these values. Note that httpOnly is always set to true.

```APIDOC
## Session Cookie Options via Environment Variables

### Description
Configure session cookie attributes using environment variables. The SDK automatically picks up these values. Note that `httpOnly` is always set to `true` for security reasons and cannot be configured.

### Environment Variables

- **AUTH0_COOKIE_DOMAIN** (String): Set cookie for subdomains.
- **AUTH0_COOKIE_PATH** (String): Limit cookie to a specific path.
- **AUTH0_COOKIE_TRANSIENT** (Boolean): Make cookie transient (session-only).
- **AUTH0_COOKIE_SECURE** (Boolean): Recommended for production.
- **AUTH0_COOKIE_SAME_SITE** (String): Specifies the `SameSite` attribute ('Lax', 'Strict', 'None').

### Example
```bash
export AUTH0_COOKIE_DOMAIN='.example.com'
export AUTH0_COOKIE_PATH='/app'
export AUTH0_COOKIE_TRANSIENT=true
export AUTH0_COOKIE_SECURE=true
export AUTH0_COOKIE_SAME_SITE='Lax'
```
```

--------------------------------

### Configure Auth0 Client Logout Strategy

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Set the logout strategy for the Auth0 client. Options include 'auto' (default), 'oidc', and 'v2'. The 'v2' strategy supports wildcard URLs for logout redirects.

```typescript
export const auth0 = new Auth0Client({
  logoutStrategy: "auto" // default behavior
  // ... other config
});

// Example: Using v2 logout for wildcard URL support
export const auth0 = new Auth0Client({
  logoutStrategy: "v2"
  // ... other config
});

```

--------------------------------

### Federated Logout

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Enable logging out from both Auth0 and the associated identity provider (IdP) using the `federated` parameter.

```APIDOC
## Logout with Federated Identity Provider

### Description
Perform a federated logout to sign the user out of both their Auth0 session and their external identity provider (e.g., Google, Facebook).

### Method
GET

### Endpoint
/auth/logout

### Query Parameters
- **federated** (boolean) - Optional - If present, initiates federated logout from the identity provider.
- **returnTo** (string) - Optional - The URL to redirect to after logout. Can be used in conjunction with `federated`.

### Request Example
```html
<!-- Regular logout (Auth0 session only) -->
<a href="/auth/logout">Logout</a>

<!-- Federated logout (Auth0 + Identity Provider) -->
<a href="/auth/logout?federated">Logout from IdP</a>

<!-- Federated logout with custom returnTo -->
<a href="/auth/logout?federated&returnTo=https://example.com/goodbye">Logout from IdP</a>
```

### Note
The `federated` parameter is supported across all logout strategies (`auto`, `oidc`, and `v2`) and is passed to the relevant Auth0 logout endpoint.

- **OIDC logout**: `https://your-domain.auth0.com/oidc/logout?federated&...`
- **V2 logout**: `https://your-domain.auth0.com/v2/logout?federated&...`
```

--------------------------------

### Configure Session Cookie Options via Environment Variables

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Set session cookie attributes using environment variables. These are automatically picked up by the SDK. Note that httpOnly is always true for security.

```env
AUTH0_COOKIE_DOMAIN='.example.com'
AUTH0_COOKIE_PATH='/app'
AUTH0_COOKIE_TRANSIENT=true
AUTH0_COOKIE_SECURE=true
AUTH0_COOKIE_SAME_SITE='Lax'
```

--------------------------------

### Import UserProvider and useUser from @auth0/nextjs-auth0/client (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

Client-side methods and components, such as `UserProvider` and `useUser`, are now exported under the `/client` path in v2.x. This ensures proper client-side rendering and hook usage in Next.js applications.

```javascript
// pages/_app.js
import React from "react"
import { UserProvider } from "@auth0/nextjs-auth0/client"

export default function App({ Component, pageProps }) {
  return (
    <UserProvider>
      <Component {...pageProps} />
    </UserProvider>
  )
}
```

```javascript
// pages/index.js

// The SSR version of withPageAuthRequired is still in the root export
import { withPageAuthRequired as withPageAuthRequiredSSR } from "@auth0/nextjs-auth0"
import {
  useUser,
  withPageAuthRequired as withPageAuthRequiredCSR,
} from "@auth0/nextjs-auth0/client"

export default withPageAuthRequiredCSR(function Index() {
  const { user, error, isLoading } = useUser()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>{error.message}</div>

  if (user) {
    return (
      <div>
        Welcome {user.name}! <a href="/api/auth/logout">Logout</a>
      </div>
    )
  }

  return <a href="/api/auth/login">Login</a>
})

export const getServerSideProps = withPageAuthRequiredSSR()
```

--------------------------------

### Configure Transaction Management Mode (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Control whether multiple concurrent authentication transactions are allowed. Setting `enableParallelTransactions` to true enables parallel mode (default), while false enforces single transaction mode.

```typescript
const authClient = new Auth0Client({
  enableParallelTransactions: true // Default: allows multiple concurrent logins
  // ... other options
});

```

```typescript
const authClient = new Auth0Client({
  enableParallelTransactions: false // Only one active transaction at a time
  // ... other options
});

```

--------------------------------

### Configure Custom Auth0 Routes in Next.js

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet shows how to customize the default route paths for Auth0 authentication flows (login, logout, callback, backchannel logout) using the `routes` configuration option when instantiating the `Auth0Client`.

```typescript
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  routes: {
    login: "/login",
    logout: "/logout",
    callback: "/callback",
    backChannelLogout: "/backchannel-logout"
  }
});
```

--------------------------------

### Next.js Middleware for Rolling Sessions

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Define a broad middleware matcher in Next.js to enable rolling sessions for the Auth0 authentication. A broad matcher ensures that the middleware runs on all relevant requests, allowing for session extension and consistent authentication state.

```typescript
// ✅ CORRECT: Broad matcher enables rolling sessions
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*"]
};
```

--------------------------------

### Update Auth0 SDK Configuration (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

Demonstrates the updated configuration options for initializing Auth0 in a Next.js application after migrating to v1.x. Key changes include renaming `domain` to `issuerBaseURL`, `clientId` to `clientID`, and restructuring of `redirectUri` and `postLogoutRedirectUri` into `routes.callback` and `routes.postLogoutRedirect` respectively. It also shows how `scope` and `audience` are now passed via `authorizationParams` and session cookie options have been simplified.

```javascript
import { initAuth0 } from "@auth0/nextjs-auth0"

export default initAuth0({
  baseURL: "http://localhost:3000",
  issuerBaseURL: "https://my-tenant.auth0.com",
  clientID: "MY_CLIENT_ID",
  clientSecret: "MY_CLIENT_SECRET",
  secret: "some_very_long_secret_string",
  clockTolerance: 60,
  httpTimeout: 5000,
  authorizationParams: {
    scope: "openid profile email",
    audience: "MY_AUDIENCE",
  },
  routes: {
    callback: "/api/callback",
    postLogoutRedirect: "/",
  },
  session: {
    rollingDuration: 60 * 60 * 24,
    absoluteDuration: 60 * 60 * 24 * 7,
  },
})
```

--------------------------------

### Optional appBaseUrl Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Auth0ClientOptions.html

Specifies the base URL of your application, for example, 'http://localhost:3000'. If not provided, it defaults to the APP_BASE_URL environment variable.

```typescript
appBaseUrl?: string;
```

--------------------------------

### Access idToken from Auth0 Session

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Shows how to retrieve the `idToken` from the authenticated user's session. This is useful when you need to pass the ID token to other services or for specific authentication-related tasks within your application.

```js
const session = await auth0.getSession();
const idToken = session.tokenSet.idToken;

```

--------------------------------

### Get Session by ID - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

Implements the 'get' method for the SessionDataStore interface. This function retrieves session data from the store based on the provided session ID. It returns a Promise that resolves with the SessionData object if found, or null if the session does not exist.

```typescript
get(id: string): Promise<null | SessionData>
```

--------------------------------

### Modify Session Claims with beforeSessionSaved Hook

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

The beforeSessionSaved hook in Auth0Client allows modification of session claims before they are persisted. It receives session data and an ID token, and must return a Promise resolving to modified SessionData. This example filters default ID token claims and retains a custom 'foo' claim.

```ts
import {
  Auth0Client,
  filterDefaultIdTokenClaims
} from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  async beforeSessionSaved(session, idToken) {
    return {
      ...session,
      user: {
        ...filterDefaultIdTokenClaims(session.user),
        foo: session.user.foo // keep the foo claim
      }
    };
  }
});
```

--------------------------------

### Mandatory Configuration Options for Auth0Client Initialization

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

The Auth0 SDK requires specific configuration options to be provided, either through constructor options or environment variables. Missing options will result in warnings.

```javascript
// Example using constructor options:
const auth0Client = new Auth0Client({
  domain: 'YOUR_AUTH0_DOMAIN',
  clientId: 'YOUR_AUTH0_CLIENT_ID',
  appBaseUrl: 'YOUR_APP_BASE_URL',
  secret: 'YOUR_AUTH0_SECRET',
  // Either clientSecret or clientAssertionSigningKey is required
  clientSecret: 'YOUR_AUTH0_CLIENT_SECRET',
  // clientAssertionSigningKey: 'YOUR_CLIENT_ASSERTION_SIGNING_KEY',
});

// Example using environment variables (preferred):
// AUTH0_DOMAIN=YOUR_AUTH0_DOMAIN
// AUTH0_CLIENT_ID=YOUR_AUTH0_CLIENT_ID
// APP_BASE_URL=YOUR_APP_BASE_URL
// AUTH0_SECRET=YOUR_AUTH0_SECRET
// AUTH0_CLIENT_SECRET=YOUR_AUTH0_CLIENT_SECRET
// OR
// AUTH0_CLIENT_ASSERTION_SIGNING_KEY=YOUR_CLIENT_ASSERTION_SIGNING_KEY
```

--------------------------------

### Configure Default Login Handler Options (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

This code demonstrates how to configure default options for the `login` handler within `handleAuth`. It shows passing a static options object or a function that dynamically generates options based on the request, enabling features like specifying the connection.

```javascript
export default handleAuth({
  login: handleLogin({
    authorizationParams: { connection: "github" },
  }),
})

export default handleAuth({
  login: handleLogin((req) => {
    return {
      authorizationParams: { connection: "github" },
    }
  }),
})
```

--------------------------------

### Update handleLogin Options in Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

This snippet demonstrates the update for the `handleLogin` function in nextjs-auth0. The `authParams` object has been renamed to `authorizationParams`, and `redirectTo` has been changed to `returnTo`. This ensures compatibility with the latest library version.

```javascript
// pages/api/login.js
import auth0 from "../../utils/auth0"

export default async function login(req, res) {
  try {
    await auth0.handleLogin(req, res, {
      authorizationParams: {
        login_hint: "foo@acme.com",
        ui_locales: "nl",
        scope: "some other scope",
        foo: "bar",
      },
      returnTo: "/custom-url",
    })
  } catch (error) {
    console.error(error)
    res.status(error.status || 500).end(error.message)
  }
}
```

--------------------------------

### Configure Broad Default Scopes in Auth0Client (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This code snippet illustrates the best practice of configuring broad default scopes within the Auth0Client constructor. By defining comprehensive scopes for common operations, you can minimize the need for dynamic scope requests, thereby reducing the number of tokens stored in the session.

```typescript
export const auth0 = new Auth0Client({
  authorizationParameters: {
    audience: "https://api.example.com",
    // Configure broad default scopes for most common operations
    scope: "openid profile email offline_access read:products read:orders read:users"
  }
});
```

--------------------------------

### Configure Scopes Per Audience in Auth0Client (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet shows how to initialize Auth0Client with an object for authorization parameters, allowing you to define default scopes for multiple audiences. This is useful when your application interacts with several APIs, each requiring different permissions.

```typescript
import {
  Auth0Client
} from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  authorizationParameters: {
    audience: "https://api.example.com", // Default audience
    scope: {
      "https://api.example.com": "openid profile email offline_access read:products read:orders",
      "https://analytics.example.com": "openid profile email offline_access read:analytics write:analytics",
      "https://admin.example.com": "openid profile email offline_access read:admin write:admin delete:admin"
    }
  }
});
```

--------------------------------

### Mount SDK Routes as Middleware (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Integrates Auth0 SDK routes to function as middleware within a Next.js application. This setup is crucial for handling authentication and authorization flows at the request level.

```typescript
import { NextRequest, NextResponse } from "next/server";

async function middleware(req: NextRequest): Promise<NextResponse>
```

--------------------------------

### Get Access Token (Options Only)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Illustrates retrieving an access token without explicit request and response objects, useful for scenarios where these are not directly available but token refresh logic is needed. Requires optional configuration.

```typescript
import { Auth0Client } from '@auth0/nextjs-auth0';

const auth0Client = new Auth0Client({ /* options */ });

async function getMyToken() {
  const tokenData = await auth0Client.getAccessToken({ refresh: false });
  return tokenData.token;
}
```

--------------------------------

### Configuring Base Path in next.config.js

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

To configure the SDK to use a base path in your Next.js application, you need to set the `basePath` option in `next.config.js` and the `NEXT_PUBLIC_BASE_PATH` environment variable. This example shows how to set the environment variable.

```javascript
// next.config.js
module.exports = {
  // ... other configurations
  basePath: '/dashboard',
};

// .env.local
NEXT_PUBLIC_BASE_PATH=/dashboard
```

--------------------------------

### Initialize Auth0Client with Options

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Demonstrates how to create a new instance of Auth0Client using optional configuration options. This is the primary way to instantiate the client for use in server-side logic.

```typescript
import { Auth0Client } from "@auth0/nextjs-auth0";

const auth0Client = new Auth0Client({ /* options */ });
```

--------------------------------

### Start Interactive Login Flow (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Initiates an interactive login process for users, often involving redirects to Auth0's login page. This function can accept optional configuration options to customize the login experience.

```typescript
import { StartInteractiveLoginOptions } from "./types";
import { NextResponse } from "next/server";

async function startInteractiveLogin(options?: StartInteractiveLoginOptions): Promise<NextResponse>
```

--------------------------------

### Configure OIDC Logout URL Privacy (Next.js Auth0)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Control whether the `id_token_hint` parameter is included in OIDC logout URLs. Setting `includeIdTokenHintInOIDCLogoutUrl` to `false` enhances privacy but reduces security.

```typescript
export const auth0 = new Auth0Client({
  logoutStrategy: "auto", // or "oidc"
  includeIdTokenHintInOIDCLogoutUrl: true // default value
  // ... other config
});

export const auth0 = new Auth0Client({
  logoutStrategy: "auto", // or "oidc"
  includeIdTokenHintInOIDCLogoutUrl: false // exclude id_token_hint for privacy
  // ... other config
});

```

--------------------------------

### Configuring Session Durations for Auth0 Client

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Configure session persistence for the Auth0 client by specifying session options, including rolling session behavior, absolute duration, and inactivity duration. These settings control how long user sessions remain active.

```typescript
export const auth0 = new Auth0Client({
  session: {
    rolling: true,
    absoluteDuration: 60 * 60 * 24 * 30, // 30 days in seconds
    inactivityDuration: 60 * 60 * 24 * 7 // 7 days in seconds
  }
});
```

--------------------------------

### Access Protected API Route from Frontend (Page Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to fetch data from a protected API route (`/api/protected`) on the frontend within a Next.js application using `withPageAuthRequired` and the `useSWR` hook. This ensures that the frontend component itself requires authentication.

```jsx
import { withPageAuthRequired } from "@auth0/nextjs-auth0";
import useSWR from "swr";

const fetcher = async (uri) => {
  const response = await fetch(uri);
  return response.json();
};

export default withPageAuthRequired(function Products() {
  const { data, error } = useSWR("/api/protected", fetcher);
  if (error) return <div>oops... {error.message}</div>;
  if (data === undefined) return <div>Loading...</div>;
  return <div>{data.protected}</div>;
});

```

--------------------------------

### Auth0Client Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Initializes a new Auth0Client instance with optional configuration options.

```APIDOC
## Auth0Client Constructor

### Description
Initializes a new Auth0Client instance.

### Method
Constructor

### Parameters
#### Request Body
- **options** (Auth0ClientOptions) - Optional - Configuration options for the Auth0 client.

### Request Example
```json
{
  "options": {
    "domain": "your-auth0-domain.com",
    "clientId": "your-client-id"
  }
}
```

### Response
#### Success Response (200)
- **Auth0Client** (object) - An instance of the Auth0Client.

### Response Example
```json
{
  "message": "Auth0Client initialized successfully"
}
```
```

--------------------------------

### Configuration Validation

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

Understand the mandatory configuration options required for initializing the Auth0Client and how the SDK validates them.

```APIDOC
## Configuration Validation

### Description
The SDK validates required configuration options upon initializing the `Auth0Client`.

### Mandatory Options
These options must be provided via constructor options or environment variables:

*   `domain` (or `AUTH0_DOMAIN`)
*   `clientId` (or `AUTH0_CLIENT_ID`)
*   `appBaseUrl` (or `APP_BASE_URL`)
*   `secret` (or `AUTH0_SECRET`)
*   Either:
    *   `clientSecret` (or `AUTH0_CLIENT_SECRET`)
    *   OR `clientAssertionSigningKey` (or `AUTH0_CLIENT_ASSERTION_SIGNING_KEY`)

### Validation Warnings
If any required options are missing, the SDK will issue a warning detailing the missing options and how to provide them.
```

--------------------------------

### Access Protected API Route from Frontend (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Illustrates fetching data from a protected API route (`/api/protected`) on the frontend in an App Router Next.js application. It utilizes `withPageAuthRequired` and `useSWR`, ensuring the frontend component requires user authentication to display the data.

```jsx
"use client";

import { withPageAuthRequired } from "@auth0/nextjs-auth0";
import useSWR from "swr";

const fetcher = async (uri) => {
  const response = await fetch(uri);
  return response.json();
};

export default withPageAuthRequired(function Products() {
  const { data, error } = useSWR("/api/protected", fetcher);
  if (error) return <div>oops... {error.message}</div>;
  if (data === undefined) return <div>Loading...</div>;
  return <div>{data.protected}</div>;
});

```

--------------------------------

### Update getSession to use await (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

In v2.x, `getSession` is now an async function and returns a Promise. You must use `await` when calling it. This change applies to API routes in Next.js.

```javascript
// /pages/api/my-api
import { getSession } from "@auth0/nextjs-auth0"

async function myApiRoute(req, res) {
  const session = await getSession(req, res)
  // ...
}
```

--------------------------------

### V4 Middleware Configuration with Route Matching

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This TypeScript code configures the Auth0 middleware for v4 applications. It includes the standard middleware function and an export for `config`, which defines a `matcher` to include most paths while excluding static assets and metadata files. This ensures the middleware is applied to relevant application routes.

```typescript
import type { NextRequest } from "next/server"

import { auth0 } from "./lib/auth0" // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  return await auth0.middleware(request) // Returns a NextResponse object
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
}
```

--------------------------------

### Configure Session Cookie Options via Auth0ClientOptions (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Directly configure session cookie attributes when initializing Auth0Client in TypeScript. These settings override environment variables. The httpOnly attribute is always true and cannot be changed.

```typescript
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  session: {
    cookie: {
      domain: ".example.com",
      path: "/app",
      transient: true,
      // httpOnly is always true and cannot be configured
      secure: process.env.NODE_ENV === "production",
      sameSite: "Lax"
      // name: 'appSession', // Optional: custom cookie name, defaults to '__session'
    }
    // ... other session options like absoluteDuration ...
  }
  // ... other client options ...
});

```

--------------------------------

### Client Configuration Options

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Customize the Auth0 client by providing various options during initialization. These options can also be set via environment variables.

```APIDOC
## Client Configuration

### Description

This section details the available options for customizing the Auth0 client within the nextjs-auth0 SDK. These settings allow you to configure authentication flows, tenant details, and security parameters.

### Method

N/A (Configuration options are applied during SDK initialization)

### Endpoint

N/A (Configuration options are applied during SDK initialization)

### Parameters

#### Initialization Options

- **domain** (`string`) - Required - The Auth0 domain for your tenant (e.g., `example.us.auth0.com` or `https://example.us.auth0.com`). Defaults to the `AUTH0_DOMAIN` environment variable if not provided.
- **clientId** (`string`) - Required - The Auth0 client ID for your application. Defaults to the `AUTH0_CLIENT_ID` environment variable if not provided.
- **clientSecret** (`string`) - Optional - The Auth0 client secret. Required for certain authentication flows. Defaults to the `AUTH0_CLIENT_SECRET` environment variable if not provided.
- **authorizationParameters** (`object`) - Optional - An object containing parameters to be passed to the `/authorize` endpoint. Refer to the [Passing authorization parameters](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md#passing-authorization-parameters) documentation for details.
- **clientAssertionSigningKey** (`string` or `CryptoKey`) - Optional - The private key used for signing client assertions when using `private_key_jwt` client authentication. This can also be set via the `AUTH0_CLIENT_ASSERTION_SIGNING_KEY` environment variable.

### Request Example

```javascript
import { initAuth0 } from '@auth0/nextjs-auth0';

export default initAuth0({
  domain: 'YOUR_AUTH0_DOMAIN',
  clientId: 'YOUR_AUTH0_CLIENT_ID',
  clientSecret: 'YOUR_AUTH0_CLIENT_SECRET',
  authorizationParams: {
    audience: 'YOUR_API_AUDIENCE',
    scope: 'read:users'
  }
});
```

### Response

N/A (These are configuration options, not API responses.)
```

--------------------------------

### Protect Client-Side Rendered Page with Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Protects a client-side rendered page by ensuring a valid user session exists. If no session is found, the user is redirected to the login page. This uses the `withPageAuthRequired` higher-order function.

```tsx
"use client";

import { withPageAuthRequired } from "@auth0/nextjs-auth0";

export default withPageAuthRequired(function Page({ user }) {
  return <div>Hello, {user.name}!</div>;
});

```

--------------------------------

### Customizing Auth0 Callback Handling in Next.js

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Implement a custom `onCallback` hook to manage user redirection after authentication with Auth0. This hook handles errors from Auth0 or transaction completion, returning a `NextResponse` to redirect the user appropriately.

```typescript
export const auth0 = new Auth0Client({
  async onCallback(error, context, session) {
    // redirect the user to a custom error page
    if (error) {
      return NextResponse.redirect(
        new URL(`/error?error=${error.message}`, process.env.APP_BASE_URL)
      );
    }

    // complete the redirect to the provided returnTo URL
    return NextResponse.redirect(
      new URL(context.returnTo || "/", process.env.APP_BASE_URL)
    );
  }
});
```

--------------------------------

### Define StartInteractiveLoginOptions Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.StartInteractiveLoginOptions.html

This TypeScript interface defines the structure for options when starting an interactive login. It includes optional authorization parameters and a returnTo URL for post-login redirection. This is used internally by the SDK to manage login configurations.

```typescript
interface StartInteractiveLoginOptions {
    [authorizationParameters](#authorizationparameters)?: [AuthorizationParameters](types.AuthorizationParameters.html);
    [returnTo](#returnto)?: string;
}
```

--------------------------------

### Update handleLogout Options in Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

This snippet shows the migration for the `handleLogout` function in nextjs-auth0. The `redirectTo` option has been renamed to `returnTo` to align with the updated API. This change is crucial for correct logout redirection.

```javascript
// pages/api/logout.js
import auth0 from "../../utils/auth0"

export default async function logout(req, res) {
  try {
    await auth0.handleLogout(req, res, {
      returnTo: "/custom-url",
    })
  } catch (error) {
    console.error(error)
    res.status(error.status || 500).end(error.message)
  }
}
```

--------------------------------

### Update getAccessToken Method (Before V1 - JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

Illustrates the older method of retrieving an access token using the `tokenCache` in @auth0/nextjs-auth0 v0.x. This code snippet shows the pattern that has been replaced in v1.x with a more direct `getAccessToken` method, highlighting the removal of the `tokenCache` abstraction.

```javascript
// pages/api/shows.js
import auth0 from "../../lib/auth0"

export default async function shows(req, res) {
  const tokenCache = auth0.tokenCache(req, res)
  const { accessToken } = await tokenCache.getAccessToken({
    scopes: ["read:shows"],
  })
  // ...
}
```

--------------------------------

### V4 Middleware for Auth0 Authentication

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This TypeScript code shows the v4 approach to handling authentication using middleware. It imports `NextRequest` from `next/server` and the `auth0` instance from a local configuration file. The `middleware` function then calls `auth0.middleware(request)` to process authentication requests.

```typescript
import type { NextRequest } from "next/server"

import { auth0 } from "./lib/auth0" // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  return await auth0.middleware(request)
}
```

--------------------------------

### Get Access Token for Connection (Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves an access token for a connection, accepting request and response objects. This overload is intended for middleware, `getServerSideProps`, and API routes within the Pages Router.

```typescript
import { getAccessTokenForConnection } from "@auth0/nextjs-auth0";
import type { NextRequest, NextResponse } from "next/server";

// ... inside an async function or handler
const session = await getAccessTokenForConnection(options, req, res);

```

--------------------------------

### Get Session Data (Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves the session data for the current request, requiring a request object. This version is applicable for middleware and `getServerSideProps` in the Pages Router.

```typescript
import { getSession } from "@auth0/nextjs-auth0";
import type { NextRequest } from "next/server";

// ... inside an async function or handler
const session = await getSession(req);

```

--------------------------------

### Update getAccessToken Method Signature (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

Demonstrates the refactored `getAccessToken` method in @auth0/nextjs-auth0 v1.x. The previous `tokenCache` object has been removed. Instead, `getAccessToken` is now a direct method of the auth0 instance, accepting the request, response, and token options as arguments. This simplifies token retrieval and management.

```javascript
// pages/api/shows.js
import auth0 from "../../lib/auth0"

export default async function shows(req, res) {
  const { accessToken } = await auth0.getAccessToken(req, res, {
    scopes: ["read:shows"],
  })
  // ...
}
```

--------------------------------

### Update handleCallback Options in Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

This snippet illustrates the update for the `handleCallback` function in nextjs-auth0. The callback option `onUserLoaded` has been renamed to `afterCallback`. This change affects how user data is processed after authentication.

```javascript
// pages/api/callback.js
import auth0 from "../../utils/auth0"

export default async function callback(req, res) {
  try {
    await auth0.handleCallback(req, res, {
      async afterCallback(req, res, session, state) {
        return session
      },
    })
  } catch (error) {
    console.error(error)
    res.status(error.status || 500).end(error.message)
  }
}
```

--------------------------------

### Persist All ID Token Claims with beforeSessionSaved Hook

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

An alternative implementation of the beforeSessionSaved hook where the entire session object, including all ID token claims, is returned. Be mindful that this can increase cookie size. It's recommended to only persist necessary claims.

```ts
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  async beforeSessionSaved(session, idToken) {
    return session;
  }
});
```

--------------------------------

### Configure Transaction Cookie Max Age (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Customize the expiration time for transaction cookies by setting the `maxAge` property within `transactionCookie` options when initializing Auth0Client. This controls how long state is maintained during authentication flows.

```typescript
export const auth0 = new Auth0Client({
  transactionCookie: {
    maxAge: 1800, // 30 minutes (in seconds)
    // ... other options
  },
}

```

--------------------------------

### Get Access Token (Server-Side)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Shows how to retrieve an access token on the server-side using the Auth0Client. This method can be used within middleware, getServerSideProps, and API routes in the Pages Router. It accepts optional refresh options.

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Auth0Client } from '@auth0/nextjs-auth0';

const auth0Client = new Auth0Client({ /* options */ });

async function handler(req: NextRequest, res: NextResponse) {
  const accessToken = await auth0Client.getAccessToken(req, res, { refresh: true });
  // Use the accessToken
  return new NextResponse(JSON.stringify(accessToken));
}
```

--------------------------------

### Protect Server Component with `withPageAuthRequired` (Next.js App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This code shows how to protect a Server Component in the Next.js App Router using `auth0.withPageAuthRequired()`. Similar to the Pages Router, unauthenticated users will be redirected to the login page. A `returnTo` option is necessary as Server Components are not inherently aware of the page's URL. User session data is then fetched using `auth0.getSession()`.

```jsx
// app/profile/page.js
import { auth0 } from "@/lib/auth0";

export default auth0.withPageAuthRequired(
  async function Profile() {
    const { user } = await auth0.getSession();
    return <div>Hello {user.name}</div>;
  },
  { returnTo: "/profile" }
);
// You need to provide a `returnTo` since Server Components aren't aware of the page's URL

```

--------------------------------

### Get Cookie Prefix - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

Returns the configured prefix for transaction cookies. This utility method is helpful for understanding how transaction cookies are named and for manual cookie management or debugging purposes.

```typescript
getCookiePrefix(): string
```

--------------------------------

### Update User Session in Next.js Middleware (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to use the `updateSession` helper in Next.js middleware to add custom data to the user's session. This function requires the `request`, `response`, and `session` objects as parameters to ensure session updates are persisted correctly within the same request lifecycle.

```typescript
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "@/lib/auth0";

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  await auth0.updateSession(request, authRes, {
    ...session,
    user: {
      ...session.user,
      // add custom user data
      updatedAt: Date.now()
    }
  });

  // the headers from the auth middleware should always be returned
  return authRes;
}
```

--------------------------------

### Accessing Authenticated User on Client (Next.js)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet demonstrates how to access the currently authenticated user's data on the client-side in a Next.js application using the `useUser()` hook. It handles loading states and displays user information. The hook utilizes SWR for efficient data caching and revalidation.

```tsx
"use client";

import { useUser } from "@auth0/nextjs-auth0";

export default function Profile() {
  const { user, isLoading, error } = useUser();

  if (isLoading) return <div>Loading...</div>;

  return (
    <main>
      <h1>Profile</h1>
      <div>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>
    </main>
  );
}

```

--------------------------------

### Configure Default Audience for Multi-Resource Refresh Tokens

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This code snippet illustrates how to configure a default audience when initializing the `Auth0Client` in your Next.js application. This is crucial for enabling Multi-Resource Refresh Tokens (MRRT), allowing a single refresh token to obtain access tokens for multiple audiences.

```typescript
// lib/auth0.ts
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client({
  authorizationParameters: {
    audience: "https://api.example.com", // Your default audience
    scope: "openid profile email offline_access read:products read:orders"
  }
});
```

--------------------------------

### Get Session Data (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves the session data for the current request. This function is designed for use in Server Components, Server Actions, and Route Handlers within the App Router.

```typescript
import { getSession } from "@auth0/nextjs-auth0";

// ... inside an async function or handler
const session = await getSession();

```

--------------------------------

### Configure Parallel Transactions (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionStoreOptions.html

Example demonstrating the `enableParallelTransactions` option within `TransactionStoreOptions`. Setting this to `true` (default) allows multiple concurrent login transactions, useful for multi-tab support. Setting it to `false` enforces a single transaction at a time.

```typescript
interface TransactionStoreOptions {
    secret: string;
    enableParallelTransactions?: boolean;
}
```

--------------------------------

### AuthClient Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Initializes a new instance of the AuthClient class with the provided options.

```APIDOC
## AuthClient Constructor

### Description
Initializes a new instance of the AuthClient class.

### Method
constructor

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
*   **options** (AuthClientOptions) - Required - Configuration options for the AuthClient.

### Request Example
```json
{
  "options": { ... } 
}
```

### Response
#### Success Response (200)
*   **AuthClient** - An instance of the AuthClient class.

#### Response Example
```json
{
  "instance": "AuthClient instance"
}
```
```

--------------------------------

### Propagate Headers in Next.js Middleware for API Routes/getServerSideProps (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This code snippet illustrates how to propagate headers from middleware to subsequent server-side operations like API routes or `getServerSideProps` in a Next.js application. By combining headers using `NextResponse.next`, it prevents redundant token refreshes when `getAccessToken` is called in both middleware and other server contexts. This ensures consistent access token management. Dependencies include `next/server` and `@auth0/nextjs-auth0`.

```typescript
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  const accessToken = await auth0.getAccessToken(request, authRes);

  // create a new response with the updated request headers
  const resWithCombinedHeaders = NextResponse.next({
    request: {
      headers: request.headers
    }
  });

  // set the response headers (set-cookie) from the auth response
  authRes.headers.forEach((value, key) => {
    resWithCombinedHeaders.headers.set(key, value);
  });

  // the headers from the auth middleware should always be returned
  return resWithCombinedHeaders;
}
```

--------------------------------

### Initialize Theme and Display Settings (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelLogoutError.html

This JavaScript code snippet initializes the theme preference based on local storage and hides the body content temporarily. It then uses `setTimeout` to either show a specific page if `window.app` exists or remove the display style from the body, ensuring a smooth initial page load experience.

```javascript
document.documentElement.dataset.theme = localStorage.getItem("tsd-theme") || "os";
document.body.style.display="none";
setTimeout(() => window.app?app.showPage():document.body.style.removeProperty("display"),500)
```

--------------------------------

### Protect API Route (App Router) with Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Secures an API route using `auth0.withApiAuthRequired` for the App Router. Similar to the Page Router, requests without a valid session cookie will fail with a `401`. It uses `NextResponse` for handling responses.

```js
import { auth0 } from "@/lib/auth0";
import { NextResponse } from "next/server";

export const GET = auth0.withApiAuthRequired(async function myApiRoute(req) {
  const res = new NextResponse();
  const { user } = await auth0.getSession(req);
  return NextResponse.json({ protected: "My Secret", id: user.sub }, res);
});

```

--------------------------------

### Handling Response in afterCallback (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

This snippet illustrates how the `afterCallback` function can now directly interact with the response object. It demonstrates terminating the request with a 401 status or setting a redirect header, preventing the previous `ERR_HTTP_HEADERS_SENT` errors.

```javascript
const afterCallback = (req, res, session, state) => {
  if (session.user.isAdmin) {
    return session;
  } else {
    res.status(401).end('User is not admin');
  }
}; // Terminates the request with 401 if user is not admin

const afterCallback = (req, res, session, state) => {
  if (!session.user.isAdmin) {
    res.setHeader('Location', '/admin');
  }
  return session;
}; // Redirects to `/admin` if user is admin
```

--------------------------------

### SDK Routes

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

Overview of the 6 routes mounted by the nextjs-auth0 SDK, including their purpose and configuration options.

```APIDOC
## SDK Routes

### Description
The SDK mounts six core authentication-related routes.

### Mounted Routes
1.  `/auth/login`: Initiates the user authentication flow.
2.  `/auth/logout`: Must be added to your Auth0 application's Allowed Logout URLs.
3.  `/auth/callback`: Must be added to your Auth0 application's Allowed Callback URLs.
4.  `/auth/profile`: Returns user session attributes.
5.  `/auth/access-token`: Returns an access token (automatically refreshed if a refresh token is available). Enabled by default.
6.  `/auth/backchannel-logout`: Receives `logout_token` for back-channel logout events.

### Access Token Endpoint

The `/auth/access-token` route is enabled by default but is only necessary if the access token is needed on the client-side. It can be disabled by setting `enableAccessTokenEndpoint` to `false`.
```

--------------------------------

### Configure Parallel Transactions in Auth0Client V4

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This snippet illustrates the default and custom configuration for parallel transaction handling in Auth0Client V4. By default, `enableParallelTransactions` is true, allowing multiple login flows concurrently. Setting it to false enforces a single-transaction mode.

```typescript
export const auth0 = new Auth0Client({
  // enableParallelTransactions: true, // true by default
  //  ... other options
});
```

```typescript
export const auth0 = new Auth0Client({
  enableParallelTransactions: false, // Single-transaction mode
  // ... other options
});
```

--------------------------------

### TypeScript - AbstractSessionStore Methods

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

Provides essential methods for session management within the AbstractSessionStore. These include calculating maximum age for session cookies, deleting session data, retrieving the current epoch time, and getting session data based on request cookies.

```typescript
calculateMaxAge(createdAt: number): number
```

```typescript
delete(
    reqCookies: RequestCookies | ReadonlyRequestCookies,
    resCookies: ResponseCookies
): Promise<void>
```

```typescript
epoch(): number
```

```typescript
get(
    reqCookies: RequestCookies | ReadonlyRequestCookies
): Promise<null | SessionData>
```

--------------------------------

### Implement Custom Unauthorized Handler with handleAuth

Source: https://github.com/auth0/nextjs-auth0/blob/main/V3_MIGRATION_GUIDE.md

Shows how to implement a custom unauthorized response handler using `handleAuth` from `@auth0/nextjs-auth0`. This is necessary when the default '/401' handler is removed (e.g., in Next.js 13.1 and later) and you need to protect API routes with `withMiddlewareAuthRequired`.

```typescript
import { handleAuth } from "@auth0/nextjs-auth0"

export default handleAuth({
  "401"(_req, res) {
    res.status(401).json({
      error: "not_authenticated",
      description:
        "The user does not have an active session or is not authenticated",
    })
  },
})
```

--------------------------------

### Next.js Protected Page with getServerSideProps | JavaScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredPageRouterOptions.html

Example demonstrating how to create a protected page in Next.js using `auth0.withPageAuthRequired`. This snippet shows how to define `getServerSideProps` to optionally access user session data and merge custom props.

```javascript
import { auth0 } from "@/lib/auth0";

export default function ProtectedPage({ user, customProp }) {
  return <div>Protected content</div>;
}

export const getServerSideProps = auth0.withPageAuthRequired({
  // returnTo: '/unauthorized',
  async getServerSideProps(ctx) {
    // access the user session if needed
    // const session = await auth0.getSession(ctx.req);
    return {
      props: {
        // customProp: 'bar',
      }
    };
  }
});
```

--------------------------------

### Base Path Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

How to configure the SDK to recognize a base path set in Next.js, ensuring authentication routes are mounted correctly.

```APIDOC
## Base Path Configuration

### Description

When your Next.js application is configured with a base path (e.g., `/dashboard`) in `next.config.js`, you must also configure the SDK to use this base path. This ensures that authentication routes are mounted under the correct path.

### Configuration

Set the `NEXT_PUBLIC_BASE_PATH` environment variable to match your Next.js application's base path.

### Example

If `NEXT_PUBLIC_BASE_PATH` is set to `/dashboard`, authentication routes will be mounted as follows:
- `/dashboard/auth/login`
- `/dashboard/auth/callback`
- `/dashboard/auth/profile`

### Recommendation

> [!NOTE]
> It is not recommended to use the `NEXT_PUBLIC_BASE_PATH` environment variable in conjunction with an `APP_BASE_URL` that already contains a path component. If your application uses a base path, set `APP_BASE_URL` to the root URL (e.g., `https://example.com`) and use `NEXT_PUBLIC_BASE_PATH` for the path (e.g., `/dashboard`).
```

--------------------------------

### Protect API Route (Page Router) with Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Secures an API route using `auth0.withApiAuthRequired` for the Page Router. Requests without a valid session cookie will result in a `401` Unauthorized response. The user's session information is then available within the route handler.

```js
import { auth0 } from "@/lib/auth0";

export default auth0.withApiAuthRequired(async function myApiRoute(req, res) {
  const { user } = await auth0.getSession(req);
  res.json({ protected: "My Secret", id: user.sub });
});

```

--------------------------------

### Propagate Session Updates in Next.js Middleware (Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Illustrates how to ensure session updates made in middleware are propagated to the request object for use within the same request in the Pages Router. This involves creating a new `NextResponse` with combined headers, including those from the authentication middleware, to make the updated session accessible.

```typescript
import { NextRequest, NextResponse } from "next/server";

import { auth0 } from "@/lib/auth0";

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession(request);

  if (!session) {
    // user is not authenticated, redirect to login page
    return NextResponse.redirect(
      new URL("/auth/login", request.nextUrl.origin)
    );
  }

  await auth0.updateSession(request, authRes, {
    ...session,
    user: {
      ...session.user,
      // add custom user data
      updatedAt: Date.now()
    }
  });

  // create a new response with the updated request headers
  const resWithCombinedHeaders = NextResponse.next({
    request: {
      headers: request.headers
    }
  });

  // set the response headers (set-cookie) from the auth response
  authRes.headers.forEach((value, key) => {
    resWithCombinedHeaders.headers.set(key, value);
  });

  // the headers from the auth middleware should always be returned
  return resWithCombinedHeaders;
}
```

--------------------------------

### Force Access Token Refresh in App Router (Server Components)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet demonstrates how to force a refresh of the access token in Next.js App Router using `getAccessToken` with the `refresh: true` option. It's applicable for Server Components, Route Handlers, and Server Actions. It requires the `auth0` instance to be imported from a local configuration.

```typescript
// app/api/my-api/route.ts
import { auth0 } from "@/lib/auth0";

export async function GET() {
  try {
    // Force a refresh of the access token
    const { token, expiresAt } = await auth0.getAccessToken({ refresh: true });

    // Use the refreshed token
    // ...
  } catch (error) {
    console.error("Error getting access token:", error);
    return Response.json(
      { error: "Failed to get access token" },
      { status: 500 }
    );
  }
}
```

--------------------------------

### Get Transaction State - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

Retrieves the transaction state from encrypted cookies. It takes the request cookies object and a state identifier as input. This method is vital for restoring authentication context during multi-step authentication flows.

```typescript
get(
    reqCookies: RequestCookies,
    state: string,
): Promise<null | JWTDecryptResult<TransactionState>>
```

--------------------------------

### Update User Session on Server (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

Demonstrates how to update the current user's session on the server within the App Router using the `auth0.updateSession()` helper. This function modifies the session object with new properties, such as an updated timestamp. Note that this is not usable in Server Components.

```tsx
import { NextResponse } from "next/server";

import { auth0 } from "@/lib/auth0";

export async function GET() {
  const session = await auth0.getSession();

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  await auth0.updateSession({
    ...session,
    updatedAt: Date.now()
  });

  return NextResponse.json(null, { status: 200 });
}

```

--------------------------------

### SDK Configuration Options

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Details on optional configuration parameters for the Auth0 client, such as HTTP timeout and telemetry settings.

```APIDOC
## SDK Configuration Options

### Description

These options can be passed during the initialization of the `Auth0Client` or set via environment variables to customize SDK behavior.

### Parameters

#### Client Configuration Options

- **httpTimeout** (`number`) - Optional - Integer value for the HTTP timeout in milliseconds for authentication requests. Defaults to `5000` milliseconds.
- **enableTelemetry** (`boolean`) - Optional - Boolean value to opt-out of sending the library name and version to your authorization server via the `Auth0-Client` header. Defaults to `true`.

### Configuration Source

Configuration can be provided via:
1. **Constructor Options**: Directly passing an options object when creating `Auth0Client`.
2. **Environment Variables**: Using specific environment variables (e.g., `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`).

Refer to the SDK's documentation for a complete list of environment variables and their corresponding constructor options.
```

--------------------------------

### Update getSession to include Response Object (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V1_MIGRATION_GUIDE.md

Shows the change in the `getSession` function signature in @auth0/nextjs-auth0 v1.x. The `getSession` function now requires both the request (`req`) and response (`res`) objects as arguments to ensure any session updates are persisted correctly. This is a mandatory change for session management in the new version.

```javascript
// pages/api/shows.js
import auth0 from "../../lib/auth0"

export default function shows(req, res) {
  const session = auth0.getSession(req, res) // Note: the extra argument
  // ...
}
```

--------------------------------

### Add Type Annotations for Request/Response in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/V3_MIGRATION_GUIDE.md

Demonstrates how to add explicit type annotations for `NextApiRequest` and `NextApiResponse` when using `withApiAuthRequired` in TypeScript. This helps TypeScript infer types correctly, especially after SDK updates that support the App Router.

```typescript
import { NextApiRequest, NextApiResponse } from "next"
import { withApiAuthRequired } from "@auth0/nextjs-auth0"

export default withApiAuthRequired(async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  res.status(200).json({})
})
```

--------------------------------

### Configuration Validation

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Details on the mandatory configuration options the SDK validates during initialization.

```APIDOC
## Configuration Validation

### Description

The Auth0 SDK performs validation to ensure all required configuration options are provided upon initializing the `Auth0Client`. Missing options will result in warnings.

### Mandatory Options

The following options are mandatory and must be provided either via constructor arguments or environment variables:

- `domain` (or `AUTH0_DOMAIN` environment variable)
- `clientId` (or `AUTH0_CLIENT_ID` environment variable)
- `appBaseUrl` (or `APP_BASE_URL` environment variable)
- `secret` (or `AUTH0_SECRET` environment variable)
- Either:
    - `clientSecret` (or `AUTH0_CLIENT_SECRET` environment variable)
    - OR `clientAssertionSigningKey` (or `AUTH0_CLIENT_ASSERTION_SIGNING_KEY` environment variable)

### Validation Outcome

If any required options are missing, the SDK will issue a warning detailing the missing options and guidance on how to provide them.
```

--------------------------------

### AbstractSessionStore Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

Initializes a new instance of the AbstractSessionStore class. This constructor takes session store options as named parameters.

```APIDOC
## Constructor AbstractSessionStore

### Description
Initializes a new instance of the AbstractSessionStore class.

### Method
CONSTRUCTOR

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
*   **__namedParameters** (SessionStoreOptions) - Required - Options for configuring the session store.

### Request Example
```json
{
  "secret": "your_secret_key",
  "sessionCookieName": "app-session",
  "cookieConfig": {
    "secure": true,
    "httpOnly": true,
    "sameSite": "lax",
    "path": "/"
  },
  "store": { /* implementation of SessionDataStore */ }
}
```

### Response
#### Success Response (200)
This constructor does not return a value directly, it initializes the class instance.

#### Response Example
None
```

--------------------------------

### Protect Next.js Pages with WithPageAuthRequired (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequired.html

The WithPageAuthRequired type alias protects Next.js pages, supporting both Page Router and App Router configurations. It is defined in the server helpers of the @auth0/nextjs-auth0 library. Ensure you have the library installed as a dependency.

```typescript
/**
 * Protects Page router pages [WithPageAuthRequiredPageRouter](server.WithPageAuthRequiredPageRouter.html) or App router pages [WithPageAuthRequiredAppRouter](server.WithPageAuthRequiredAppRouter.html)
 */
export type WithPageAuthRequired<T extends NextPageContext | AppRouterContext = NextPageContext | AppRouterContext> = T extends NextPageContext
    ? WithPageAuthRequiredPageRouter<T>
    : T extends AppRouterContext
        ? WithPageAuthRequiredAppRouter<T>
        : never;
```

--------------------------------

### Intercept Auth Routes with Middleware in Next.js

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This snippet demonstrates how to use Next.js middleware to intercept authentication routes handled by nextjs-auth0. It allows custom logic to be executed before the default auth handlers, such as logging or setting additional cookies during logout.

```typescript
import type { NextRequest } from 'next/server';
import { auth0 } from './lib/auth0';

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request);
  
  // Intercept specific auth routes
  if (request.nextUrl.pathname === '/auth/logout') {
    // Custom logout logic runs BEFORE the actual logout
    console.log('User is logging out');
    
    // Example: Set custom cookies
    authRes.cookies.set('logoutTime', new Date().toISOString());
  }
  
  if (request.nextUrl.pathname === '/auth/login') {
    // Custom login logic runs BEFORE the actual login
    console.log('User is attempting to login');
  }
  
  return authRes;
}
```

--------------------------------

### Create Auth0 Client Instance (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Initializes an Auth0Client instance for server-side authentication. This client will be imported and used throughout the application to access authentication methods. It uses safe defaults for managing authentication cookies.

```typescript
import { Auth0Client } from "@auth0/nextjs-auth0/server";

export const auth0 = new Auth0Client();
```

--------------------------------

### Next.js Middleware for Route Protection

Source: https://github.com/auth0/nextjs-auth0/blob/main/V4_MIGRATION_GUIDE.md

This TypeScript code demonstrates how to implement middleware in Next.js to protect routes by checking for user sessions. It allows access to public routes and redirects unauthenticated users to the login page. It handles Auth0 specific routes and ensures protected routes require authentication.

```typescript
export async function middleware(request) {
    const authRes = await auth0.middleware(request); // Returns a NextResponse object

    // Ensure your own middleware does not handle the `/auth` routes, auto-mounted and handled by the SDK
    if (request.nextUrl.pathname.startsWith("/auth")) {
      return authRes;
    }

    // Allow access to public routes without requiring a session
    if (request.nextUrl.pathname === ("/")) {
      return authRes;
    }

    // Any route that gets to this point will be considered a protected route, and require the user to be logged-in to be able to access it
    const { origin } = new URL(request.url)
    const session = await auth0.getSession(request)

    // If the user does not have a session, redirect to login
    if (!session) {
      return NextResponse.redirect(`${origin}/auth/login`)
    }

    // If a valid session exists, continue with the response from Auth0 middleware
    // You can also add custom logic here...
    return authRes
}
```

--------------------------------

### Get Token Set in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Retrieves OAuth token sets, with an option to force a refresh. This function handles token expiration and retrieval, returning a promise that resolves to a tuple containing either an SDK error or the token set information.

```typescript
async getTokenSet(
    tokenSet: TokenSet,
    forceRefresh?: boolean
): Promise<[SdkError, null] | [null, GetTokenSetResponse]> {
    // Implementation details for retrieving token set
}
```

--------------------------------

### Get Access Token for Connection (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves an access token for a connection. This method is suitable for Server Components, Server Actions, and Route Handlers in the App Router. Note that Server Components cannot set cookies, so the token may not persist.

```typescript
import { getAccessTokenForConnection } from "@auth0/nextjs-auth0";

// ... inside an async function or handler
const session = await getAccessTokenForConnection(options);

```

--------------------------------

### Force Access Token Refresh in Pages Router (getServerSideProps, API Routes)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet shows how to force an access token refresh in the Next.js Pages Router when using `getServerSideProps` or API Routes. It utilizes the `getAccessToken` function from `@auth0/nextjs-auth0` and requires passing request and response objects along with the options object `{ refresh: true }`.

```typescript
// pages/api/my-pages-api.ts
import type { NextApiRequest, NextApiResponse } from "next";
import { getAccessToken, withApiAuthRequired } from "@auth0/nextjs-auth0";

export default withApiAuthRequired(async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Force a refresh of the access token
    const { token, expiresAt } = await getAccessToken(req, res, {
      refresh: true
    });

    // Use the refreshed token
    // ...
  } catch (error: any) {
    console.error("Error getting access token:", error);
    res.status(error.status || 500).json({ error: error.message });
  }
});
```

--------------------------------

### Augment Server-Side Props with User Data (Next.js/Auth0)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.GetServerSidePropsResultWithSession.html

This example demonstrates how to use `auth0.withPageAuthRequired()` to wrap your `getServerSideProps` function. This augmentation automatically adds the authenticated user's information to the props object, making it available to your page component. This requires the `@auth0/nextjs-auth0` library.

```javascript
import { auth0 } from "@/lib/auth0";

export default function Profile({ user }) {
  return <div>Hello {user.name}</div>;
}

export const getServerSideProps = auth0.withPageAuthRequired();
```

--------------------------------

### Get Access Token (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/client.getAccessToken.html

The getAccessToken function retrieves an access token, typically used for authenticating with external APIs. It returns a Promise that resolves to a string representing the access token. This function is defined in src/client/helpers/get-access-token.ts.

```typescript
getAccessToken(): Promise<string>
```

--------------------------------

### Intercept Auth Handlers for Custom Logic (Next.js)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This TypeScript snippet shows how to intercept Auth0's default authentication handlers (like logout) in Next.js middleware to execute custom logic. It checks the pathname and allows for actions such as setting or deleting cookies before the Auth0 response is returned.

```ts
export async function middleware(request) {
  // prepare NextResponse object from auth0 middleware
  const authRes = await auth0.middleware(request);

  // The following interceptUrls can be used:
  //    "/auth/login" : intercept login auth handler
  //    "/auth/logout" : intercept logout auth handler
  //    "/auth/callback" : intercept callback auth handler
  //    "/your/login/returnTo/url" : intercept redirect after login, this is the login returnTo url
  //    "/your/logout/returnTo/url" : intercept redirect after logout, this is the logout returnTo url

  const interceptUrl = "/auth/logout";

  // intercept auth handler
  if (request.nextUrl.pathname === interceptUrl) {
    // do custom stuff
    console.log("Pre-logout code");

    // Example: Set a cookie
    authRes.cookies.set("myCustomCookie", "cookieValue", { path: "/" });
    // Example: Set another cookie with options
    authRes.cookies.set({
      name: "anotherCookie",
      value: "anotherValue",
      httpOnly: true,
      path: "/"
    });

    // Example: Delete a cookie
    // authRes.cookies.delete('cookieNameToDelete');

    // you can also do an early return here with your own NextResponse object
    // return NextResponse.redirect(new URL('/custom-logout-page'));
  }

  // return the original auth0-handled NextResponse object
  return authRes;
}
```

--------------------------------

### AbstractSessionStore Methods

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

Documentation for the methods provided by the AbstractSessionStore class for managing session data.

```APIDOC
## AbstractSessionStore Methods

### calculateMaxAge

#### Description
Calculates the maximum age of the session based on its creation time and configured durations (rolling and absolute).

#### Method
`calculateMaxAge`

#### Parameters
*   **createdAt** (number) - The timestamp when the session was created.

#### Returns
*   **number** - The calculated maximum age of the session in seconds.

### delete

#### Description
Deletes the current session.

#### Method
`delete`

#### Parameters
*   **reqCookies** (RequestCookies | ReadonlyRequestCookies) - The request cookies object.
*   **resCookies** (ResponseCookies) - The response cookies object to set the deletion headers.

#### Returns
*   **Promise<void>** - A promise that resolves when the session is deleted.

### epoch

#### Description
Returns the current time in seconds since the Unix epoch.

#### Method
`epoch`

#### Returns
*   **number** - The current time in seconds since the Unix epoch.

### get

#### Description
Retrieves session data from the store.

#### Method
`get`

#### Parameters
*   **reqCookies** (RequestCookies | ReadonlyRequestCookies) - The request cookies object containing the session ID.

#### Returns
*   **Promise<null | SessionData>** - A promise that resolves with the session data if found, otherwise null.
```

--------------------------------

### Check Authentication Status in getServerSideProps (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

This code snippet demonstrates how to check the user's authentication status within `getServerSideProps` using the `getSession` function. It differentiates between authenticated and unauthenticated user states, allowing for conditional logic.

```javascript
export const getServerSideProps = async (ctx) => {
  const session = await getSession(ctx.req, ctx.res)
  if (session) {
    // User is authenticated
  } else {
    // User is not authenticated
  }
}
```

--------------------------------

### Use updateSession to modify session data (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/V2_MIGRATION_GUIDE.md

In v2.x, session modifications are no longer implicit. You must now explicitly use the `updateSession` function to serialize and update the session cookie. This provides more control and clarity over session persistence.

```javascript
// /pages/api/update-user
import { getSession, updateSession } from "@auth0/nextjs-auth0"

async function myApiRoute(req, res) {
  const session = await getSession(req, res)
  // The session is updated, serialized and the cookie is updated
  // everytime you call `updateSession`.
  await updateSession(req, res, {
    ...session,
    user: { ...session.user, foo: "bar" },
  })
  res.json({ success: true })
}
```

--------------------------------

### Implement Auth0 Authentication Middleware (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Sets up Next.js middleware to handle authentication requests using the Auth0 SDK. It matches all paths except for static files and metadata files, ensuring session management and security features are applied broadly. The middleware relies on the auth0 client instance created previously.

```typescript
import type { NextRequest } from "next/server";

import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  return await auth0.middleware(request);
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)"
  ]
};
```

--------------------------------

### Configure Webpack to Ignore Navigation/Headers Modules in Next.js 12

Source: https://github.com/auth0/nextjs-auth0/blob/main/V3_MIGRATION_GUIDE.md

Provides a Webpack configuration snippet for Next.js 12 projects to ignore the `next/navigation` and `next/headers` modules. This is required when using v3 of the SDK with middleware in Next.js 12, as these modules are not available in that version and can cause resolution errors.

```javascript
const webpack = require("webpack")

/** @type {import('next').NextConfig} */
module.exports = {
  webpack(config) {
    config.plugins.push(
      new webpack.IgnorePlugin({
        resourceRegExp: /^next\/(navigation|headers)$/,
      })
    )
    return config
  },
}
```

--------------------------------

### Protect SSR Page with `withPageAuthRequired` (Next.js Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md

This snippet demonstrates how to protect a Server-Side Rendered (SSR) page in the Next.js Pages Router using `auth0.withPageAuthRequired()`. Requests to the protected page without a valid session cookie will automatically redirect the user to the login page. You can optionally merge custom `getServerSideProps` with the user props.

```jsx
// pages/profile.js
import { auth0 } from "@/lib/auth0";

export default function Profile({ user }) {
  return <div>Hello {user.name}</div>;
}

// You can optionally pass your own `getServerSideProps` function into
// `withPageAuthRequired` and the props will be merged with the `user` prop
export const getServerSideProps = auth0.withPageAuthRequired();

```

--------------------------------

### Get Connection Token Set in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Exchanges a refresh token for an access token for a specific connection. It validates the presence of the refresh token and performs a token exchange request to the authorization server. This function returns a promise that resolves to a tuple indicating success or failure.

```typescript
async getConnectionTokenSet(
    tokenSet: TokenSet,
    connectionTokenSet: undefined | ConnectionTokenSet,
    options: AccessTokenForConnectionOptions
): Promise<
    [AccessTokenForConnectionError, null]
    | [null, ConnectionTokenSet]
> {
    // Implementation details for token exchange
}
```

--------------------------------

### Initialize AuthClient Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Initializes a new AuthClient instance with provided options. This is the entry point for most authentication operations within the library.

```typescript
new AuthClient(options: AuthClientOptions): AuthClient
```

--------------------------------

### SessionDataStore Interface Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

Defines the structure for storing and retrieving session data. It includes methods for deleting, getting, and setting session information, identified by a session ID. The 'deleteByLogoutToken' method provides an alternative deletion mechanism using a logout token.

```typescript
interface SessionDataStore {
    [delete](id: string): Promise<void>;
    [deleteByLogoutToken]?(logoutToken: LogoutToken): Promise<void>;
    [get](id: string): Promise<null | SessionData>;
    [set](id: string, session: SessionData): Promise<void>;
}
```

--------------------------------

### Auth0Provider

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/modules/client.html

The Auth0Provider component is a React Context Provider that makes authentication methods available to your entire application. It should wrap your entire application.

```APIDOC
## Auth0Provider

### Description
Provides authentication methods and context to the entire Next.js application.

### Method
Component

### Endpoint
N/A (Component Wrapper)

### Parameters
#### Props
- **domain** (string) - Required - Your Auth0 domain.
- **clientId** (string) - Required - Your Auth0 application's client ID.
- **redirectUri** (string) - Optional - The URI to redirect to after authentication.

### Request Example
```jsx
import { Auth0Provider } from '@auth0/nextjs-auth0';

function MyApp({ Component, pageProps }) {
  return (
    <Auth0Provider
      domain="YOUR_AUTH0_DOMAIN"
      clientId="YOUR_AUTH0_CLIENT_ID"
      redirectUri={window.location.origin}
    >
      <Component {...pageProps} />
    </Auth0Provider>
  );
}

export default MyApp;
```

### Response
N/A (Provides context and methods)
```

--------------------------------

### SdkError Class Documentation

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.SdkError.html

Documentation for the base SdkError class, including its constructor and properties, as well as its inheritance hierarchy.

```APIDOC
## SdkError Class

### Description

The base `SdkError` class provides a standardized way to handle errors within the Auth0 NextJS SDK. It extends the built-in JavaScript `Error` class and includes a `code` property for specific error codes.

### Hierarchy

*   `Error`
    *   `SdkError`
        *   `OAuth2Error`
        *   `DiscoveryError`
        *   `MissingStateError`
        *   `InvalidStateError`
        *   `AuthorizationError`
        *   `AuthorizationCodeGrantRequestError`
        *   `AuthorizationCodeGrantError`
        *   `BackchannelLogoutError`
        *   `BackchannelAuthenticationNotSupportedError`
        *   `BackchannelAuthenticationError`
        *   `AccessTokenError`
        *   `AccessTokenForConnectionError`

### Constructors

#### `constructor(message?: string)`

*   **Description**: Creates an instance of `SdkError`.
*   **Parameters**:
    *   `message` (string) - Optional. The error message.
*   **Returns**: `SdkError`

### Properties

#### `code` (string)

*   **Description**: A string representing the specific error code.
*   **Visibility**: Protected
*   **Inherited**: No
*   **Defined in**: `src/errors/index.ts:2`
```

--------------------------------

### Configure Auth0 Environment Variables

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Sets up necessary environment variables for Auth0 authentication in a .env.local file. These include domain, client ID, client secret, session secret, and base URL. The AUTH0_SECRET can be generated using openssl rand -hex 32.

```env
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_SECRET=
APP_BASE_URL=
```

--------------------------------

### Base Path Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

Configure the SDK to use a base path for authentication routes in your Next.js application.

```APIDOC
## Base Path Configuration

### Description
Configure the SDK to respect a base path set in your Next.js application's `next.config.js` file.

### Configuration
Set the `NEXT_PUBLIC_BASE_PATH` environment variable to match the `basePath` option in `next.config.js`.

### Example
If `NEXT_PUBLIC_BASE_PATH` is set to `/dashboard`, authentication routes will be mounted on paths like `/dashboard/auth/login`, `/dashboard/auth/callback`, etc.

### Recommendation
Avoid using `NEXT_PUBLIC_BASE_PATH` with an `APP_BASE_URL` that includes a path component. Set `APP_BASE_URL` to the root URL and use `NEXT_PUBLIC_BASE_PATH` for the application's base path.
```

--------------------------------

### Customizing Auth Handlers

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Information on how to customize the authentication flow using middleware interception and the `onCallback` hook.

```APIDOC
## Customizing Auth Handlers

### Description

This section outlines methods for customizing the default authentication flow handled by the middleware, allowing for custom logic before or after authentication.

### Approaches

1.  **Run custom code before auth handlers**: Intercept auth routes in your middleware to add custom logic before authentication actions.
2.  **Run code after authentication**: Use the `onCallback` hook to add custom logic after authentication completes.

### Additional Customization Options

-   Login parameters via query parameters or static configuration.
-   Session data modification using the `beforeSessionSaved` hook.
-   Logout redirects using query parameters.

### Security Recommendations

> [!IMPORTANT]
> When customizing auth handlers, always validate user inputs (especially redirect URLs) to prevent security vulnerabilities like open redirects. Use relative URLs when possible and implement proper input sanitization.

### Examples

For detailed examples and step-by-step migration patterns from v3, see the [Customizing Auth Handlers](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md#customizing-auth-handlers) guide.
```

--------------------------------

### handleLogin API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Handles the login process for users. It typically redirects the user to the authentication provider and handles the callback.

```APIDOC
## POST /api/auth/login

### Description
Handles the initiation of the user login process. This endpoint is responsible for redirecting the user to the authentication provider and managing the subsequent callback.

### Method
POST

### Endpoint
/api/auth/login

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
```json
{
  "req": "<NextRequest Object>"
}
```

### Response
#### Success Response (200)
- **NextResponse** (object) - A NextResponse object representing the result of the login process.

#### Response Example
```json
{
  "response": "<NextResponse Object>"
}
```
```

--------------------------------

### Customizing Auth Handlers

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

Learn how to customize the authentication flow in nextjs-auth0 by running custom code before or after authentication handlers, and explore additional customization options.

```APIDOC
## Customizing Auth Handlers

### Description
Allows customization of the authentication flow by running custom code before auth handlers or using the `onCallback` hook after authentication.

### Approaches
1.  **Run custom code before auth handlers**: Intercept auth routes in your middleware to add custom logic before authentication actions.
2.  **Run code after authentication**: Use the `onCallback` hook to add custom logic after authentication completes.

### Additional Customization
*   Login parameters via query parameters or static configuration.
*   Session data modification using the `beforeSessionSaved` hook.
*   Logout redirects using query parameters.

### Security Considerations
Always validate user inputs (especially redirect URLs) to prevent security vulnerabilities like open redirects. Use relative URLs when possible and implement proper input sanitization.

### Further Information
Refer to the [EXAMPLES.md](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md#customizing-auth-handlers) for detailed examples and migration patterns.
```

--------------------------------

### AbstractSessionStore Properties

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

Details about the properties available on an AbstractSessionStore instance, including configuration and session data.

```APIDOC
## AbstractSessionStore Properties

### cookieConfig
*   **cookieConfig** (CookieOptions) - The configuration object for session cookies.

### secret
*   **secret** (string) - The secret key used for encrypting session data.

### sessionCookieName
*   **sessionCookieName** (string) - The name of the cookie used to store the session ID.

### store
*   **store** (SessionDataStore | undefined) - An optional instance of a session data store for persisting session data.
```

--------------------------------

### handleProfile API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Retrieves the user's profile information.

```APIDOC
## GET /api/auth/me

### Description
Retrieves the currently authenticated user's profile information from the authentication provider.

### Method
GET

### Endpoint
/api/auth/me

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
```json
{
  "req": "<NextRequest Object>"
}
```

### Response
#### Success Response (200)
- **UserProfile** (object) - An object containing the user's profile details.

#### Response Example
```json
{
  "user": {
    "sub": "auth0|1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```
```

--------------------------------

### Session Cookie Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Environment variables for configuring the session cookie, including domain, path, and security settings.

```APIDOC
## Session Cookie Configuration

### Description

Configure the session cookie used by the SDK by setting the following environment variables.

### Environment Variables

- `AUTH0_COOKIE_DOMAIN`
- `AUTH0_COOKIE_PATH`
- `AUTH0_COOKIE_TRANSIENT`
- `AUTH0_COOKIE_SECURE`
- `AUTH0_COOKIE_SAME_SITE`

### Details

Respective counterparts are also available in the client configuration. For more details, refer to the [Cookie Configuration](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md#cookie-configuration) documentation.
```

--------------------------------

### Environment Variables for Session Cookie Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

These environment variables allow you to configure the session cookie's domain, path, transient status, security, and same-site policy. Corresponding client configuration options are also available for finer control.

```env
AUTH0_COOKIE_DOMAIN=
AUTH0_COOKIE_PATH=
AUTH0_COOKIE_TRANSIENT=
AUTH0_COOKIE_SECURE=
AUTH0_COOKIE_SAME_SITE=
```

--------------------------------

### startInteractiveLogin

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Initiates an interactive login flow for the user. This method is used to redirect the user to the Auth0 login page to authenticate.

```APIDOC
## startInteractiveLogin

### Description
Initiates an interactive login flow, redirecting the user to the Auth0 login page. This method is commonly used for initiating the authentication process when a user needs to log in.

### Method
GET (typically initiates a redirect)

### Endpoint
/authorize (Auth0 endpoint for login initiation)

### Parameters
#### Path Parameters
None

#### Query Parameters
- **options** (StartInteractiveLoginOptions) - Optional - Configuration options for the interactive login, such as redirect URIs, scope, etc.

#### Request Body
None

### Request Example
```typescript
// Example usage within a Next.js page or API route
import { startInteractiveLogin } from '@auth0/nextjs-auth0';

// ...

const handleLogin = async (req, res) => {
  await startInteractiveLogin(req, res, {
    returnTo: '/profile'
  });
};
```

### Response
#### Success Response (200)
- **NextResponse** - A redirect response to the Auth0 authorization server.

#### Response Example
(This method returns a redirect, so the response is an HTTP redirect)
```
HTTP/1.1 302 Found
Location: https://YOUR_DOMAIN/authorize?client_id=...&redirect_uri=...&response_type=code&scope=openid%20profile%20email&state=...&nonce=...
```
```

--------------------------------

### Add Authentication Middleware in Next.js

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

This code snippet demonstrates how to create a middleware.ts file in your Next.js project to handle authentication using Auth0. It configures the middleware to protect routes and includes a matcher to specify which paths should be protected. Adjust the import path for the auth0 client if necessary.

```typescript
import type { NextRequest } from "next/server";
import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export async function middleware(request: NextRequest) {
  return await auth0.middleware(request);
}

export const config = {
  matcher: [
    /*     * Match all request paths except for the ones starting with:     * - _next/static (static files)     * - _next/image (image optimization files)     * - favicon.ico, sitemap.xml, robots.txt (metadata files)     */
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)"
  ]
};
```

--------------------------------

### startInteractiveLogin API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Initiates an interactive login flow, typically involving redirects to an identity provider.

```APIDOC
## POST /api/auth/login/interactive

### Description
Initiates an interactive login flow, guiding the user through the authentication process with an external identity provider.

### Method
POST

### Endpoint
/api/auth/login/interactive

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **options** (StartInteractiveLoginOptions) - Optional - Configuration options for the interactive login.
  - **appState** (object) - Optional - Custom state to be preserved during the authentication flow.

### Request Example
```json
{
  "options": {
    "appState": {
      "returnTo": "/dashboard"
    }
  }
}
```

### Response
#### Success Response (200)
- **NextResponse** (object) - A NextResponse object initiating the interactive login redirect.

#### Response Example
```json
{
  "response": "<NextResponse Object>"
}
```
```

--------------------------------

### middleware

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Mounts the SDK routes to run as a middleware function. This is typically used in Next.js applications to handle authentication and session management at the middleware level.

```APIDOC
## middleware

### Description
Mounts the SDK routes to run as a middleware function. This function is responsible for handling incoming requests and orchestrating authentication flows, session management, and route protection.

### Method
GET, POST, PUT, DELETE (handles various HTTP methods)

### Endpoint
Customizable based on Next.js configuration.

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
(This is a middleware function, so it intercepts requests. The request object is the standard NextRequest)
```typescript
// Example usage in next.config.js or middleware.ts
import { middleware } from '@auth0/nextjs-auth0/edge';

export default middleware(req, event, context);
```

### Response
#### Success Response (200)
- **NextResponse** - The response object, potentially redirecting or returning content based on authentication status.

#### Response Example
(The response depends on the authentication outcome; it might be a redirect to a login page or a modified request)
```typescript
// Example successful response (e.g., authenticated user proceeds)
// Next response object with appropriate headers and body
```
```

--------------------------------

### StartInteractiveLoginOptions Properties (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.StartInteractiveLoginOptions.html

This section details the properties of the StartInteractiveLoginOptions interface. 'authorizationParameters' allows passing custom parameters to the authorization server, while 'returnTo' specifies the redirect URL after a successful login.

```typescript
authorizationParameters?: [AuthorizationParameters](types.AuthorizationParameters.html)
// Authorization parameters to be passed to the authorization server.
```

```typescript
returnTo?: string
// The URL to redirect to after a successful login.
```

--------------------------------

### AuthClientOptions Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthClientOptions.html

This section details the properties available for configuring the AuthClientOptions. These options are used to set up authentication, authorization, session management, and other related functionalities.

```APIDOC
## AuthClientOptions Interface

### Description

The `AuthClientOptions` interface defines the configuration object used to initialize the Auth0 client in a Next.js application.

### Properties

#### `allowInsecureRequests` (boolean) - Optional

Allows insecure requests (e.g., HTTP instead of HTTPS). Use with caution.

#### `appBaseUrl` (string) - Required

The base URL of your application.

#### `authorizationParameters` (AuthorizationParameters) - Optional

Parameters to be included in the authorization request.

#### `beforeSessionSaved` (BeforeSessionSavedHook) - Optional

A hook that runs before the session is saved.

#### `clientAssertionSigningAlg` (string) - Optional

The signing algorithm to use for client assertions.

#### `clientAssertionSigningKey` (string | CryptoKey) - Optional

The signing key to use for client assertions.

#### `clientId` (string) - Required

The Client ID obtained from your Auth0 application settings.

#### `clientSecret` (string) - Optional

The Client Secret obtained from your Auth0 application settings. Required for certain grant types.

#### `domain` (string) - Required

The domain of your Auth0 tenant (e.g., 'your-tenant.auth0.com').

#### `enableAccessTokenEndpoint` (boolean) - Optional

Enables the use of the access token endpoint for token exchange.

#### `enableTelemetry` (boolean) - Optional

Enables or disables telemetry reporting for the SDK.

#### `fetch` (Function) - Optional

A custom fetch implementation to use for making HTTP requests.

#### `httpTimeout` (number) - Optional

Specifies the timeout in milliseconds for HTTP requests.

#### `includeIdTokenHintInOIDCLogoutUrl` (boolean) - Optional

Includes the `id_token_hint` parameter in OIDC logout URLs.

#### `jwksCache` (JWKSCacheInput) - Optional

Configuration for caching JSON Web Key Sets (JWKS).

#### `logoutStrategy` (LogoutStrategy) - Optional

Defines the strategy to be used for logout.

#### `noContentProfileResponseWhenUnauthenticated` (boolean) - Optional

If true, an unauthenticated user requesting a profile will receive an empty response with a 204 status code instead of an error.

#### `onCallback` (OnCallbackHook) - Optional

A hook that runs after the callback from the authentication provider.

#### `pushedAuthorizationRequests` (boolean) - Optional

Enables the use of Pushed Authorization Requests (PAR).

#### `routes` (Routes) - Required

Configuration for the application's authentication routes (login, logout, callback, etc.).

#### `secret` (string) - Required

A secret string used for encrypting session data. This should be a strong, randomly generated secret.

#### `sessionStore` (AbstractSessionStore) - Required

The session store implementation to use for persisting user sessions.

#### `signInReturnToPath` (string) - Optional

The path to redirect to after a successful sign-in if no other return path is specified.

#### `transactionStore` (TransactionStore) - Required

The transaction store implementation to use for managing authentication transactions.

```

--------------------------------

### Auth0 Next.js SDK Routes

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Routes.html

The Auth0 Next.js SDK provides predefined routes for common authentication flows.

```APIDOC
## Auth0 Next.js SDK Routes

### Description
This section outlines the available routes for authentication operations managed by the Auth0 Next.js SDK.

### Method
N/A (These are string representations of paths, not endpoints to be called directly with a method)

### Endpoint
N/A (These are path segments, not full endpoints)

### Parameters
None

### Request Example
None

### Response
None

## Routes Interface

### Description
The `Routes` interface defines the available route paths within the Auth0 Next.js SDK.

### Properties

- **accessToken** (string) - The route for obtaining an access token.
- **backChannelLogout** (string) - The route for back-channel logout.
- **callback** (string) - The callback route after authentication.
- **login** (string) - The login route.
- **logout** (string) - The logout route.
- **profile** (string) - The route for user profile information.
```

--------------------------------

### Handle User Login and Session Display (React/TSX)

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

A Next.js page component that checks for an active user session using `auth0.getSession()`. If no session exists, it renders links for signing up or logging in. If a session is found, it displays a welcome message with the user's name.

```tsx
import { auth0 } from "./lib/auth0"; // Adjust path if your auth0 client is elsewhere

export default async function Home() {
  const session = await auth0.getSession();

  if (!session) {
    return (
      <main>
        <a href="/auth/login?screen_hint=signup">Sign up</a>
        <a href="/auth/login">Log in</a>
      </main>
    );
  }

  return (
    <main>
      <h1>Welcome, {session.user.name}!</h1>
    </main>
  );
}
```

--------------------------------

### Specify Return Path after Login

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/client.WithPageAuthRequiredOptions.html

Configures the path to which the user will be redirected after a successful login. This ensures a seamless user experience by returning them to their intended page.

```javascript
withPageAuthRequired(Profile, {
  returnTo: '/profile'
});
```

--------------------------------

### Auth0 Next.js SDK Types

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/modules/types.html

This section details the types, interfaces, and enumerations available within the Auth0 Next.js SDK v4.10.0. It includes definitions for options, configurations, and data structures used for authentication, session management, and callback handling.

```APIDOC
## Auth0 Next.js SDK - Types

This documentation outlines the types, interfaces, and enumerations provided by the `@auth0/nextjs-auth0` SDK.

### Enumerations

#### SUBJECT_TOKEN_TYPES

*   **Description**: Defines the types of subject tokens.
*   **Example**: `SUBJECT_TOKEN_TYPES.ACCESS_TOKEN`

### Interfaces

#### Auth0ClientOptions

*   **Description**: Options for configuring the Auth0 client.
*   **Fields**:
    *   `clientId` (string) - Required - Your Auth0 application's Client ID.
    *   `clientSecret` (string) - Optional - Your Auth0 application's Client Secret (use with caution).
    *   `domain` (string) - Required - Your Auth0 tenant domain.
    *   `redirectUri` (string) - Required - The URI Auth0 will redirect to after authentication.
    *   `audience` (string) - Optional - The audience for the tokens.
    *   `scope` (string) - Optional - The scopes to request.

#### SessionConfiguration

*   **Description**: Configuration for session management.
*   **Fields**:
    *   `cookie` (SessionCookieOptions) - Optional - Options for the session cookie.
    *   `store` (SessionStoreOptions) - Optional - Options for the session store.
    *   `rolling` (boolean) - Optional - Whether to roll the session cookie on each request.
    *   `rollingDuration` (number) - Optional - The duration in seconds to roll the session cookie.
    *   `absoluteDuration` (number) - Optional - The absolute duration in seconds for the session.

#### User

*   **Description**: Represents a user profile.
*   **Fields**:
    *   `sub` (string) - Required - The unique identifier for the user.
    *   `email` (string) - Optional - The user's email address.
    *   `name` (string) - Optional - The user's full name.
    *   `picture` (string) - Optional - The URL of the user's profile picture.

### Type Aliases

#### LogoutStrategy

*   **Description**: Defines the strategy for logging out.
*   **Possible Values**:
    *   `'oidc'
    *   `'all'

```

--------------------------------

### TypeScript - AbstractSessionStore Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

Initializes an AbstractSessionStore with session store options. This constructor is intended for internal use and is part of the base class for managing session cookies and data.

```typescript
new AbstractSessionStore(
    __namedParameters: SessionStoreOptions
): AbstractSessionStore
```

--------------------------------

### Perform Backchannel Authentication

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Initiates a backchannel authentication request. This method is used for server-to-server authentication flows and returns a promise that resolves with either an SdkError or the authentication response.

```typescript
backchannelAuthentication(
  options: BackchannelAuthenticationOptions
): Promise<[SdkError, null] | [null, BackchannelAuthenticationResponse]>
```

--------------------------------

### startInteractiveLogin Function for Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

The startInteractiveLogin function initiates an interactive login flow for Auth0 within a Next.js application. It can optionally accept StartInteractiveLoginOptions and returns a Promise<NextResponse> to manage the user's login experience.

```typescript
startInteractiveLogin(
    options?: StartInteractiveLoginOptions
): Promise<NextResponse<unknown>>
```

--------------------------------

### Initiate Backchannel Authentication (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Authenticates a user via Client-Initiated Backchannel Authentication, returning a token set. This requires the feature to be enabled in the Auth0 dashboard and polls the token endpoint until authentication is complete.

```typescript
import { BackchannelAuthenticationOptions, BackchannelAuthenticationResponse } from "./types";

async function getTokenByBackchannelAuth(options: BackchannelAuthenticationOptions): Promise<BackchannelAuthenticationResponse>
```

--------------------------------

### handler API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

A general handler for authentication-related requests.

```APIDOC
## POST /api/auth/[...path]

### Description
A versatile handler that manages various authentication-related requests based on the provided path.

### Method
POST

### Endpoint
/api/auth/[...path]

### Parameters
#### Path Parameters
- **path** (string[]) - Required - An array of strings representing the path segments for the request.

#### Query Parameters
None

#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
```json
{
  "req": "<NextRequest Object>"
}
```

### Response
#### Success Response (200)
- **NextResponse** (object) - A NextResponse object representing the result of the request.

#### Response Example
```json
{
  "response": "<NextResponse Object>"
}
```
```

--------------------------------

### backchannelAuthentication

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Performs backchannel authentication to obtain tokens.

```APIDOC
## backchannelAuthentication

### Description
Performs backchannel authentication to obtain tokens using the provided options.

### Method
POST (assumed, as it involves sending options for authentication)

### Endpoint
/api/auth/backchannel-authentication (example, actual endpoint may vary)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
*   **options** (BackchannelAuthenticationOptions) - Required - Options for backchannel authentication.

### Request Example
```json
{
  "options": {
    "username": "user@example.com",
    "password": "your_password"
  }
}
```

### Response
#### Success Response (200)
*   **result** (Promise<[SdkError | null, BackchannelAuthenticationResponse | null]>) - A promise that resolves to a tuple containing either an error or the authentication response.

#### Response Example
```json
{
  "result": [
    null,
    {
      "access_token": "your_access_token",
      "id_token": "your_id_token"
    }
  ]
}
```
```

--------------------------------

### ConnectionTokenSet Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.ConnectionTokenSet.html

Details of the ConnectionTokenSet interface, including its properties and their types.

```APIDOC
## ConnectionTokenSet Interface

### Description
Represents a set of tokens related to a connection, including access token, connection identifier, expiration time, and optional scope.

### Interface
```typescript
interface ConnectionTokenSet {
    accessToken: string;
    connection: string;
    expiresAt: number;
    scope?: string;
    [key: string]: unknown;
}
```

### Properties
#### accessToken
- **accessToken** (string) - The access token.

#### connection
- **connection** (string) - The identifier for the connection.

#### expiresAt
- **expiresAt** (number) - The timestamp indicating when the token expires.

#### scope (Optional)
- **scope** (string) - An optional scope associated with the token.

#### Indexable
- **[key: string]** (unknown) - Allows for additional, dynamic properties.
```

--------------------------------

### TransactionStoreOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionStoreOptions.html

Configuration options for managing login transactions.

```APIDOC
## TransactionStoreOptions Interface

### Description

Defines the structure for configuring the transaction store, which is used to manage login sessions and their associated data.

### Properties

#### `cookieOptions` (TransactionCookieOptions) - Optional

Options for customizing the transaction cookies, such as their path, domain, and security settings.

#### `enableParallelTransactions` (boolean) - Optional

Controls whether multiple parallel login transactions are allowed. When false, only one transaction cookie is maintained at a time. When true (default), multiple transaction cookies can coexist for multi-tab support.

*   **Default**: `true`

#### `secret` (string) - Required

A secret string used for encrypting and signing transaction data to ensure its integrity and confidentiality.
```

--------------------------------

### Auth0ClientOptions Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Auth0ClientOptions.html

The Auth0ClientOptions interface allows you to configure various aspects of the Auth0 client, including security, application base URL, authorization parameters, and session management.

```APIDOC
## Auth0ClientOptions Interface

### Description

This interface defines the configuration options available when initializing the Auth0 client. These options control authentication flows, security settings, and application-specific details.

### Method

N/A (Interface definition)

### Endpoint

N/A (Interface definition)

### Parameters

#### Optional Properties

- **allowInsecureRequests** (boolean) - Allows insecure requests to the authorization server, useful for local testing with non-TLS providers. Only usable when NODE_ENV is not 'production'.
- **appBaseUrl** (string) - The base URL of your application. Defaults to the APP_BASE_URL environment variable.
- **authorizationParameters** (AuthorizationParameters) - Additional parameters to send to the `/authorize` endpoint.
- **beforeSessionSaved** (BeforeSessionSavedHook) - A hook that runs before the session is saved.
- **clientAssertionSigningAlg** (string) - The signing algorithm for client assertions.
- **clientAssertionSigningKey** (string | CryptoKey) - The signing key for client assertions.
- **clientId** (string) - Your Auth0 application's client ID.
- **clientSecret** (string) - Your Auth0 application's client secret.
- **domain** (string) - Your Auth0 tenant's domain.
- **enableAccessTokenEndpoint** (boolean) - Enables the access token endpoint.
- **enableParallelTransactions** (boolean) - Enables parallel transactions.
- **enableTelemetry** (boolean) - Enables telemetry.
- **httpTimeout** (number) - The HTTP request timeout in milliseconds.
- **includeIdTokenHintInOIDCLogoutUrl** (boolean) - Includes the ID token hint in the OIDC logout URL.
- **logoutStrategy** (LogoutStrategy) - The strategy to use for logging out.
- **noContentProfileResponseWhenUnauthenticated** (boolean) - If true, the profile endpoint will return no content when unauthenticated.
- **onCallback** (OnCallbackHook) - A hook that runs on callback.
- **pushedAuthorizationRequests** (boolean) - Enables pushed authorization requests.
- **routes** (Partial<Pick<Routes, "login" | "callback" | "logout" | "backChannelLogout">>) - Customizes the application's routes for login, callback, logout, and back-channel logout.
- **secret** (string) - A secret used for session encryption.
- **session** (SessionConfiguration) - Configuration for session management.
- **sessionStore** (SessionDataStore) - A custom store for session data.
- **signInReturnToPath** (string) - The path to redirect to after sign-in.
- **transactionCookie** (TransactionCookieOptions) - Options for the transaction cookie.

### Request Example

```json
{
  "allowInsecureRequests": false,
  "appBaseUrl": "https://example.com",
  "clientId": "YOUR_CLIENT_ID",
  "domain": "YOUR_AUTH0_DOMAIN"
}
```

### Response

N/A (Interface definition)

### Response Example

N/A (Interface definition)
```

--------------------------------

### MissingStateError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.MissingStateError.html

Documentation for the MissingStateError class, which is part of the SDK's error handling.

```APIDOC
## MissingStateError Class

### Description

Represents an error that occurs when the state parameter is missing during an authentication flow.

### Hierarchy

*   [SdkError](errors.SdkError.html)
    *   MissingStateError

### Constructors

#### constructor()

*   `new MissingStateError(message?: string): MissingStateError`
    *   **Parameters**
        *   `message` (string) - Optional. The error message.
    *   **Returns**
        *   MissingStateError
    *   Overrides [SdkError](errors.SdkError.html).[constructor](errors.SdkError.html#constructor)

### Properties

#### code

*   `code`: string = "missing_state"
    *   Overrides [SdkError](errors.SdkError.html).[code](errors.SdkError.html#code)
    *   Defined in `src/errors/index.ts:32`
```

--------------------------------

### BackchannelAuthenticationNotSupportedError Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationNotSupportedError.html

The constructor for the BackchannelAuthenticationNotSupportedError class. It initializes a new instance of the error, inheriting functionality from the parent SdkError class. This method is called when an instance of this specific error needs to be created.

```typescript
new BackchannelAuthenticationNotSupportedError(): BackchannelAuthenticationNotSupportedError
```

--------------------------------

### Session Cookie Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/index.html

Configure the session cookie for nextjs-auth0 using environment variables like AUTH0_COOKIE_DOMAIN, AUTH0_COOKIE_PATH, etc.

```APIDOC
## Session Cookie Configuration

### Description
Configure the session cookie settings for the nextjs-auth0 SDK using environment variables.

### Environment Variables
*   `AUTH0_COOKIE_DOMAIN`
*   `AUTH0_COOKIE_PATH`
*   `AUTH0_COOKIE_TRANSIENT`
*   `AUTH0_COOKIE_SECURE`
*   `AUTH0_COOKIE_SAME_SITE`

### Note
Respective counterparts are also available in the client configuration. See [Cookie Configuration](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md#cookie-configuration) for more details.
```

--------------------------------

### handleLogout API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Handles the user logout process, terminating the user's session.

```APIDOC
## POST /api/auth/logout

### Description
Handles the termination of the user's session. This endpoint clears authentication tokens and redirects the user.

### Method
POST

### Endpoint
/api/auth/logout

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
```json
{
  "req": "<NextRequest Object>"
}
```

### Response
#### Success Response (200)
- **NextResponse** (object) - A NextResponse object representing the result of the logout process.

#### Response Example
```json
{
  "response": "<NextResponse Object>"
}
```
```

--------------------------------

### Authentication Flow API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Handles core authentication flows including access token generation, callback processing, and logout.

```APIDOC
## POST /api/auth/callback

### Description
Handles the callback from the authentication provider after a user logs in.

### Method
POST

### Endpoint
/api/auth/callback

### Parameters
#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
N/A (This endpoint is typically hit by the authentication provider)

### Response
#### Success Response (200)
- **res** (NextResponse) - A Next.js response object, often redirecting the user.

#### Response Example
N/A (Response is handled by Next.js)

## POST /api/auth/logout

### Description
Handles the back-channel logout process initiated by the identity provider.

### Method
POST

### Endpoint
/api/auth/logout

### Parameters
#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
N/A (This endpoint is typically hit by the authentication provider)

### Response
#### Success Response (200)
- **res** (NextResponse) - A Next.js response object, often redirecting the user.

#### Response Example
N/A (Response is handled by Next.js)

## POST /api/auth/access-token

### Description
Generates an access token for the current user session.

### Method
POST

### Endpoint
/api/auth/access-token

### Parameters
#### Request Body
- **req** (NextRequest) - Required - The incoming Next.js request object.

### Request Example
N/A (This endpoint is typically called from the client-side or server-side within your application)

### Response
#### Success Response (200)
- **res** (NextResponse) - A Next.js response object containing the access token or related information.

#### Response Example
N/A (Response is handled by Next.js)
```

--------------------------------

### Protect Next.js Server Component with Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredAppRouter.html

Wrap your Next.js Server Component with `auth0.withPageAuthRequired` to enforce authentication. If the user is not authenticated, they will be redirected to the login page. Ensure the `returnTo` option is specified for proper redirection after login, especially for dynamic routes.

```javascript
import { auth0 } from "@/lib/auth0";

const ProtectedPage = auth0.withPageAuthRequired(async function ProtectedPage() {
  return <div>Protected content</div>;
}, { returnTo: '/protected-page' });

export default ProtectedPage;
```

--------------------------------

### User Authentication API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/server.filterDefaultIdTokenClaims.html

This section details functions related to user authentication and claim filtering within the Auth0 NextJS SDK.

```APIDOC
## filterDefaultIdTokenClaims

### Description
Filters the provided claims to include only those considered default ID token claims.

### Method
N/A (This is a client-side function)

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **claims** (object) - Required - The claims object to filter.

### Request Example
```json
{
  "claims": {
    "sub": "auth0|12345",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "https://example.com/roles": ["admin"]
  }
}
```

### Response
#### Success Response (200)
- **User[]** - An array of user objects containing only default ID token claims.

#### Response Example
```json
[
  {
    "sub": "auth0|12345",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
]
```
```

--------------------------------

### Configure Fetch API in Auth0 Next.js SDK

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthClientOptions.html

Allows customization of the global `fetch` function used by the SDK. This is useful for adding custom headers, interceptors, or modifying request/response behavior. It accepts a function that mirrors the standard Fetch API signature. No external dependencies are required.

```typescript
fetch?: {
    (input: URL | RequestInfo, init?: RequestInit): Promise<Response>;
    (input: string | Request | URL, init?: RequestInit): Promise<Response>;
}
```

--------------------------------

### SessionStoreOptions Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionStoreOptions.html

Configuration options for session storage, including durations, cookie settings, and encryption secrets.

```APIDOC
## SessionStoreOptions

### Description

Interface for configuring session storage options within the @auth0/nextjs-auth0 library. This includes settings related to session duration, cookie behavior, and security.

### Properties

#### Path Parameters

* None

#### Query Parameters

* None

#### Request Body

##### `absoluteDuration` (number) - Optional

The absolute duration in seconds after which the session will expire. This duration is fixed and will not be extended by activity. Defaults to 3 days.

##### `cookie` (SessionCookieOptions) - Optional

An object containing options for the session cookie. This is inherited from `SessionConfiguration`.

##### `cookieOptions` (SessionCookieOptions) - Optional

Specific options for the session cookie, separate from the general cookie configuration.

##### `inactivityDuration` (number) - Optional

The duration in seconds of inactivity after which the session will expire. The session will be extended if activity occurs before this duration is reached. Defaults to 1 day.

##### `rolling` (boolean) - Optional

A boolean indicating whether to use rolling sessions. If true, the session is extended as long as it's used within the `inactivityDuration`. Defaults to `true`.

##### `secret` (string) - Required

The secret key used for encrypting and signing session data. This is crucial for security.

##### `store` (SessionDataStore) - Optional

A custom session data store implementation. If not provided, a default store will be used.

### Request Example

```json
{
  "absoluteDuration": 259200, 
  "inactivityDuration": 86400, 
  "rolling": true, 
  "secret": "your-super-secret-key",
  "cookieOptions": {
    "secure": true,
    "httpOnly": true,
    "sameSite": "lax"
  }
}
```

### Response

*This interface is used for configuration and does not have a direct response in the API context. Its properties are used to configure server-side session management.*
```

--------------------------------

### useUser

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/modules/client.html

The useUser hook provides access to the authenticated user's profile information within your React components.

```APIDOC
## useUser

### Description
Hooks into the user object provided by the Auth0Provider.

### Method
Hook

### Endpoint
N/A

### Parameters
None

### Request Example
```jsx
import { useUser } from '@auth0/nextjs-auth0';

function Profile() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <img src={user.picture} alt="User profile picture" />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

### Response
#### Success Response (Object)
- **user** (object | undefined) - The authenticated user's profile information, or undefined if not logged in or loading.
- **error** (Error | undefined) - An error object if an error occurred during authentication, or undefined.
- **isLoading** (boolean) - A boolean indicating if the user data is currently being fetched.
```

--------------------------------

### Generate Auth0 Secret

Source: https://github.com/auth0/nextjs-auth0/blob/main/README.md

Generates a secure hexadecimal secret for session encryption using the openssl command-line tool. A 32-byte hex string is recommended.

```shell
openssl rand -hex 32
```

--------------------------------

### Token Management API

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Provides methods for managing OAuth tokens, including exchanging refresh tokens for access tokens and retrieving token sets with optional refresh.

```APIDOC
## GET /auth/token-set

### Description
Retrieves OAuth token sets, handling token refresh when necessary or if forced.

### Method
GET

### Endpoint
/auth/token-set

### Parameters
#### Query Parameters
- **forceRefresh** (boolean) - Optional - If true, forces a token refresh.

### Request Body
N/A

### Request Example
N/A

### Response
#### Success Response (200)
- **tokenSet** (object) - The retrieved or refreshed token set.
- **idTokenClaims** (object) - The claims from the ID token (if available).

#### Response Example
```json
{
  "tokenSet": {
    "accessToken": "eyJ...".
    "expiresIn": 3600,
    "scope": "openid profile",
    "tokenType": "Bearer",
    "refreshToken": "Eyx..."
  },
  "idTokenClaims": {
    "sub": "auth0|12345",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

## POST /auth/connection/token-set

### Description
Exchanges a refresh token for an access token for a specific connection.

### Method
POST

### Endpoint
/auth/connection/token-set

### Parameters
#### Request Body
- **tokenSet** (object) - Required - The current token set containing the refresh token.
- **connectionTokenSet** (object) - Optional - Details for the connection token set.
- **options** (object) - Required - Options for obtaining the access token for the connection.

### Request Example
```json
{
  "tokenSet": {
    "refreshToken": "Eyx..."
  },
  "connectionTokenSet": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret"
  },
  "options": {
    "audience": "your-api-audience"
  }
}
```

### Response
#### Success Response (200)
- **accessToken** (string) - The newly obtained access token.
- **expiresIn** (number) - The expiration time of the access token in seconds.
- **scope** (string) - The scope granted to the access token.

#### Response Example
```json
{
  "accessToken": "eyz...".
  "expiresIn": 3600,
  "scope": "read:data"
}
```
```

--------------------------------

### BackchannelAuthenticationOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.BackchannelAuthenticationOptions.html

Defines the structure for configuring Client-Initiated Backchannel Authentication (CIBA) in the Auth0 Next.js SDK.

```APIDOC
## Backchannel Authentication Options

### Description

This interface outlines the available options for configuring Client-Initiated Backchannel Authentication (CIBA) flows within the Auth0 Next.js SDK. It allows for customization of authorization details, parameters, binding messages, login hints, and requested expiry times.

### Method

Not Applicable (Interface Definition)

### Endpoint

Not Applicable (Interface Definition)

### Parameters

#### Request Body (Implicit for configuration)

- **authorizationDetails** (AuthorizationDetails[]) - Optional - Optional authorization details to use Rich Authorization Requests (RAR). See: https://auth0.com/docs/get-started/apis/configure-rich-authorization-requests
- **authorizationParams** (AuthorizationParameters) - Optional - Authorization Parameters to be sent with the authorization request.
- **bindingMessage** (string) - Required - Human-readable message to be displayed at the consumption device and authentication device. This allows the user to ensure the transaction initiated by the consumption device is the same that triggers the action on the authentication device.
- **loginHint** ({ sub: string }) - Required - The login hint to inform which user to use. The `sub` claim of the user trying to login via CIBA, to which a push notification to authorize the login will be sent.
- **requestedExpiry** (number) - Optional - Set a custom expiry time for the CIBA flow in seconds. Defaults to 300 seconds (5 minutes) if not set.

### Request Example

```json
{
  "bindingMessage": "Please approve the login request for your account.",
  "loginHint": {
    "sub": "auth0|user123"
  },
  "requestedExpiry": 600,
  "authorizationParams": {
    "scope": "openid profile email offline_access",
    "audience": "https://your-api.example.com"
  }
}
```

### Response

#### Success Response (N/A)

This is an interface definition for configuration, not an endpoint that returns a direct response.

#### Response Example (N/A)

Not Applicable (Interface Definition)
```

--------------------------------

### getTokenByBackchannelAuth

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Authenticates using Client-Initiated Backchannel Authentication and returns the token set and optionally the ID token claims and authorization details. This method initializes the backchannel authentication process with Auth0 and polls the token endpoint until authentication is complete. Feature must be enabled in the Auth0 dashboard.

```APIDOC
## getTokenByBackchannelAuth

### Description
Authenticates using Client-Initiated Backchannel Authentication and returns the token set and optionally the ID token claims and authorization details. This method will initialize the backchannel authentication process with Auth0, and poll the token endpoint until the authentication is complete.

Using Client-Initiated Backchannel Authentication requires the feature to be enabled in the Auth0 dashboard.

### Method
POST (implied by authentication flow)

### Endpoint
/oauth/token (implied by Backchannel Authentication flow)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **options** (BackchannelAuthenticationOptions) - Required - Configuration for the backchannel authentication.

### Request Example
```json
{
  "options": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "device_code": "DEVICE_CODE_FROM_AUTHORIZATION_REQUEST",
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
  }
}
```

### Response
#### Success Response (200)
- **token_set** (object) - The set of tokens obtained.
- **id_token_claims** (object) - Optional claims from the ID token.
- **authorization_details** (object) - Optional authorization details.

#### Response Example
```json
{
  "token_set": {
    "access_token": "eyJ...".",
    "refresh_token": "eyJ...".",
    "id_token": "eyJ...".",
    "expires_in": 3600
  },
  "id_token_claims": {
    "sub": "auth0|1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "authorization_details": {
    "granted_scopes": ["openid", "profile", "email"]
  }
}
```
```

--------------------------------

### User Interface Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.User.html

Defines the structure of a user object within the @auth0/nextjs-auth0 library. It includes standard user properties and allows for arbitrary key-value pairs.

```typescript
interface User {
    [email](#email)?: string;
    [email_verified](#email_verified)?: boolean;
    [family_name](#family_name)?: string;
    [given_name](#given_name)?: string;
    [name](#name)?: string;
    [nickname](#nickname)?: string;
    [org_id](#org_id)?: string;
    [picture](#picture)?: string;
    [sub](#sub): string;
    [key: string]: any;
}
```

--------------------------------

### handleProfile Function for Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

This handleProfile function is responsible for retrieving user profile information in a Next.js application using Auth0. It processes the NextRequest and returns a Promise<NextResponse>, enabling access to authenticated user data.

```typescript
handleProfile(req: NextRequest): Promise<NextResponse<unknown>>
```

--------------------------------

### User Interface Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.User.html

Defines the structure of a user object, including properties like email, name, and a unique subject identifier.

```APIDOC
## User Interface

### Description
Represents a user object with various optional and required properties.

### Properties

*   **email** (string) - Optional - The user's email address.
*   **email_verified** (boolean) - Optional - Indicates if the user's email has been verified.
*   **family_name** (string) - Optional - The user's family name.
*   **given_name** (string) - Optional - The user's given name.
*   **name** (string) - Optional - The user's full name.
*   **nickname** (string) - Optional - The user's nickname.
*   **org_id** (string) - Optional - The organization ID that the user belongs to. This field is populated when the user logs in through an organization.
*   **picture** (string) - Optional - A URL to the user's profile picture.
*   **sub** (string) - Required - The unique subject identifier for the user.
*   **[key: string]** (any) - Optional - Allows for additional arbitrary properties.
```

--------------------------------

### withPageAuthRequired

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/modules/client.html

The withPageAuthRequired higher-order component protects Next.js pages, ensuring that only authenticated users can access them.

```APIDOC
## withPageAuthRequired

### Description
A higher-order component (HOC) that protects Next.js pages, redirecting unauthenticated users to the login page.

### Method
Higher-Order Component

### Endpoint
N/A

### Parameters
#### Options
- **options** (object) - Optional - Configuration options for the HOC.
  - **returnTo** (string) - Optional - The URL to redirect to after login. Defaults to the current page.
  - **loginOptions** (object) - Optional - Options to pass to the underlying login method.

### Request Example
```javascript
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

export default withPageAuthRequired(function MyPage(props) {
  // ... page content
});
```

### Response
Returns a protected page component.
```

--------------------------------

### handleLogin Function for Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

The handleLogin function is designed to process login requests within a Next.js application using Auth0. It takes a NextRequest object as input and returns a Promise resolving to a NextResponse. This function is crucial for initiating the authentication flow.

```typescript
handleLogin(req: NextRequest): Promise<NextResponse<unknown>>
```

--------------------------------

### SessionDataStore Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

The SessionDataStore interface provides methods for managing user sessions. It allows for creating, retrieving, and deleting session data.

```APIDOC
## SessionDataStore Interface

### Description
An interface for managing session data, allowing for the creation, retrieval, and deletion of sessions.

### Methods

#### `set(id: string, session: SessionData): Promise<void>`

*   **Description**: Upserts a session in the store given a session ID and `SessionData`.
*   **Parameters**:
    *   `id` (string) - The unique identifier for the session.
    *   `session` (SessionData) - The session data to be stored.
*   **Returns**: A promise that resolves when the session is successfully set.

#### `get(id: string): Promise<null | SessionData>`

*   **Description**: Retrieves the session from the store given a session ID.
*   **Parameters**:
    *   `id` (string) - The unique identifier for the session to retrieve.
*   **Returns**: A promise that resolves with the `SessionData` if found, or `null` if not found.

#### `delete(id: string): Promise<void>`

*   **Description**: Destroys the session with the given session ID.
*   **Parameters**:
    *   `id` (string) - The unique identifier for the session to delete.
*   **Returns**: A promise that resolves when the session is successfully deleted.

#### `deleteByLogoutToken?(logoutToken: LogoutToken): Promise<void>`

*   **Description**: Deletes the session associated with the provided logout token. This token may contain a session ID, a user ID, or both.
*   **Parameters**:
    *   `logoutToken` (LogoutToken) - The logout token used to identify the session for deletion.
*   **Returns**: A promise that resolves when the session is successfully deleted.

### Type Definitions

*   `SessionData`: Represents the data stored for a user session.
*   `LogoutToken`: Represents a token used for logging out a user, which may include session or user identifiers.
```

--------------------------------

### withPageAuthRequiredAppRouter

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredAppRouter.html

Wrap your Server Components with `withPageAuthRequired` to ensure users are authenticated before accessing a page. If not authenticated, the user will be redirected to the login page.

```APIDOC
## `withPageAuthRequired` for App Router

### Description
Wraps a Server Component to protect it, ensuring the user is authenticated. If the user is not authenticated, they will be redirected to the login page.

### Method
This is a higher-order function that wraps your existing page component.

### Endpoint
This function is used within your Next.js App Router pages (e.g., `app/page.js`).

### Parameters
#### Function Arguments
- **fn** (`AppRouterPageRoute`) - The Server Component function to wrap.
- **opts** (`WithPageAuthRequiredAppRouterOptions`, Optional) - Options to configure the authentication wrapper.
  
  #### `WithPageAuthRequiredAppRouterOptions`
  - **returnTo** (`string` or `(opts: { params: Promise<Record<string, string>>, searchParams: Promise<Record<string, string>> }) => string`, Optional) - The URL to redirect the user to after successful login. Can be a string or a function that dynamically generates the return URL based on route parameters and search parameters.

### Request Example
```javascript
// app/protected-page/page.js
import { auth0 } from "@/lib/auth0";

const ProtectedPage = auth0.withPageAuthRequired(async function ProtectedPage() {
  return <div>Protected content</div>;
}, { returnTo: '/protected-page' });

export default ProtectedPage;
```

### Request Example with Dynamic Routes
```javascript
// app/protected-page/[slug]/page.js
import { AppRouterPageRouteOpts } from '@auth0/nextjs-auth0/server';
import { auth0 } from "@/lib/auth0";

const ProtectedPage = auth0.withPageAuthRequired(async function ProtectedPage({ params, searchParams }: AppRouterPageRouteOpts) {
  const slug = (await params)?.slug as string;
  return <div>Protected content for {slug}</div>;
}, {
  returnTo({ params }) {
    return `/protected-page/${(await params)?.slug}`;
  }
});

export default ProtectedPage;
```

### Response
This function does not directly return a response. Instead, it returns a protected Server Component.

#### Success Response (Implicit)
If the user is authenticated, the original Server Component is rendered.

#### Error Handling (Implicit)
If the user is not authenticated, they are redirected to the login page. The specific error handling for authentication failures is managed internally by the SDK.

*   Defined in `src/server/helpers/with-page-auth-required.ts:169`
```

--------------------------------

### getAccessTokenForConnection

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves an access token for a given connection. This method has different overloads for App Router and Pages Router contexts.

```APIDOC
## GET /auth0/nextjs-auth0/getAccessTokenForConnection

### Description
Retrieves an access token for a connection. This overload is intended for use in Server Components, Server Actions, and Route Handlers within the App Router. Note that Server Components cannot set cookies, so the token will be refreshed but not persisted.

### Method
GET

### Endpoint
/auth0/nextjs-auth0/getAccessTokenForConnection

### Parameters
#### Query Parameters
- **options** (AccessTokenForConnectionOptions) - Required - Options for retrieving the access token.

### Response
#### Success Response (200)
- **token** (string) - The access token.
- **expiresAt** (number) - The expiration timestamp of the token.

#### Response Example
```json
{
  "token": "your_access_token",
  "expiresAt": 1678886400
}
```
```

```APIDOC
## GET /auth0/nextjs-auth0/getAccessTokenForConnection

### Description
Retrieves an access token for a connection. This overload is intended for use in middleware, `getServerSideProps`, and API routes within the Pages Router, requiring request and response objects for persistence.

### Method
GET

### Endpoint
/auth0/nextjs-auth0/getAccessTokenForConnection

### Parameters
#### Query Parameters
- **options** (AccessTokenForConnectionOptions) - Required - Options for retrieving the access token.
- **req** (NextRequest | PagesRouterRequest) - Optional - The request object.
- **res** (NextResponse | PagesRouterResponse) - Optional - The response object.

### Response
#### Success Response (200)
- **token** (string) - The access token.
- **expiresAt** (number) - The expiration timestamp of the token.

#### Response Example
```json
{
  "token": "your_access_token",
  "expiresAt": 1678886400
}
```
```

--------------------------------

### Handle Dynamic Routes and Search Params with Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredAppRouter.html

Use `withPageAuthRequired` with a custom `returnTo` function to preserve dynamic route parameters and search parameters after user login. This function receives `params` and `searchParams` to construct the correct return URL.

```javascript
import { AppRouterPageRouteOpts } from '@auth0/nextjs-auth0/server';
import { auth0 } from "@/lib/auth0";

const ProtectedPage = auth0.withPageAuthRequired(async function ProtectedPage({ params, searchParams }: AppRouterPageRouteOpts) {
  const slug = (await params)?.slug as string;
  return <div>Protected content for {slug}</div>;
}, {
  returnTo({ params }) {
    return `/protected-page/${(await params)?.slug}`;
  }
});

export default ProtectedPage;
```

--------------------------------

### TransactionState Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionState.html

Details of the TransactionState interface, including its properties, types, and hierarchy.

```APIDOC
## TransactionState Interface

### Description
Represents the state of a transaction during the authentication process.

### Properties

#### codeVerifier
- **codeVerifier** (string) - Required - The code verifier used in the OAuth 2.0 authorization code flow.

#### maxAge
- **maxAge** (number) - Optional - The maximum age of the authentication session in seconds.

#### nonce
- **nonce** (string) - Required - A random string used to mitigate replay attacks.

#### responseType
- **responseType** (string) - Required - The type of response requested from the authorization server.

#### returnTo
- **returnTo** (string) - Required - The URL to redirect to after the authentication process is complete.

#### state
- **state** (string) - Required - A string that maintains state between the request and callback.

#### [propName: string]
- **[propName: string]** (unknown) - Any other JWT Claim Set member.
```

--------------------------------

### Session Management: set()

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

The `set` method is used to save session data by adding an encrypted session cookie to the response. It can optionally use the `iat` property of the session to compute the `maxAge` for the cookie.

```APIDOC
## POST /auth/session/set

### Description
Saves session data by adding an encrypted session cookie to the response. If the `iat` property is present on the session, it will be used to compute the `maxAge` for the cookie.

### Method
POST

### Endpoint
/auth/session/set

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **reqCookies** (RequestCookies | ReadonlyRequestCookies) - Required - The request cookies.
- **resCookies** (ResponseCookies) - Required - The response cookies.
- **session** (SessionData) - Required - The session data to be saved.
- **isNew** (boolean) - Optional - Indicates if the session is new.

### Request Example
```json
{
  "reqCookies": {},
  "resCookies": {},
  "session": {
    "userId": "123",
    "iat": 1678886400
  },
  "isNew": false
}
```

### Response
#### Success Response (200)
- **message** (string) - Indicates successful session update.

#### Response Example
```json
{
  "message": "Session updated successfully."
}
```
```

--------------------------------

### SdkError Constructor and Properties (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.SdkError.html

Defines the SdkError class, a base class for SDK-specific errors. It inherits from the built-in Error class and includes a 'code' property to categorize the error. This is fundamental for error handling within the Auth0 Next.js SDK.

```typescript
class SdkError extends Error {
  code: string;

  constructor(message?: string) {
    super(message);
    this.code = ""; // Typically set by subclasses
  }
}
```

--------------------------------

### BackchannelAuthenticationError Constructor (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationError.html

Illustrates the constructor for the BackchannelAuthenticationError class. It takes an optional 'cause' parameter, which should be an OAuth2Error object, providing details about the underlying authentication error.

```typescript
new BackchannelAuthenticationError(
    		__namedParameters: { cause?: OAuth2Error }
    	);
```

--------------------------------

### getAccessToken

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/modules/client.html

The getAccessToken function retrieves an access token for making authorized requests to your API.

```APIDOC
## getAccessToken

### Description
Retrieves an access token for making authorized API requests.

### Method
Function

### Endpoint
N/A

### Parameters
#### Options
- **req** (object) - Optional - The Next.js request object (for server-side usage).
- **res** (object) - Optional - The Next.js response object (for server-side usage).

### Request Example
```javascript
import { getAccessToken } from '@auth0/nextjs-auth0';

export default async function myApiHandler(req, res) {
  const { token } = await getAccessToken(req, res);
  // Use the token to make authenticated requests to your API
}
```

### Response
#### Success Response (Object)
- **token** (string) - The access token.
- **accessToken** (string) - Alias for token.

#### Error Response
Throws an error if the token cannot be retrieved.
```

--------------------------------

### handler Function for Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

The general handler function serves as a core request processor for the Auth0 integration in Next.js. It takes a NextRequest and returns a Promise<NextResponse>, acting as a central point for various authentication-related operations.

```typescript
handler(req: NextRequest): Promise<NextResponse<unknown>>
```

--------------------------------

### Auth0Provider Function Signature

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/client.Auth0Provider.html

This TypeScript code defines the function signature for the Auth0Provider component. It specifies the expected props, including children and an optional user object, and indicates that it returns a React Element.

```typescript
Auth0Provider(__namedParameters: { children: ReactNode; user?: User }): Element[]
```

--------------------------------

### TypeScript Interface: BackchannelAuthenticationOptions

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.BackchannelAuthenticationOptions.html

Defines the structure for options used in Client-Initiated Backchannel Authentication (CIBA) flows. It includes optional authorization details and parameters, a required binding message, a login hint specifying the user's subject identifier, and an optional custom expiry time for the flow.

```typescript
interface BackchannelAuthenticationOptions {
    authorizationDetails?: AuthorizationDetails[];
    authorizationParams?: AuthorizationParameters;
    bindingMessage: string;
    loginHint: { sub: string };
    requestedExpiry?: number;
}
```

--------------------------------

### AccessTokenForConnectionOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AccessTokenForConnectionOptions.html

The AccessTokenForConnectionOptions interface defines the structure for options used when retrieving an access token for a specific connection. It includes mandatory and optional parameters for configuring the token retrieval process.

```APIDOC
## AccessTokenForConnectionOptions

### Description
Options for retrieving a connection access token.

### Method
N/A (Interface Definition)

### Endpoint
N/A (Interface Definition)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **connection** (string) - Required - The connection name for which you want to retrieve the access token.
- **login_hint** (string) - Optional - An optional login hint to pass to the authorization server.
- **subject_token_type** (SUBJECT_TOKEN_TYPES) - Optional - The type of token that is being exchanged. Defaults to `SUBJECT_TYPE_REFRESH_TOKEN`.
  Allowed values: `urn:ietf:params:oauth:token-type:refresh_token`, `urn:ietf:params:oauth:token-type:access_token`

### Request Example
```json
{
  "connection": "your-connection-name",
  "login_hint": "user@example.com",
  "subject_token_type": "urn:ietf:params:oauth:token-type:access_token"
}
```

### Response
#### Success Response (200)
N/A (This is an interface for request options, not a direct API response)

#### Response Example
N/A
```

--------------------------------

### finalizeSession

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Filters and processes ID token claims for a session, optionally allowing custom processing via a callback.

```APIDOC
## finalizeSession

### Description
Filters and processes ID token claims for a session. If a `beforeSessionSaved` callback is configured, it will be invoked to allow custom processing of the session and ID token. Otherwise, default filtering will be applied to remove standard ID token claims from the user object.

### Method
POST (assumed, as it processes session data)

### Endpoint
/api/auth/finalize-session (example, actual endpoint may vary)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
*   **session** (SessionData) - Required - The session data to be finalized.
*   **idToken** (string) - Optional - The ID token associated with the session.

### Request Example
```json
{
  "session": {
    "user": { "sub": "auth0|12345", "name": "Test User" },
    "accessToken": "your_access_token"
  },
  "idToken": "your_id_token"
}
```

### Response
#### Success Response (200)
*   **result** (Promise<SessionData>) - A promise that resolves to the finalized session data.

#### Response Example
```json
{
  "result": {
    "user": { "sub": "auth0|12345", "name": "Test User" },
    "accessToken": "your_access_token"
  }
}
```
```

--------------------------------

### Optional authorizationParameters Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Auth0ClientOptions.html

Allows for additional parameters to be sent to the '/authorize' endpoint during the authentication flow. This enables customization of the authorization request.

```typescript
authorizationParameters?: AuthorizationParameters;
```

--------------------------------

### CookieOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.CookieOptions.html

The CookieOptions interface defines the structure for configuring cookie behavior in the @auth0/nextjs-auth0 library. It includes properties for domain, httpOnly, maxAge, path, sameSite, secure, and transient.

```APIDOC
## CookieOptions Interface

### Description

The `CookieOptions` interface specifies the configuration settings for cookies used by the authentication system. This allows customization of how cookies are set and managed by the library.

### Properties

#### Path Parameters

- **domain** (string) - Optional - The domain for which the cookie is valid.
- **httpOnly** (boolean) - Required - Specifies if the cookie is accessible by client-side scripts.
- **maxAge** (number) - Optional - The maximum age of the cookie in seconds.
- **path** (string) - Required - The path on the server on which the cookie is available.
- **sameSite** ("lax" | "strict" | "none") - Required - Controls when cookies are sent with cross-site requests.
- **secure** (boolean) - Required - Specifies if the cookie should only be sent over HTTPS.
- **transient** (boolean) - Optional - Indicates if the cookie is a session cookie (deleted when the browser closes).

### Request Example

```json
{
  "domain": "example.com",
  "httpOnly": true,
  "maxAge": 86400,
  "path": "/",
  "sameSite": "lax",
  "secure": true,
  "transient": false
}
```

### Response

*This interface defines options for setting cookies and does not represent a direct API response.*

#### Success Response (N/A)

*N/A*

#### Response Example

*N/A*
```

--------------------------------

### DiscoveryError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.DiscoveryError.html

Details regarding the DiscoveryError class, which extends SdkError and represents a discovery-related error.

```APIDOC
## DiscoveryError Class

### Description

The `DiscoveryError` class is a custom error type used within the @auth0/nextjs-auth0 library. It extends the base `SdkError` class and is specifically used to indicate errors encountered during the discovery process, such as fetching configuration details.

### Hierarchy

*   [SdkError](errors.SdkError.html)
    *   DiscoveryError

### Constructors

#### new DiscoveryError(message?: string)

*   **Parameters**
    *   `message` (string) - Optional. A descriptive message for the error.

*   **Returns**
    *   DiscoveryError

*   **Description**
    *   Initializes a new instance of the `DiscoveryError` class. It inherits its constructor from `SdkError`.

### Properties

#### code: string

*   **Type**
    *   string

*   **Default Value**
    *   `"discovery_error"`

*   **Description**
    *   A string identifier for the type of error. For `DiscoveryError`, this is always `"discovery_error"`. This property is inherited from `SdkError`.
```

--------------------------------

### Auth0ClientOptions Interface Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Auth0ClientOptions.html

Defines the configuration options for the Auth0 client in Next.js applications. This interface includes settings for authentication parameters, session management, routing, and security.

```typescript
interface Auth0ClientOptions {
    allowInsecureRequests?: boolean;
    appBaseUrl?: string;
    authorizationParameters?: AuthorizationParameters;
    beforeSessionSaved?: BeforeSessionSavedHook;
    clientAssertionSigningAlg?: string;
    clientAssertionSigningKey?: string | CryptoKey;
    clientId?: string;
    clientSecret?: string;
    domain?: string;
    enableAccessTokenEndpoint?: boolean;
    enableParallelTransactions?: boolean;
    enableTelemetry?: boolean;
    httpTimeout?: number;
    includeIdTokenHintInOIDCLogoutUrl?: boolean;
    logoutStrategy?: LogoutStrategy;
    noContentProfileResponseWhenUnauthenticated?: boolean;
    onCallback?: OnCallbackHook;
    pushedAuthorizationRequests?: boolean;
    routes?: Partial<
        Pick<Routes, "login" | "callback" | "logout" | "backChannelLogout">
    >;
    secret?: string;
    session?: SessionConfiguration;
    sessionStore?: SessionDataStore;
    signInReturnToPath?: string;
    transactionCookie?: TransactionCookieOptions;
}
```

--------------------------------

### Define DiscoveryError Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.DiscoveryError.html

This TypeScript code defines the constructor for the DiscoveryError class. It accepts an optional message string and inherits from the SdkError constructor. The 'code' property is initialized to 'discovery_error'.

```typescript
new DiscoveryError(message?: string): DiscoveryError

/**
 * Optional message string for the error.
 */
message: string

/**
 * Overrides the base SdkError constructor.
 */
constructor(message?: string)
```

--------------------------------

### InvalidStateError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.InvalidStateError.html

Documentation for the InvalidStateError class, which extends SdkError and is used to represent invalid state issues within the SDK.

```APIDOC
## Class: InvalidStateError

### Description

Represents an error where the SDK is in an invalid state, preventing correct operation. This error class extends `SdkError`.

### Hierarchy

*   `SdkError`
    *   `InvalidStateError`

### Constructors

#### constructor(message?: string)

*   **Parameters**
    *   `message` (string) - Optional. A descriptive message for the error.
*   **Returns**
    *   `InvalidStateError` - An instance of InvalidStateError.

### Properties

#### code: string

*   **Value**: "invalid_state"
*   **Description**: A string code representing the type of error.
*   **Inherited**: From `SdkError`
```

--------------------------------

### AccessTokenForConnectionError Constructor - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AccessTokenForConnectionError.html

This constructor initializes a new instance of the AccessTokenForConnectionError. It requires an error code and message, and optionally accepts an OAuth2Error object as the cause of the error. This class extends the base SdkError.

```typescript
new AccessTokenForConnectionError(
    code: string,
    message: string,
    cause?: OAuth2Error
): AccessTokenForConnectionError
```

--------------------------------

### Use User Hook in JavaScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/client.useUser.html

The `useUser` hook from `@auth0/nextjs-auth0` provides user authentication status. It returns an object containing `user`, `error`, `isLoading`, and an `invalidate` function. The `user` can be null, undefined, or a User object. The `error` can be an Error object or undefined. `isLoading` indicates if the authentication state is being fetched.

```javascript
import { useUser } from "@auth0/nextjs-auth0";

function Profile() {
  const { user, error, isLoading, invalidate } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (user) {
    return (
      <div>
        Welcome, {user.name}!
        <button onClick={() => invalidate()}>Log out</button>
      </div>
    );
  }
  return <div>Please log in.</div>;
}
```

--------------------------------

### SessionStoreOptions Interface Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionStoreOptions.html

Defines the structure for session store options in TypeScript. It includes optional properties for session duration, cookie configurations, and an optional data store, along with a required secret for session security.

```typescript
interface SessionStoreOptions {
    absoluteDuration?: number;
    cookie?: SessionCookieOptions;
    cookieOptions?: SessionCookieOptions;
    inactivityDuration?: number;
    rolling?: boolean;
    secret: string;
    store?: SessionDataStore;
}
```

--------------------------------

### Define AuthClientOptions Interface in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthClientOptions.html

This TypeScript interface defines the structure for configuring an authentication client. It includes properties for Auth0 domain, client ID, application base URL, session management, and various optional settings for advanced configurations like token endpoints and hooks.

```typescript
interface AuthClientOptions {
    [allowInsecureRequests](#allowinsecurerequests)?: boolean;
    [appBaseUrl](#appbaseurl): string;
    [authorizationParameters](#authorizationparameters)?: [AuthorizationParameters](types.AuthorizationParameters.html);
    [beforeSessionSaved](#beforesessionsaved)?: [BeforeSessionSavedHook](../types/types.BeforeSessionSavedHook.html);
    [clientAssertionSigningAlg](#clientassertionsigningalg)?: string;
    [clientAssertionSigningKey](#clientassertionsigningkey)?: string | CryptoKey;
    [clientId](#clientid): string;
    [clientSecret](#clientsecret)?: string;
    [domain](#domain): string;
    [enableAccessTokenEndpoint](#enableaccesstokenendpoint)?: boolean;
    [enableTelemetry](#enabletelemetry)?: boolean;
    [fetch](#fetch)?: {
        (input: URL | RequestInfo, init?: RequestInit): Promise<Response>;
        (input: string | Request | URL, init?: RequestInit): Promise<Response>;
    };
    [httpTimeout](#httptimeout)?: number;
    [includeIdTokenHintInOIDCLogoutUrl](#includeidtokenhintinoidclogouturl)?: boolean;
    [jwksCache](#jwkscache)?: JWKSCacheInput;
    [logoutStrategy](#logoutstrategy)?: [LogoutStrategy](../types/types.LogoutStrategy.html);
    [noContentProfileResponseWhenUnauthenticated](#nocontentprofileresponsewhenunauthenticated)?: boolean;
    [onCallback](#oncallback)?: [OnCallbackHook](../types/types.OnCallbackHook.html);
    [pushedAuthorizationRequests](#pushedauthorizationrequests)?: boolean;
    [routes](#routes): [Routes](types.Routes.html);
    [secret](#secret): string;
    [sessionStore](#sessionstore): [AbstractSessionStore](../classes/server.AbstractSessionStore.html);
    [signInReturnToPath](#signinreturntopath)?: string;
    [transactionStore](#transactionstore): [TransactionStore](../classes/server.TransactionStore.html);
}
```

--------------------------------

### Define AccessTokenForConnectionOptions Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AccessTokenForConnectionOptions.html

This TypeScript interface defines the structure for options when requesting an access token for a specific Auth0 connection. It includes mandatory and optional parameters like connection name, login hint, and subject token type.

```typescript
interface AccessTokenForConnectionOptions {
    [connection]: string;
    [login_hint]?: string;
    [subject_token_type]?: SUBJECT_TOKEN_TYPES;
}
```

--------------------------------

### TransactionStore Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

The TransactionStore class is responsible for storing and managing the state required for authentication transactions. It utilizes encrypted, stateless cookies for this purpose.

```APIDOC
## TransactionStore Class

### Description

The TransactionStore class is responsible for storing the state required to successfully complete an authentication transaction. The store relies on encrypted, stateless cookies to store the transaction state.

### Constructor

*   `new TransactionStore(transactionStoreOptions: TransactionStoreOptions): TransactionStore`
    *   **Parameters**
        *   `transactionStoreOptions` (TransactionStoreOptions) - Options for configuring the transaction store.
    *   **Returns**
        *   `TransactionStore`

### Methods

#### `delete(resCookies: ResponseCookies, state: string): Promise<void>`

*   **Description**: Deletes a specific transaction cookie.
*   **Parameters**:
    *   `resCookies` (ResponseCookies) - The response cookies object.
    *   `state` (string) - The state identifier of the transaction to delete.
*   **Returns**:
    *   `Promise<void>`

#### `deleteAll(reqCookies: RequestCookies, resCookies: ResponseCookies): Promise<void>`

*   **Description**: Deletes all transaction cookies based on the configured prefix.
*   **Parameters**:
    *   `reqCookies` (RequestCookies) - The request cookies object.
    *   `resCookies` (ResponseCookies) - The response cookies object.
*   **Returns**:
    *   `Promise<void>`

#### `get(reqCookies: RequestCookies, state: string): Promise<null | JWTDecryptResult<TransactionState>>`

*   **Description**: Retrieves transaction state from a cookie.
*   **Parameters**:
    *   `reqCookies` (RequestCookies) - The request cookies object.
    *   `state` (string) - The state identifier of the transaction to retrieve.
*   **Returns**:
    *   `Promise<null | JWTDecryptResult<TransactionState>>` - The decrypted transaction state or null if not found.

#### `getCookiePrefix(): string`

*   **Description**: Returns the configured prefix for transaction cookies.
*   **Returns**:
    *   `string` - The cookie prefix.

#### `save(resCookies: ResponseCookies, transactionState: TransactionState, reqCookies?: RequestCookies): Promise<void>`

*   **Description**: Saves the transaction state to an encrypted cookie.
*   **Parameters**:
    *   `resCookies` (ResponseCookies) - The response cookies object to set the transaction cookie on.
    *   `transactionState` (TransactionState) - The transaction state to save.
    *   `reqCookies` (RequestCookies, Optional) - Optional request cookies to check for existing transactions. When provided and `enableParallelTransactions` is false, will check for existing transaction cookies. When omitted, the existence check is skipped for performance optimization.
*   **Returns**:
    *   `Promise<void>`
*   **Throws**:
    *   When transaction state is missing required state parameter.

```

--------------------------------

### BackchannelAuthenticationNotSupportedError Class Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationNotSupportedError.html

Defines the BackchannelAuthenticationNotSupportedError class, which extends SdkError. It includes a constructor and a 'code' property specific to this error type. This class is part of the error handling mechanisms in the @auth0/nextjs-auth0 SDK.

```typescript
export declare class BackchannelAuthenticationNotSupportedError extends SdkError {
    constructor();
    code: string;
}
```

--------------------------------

### getAccessToken

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves an access token, optionally forcing a refresh. Can be used in server-side contexts with request and response objects.

```APIDOC
## getAccessToken

### Description
Retrieves an access token. This method can be used in middleware and `getServerSideProps`, API routes in the **Pages Router**.

### Method
POST (or GET depending on implementation)

### Endpoint
`/api/auth/token` (example, actual endpoint may vary)

### Parameters
#### Query Parameters
- **refresh** (boolean) - Optional - Force a refresh of the access token.

#### Request Body
- **req** (NextRequest | PagesRouterRequest) - Required - The request object.
- **res** (NextResponse | PagesRouterResponse) - Required - The response object.
- **options** (GetAccessTokenOptions) - Optional - Optional configuration for getting the access token.

### Request Example
```json
{
  "req": { ... },
  "res": { ... },
  "options": {
    "refresh": true
  }
}
```

### Response
#### Success Response (200)
- **token** (string) - The access token.
- **expiresAt** (number) - The expiration timestamp of the token.
- **scope** (string) - The scope of the token (optional).

#### Response Example
```json
{
  "token": "eyJ...".substring(7),
  "expiresAt": 1678886400,
  "scope": "read:users"
}
```
```

--------------------------------

### AuthorizationError Constructor - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationError.html

Initializes a new instance of the AuthorizationError class. It requires a 'cause' property, which is an OAuth2Error, and optionally accepts a 'message'. This constructor overrides the base SdkError constructor.

```typescript
new AuthorizationError({
    cause: OAuth2Error,
    message?: string
})
```

--------------------------------

### AuthorizationCodeGrantRequestError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantRequestError.html

Documentation for the AuthorizationCodeGrantRequestError class, which extends SdkError and is used for authorization code grant request errors.

```APIDOC
## AuthorizationCodeGrantRequestError Class

### Description
Represents an error that occurs during an authorization code grant request.
This class extends `SdkError`.

### Class
`AuthorizationCodeGrantRequestError`

### Constructors

#### `new AuthorizationCodeGrantRequestError(message?: string)`

*   **Parameters**
    *   `message` (string) - Optional. A descriptive message for the error.

*   **Returns** `AuthorizationCodeGrantRequestError`

*   **Overrides** `SdkError.constructor`

*   **Defined in** `src/errors/index.ts:63`

### Properties

#### `code`

*   **Type**: `string`
*   **Value**: `"authorization_code_grant_request_error"`
*   **Description**: A unique code identifying this specific error type.
*   **Overrides** `SdkError.code`
*   **Defined in** `src/errors/index.ts:61`
```

--------------------------------

### getSession

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Retrieves the session data for the current request. This method is available for both App Router and Pages Router contexts.

```APIDOC
## GET /auth0/nextjs-auth0/getSession

### Description
Retrieves the session data for the current request. This overload is intended for use in Server Components, Server Actions, and Route Handlers within the App Router.

### Method
GET

### Endpoint
/auth0/nextjs-auth0/getSession

### Parameters
None

### Response
#### Success Response (200)
- **sessionData** (SessionData | null) - The session data if available, otherwise null.

#### Response Example
```json
{
  "user": {
    "sub": "auth0|1234567890abcdef",
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "expiresAt": 1678886400
}
```
```

```APIDOC
## GET /auth0/nextjs-auth0/getSession

### Description
Retrieves the session data for the current request. This overload is intended for use in middleware, `getServerSideProps`, and API routes within the Pages Router, requiring the request object.

### Method
GET

### Endpoint
/auth0/nextjs-auth0/getSession

### Parameters
#### Query Parameters
- **req** (NextRequest | PagesRouterRequest) - Required - The request object.

### Response
#### Success Response (200)
- **sessionData** (SessionData | null) - The session data if available, otherwise null.

#### Response Example
```json
{
  "user": {
    "sub": "auth0|1234567890abcdef",
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "expiresAt": 1678886400
}
```
```

--------------------------------

### Enforce Email Verification on User Load with nextjs-auth0 (JavaScript)

Source: https://github.com/auth0/nextjs-auth0/wiki/Examples

This snippet shows how to implement the `onUserLoaded` hook within the `handleCallback` function to check if the user's email is verified. If not verified, it throws an error, preventing session creation and redirecting the user. Requires the 'email' scope to be included in `AUTH0_SCOPE`.

```javascript
import auth0 from '../../lib/auth0';

export default async function callback(req, res) {
  try {
    await auth0.handleCallback(req, res, {
      onUserLoaded: async (req, res, session, state) => {
        if (!session.user.email_verified) {
          const err = new Error('You need to validate your email address first');
          err.code = 'require_email_verification';

          throw err;
        }

        return session;
      }
    });
  } catch (error) {
    if (error.code === 'require_email_verification') {
      res.writeHead(302, {
        Location: '/email-validate'
      });
      res.end();
    }

    res.status(error.status || 500).end(error.message);
  }
}
```

--------------------------------

### Define Auth0 Next.js Routes Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Routes.html

This TypeScript interface defines the structure for authentication routes used within the Auth0 Next.js SDK. It includes properties for accessing token, logout, callback, login, and profile URLs. This is crucial for configuring and managing authentication flows in a Next.js application.

```typescript
interface Routes {
    [accessToken]: string;
    [backChannelLogout]: string;
    [callback]: string;
    [login]: string;
    [logout]: string;
    [profile]: string;
}
```

--------------------------------

### Define BackchannelLogoutError Class (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelLogoutError.html

This TypeScript code defines the BackchannelLogoutError class, which extends SdkError. It includes a constructor that accepts an optional message and sets a default error code for backchannel logout operations. This class is intended for use within the @auth0/nextjs-auth0 library.

```typescript
export declare class BackchannelLogoutError extends SdkError {
    constructor(message?: string);
    code: string;
}
```

--------------------------------

### AccessTokenError Constructor - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AccessTokenError.html

This constructor is used to create an instance of the AccessTokenError. It requires a string for the error code and message, and optionally accepts an OAuth2Error object as the cause. This error class inherits from SdkError.

```typescript
new AccessTokenError(
    code: string,
    message: string,
    cause?: OAuth2Error
): AccessTokenError
```

--------------------------------

### Define BackchannelAuthenticationResponse Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.BackchannelAuthenticationResponse.html

This TypeScript interface defines the structure of the response object for backchannel authentication. It includes optional authorization details, optional ID token claims, and a mandatory token set. This is crucial for correctly parsing and utilizing authentication tokens and related information.

```typescript
interface BackchannelAuthenticationResponse {
    [authorizationDetails](#authorizationdetails)?: [AuthorizationDetails](types.AuthorizationDetails.html)[];
    [idTokenClaims](#idtokenclaims)?: { [key: string]: any };
    [tokenSet](#tokenset): [TokenSet](types.TokenSet.html);
}
```

--------------------------------

### ConnectionTokenSet Interface Definition (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.ConnectionTokenSet.html

Defines the structure of a token set, including access token, connection identifier, and expiration timestamp. It also supports additional arbitrary string keys.

```typescript
interface ConnectionTokenSet {
    [accessToken](#accesstoken): string;
    [connection](#connection): string;
    [expiresAt](#expiresat): number;
    [scope](#scope)?: string;
    [key: string]: unknown;
}
```

--------------------------------

### SessionData Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionData.html

The SessionData interface defines the structure of session data, including token sets, user information, and internal session details.

```APIDOC
## SessionData Interface

### Description
The `SessionData` interface represents the structure of the session object that holds user authentication and session-related information.

### Interface
```typescript
interface SessionData {
    [connectionTokenSets](#connectiontokensets)?: [ConnectionTokenSet][]
    [internal](#internal): { createdAt: number; sid: string }
    [tokenSet](#tokenset): [TokenSet]
    [user](#user): [User]
    [key: string]: unknown
}
```

### Properties

#### `connectionTokenSets` (Optional)
- **Type**: `[ConnectionTokenSet][]`
- **Description**: An optional array of connection token sets.
- **Defined in**: src/types/index.ts:26

#### `internal`
- **Type**: `{ createdAt: number; sid: string }`
- **Description**: Internal session details including creation timestamp and session ID.
- **Defined in**: src/types/index.ts:20

#### `tokenSet`
- **Type**: `[TokenSet]`
- **Description**: The primary token set for the session.
- **Defined in**: src/types/index.ts:19

#### `user`
- **Type**: `[User]`
- **Description**: The user object associated with the session.
- **Defined in**: src/types/index.ts:18

#### Indexable
- **Type**: `unknown`
- **Description**: Allows for additional arbitrary properties to be stored on the session data.
- **Defined in**: src/types/index.ts:17
```

--------------------------------

### AuthorizationCodeGrantRequestError Constructor

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantRequestError.html

Defines the constructor for the AuthorizationCodeGrantRequestError class. It accepts an optional message string and inherits from the SdkError class. This error is specific to authorization code grant requests.

```typescript
new AuthorizationCodeGrantRequestError(
    message?: string,
): AuthorizationCodeGrantRequestError
```

--------------------------------

### Optional allowInsecureRequests Configuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.Auth0ClientOptions.html

Allows insecure requests to the authorization server, primarily for local testing with non-TLS compliant mock OIDC providers. This option is only valid when NODE_ENV is not set to 'production'.

```typescript
allowInsecureRequests?: boolean;
```

--------------------------------

### TransactionCookieOptions

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionCookieOptions.html

Configuration options for transaction cookies used in @auth0/nextjs-auth0.

```APIDOC
## TransactionCookieOptions

### Description
This interface defines the configurable properties for transaction cookies within the `@auth0/nextjs-auth0` library. These options allow customization of cookie behavior, including its domain, expiration, path, prefix, SameSite attribute, and security settings.

### Properties

#### `domain`
- **Type**: `string`
- **Optional**: Yes
- **Description**: Specifies the value for the `Set-Cookie` attribute `Domain`. By default, no domain is set, and most clients will consider the cookie to apply only to the current domain.

#### `maxAge`
- **Type**: `number`
- **Optional**: Yes
- **Description**: The expiration time for transaction cookies in seconds. If not provided, it defaults to 1 hour (3600 seconds).
- **Default**: `3600`

#### `path`
- **Type**: `string`
- **Optional**: Yes
- **Description**: The `path` attribute of the transaction cookie. Will be set to `/` by default.

#### `prefix`
- **Type**: `string`
- **Optional**: Yes
- **Description**: The prefix of the cookie used to store the transaction state.
- **Default**: `__txn_{state}`

#### `sameSite`
- **Type**: `"lax" | "strict" | "none"`
- **Optional**: Yes
- **Description**: The `SameSite` attribute of the transaction cookie.
- **Default**: `lax`

#### `secure`
- **Type**: `boolean`
- **Optional**: Yes
- **Description**: The `secure` attribute of the transaction cookie. If the protocol of the application's base URL is `https`, then `true`, otherwise `false`.
- **Default**: Depends on the protocol of the application's base URL.

### Example Usage (Conceptual)
```javascript
// Example of setting custom cookie options
import { initAuth0 } from '@auth0/nextjs-auth0';

const auth0 = initAuth0({
  domain: process.env.AUTH0_DOMAIN,
  clientId: process.env.AUTH0_CLIENT_ID,
  clientSecret: process.env.AUTH0_CLIENT_SECRET,
  // ... other options
  session: {
    cookie: {
      domain: 'example.com',
      maxAge: 7200, // 2 hours
      path: '/app',
      prefix: '__custom_txn_',
      sameSite: 'strict',
      secure: true
    }
  }
});
```
```

--------------------------------

### handleLogout Function for Next.js Auth0

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

The handleLogout function handles user logout requests in a Next.js application integrated with Auth0. It accepts a NextRequest and returns a Promise<NextResponse>, facilitating the termination of user sessions securely.

```typescript
handleLogout(req: NextRequest): Promise<NextResponse<unknown>>
```

--------------------------------

### Handle Back Channel Logout in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Manages back-channel logout requests initiated by an identity provider. This function takes a NextRequest and returns a Promise resolving to a NextResponse, facilitating secure logout processes.

```typescript
async handleBackChannelLogout(req: NextRequest): Promise<NextResponse<unknown>> {
    // Implementation details for back-channel logout
}
```

--------------------------------

### SessionConfiguration Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

Defines the structure for configuring session settings, including absolute and inactivity durations, cookie options, and rolling session behavior.

```APIDOC
## SessionConfiguration Interface

### Description

This interface allows you to configure various aspects of the user session, including how long a session is valid in absolute terms, how long it remains valid after inactivity, and specific cookie settings.

### Properties

#### `absoluteDuration` (number) - Optional

The maximum duration (in seconds) after which a session will expire, regardless of activity. Defaults to 3 days.

#### `cookie` (SessionCookieOptions) - Optional

An object containing options to configure the session cookie, such as its name, domain, and path.

#### `inactivityDuration` (number) - Optional

The duration (in seconds) of user inactivity after which the session will expire. Defaults to 1 day. The session is extended as long as it was active before this duration is reached.

#### `rolling` (boolean) - Optional

A boolean indicating whether to use rolling sessions. If `true`, the session's validity period is extended each time the user interacts with the application, up to the `absoluteDuration`. Defaults to `true`.
```

--------------------------------

### AuthorizationCodeGrantError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantError.html

Details about the AuthorizationCodeGrantError class, including its constructors and properties, which extends SdkError and is used for handling authorization code grant errors.

```APIDOC
## AuthorizationCodeGrantError

### Description
Represents an error that occurs during the authorization code grant flow. This class extends `SdkError` and provides specific details related to OAuth2 errors.

### Class Hierarchy
* [SdkError](errors.SdkError.html)
    * AuthorizationCodeGrantError

### Constructors
#### new AuthorizationCodeGrantError(params)
* **params** (`object`) - Required. An object containing:
    * **cause** ([OAuth2Error](errors.OAuth2Error.html)) - Required. The underlying OAuth2 error object.
    * **message** (`string`) - Optional. A custom error message.

### Properties
* **cause** ([OAuth2Error](errors.OAuth2Error.html))
    The underlying OAuth2 error object that caused this exception.
* **code** (`string`)
    A string representing the error code, which is `"authorization_code_grant_error"` for this class.

### Example Usage (Conceptual)
```javascript
try {
  // Some operation that might throw AuthorizationCodeGrantError
  // For example, handling a callback with an OAuth2 error
  const error = new AuthorizationCodeGrantError({ cause: oauth2ErrorObject });
  throw error;
} catch (error) {
  if (error instanceof AuthorizationCodeGrantError) {
    console.error("Authorization Code Grant Error:", error.message);
    console.error("OAuth2 Cause:", error.cause);
    console.error("Error Code:", error.code);
  } else {
    // Handle other errors
  }
}
```
```

--------------------------------

### OAuth2Error Class Constructor - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.OAuth2Error.html

Defines the constructor for the OAuth2Error class. It accepts a named parameter object containing a mandatory 'code' string and an optional 'message' string. This class inherits from SdkError.

```typescript
new OAuth2Error({
    code: string;
    message?: string;
})
```

--------------------------------

### Initialize AuthorizationCodeGrantError - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantError.html

Demonstrates how to instantiate the AuthorizationCodeGrantError class. It requires an OAuth2Error object for the 'cause' property and can optionally include a custom error message.

```typescript
new AuthorizationCodeGrantError({
    cause: oauth2ErrorObject,
    message: "Custom error message here."
})
```

--------------------------------

### updateSession (App Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Updates the session of the currently authenticated user. This overload is specifically for use within Server Actions and Route Handlers in the App Router of Next.js.

```APIDOC
## updateSession (App Router)

### Description
Updates the session of the currently authenticated user. If the user does not have a session, an error is thrown. This method is intended for use in Server Actions and Route Handlers in the **App Router**.

### Method
POST (or other methods depending on context)

### Endpoint
Relevant endpoint within the application's App Router structure (Server Action or Route Handler).

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **session** (SessionData) - Required - The session data to update.

### Request Example
```typescript
// Example in a Server Action
'use server';

import { updateSession } from '@auth0/nextjs-auth0';
import { cookies } from 'next/headers';

export async function POST(request) {
  const session = await getSession(cookies()); // Assuming getSession is adapted for App Router
  if (!session) {
    throw new Error('No active session found.');
  }

  const updatedSessionData = { ...session.user, customField: 'anotherValue' };

  await updateSession(updatedSessionData);

  return Response.json({ message: 'Session updated successfully' });
}
```

### Response
#### Success Response (200)
- **void** - The function returns a promise that resolves to void upon successful session update.

#### Response Example
(This function modifies the session and returns a promise that resolves to void. The actual HTTP response is handled by the calling Server Action or Route Handler.)
```

--------------------------------

### Protect Next.js Page with Auth0 Authentication

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredPageRouter.html

This snippet demonstrates how to use `auth0.withPageAuthRequired()` to protect a Next.js page. It ensures that users must be authenticated to access the page. If not, they are redirected to the login page and then back to the protected page after authentication.

```javascript
import { auth0 } from "@/lib/auth0";

export default function ProtectedPage() {
  return <div>Protected content</div>;
}

export const getServerSideProps = auth0.withPageAuthRequired();
```

--------------------------------

### BackchannelAuthenticationError Class Definition (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationError.html

Defines the BackchannelAuthenticationError class, extending SdkError. It includes a constructor that accepts an optional 'cause' of type OAuth2Error and a 'code' property set to 'backchannel_authentication_error'.

```typescript
export declare class BackchannelAuthenticationError extends SdkError {
    constructor(__namedParameters: { cause?: OAuth2Error });
    code: string;
    cause?: OAuth2Error;
}
```

--------------------------------

### Define TransactionStoreOptions Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionStoreOptions.html

Defines the structure for transaction store options, including optional cookie configurations and a mandatory secret. The `enableParallelTransactions` property controls concurrent login handling.

```typescript
interface TransactionStoreOptions {
    [cookieOptions](#cookieoptions)?: [TransactionCookieOptions](types.TransactionCookieOptions.html);
    [enableParallelTransactions](#enableparalleltransactions)?: boolean;
    [secret](#secret): string;
}
```

--------------------------------

### Customize withPageAuthRequired Error Handling

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/client.WithPageAuthRequiredOptions.html

Provides a custom React element to display when an error occurs during user profile fetching. This option allows developers to control the UI feedback for authentication errors.

```javascript
withPageAuthRequired(Profile, {
  onError: error => <div>Error: {error.message}</div>
});
```

--------------------------------

### Testing Utilities - generateSessionCookie

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/testing.generateSessionCookie.html

Generates a session cookie for testing purposes within the Auth0 Next.js SDK. This function is protected and intended for internal testing scenarios.

```APIDOC
## Testing Utilities - generateSessionCookie

### Description
Generates a session cookie for testing purposes. This function is protected and intended for internal testing scenarios.

### Method
N/A (This is a function, not an HTTP endpoint)

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
This function does not take a request body in the traditional API sense. It accepts parameters directly.

- **session** (Partial<SessionData>) - Required - Represents a partial session data object.
- **config** (GenerateSessionCookieConfig) - Required - Configuration object for generating the session cookie.

### Request Example
N/A (This is a function call, not an HTTP request)

### Response
#### Success Response (Promise<string>)
- **string** - The generated session cookie string.

#### Response Example
```javascript
// Example of how the function might be called (actual return value is a string)
const sessionCookie = await generateSessionCookie({
  user: { sub: 'google-oauth2|12345' },
  // ... other session properties
}, {
  cookieSecret: 'your-secret',
  // ... other config properties
});
```
```

--------------------------------

### AuthorizationParameters Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthorizationParameters.html

Defines the optional parameters that can be passed during authorization requests to customize behavior, such as specifying the audience, maximum age for reauthentication, organization, redirect URI, and requested scopes.

```APIDOC
## AuthorizationParameters Interface

### Description

This interface defines the optional parameters that can be used to customize authorization requests.

### Method

N/A (This is an interface definition, not an API endpoint)

### Endpoint

N/A

### Parameters

#### Query Parameters (Implicitly used in authorization requests)

- **audience** (string, optional) - The unique identifier of the target API you want to access.
- **max_age** (number, optional) - The maximum amount of time, in seconds, after which a user must reauthenticate.
- **organization** (string, optional) - The unique identifier of the organization that the user should be logged into. The organization ID will be included in the user's session after successful authentication.
- **redirect_uri** (string, optional) - The URL to which the authorization server will redirect the user after granting authorization.
- **scope** (string, optional) - The scope of the access request, expressed as a list of space-delimited, case-sensitive strings. Defaults to `"openid profile email offline_access"`.
- **[key: string]** (unknown, optional) - Additional, arbitrary authorization parameters.

### Request Example

```json
{
  "audience": "https://your-api.example.com",
  "max_age": 3600,
  "organization": "org_123",
  "redirect_uri": "https://your-app.example.com/callback",
  "scope": "read:data write:data"
}
```

### Response

N/A (This is an interface definition, not an API endpoint)

#### Success Response (200)

N/A

#### Response Example

N/A
```

--------------------------------

### Define AuthorizationDetails Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthorizationDetails.html

This TypeScript code defines the AuthorizationDetails interface, which is used to structure authorization-related information. It includes a 'type' property and allows for additional string-keyed parameters.

```typescript
interface AuthorizationDetails {
    [type](#type): string;
    readonly [parameter: string]: unknown;
}
```

--------------------------------

### SessionCookieOptions Interface

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionCookieOptions.html

Defines the configurable options for session cookies used by the @auth0/nextjs-auth0 library.

```APIDOC
## SessionCookieOptions Interface

### Description
This interface defines the properties that can be used to configure the session cookie.

### Properties

#### `domain` (string) - Optional
Specifies the value for the [Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.3|Domain). By default, no domain is set, and most clients will consider the cookie to apply to only the current domain.

#### `name` (string) - Optional
The name of the session cookie.
Default: `__session`.

#### `path` (string) - Optional
The path attribute of the session cookie. Will be set to '/' by default.

#### `sameSite` ("lax" | "strict" | "none") - Optional
The sameSite attribute of the session cookie.
Default: `lax`.

#### `secure` (boolean) - Optional
The secure attribute of the session cookie.
Default: depends on the protocol of the application's base URL. If the protocol is `https`, then `true`, otherwise `false`.

#### `transient` (boolean) - Optional
The transient attribute of the session cookie. When true, the cookie will not persist beyond the current session.
```

--------------------------------

### WithPageAuthRequiredAppRouterOptions Type Alias

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredAppRouterOptions.html

This type alias defines the options available when using `withPageAuthRequired` in the Next.js App Router. It primarily allows specifying a `returnTo` URL.

```APIDOC
## Type Alias: WithPageAuthRequiredAppRouterOptions

### Description

Specify the URL to `returnTo` - this is important in app router pages because the server component won't know the URL of the page.

### Type Definition

```typescript
type WithPageAuthRequiredAppRouterOptions = {
  returnTo?: string | ((obj: AppRouterPageRouteOpts) => Promise<string> | string);
}
```

### Properties

#### `returnTo` (Optional)

- **Type**: `string` | `(obj: AppRouterPageRouteOpts) => Promise<string> | string`
- **Description**: The URL to redirect the user to after authentication. This can be a static string or a function that dynamically resolves the URL based on the `AppRouterPageRouteOpts`.
```

--------------------------------

### Implement Page Authentication with WithPageAuthRequired (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/client.WithPageAuthRequired.html

This snippet demonstrates how to use the WithPageAuthRequired higher-order component to protect a Next.js page. It wraps a React component, ensuring that only authenticated users can access it. If a user is not authenticated, they will be redirected to the login page. This is a common pattern for securing pages in applications using Next.js and Auth0.

```typescript
import { withPageAuthRequired } from "@auth0/nextjs-auth0";

// Assume MyPage is your React component for the page
const MyPage = (props) => {
  // Page content here
  return <div>My Protected Page</div>;
};

export default withPageAuthRequired(MyPage);
```

--------------------------------

### Handle Callback in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Processes the callback requests after a user authentication flow. This function is essential for completing the OAuth or OIDC authentication in a Next.js application, returning a NextResponse.

```typescript
async handleCallback(req: NextRequest): Promise<NextResponse<unknown>> {
    // Implementation details for handling callback
}
```

--------------------------------

### Define MissingStateError Class in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.MissingStateError.html

This TypeScript code defines the MissingStateError class, which extends SdkError. It includes a constructor that accepts an optional message and a 'code' property initialized to 'missing_state'. This class is part of the error handling mechanism in the @auth0/nextjs-auth0 library.

```typescript
export declare class MissingStateError extends SdkError {
    code: string;
    constructor(message?: string);
}
```

--------------------------------

### Define Return URL for Auth in Next.js App Router

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.WithPageAuthRequiredAppRouterOptions.html

This type alias defines an optional `returnTo` property. This property is crucial for App Router pages as it specifies the URL to redirect to after authentication. It can be a string or a function that returns a string, potentially based on options passed to the route handler.

```typescript
type WithPageAuthRequiredAppRouterOptions = {
    returnTo?:
        | string
        | ((obj: AppRouterPageRouteOpts) => Promise<string> | string);
}
```

--------------------------------

### WithPageAuthRequired

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/client.WithPageAuthRequired.html

The WithPageAuthRequired higher-order component (HOC) protects pages by redirecting unauthenticated users to the login page.

```APIDOC
## WithPageAuthRequired

### Description
When an anonymous user visits a page wrapped with this higher order component, they will be redirected to the login page and then returned to the page they were redirected from after successful login.

### Method
Higher-Order Component (HOC)

### Endpoint
N/A (Client-side Higher-Order Component)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```javascript
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

function MyPage(props) {
  // Your page content here
  return <div>Hello {props.user.name}</div>;
}

export default withPageAuthRequired(MyPage);
```

### Response
#### Success Response (200)
Returns the wrapped React component with user authentication.

#### Response Example
(This is a HOC, the response is the protected page component itself)
```json
{
  "user": {
    "sub": "auth0|1234567890abcdef",
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
    // ... other user properties
  }
}
```

#### Type Declaration
```typescript
<P extends object>(Component: ComponentType<P & UserProps>, options?: WithPageAuthRequiredOptions) => React.FC<P>
```

#### Type Parameters
*   `P` extends `object`

#### Parameters
*   `Component`: `ComponentType<P & UserProps>` - The component to protect.
*   `options` (Optional): `WithPageAuthRequiredOptions` - Configuration options for the HOC.

#### Returns
`React.FC<P>` - The protected React functional component.
```

--------------------------------

### Default ID Token Claims

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/variables/server.DEFAULT_ID_TOKEN_CLAIMS.html

Defines the default set of claims included in the ID token for authentication with Auth0 using the Next.js SDK. This is a predefined array of strings.

```typescript
DEFAULT_ID_TOKEN_CLAIMS: string[] = ...
```

--------------------------------

### Handle Access Token in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Processes an incoming NextRequest to handle access token related operations. This function is designed to work within a Next.js environment and returns a Promise resolving to a NextResponse.

```typescript
async handleAccessToken(req: NextRequest): Promise<NextResponse<unknown>> {
    // Implementation details for handling access token
}
```

--------------------------------

### Set Session Cookie - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AbstractSessionStore.html

This TypeScript method `set` adds an encrypted session cookie as a `Set-Cookie` header. It takes request cookies, response cookies, and session data as input. Optionally, it accepts a boolean to indicate if the session is new. The `iat` property on the session data is used to compute the `maxAge` for the cookie.

```typescript
set(
    reqCookies: RequestCookies | ReadonlyRequestCookies,
    resCookies: ResponseCookies,
    session: SessionData,
    isNew?: boolean,
): Promise<void>
```

--------------------------------

### Protect Pages with nextjs-auth0 (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

The `withPageAuthRequired` function is used to protect your Next.js pages from unauthenticated access. It can be used with both the App Router and the Pages Router. This function redirects unauthenticated users to the login page, ensuring that only logged-in users can view protected content.

```typescript
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

export default withPageAuthRequired(function MyPage(props) {
  // ... your page component logic here
  return <div>Protected Page</div>;
});
```

--------------------------------

### OnCallbackContext Type

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.OnCallbackContext.html

The `OnCallbackContext` type alias represents an optional callback context with a `returnTo` property.

```APIDOC
## Type Alias OnCallbackContext

### Description
Represents an optional context passed during callbacks, primarily used to specify a return URL.

### Type Definition

```typescript
type OnCallbackContext = {
    returnTo?: string;
}
```

### Properties

#### `returnTo` (string) - Optional

The URL to redirect the user to after the callback is processed. This property is optional.
```

--------------------------------

### Generate Session Cookie for Testing

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/testing.generateSessionCookie.html

Generates a session cookie string for testing purposes. This function takes a partial session data object and configuration to create a valid cookie that can be used to simulate an authenticated user session in tests. It is part of the testing utilities provided by the SDK.

```typescript
import { SessionData } from "../src/types";
import { GenerateSessionCookieConfig } from "../src/testing/generate-session-cookie";

async function generateSessionCookie(
    session: Partial<SessionData>,
    config: GenerateSessionCookieConfig
): Promise<string>
```

--------------------------------

### AccessTokenForConnectionError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AccessTokenForConnectionError.html

This section details the AccessTokenForConnectionError class, which extends SdkError and is used to represent specific errors encountered when obtaining an access token.

```APIDOC
## AccessTokenForConnectionError Class

### Description

Error class representing an access token for connection error. Extends the `SdkError` class.

### Hierarchy

*   [SdkError](errors.SdkError.html)
    *   AccessTokenForConnectionError

### Constructors

#### constructor

*   `new AccessTokenForConnectionError(code: string, message: string, cause?: OAuth2Error): AccessTokenForConnectionError`

    Constructs a new `AccessTokenForConnectionError` instance.

    #### Parameters

    *   **code** (string) - Required - The error code.
    *   **message** (string) - Required - The error message.
    *   **cause** (OAuth2Error) - Optional - The OAuth2 cause of the error.

### Properties

#### code

*   **code** (string) - Required - The error code associated with the access token error.

#### cause

*   **cause** (OAuth2Error) - Optional - The OAuth2 error that caused this exception.
```

--------------------------------

### CookieOptions Interface Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.CookieOptions.html

Defines the structure for cookie options in @auth0/nextjs-auth0. This interface specifies properties like domain, httpOnly, maxAge, path, sameSite, secure, and transient, along with their types and whether they are optional. It is used for configuring HTTP cookie behavior.

```typescript
interface CookieOptions {
    [domain](#domain)?: string;
    [httpOnly](#httponly): boolean;
    [maxAge](#maxage)?: number;
    [path](#path): string;
    [sameSite](#samesite): "lax" | "strict" | "none";
    [secure](#secure): boolean;
    [transient](#transient)?: boolean;
}
```

--------------------------------

### BackchannelAuthenticationError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationError.html

Details about the BackchannelAuthenticationError class, a specific type of SdkError used for backchannel authentication failures.

```APIDOC
## Class BackchannelAuthenticationError

### Description
Represents an error that occurs during the backchannel authentication process.

### Hierarchy
*   [SdkError](errors.SdkError.html)
    *   BackchannelAuthenticationError

### Constructors

#### new BackchannelAuthenticationError( －namedParameters: { cause?: [OAuth2Error](errors.OAuth2Error.html) } )

*   **Description**: Constructs a new BackchannelAuthenticationError instance.
*   **Parameters**:
    *   `__namedParameters` (object) - An object containing optional named parameters.
        *   `cause` ([OAuth2Error](errors.OAuth2Error.html)) - Optional. The underlying OAuth2 error that caused this exception.
*   **Returns**: `BackchannelAuthenticationError` - A new instance of BackchannelAuthenticationError.

### Properties

#### `Optional` cause : [OAuth2Error](errors.OAuth2Error.html)

*   **Description**: The underlying OAuth2 error that caused this exception.
*   **Type**: [OAuth2Error](errors.OAuth2Error.html) | undefined
*   **Optional**: true

#### code : string

*   **Description**: A string representing the error code. For this error, it is always "backchannel_authentication_error".
*   **Type**: string
*   **Default**: "backchannel_authentication_error"
*   **Overrides**: [SdkError](errors.SdkError.html#code)

### Example Usage (Conceptual)

```javascript
import { BackchannelAuthenticationError } from '@auth0/nextjs-auth0';

try {
  // Some operation that might fail with a backchannel authentication error
  throw new BackchannelAuthenticationError({ cause: { error: 'invalid_request', error_description: 'Missing parameter' } });
} catch (error) {
  if (error instanceof BackchannelAuthenticationError) {
    console.error('Backchannel authentication failed:', error.message);
    console.error('Error code:', error.code);
    if (error.cause) {
      console.error('Underlying cause:', error.cause);
    }
  } else {
    // Handle other types of errors
  }
}
```
```

--------------------------------

### Protect API Routes with nextjs-auth0 (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

The `withApiAuthRequired` function is a higher-order function that wraps your API route handler. It ensures that only authenticated users can access the API endpoint. This is essential for protecting sensitive data or actions. It takes an API route handler as input and returns a new handler that includes authentication checks.

```typescript
import { withApiAuthRequired } from '@auth0/nextjs-auth0';

export const GET = withApiAuthRequired(async function MyApiRoute(req, res) {
  // ... your API logic here
  return res.json({ message: 'Hello from protected API route!' });
});
```

--------------------------------

### SessionData Interface Definition (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionData.html

Defines the structure of session data managed by @auth0/nextjs-auth0. It includes optional connection token sets, internal session metadata (creation timestamp and session ID), the primary token set, and user information. It also supports arbitrary string-keyed properties.

```typescript
interface SessionData {
    [connectionTokenSets](#connectiontokensets)?: [ConnectionTokenSet](types.ConnectionTokenSet.html)[];
    [internal](#internal): { createdAt: number; sid: string };
    [tokenSet](#tokenset): [TokenSet](types.TokenSet.html);
    [user](#user): [User](types.User.html);
    [key: string]: unknown;
}
```

--------------------------------

### OAuth2Error Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.OAuth2Error.html

Details on the OAuth2Error class, its hierarchy, constructors, and properties, emphasizing the need to escape error messages before rendering.

```APIDOC
## OAuth2Error

### Description
Errors that come from Auth0 in the `redirect_uri` callback may contain reflected user input via the OpenID Connect `error` and `error_description` query parameter. You should **not** render the error `message`, or `error` and `error_description` properties without properly escaping them first.

### Hierarchy
*   [SdkError](../modules/errors.html#SdkError)
    *   OAuth2Error

### Constructors
#### constructor( 
    __namedParameters: { code: string; message?: string }
): OAuth2Error

*   **Parameters**
    *   `__namedParameters` {object} - Required. An object containing:
        *   `code` (string) - The error code.
        *   `message` (string) - Optional. A more detailed error message.

*   **Returns**
    OAuth2Error - An instance of OAuth2Error.

### Properties
#### code
*   code: string

Overrides [SdkError](errors.SdkError.html#code).

### Example Usage (Conceptual)
```typescript
// Assuming an error occurs during authentication redirect
try {
  // some authentication logic that might throw an OAuth2Error
} catch (error) {
  if (error instanceof OAuth2Error) {
    console.error('OAuth2 Error Code:', error.code);
    // It's crucial to sanitize or escape error.message before displaying to the user
    const safeErrorMessage = sanitize(error.message);
    console.error('OAuth2 Error Message:', safeErrorMessage);
  } else {
    console.error('An unexpected error occurred:', error);
  }
}

function sanitize(message: string): string {
  // Implement proper HTML escaping or sanitization logic here
  // For example, using a library like DOMPurify or simple string replacement
  return message.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
```
```

--------------------------------

### AppRouterPageRouteOpts Type Definition (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.AppRouterPageRouteOpts.html

Defines the structure for route and search parameters within Next.js App Router pages. It includes optional promises for 'params' and 'searchParams', which can resolve to key-value string pairs or arrays of strings.

```typescript
type AppRouterPageRouteOpts = {
    params?: Promise<Record<string, string | string[]>>;
    searchParams?: Promise<{ [key: string]: undefined | string | string[] }>;
}
```

--------------------------------

### Customize withPageAuthRequired Redirecting Message

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/client.WithPageAuthRequiredOptions.html

Allows developers to render a custom message while the user is being redirected. This is useful for providing visual feedback during the authentication flow.

```javascript
withPageAuthRequired(Profile, {
  onRedirecting: () => <div>Redirecting...</div>
});
```

--------------------------------

### TypeScript Interface: TransactionState

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionState.html

Defines the structure for managing authentication transaction states in the Auth0 Next.js SDK. It includes properties like codeVerifier, nonce, responseType, returnTo, and an optional maxAge. This interface is inherited from JWTPayload and can accept additional arbitrary properties.

```typescript
interface TransactionState {
    [codeVerifier: string];
    [maxAge: number]?: number;
    [nonce: string];
    [responseType: string];
    [returnTo: string];
    [state: string];
    [propName: string]: unknown;
}
```

--------------------------------

### InvalidStateError Class Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.InvalidStateError.html

This TypeScript code defines the InvalidStateError class, which extends SdkError. It includes a constructor that accepts an optional message and a 'code' property initialized to 'invalid_state'. This error is used to handle specific state-related errors during authentication flows.

```typescript
class InvalidStateError extends SdkError {
  code: string = "invalid_state";

  constructor(message?: string) {
    super(message);
  }
}
```

--------------------------------

### BackchannelAuthenticationNotSupportedError Code Property

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationNotSupportedError.html

The 'code' property of the BackchannelAuthenticationNotSupportedError class. This string value uniquely identifies this specific type of error, 'backchannel_authentication_not_supported_error'. It is inherited and overridden from the parent SdkError class.

```typescript
code: string = "backchannel_authentication_not_supported_error"
```

--------------------------------

### GetServerSidePropsResultWithSession

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.GetServerSidePropsResultWithSession.html

Augments `getServerSideProps` with user session information when using `withPageAuthRequired`.

```APIDOC
## GetServerSidePropsResultWithSession

### Description
Type alias representing the result of `getServerSideProps` when augmented by `withPageAuthRequired`. It includes the original props plus the authenticated user object.

### Method
N/A (Type Alias)

### Endpoint
N/A (Type Alias)

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
N/A

### Response
#### Success Response (200)
- **props** (object) - The original props object augmented with a `user` field of type `User`.
- **user** (User) - The authenticated user object.

#### Response Example
```json
{
  "props": {
    "someOriginalProp": "value",
    "user": {
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
  }
}
```
```

--------------------------------

### Define AuthorizationCodeGrantError Class - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantError.html

Defines the AuthorizationCodeGrantError class, which extends SdkError. It includes a constructor that accepts an OAuth2Error cause and an optional message, and it has a fixed error code 'authorization_code_grant_error'.

```typescript
export declare class AuthorizationCodeGrantError extends SdkError {
    cause: OAuth2Error;
    code: string;
    constructor(__namedParameters: { cause: OAuth2Error; message?: string });
}
```

--------------------------------

### AppRouterPageRouteOpts Type Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.AppRouterPageRouteOpts.html

Defines the structure for route and search parameters available in Next.js App Router pages. This type is used to provide route and search parameters to page components.

```APIDOC
## AppRouterPageRouteOpts

### Description
Objects containing the route parameters and search parameters of the page.

### Type Definition
```typescript
type AppRouterPageRouteOpts = {
    params?: Promise<Record<string, string | string[]>>;
    searchParams?: Promise<{ [key: string]: undefined | string | string[] }>;
}
```

### Properties

#### `params` (Optional)
- **Type**: `Promise<Record<string, string | string[]>>`
- **Description**: A promise that resolves to an object containing route parameters. Keys are parameter names, and values can be strings or arrays of strings.

#### `searchParams` (Optional)
- **Type**: `Promise<{ [key: string]: undefined | string | string[] }>`
- **Description**: A promise that resolves to an object containing search parameters. Keys are parameter names, and values can be undefined, strings, or arrays of strings.
```

--------------------------------

### TypeScript OnCallbackHook Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.OnCallbackHook.html

Defines the signature for the OnCallbackHook, a function that processes authentication callbacks. It accepts an optional error, context object, and session data, returning a Promise that resolves to a NextResponse. This is crucial for customizing authentication flows.

```typescript
type OnCallbackHook = (
    error: SdkError | null,
    ctx: OnCallbackContext,
    session: SessionData | null,
) => Promise<NextResponse>
```

--------------------------------

### Set Session by ID - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

Implements the 'set' method for the SessionDataStore interface. This function is used to insert or update session data in the store, identified by a session ID. It takes the session ID and the SessionData object as arguments and returns a Promise that resolves upon successful upsert.

```typescript
set(id: string, session: SessionData): Promise<void>
```

--------------------------------

### Session Configuration Property: cookie

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

Allows customization of the session cookie by providing an object of SessionCookieOptions. This enables fine-grained control over cookie attributes like name, domain, and path.

```typescript
cookie?: [SessionCookieOptions](types.SessionCookieOptions.html);
```

--------------------------------

### Define TokenSet Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TokenSet.html

This TypeScript interface defines the structure for a TokenSet object, commonly used in authentication flows. It includes required properties like accessToken and expiresAt, and optional properties such as idToken, refreshToken, and scope.

```typescript
interface TokenSet {
    accessToken: string;
    expiresAt: number;
    idToken?: string;
    refreshToken?: string;
    scope?: string;
}
```

--------------------------------

### Finalize User Session

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.AuthClient.html

Processes and filters session data, potentially including an ID token. It allows for custom session manipulation via a `beforeSessionSaved` callback or applies default filtering to ID token claims.

```typescript
finalizeSession(session: SessionData, idToken?: string): Promise<SessionData>
```

--------------------------------

### Define TypeScript RoutesOptions Type Alias

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.RoutesOptions.html

This TypeScript code defines the RoutesOptions type alias. It is a partial pick of specific properties ('login', 'callback', 'logout', 'backChannelLogout') from the Routes interface, allowing for flexible configuration of authentication routes.

```typescript
type RoutesOptions = Partial<
    Pick<Routes, "login" | "callback" | "logout" | "backChannelLogout">
>
```

--------------------------------

### DiscoveryError Code Property

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.DiscoveryError.html

This TypeScript code snippet shows the 'code' property of the DiscoveryError class. It is a string with a fixed value of 'discovery_error' and overrides the 'code' property inherited from the SdkError class.

```typescript
code: string = "discovery_error"

/**
 * Overrides the base SdkError code property.
 */
code: string
```

--------------------------------

### BackchannelAuthenticationError Properties (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.BackchannelAuthenticationError.html

Details the properties of the BackchannelAuthenticationError class. It includes an optional 'cause' property to hold the underlying OAuth2Error and a 'code' property, which is a string literal 'backchannel_authentication_error'.

```typescript
cause?: OAuth2Error;
code: string = "backchannel_authentication_error";
```

--------------------------------

### PageRoute Type Alias

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.PageRoute.html

Defines a page route that has been augmented with WithPageAuthRequired, providing session information to server-side props.

```APIDOC
## PageRoute Type Alias

### Description
A page route that has been augmented with [WithPageAuthRequired](server.WithPageAuthRequired.html).

### Type Parameters
* P
* Q extends ParsedUrlQuery = ParsedUrlQuery

### Type Declaration
* (ctx: GetServerSidePropsContext<[Q](#q)>): Promise<[GetServerSidePropsResultWithSession](server.GetServerSidePropsResultWithSession.html)<[P](#p)>>
    * ### Parameters
        * ctx: GetServerSidePropsContext<[Q](#q)> - The context for server-side rendering, including session information.
    * ### Returns
        Promise<[GetServerSidePropsResultWithSession](server.GetServerSidePropsResultWithSession.html)<[P](#p)>> - A promise that resolves to the server-side props result with session data.

### Defined in
src/server/helpers/with-page-auth-required.ts:33
```

--------------------------------

### updateSession (Pages Router)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Updates the session of the currently authenticated user. This method is designed for use within the Pages Router of Next.js, including `getServerSideProps` and API routes.

```APIDOC
## updateSession (Pages Router)

### Description
Updates the session of the currently authenticated user. If the user does not have a session, an error is thrown. This method is intended for use in middleware and `getServerSideProps`, API routes, and middleware in the **Pages Router**.

### Method
POST (or other methods depending on context)

### Endpoint
Relevant endpoint within the application's Pages Router structure.

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **req** (NextRequest | PagesRouterRequest) - Required - The incoming Next.js request object.
- **res** (NextResponse | PagesRouterResponse) - Required - The outgoing Next.js response object.
- **session** (SessionData) - Required - The session data to update.

### Request Example
```typescript
import { updateSession } from '@auth0/nextjs-auth0';

// Example in getServerSideProps
export async function getServerSideProps(context) {
  const session = await getSession(context.req);
  if (!session) {
    return { props: { user: null } };
  }

  const updatedSessionData = { ...session.user, customField: 'newValue' };

  await updateSession(context.req, context.res, updatedSessionData);

  return {
    props: { user: session.user },
  };
}
```

### Response
#### Success Response (200)
- **void** - The function returns a promise that resolves to void upon successful session update.

#### Response Example
(This function modifies the response object in place and returns a promise that resolves to void. No specific JSON response body is returned by this function itself.)
```

--------------------------------

### Define OnCallbackContext Type - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.OnCallbackContext.html

This TypeScript code defines a type alias named 'OnCallbackContext'. It's designed to represent an object that may contain a 'returnTo' property, which is an optional string. This is commonly used in authentication flows to specify a redirect URL after a callback.

```typescript
type OnCallbackContext = {
  [returnTo](#returnto)?: string;
}
```

--------------------------------

### Update User Session (Pages Router / App Router) (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.Auth0Client.html

Updates the session data for the currently authenticated user. This function has different signatures depending on whether it's used within the Pages Router (requiring request and response objects) or the App Router (Server Actions/Route Handlers).

```typescript
import { NextRequest, NextResponse } from "next/server";
import { PagesRouterRequest, PagesRouterResponse, SessionData } from "./types";

// For Pages Router
async function updateSession(req: NextRequest | PagesRouterRequest, res: NextResponse | PagesRouterResponse, session: SessionData): Promise<void>

// For App Router
async function updateSession(session: SessionData): Promise<void>
```

--------------------------------

### SessionCookieOptions Interface Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionCookieOptions.html

Defines the structure for configuring session cookie options. This interface allows customization of domain, name, path, sameSite attribute, secure flag, and transient nature of the cookie. It is used in the @auth0/nextjs-auth0 library for managing user sessions.

```typescript
interface SessionCookieOptions {
    [domain](#domain)?: string;
    [name](#name)?: string;
    [path](#path)?: string;
    [sameSite](#samesite)?: "lax" | "strict" | "none";
    [secure](#secure)?: boolean;
    [transient](#transient)?: boolean;
}
```

--------------------------------

### AuthorizationError Class

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationError.html

The AuthorizationError class represents an error that occurs during the authorization process. It extends the SdkError class and includes specific properties related to OAuth2 errors.

```APIDOC
## Class AuthorizationError

### Description
Represents an error that occurs during the authorization process. It extends the SdkError class and includes specific properties related to OAuth2 errors.

### Hierarchy
* [SdkError](errors.SdkError.html)
    * AuthorizationError

### Constructors

#### new AuthorizationError( 
    										__namedParameters: { cause: [OAuth2Error](errors.OAuth2Error.html); message?: string },  
    ): AuthorizationError

*   **Parameters**
    *   `__namedParameters` (object) - An object containing:
        *   `cause` ([OAuth2Error](errors.OAuth2Error.html)) - The underlying OAuth2 error.
        *   `message` (string, optional) - A custom error message.

*   **Returns**
    AuthorizationError - An instance of the AuthorizationError.

### Properties

#### cause

*   **cause** (OAuth2Error) - The underlying OAuth2 error that caused this authorization error.

#### code

*   **code** (string) -  The error code, which is fixed to "authorization_error".
    *   Overrides [SdkError.code](errors.SdkError.html#code)
    *   Default value: "authorization_error"
```

--------------------------------

### SessionConfiguration Interface Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

Defines the structure for session configuration, including optional properties for absolute duration, cookie settings, inactivity duration, and rolling session behavior. This interface is crucial for customizing how user sessions are managed within the Next.js application.

```typescript
interface SessionConfiguration {
    [absoluteDuration](#absoluteduration)?: number;
    [cookie](#cookie)?: [SessionCookieOptions](types.SessionCookieOptions.html);
    [inactivityDuration](#inactivityduration)?: number;
    [rolling](#rolling)?: boolean;
}
```

--------------------------------

### Define AuthorizationParameters Interface in TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.AuthorizationParameters.html

This TypeScript code defines the AuthorizationParameters interface, which is used to configure authorization requests in the @auth0/nextjs-auth0 library. It includes optional properties for audience, max_age, organization, redirect_uri, scope, and allows for additional custom parameters.

```typescript
interface AuthorizationParameters {
    [audience](#audience)?: null | string;
    [max_age](#max_age)?: number;
    [organization](#organization)?: string;
    [redirect_uri](#redirect_uri)?: null | string;
    [scope](#scope)?: null | string;
    [key: string]: unknown;
}
```

--------------------------------

### Define TransactionCookieOptions Interface (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.TransactionCookieOptions.html

Defines the structure for configuring transaction cookie options. This interface allows specifying attributes such as domain, maximum age, path, prefix, SameSite policy, and security for cookies used to store transaction state. It is defined in 'src/server/transaction-store.ts'.

```typescript
interface TransactionCookieOptions {
    [domain](#domain)?: string;
    [maxAge](#maxage)?: number;
    [path](#path)?: string;
    [prefix](#prefix)?: string;
    [sameSite](#samesite)?: "lax" | "strict" | "none";
    [secure](#secure)?: boolean;
}
```

--------------------------------

### LogoutToken Type Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.LogoutToken.html

Defines the structure for a LogoutToken, used within the Auth0 Next.js SDK.

```APIDOC
## Type Alias: LogoutToken

### Description
Represents a token used for logout operations within the Auth0 Next.js SDK.

### Type Definition

```typescript
type LogoutToken = {
    sid?: string;
    sub?: string;
}
```

### Properties

#### sid
- **sid** (string) - Optional - The session ID.

#### sub
- **sub** (string) - Optional - The subject identifier.

### Source
Defined in `src/types/index.ts:52`
https://github.com/auth0/nextjs-auth0/blob/88edf0e2f7c1f113c01064c7a3856870baa646bc/src/types/index.ts#L52
```

--------------------------------

### OAuth2Error Class Properties - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.OAuth2Error.html

Details the 'code' property of the OAuth2Error class. This property is a string representing the error code and overrides the 'code' property inherited from the SdkError base class.

```typescript
code: string
```

--------------------------------

### AppRouterPageRoute Type Declaration - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.AppRouterPageRoute.html

Defines the AppRouterPageRoute type, which is a function that takes AppRouterPageRouteOpts and returns a Promise of a React JSX Element. This is used in server-side route handling.

```typescript
type AppRouterPageRoute = (obj: AppRouterPageRouteOpts) => Promise<React.JSX.Element>
```

--------------------------------

### AuthorizationCodeGrantRequestError Code Property

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationCodeGrantRequestError.html

Defines the static error code for the AuthorizationCodeGrantRequestError class. This property is a string representing the specific type of error, 'authorization_code_grant_request_error', and overrides the code from the base SdkError class.

```typescript
code: string = "authorization_code_grant_request_error"
```

--------------------------------

### AccessTokenError Properties - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AccessTokenError.html

The AccessTokenError class has properties for 'code' (string) and an optional 'cause' (OAuth2Error). The 'code' property is inherited and overridden from the parent SdkError class. The 'cause' property provides additional details about the underlying OAuth2 error.

```typescript
cause?: OAuth2Error
code: string
```

--------------------------------

### AuthorizationError Properties - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/errors.AuthorizationError.html

Defines the properties of the AuthorizationError class. It includes a 'cause' property of type OAuth2Error and a 'code' property, which is a string with a default value of 'authorization_error'. These properties override those from the parent SdkError class.

```typescript
cause: OAuth2Error
code: string = "authorization_error"
```

--------------------------------

### PageRoute Type Declaration with Session Data - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/server.PageRoute.html

Defines a server-side page route that is augmented with session data using Auth0's authentication helpers. It takes a GetServerSidePropsContext and returns a Promise of GetServerSidePropsResultWithSession, including the authenticated user's session. This is crucial for accessing user information within Next.js server-side rendering.

```typescript
type PageRoute<P, Q> = (
    ctx: GetServerSidePropsContext<Q>,
) => Promise<GetServerSidePropsResultWithSession<P>>;
```

--------------------------------

### Define GenerateSessionCookieConfig Type - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/testing.GenerateSessionCookieConfig.html

This TypeScript code defines the `GenerateSessionCookieConfig` type alias. It requires a `secret` property of type string, which is used to derive an encryption key for session cookies. The secret must match the SDK configuration.

```typescript
type GenerateSessionCookieConfig = {
    [secret]: string;
}
```

--------------------------------

### Save Transaction State - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

Saves the transaction state to an encrypted cookie. It accepts the response cookies object, the transaction state to save, and an optional request cookies object. This method is crucial for maintaining authentication session data across requests.

```typescript
save(
    resCookies: ResponseCookies,
    transactionState: TransactionState,
    reqCookies?: RequestCookies
): Promise<void>
```

--------------------------------

### withPageAuthRequired Function Definition (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/variables/client.withPageAuthRequired.html

This TypeScript snippet shows the definition of the `withPageAuthRequired` constant, which is typed as `WithPageAuthRequired`. This is a core part of the client-side authentication flow in Next.js applications using Auth0, ensuring pages are protected.

```typescript
withPageAuthRequired: WithPageAuthRequired = ...
```

--------------------------------

### Session Configuration Property: rolling

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

A boolean flag to enable or disable rolling sessions. When true, the session is extended based on activity within the inactivity duration, up to the absolute duration limit. Defaults to true.

```typescript
rolling?: boolean;
```

--------------------------------

### Delete Session by Logout Token - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

Implements the optional 'deleteByLogoutToken' method for the SessionDataStore interface. This function allows for session deletion using a logout token, which may contain either a session ID, a user ID, or both. It returns a Promise indicating the completion of the deletion process.

```typescript
deleteByLogoutToken?(logoutToken: LogoutToken): Promise<void>
```

--------------------------------

### Delete All Transaction Cookies - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

Deletes all transaction cookies based on the configured prefix. This method is essential for cleaning up authentication state when a session ends or is invalidated, ensuring security and proper resource management.

```typescript
deleteAll(
    reqCookies: RequestCookies,
    resCookies: ResponseCookies,
): Promise<void>
```

--------------------------------

### Session Configuration Property: inactivityDuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

Defines the session expiration time in seconds based on user inactivity. The session will be extended as long as there's activity before this duration is met. The default is 1 day.

```typescript
inactivityDuration?: number;
```

--------------------------------

### AccessTokenForConnectionErrorCode Enum Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/enums/errors.AccessTokenForConnectionErrorCode.html

Defines the enumeration members for access token-related errors in Auth0 connections. These codes help in identifying specific failure reasons, such as missing session, missing refresh tokens, or failures during token exchange.

```typescript
export enum AccessTokenForConnectionErrorCode {
  MISSING_SESSION = "missing_session",
  MISSING_REFRESH_TOKEN = "missing_refresh_token",
  FAILED_TO_EXCHANGE = "failed_to_exchange_refresh_token"
}
```

--------------------------------

### OnCallbackHook Type

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.OnCallbackHook.html

The OnCallbackHook is a type alias representing a function that can be used as a callback hook in the Auth0 Next.js SDK. It allows custom logic to be executed during the authentication callback process.

```APIDOC
## OnCallbackHook Type Definition

### Description
Represents a callback function executed during the authentication callback process. It receives error information, the callback context, and session data, and should return a Promise resolving to a NextResponse.

### Type Declaration

```typescript
(error: SdkError | null, ctx: OnCallbackContext, session: SessionData | null) => Promise<NextResponse>
```

### Parameters

*   **error** (SdkError | null) - An error object if an error occurred during the authentication process, otherwise null.
*   **ctx** (OnCallbackContext) - The context object for the callback, containing relevant information.
*   **session** (SessionData | null) - The session data if the user is authenticated, otherwise null.

### Returns

A Promise that resolves to a `NextResponse` object.

### Source Location

Defined in `src/server/auth-client.ts:58`
```

--------------------------------

### Delete Session by ID - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionDataStore.html

Implements the 'delete' method for the SessionDataStore interface. This function is responsible for destroying a session using its unique session ID. It returns a Promise that resolves when the session is successfully deleted.

```typescript
delete(id: string): Promise<void>
```

--------------------------------

### BeforeSessionSavedHook Type

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.BeforeSessionSavedHook.html

Documentation for the BeforeSessionSavedHook type alias, which is a function that can be used to modify session data before it is saved.

```APIDOC
## BeforeSessionSavedHook

### Description
A hook that can be used to modify session data before it is saved. It receives the current session data and the ID token, and should return the modified session data.

### Type Alias

`BeforeSessionSavedHook`

### Parameters

*   **session** ([`SessionData`](../interfaces/types.SessionData.html)) - The current session data.
*   **idToken** (string | null) - The ID token associated with the session.

### Returns

Promise<[`SessionData`](../interfaces/types.SessionData.html)> - A promise that resolves with the modified session data.

### Source

*   Defined in `src/server/auth-client.ts:50`
```

--------------------------------

### AccessTokenErrorCode Enumeration Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/enums/errors.AccessTokenErrorCode.html

Defines the possible error codes for access token related operations within the @auth0/nextjs-auth0 library. This enumeration is used to provide specific feedback when issues arise during token refresh or session handling.

```typescript
export declare enum AccessTokenErrorCode {
    MISSING_SESSION = "missing_session",
    MISSING_REFRESH_TOKEN = "missing_refresh_token",
    FAILED_TO_REFRESH_TOKEN = "failed_to_refresh_token"
}
```

--------------------------------

### Session Configuration Property: absoluteDuration

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/interfaces/types.SessionConfiguration.html

Sets the maximum duration for a session in seconds. Once this time is reached, the session will expire regardless of user activity. The default value is 3 days.

```typescript
absoluteDuration?: number;
```

--------------------------------

### Filter Default ID Token Claims (TypeScript)

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/functions/server.filterDefaultIdTokenClaims.html

Filters an object of claims to retain only those considered default ID token claims. This function is typically used in server-side authentication flows to process user identity information. It takes a claims object as input and returns an array of user objects representing the filtered claims. It is defined in `src/server/user.ts`.

```typescript
function filterDefaultIdTokenClaims(claims: { [key: string]: any }): User[]
```

--------------------------------

### TypeScript LogoutToken Type Definition

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.LogoutToken.html

Defines the LogoutToken type alias for logout operations. It includes optional string properties for 'sid' (session ID) and 'sub' (subject identifier). This type is crucial for handling authenticated session data during the logout process.

```typescript
type LogoutToken = {
    [sid](#sid)?: string;
    [sub](#sub)?: string;
}
```

--------------------------------

### Define SUBJECT_TYPE_ACCESS_TOKEN - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/enums/types.SUBJECT_TOKEN_TYPES.html

Defines the SUBJECT_TYPE_ACCESS_TOKEN constant, representing an OAuth 2.0 access token. This constant is used within the @auth0/nextjs-auth0 library to specify the type of token being handled. It adheres to RFC 8693 standards.

```typescript
SUBJECT_TYPE_ACCESS_TOKEN: "urn:ietf:params:oauth:token-type:access_token"
```

--------------------------------

### Define BeforeSessionSavedHook for Session Modification

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.BeforeSessionSavedHook.html

The BeforeSessionSavedHook is a type alias for a function that intercepts and modifies session data before it is persisted. It takes the current session data and an ID token as input and must return a Promise resolving to the updated session data. This allows for custom logic such as adding user claims or modifying session properties.

```typescript
type BeforeSessionSavedHook = (
  session: SessionData,
  idToken: string | null
) => Promise<SessionData>
```

--------------------------------

### LogoutStrategy Type Alias Definition - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.LogoutStrategy.html

Defines the LogoutStrategy type alias, which specifies the possible string literal values ('auto', 'oidc', 'v2') that control the logout endpoint selection. This is used within the @auth0/nextjs-auth0 library for authentication and authorization flows.

```typescript
type LogoutStrategy = "auto" | "oidc" | "v2";
```

--------------------------------

### Define SUBJECT_TYPE_REFRESH_TOKEN - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/enums/types.SUBJECT_TOKEN_TYPES.html

Defines the SUBJECT_TYPE_REFRESH_TOKEN constant, representing an OAuth 2.0 refresh token. This constant is utilized in the @auth0/nextjs-auth0 library for managing refresh tokens and complies with RFC 8693 specifications.

```typescript
SUBJECT_TYPE_REFRESH_TOKEN: "urn:ietf:params:oauth:token-type:refresh_token"
```

--------------------------------

### Define ReadonlyRequestCookies Type Alias

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/types/types.ReadonlyRequestCookies.html

This TypeScript code defines a type alias called ReadonlyRequestCookies. It creates a read-only version of RequestCookies by omitting certain mutable methods ('set', 'clear', 'delete') and then re-introducing 'set' and 'delete' from ResponseCookies. This is useful for enforcing immutability on cookies in request contexts while still allowing specific modifications.

```typescript
type ReadonlyRequestCookies = Omit<RequestCookies, "set" | "clear" | "delete"> & Pick<ResponseCookies, "set" | "delete">;
```

--------------------------------

### Delete Single Transaction Cookie - TypeScript

Source: https://github.com/auth0/nextjs-auth0/blob/main/docs/classes/server.TransactionStore.html

Deletes a single transaction cookie associated with a specific state. This method is used to invalidate individual authentication states, commonly employed during logout or specific transaction finalization steps.

```typescript
delete(resCookies: ResponseCookies, state: string): Promise<void>
```

=== COMPLETE CONTENT === This response contains all available snippets from this library. No additional content exists. Do not make further requests.