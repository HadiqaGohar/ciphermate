### Setup Auth0 CLI and Environment

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Installs the Auth0 CLI and runs the quickstart setup command to generate environment variables for a Vite project.

```bash
brew tap auth0/auth0-cli && brew install auth0
auth0 qs setup --type vite -n "My App" -p 5173
```

```powershell
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Define and Install Project Dependencies

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Defines the required packages in requirements.txt and provides the command to install them using pip.

```text
auth0-server-python>=1.0.0b7
flask[async]>=2.0.0
python-dotenv>=1.0.0
```

```shell
pip install -r requirements.txt
```

--------------------------------

### Install Dependencies and Manage Environments

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Commands for installing necessary Flask async support and activating virtual environments to resolve common runtime and module errors.

```bash
pip install "flask[async]"
```

```bash
source venv/bin/activate
```

--------------------------------

### Installing Redis and Connect-Redis for Custom Session Store

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This command installs the necessary packages, `redis` and `connect-redis`, to implement a custom session store using Redis. This is recommended for production environments.

```bash
npm install redis connect-redis
```

--------------------------------

### Start Flask Development Server

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Executes the Flask application entry point to start the development server at http://localhost:5000.

```bash
python app.py
```

--------------------------------

### Install Dependencies and Run Application (npm)

Source: https://auth0.com/docs/secure/data-privacy-and-compliance/gdpr/gdpr-track-consent-with-lock

This snippet demonstrates the basic commands to install project dependencies and start the application using npm. It's a common starting point for Node.js projects.

```text
npm install
npm run
```

--------------------------------

### Install Auth0 Python SDK

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Installs the Auth0 server SDK for Python and necessary dependencies like Flask and python-dotenv. Ensure you have Python and pip installed.

```bash
pip install auth0-server-python "flask[async]" python-dotenv
```

--------------------------------

### Setup App Component with Auth0Provider

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

Demonstrates how to set up the main `App.js` component using the `Auth0Provider` for a hooks-based implementation. This example includes functions for handling login (`authorize`) and logout (`clearSession`), utilizing the `useAuth0` hook to access authentication state and methods. It also shows conditional rendering based on the loading state.

```javascript
import React from 'react';
import {Auth0Provider, useAuth0} from 'react-native-auth0';
import {
  StyleSheet,
  Text,
  View,
  Button,
  Image,
  ActivityIndicator,
} from 'react-native';

function HomeScreen() {
  const {authorize, clearSession, user, isLoading} = useAuth0();

  const handleLogin = async () => {
    try {
      await authorize({customScheme: 'auth0sample', scope: 'openid profile email'});
    } catch (e) {
      console.error('Login error:', e);
    }
  };

  const handleLogout = async () => {
    try {
      await clearSession({customScheme: 'auth0sample'});
    } catch (e) {
      console.error('Logout error:', e);
    }
  };

  if (isLoading) {

```

--------------------------------

### Install Auth0 Dependencies and Configure package.json

Source: https://auth0.com/docs/quickstart/backend/fastify

Install the necessary Auth0 and Fastify packages and configure the package.json file with start scripts and dependencies.

```shellscript
npm install @auth0/auth0-fastify-api fastify dotenv
```

```json
{
  "name": "auth0-fastify-api",
  "version": "1.0.0",
  "type": "module",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "node --watch server.js"
  },
  "dependencies": {
    "@auth0/auth0-fastify-api": "^1.2.0",
    "dotenv": "^16.3.1",
    "fastify": "^5.0.0"
  }
}
```

--------------------------------

### Example .env file for Auth0 Configuration

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This is an example of the .env file required for Auth0 integration. It includes placeholders for the Auth0 domain, client ID, a securely generated secret, and the base URL for the application.

```env
ISSUER_BASE_URL=https://YOUR_AUTH0_DOMAIN
CLIENT_ID=YOUR_CLIENT_ID
SECRET=use-a-long-random-string-at-least-32-characters
BASE_URL=http://localhost:3000
```

--------------------------------

### Install Auth0 Hono Dependencies

Source: https://auth0.com/docs/quickstart/webapp/hono

Installs the necessary Auth0 Hono middleware package. It also shows how to install the dotenv package for managing environment variables, or alternatively, how to use Node.js's --env-file flag.

```shellscript
npm install @auth0/auth0-hono

npm install -D dotenv
```

--------------------------------

### Install Auth0 Agent Skills using npm

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

This command installs the Auth0 agent skills for quickstart and Angular integration using npm. Ensure you have Node.js and npm installed.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-angular

```

--------------------------------

### Get Auth0 MCP Server Command Line Help

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command displays a list of all available commands and usage examples for the Auth0 MCP Server. It's useful for understanding the full range of functionalities and how to use them.

```javascript
npx @auth0/auth0-mcp-server help
```

--------------------------------

### Verify Node.js and npm Installation

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

This command verifies the installed versions of Node.js and npm. Ensure you meet the prerequisites for the Auth0 integration.

```bash
node --version && npm --version

```

--------------------------------

### Initialize and Configure Project

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Commands to create a project directory, initialize npm, install Vite, and configure project scripts for development and building.

```bash
mkdir auth0-vanillajs && cd auth0-vanillajs
npm init -y && npm install --save-dev vite && npm pkg set scripts.dev="vite" scripts.build="vite build" scripts.preview="vite preview" type="module"
```

--------------------------------

### Install Nodemon for Development

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Installs nodemon as a development dependency. Nodemon automatically restarts the Node.js application when file changes are detected, which is useful during development.

```bash
npm install --save-dev nodemon
```

--------------------------------

### Define Environment Variables

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Example configuration for the .env.local file containing Auth0 domain and client ID credentials.

```text
VITE_AUTH0_DOMAIN={yourDomain} VITE_AUTH0_CLIENT_ID={yourClientId}
```

--------------------------------

### Configure Package.json for Environment Variables

Source: https://auth0.com/docs/quickstart/webapp/hono

Modifies the 'start' script in package.json to use the --env-file flag for loading environment variables from a .env file. This avoids the need to explicitly install and import the dotenv package.

```json
{
  "scripts": {
    "start": "node --env-file=.env dist/index.js"
  }
}
```

--------------------------------

### Main Application Setup in Go

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

Sets up the main application entry point. It loads environment variables using 'godotenv', initializes the 'authenticator', creates a new router using the 'router' package, and starts the HTTP server. It logs any fatal errors during these processes.

```go
package main

import (
	"log"
	"net/http"

	"github.com/joho/godotenv"

	"01-Login/platform/authenticator"
	"01-Login/platform/router"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}

```

--------------------------------

### Install Auth0 CLI on macOS

Source: https://auth0.com/docs/quickstart/spa

Installs the Auth0 CLI on macOS using Homebrew. This command is part of the manual setup process for an Auth0 application and allows for command-line management of Auth0 resources.

```bash
# Install Auth0 CLI (if not already installed)
brew tap auth0/auth0-cli && brew install auth0
```

--------------------------------

### Install Auth0 CLI

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Commands to install the Auth0 CLI tool on macOS using Homebrew for automated project setup.

```bash
brew tap auth0/auth0-cli && brew install auth0
```

--------------------------------

### Create Expo Project

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

Initializes a new Expo project for the quickstart. This command creates a minimal Expo app with the latest SDK, suitable for native module integration. The `--template blank` flag ensures a clean starting point without extra boilerplate. Note that this SDK is not compatible with Expo Go and requires a development build.

```bash
npx create-expo-app Auth0ExpoSample --template blank
cd Auth0ExpoSample
```

--------------------------------

### Project Initialization and Setup (Shell)

Source: https://auth0.com/docs/quickstart/spa/vanillajs

Commands to create a new JavaScript project directory, initialize npm, install Vite for development, and set up project scripts. It also includes commands for creating essential project files like index.html, app.js, and style.css across different operating systems.

```shellscript
mkdir auth0-vanillajs && cd auth0-vanillajs
npm init -y && npm install --save-dev vite && npm pkg set scripts.dev="vite" scripts.build="vite build" scripts.preview="vite preview" type="module"
```

```shellscript
touch index.html app.js style.css
```

```powershell
New-Item -ItemType File -Path index.html, app.js, style.css
```

--------------------------------

### Example .env.local file for Auth0 configuration

Source: https://auth0.com/docs/quickstart/webapp/nextjs/interactive

This is an example of the .env.local file generated by the Auth0 CLI setup command. It contains placeholders for Auth0 domain, client ID, client secret, and application base URL.

```env
AUTH0_DOMAIN=YOUR_AUTH0_APP_DOMAIN
AUTH0_CLIENT_ID=YOUR_AUTH0_APP_CLIENT_ID
AUTH0_CLIENT_SECRET=YOUR_AUTH0_APP_CLIENT_SECRET
AUTH0_SECRET=YOUR_LONG_RANDOM_SECRET_HERE
APP_BASE_URL=http://localhost:3000
```

--------------------------------

### Quickstart Guides Navigation

Source: https://auth0.com/docs/fr-ca

Renders a navigation section with links to quickstart guides for different platforms and technologies. It maps an array of language objects to clickable cards, each displaying an icon and the language label.

```javascript
export const QuickstartNav = () => {
  const languages = [{
    img: "nextjs.svg",
    label: "Next.js",
    href: "/docs/quickstart/webapp/nextjs"
  }, {
    img: "apple.svg",
    label: "iOS",
    href: "/docs/quickstart/native/ios-swift"
  }, {
    img: "android.svg",
    label: "Android",
    href: "/docs/quickstart/native/android"
  }, {
    img: "java.svg",
    label: "Java",
    href: "/docs/quickstart/backend/java-spring-security5/interactive"
  }, {
    img: "dotnet.svg",
    label: ".NET",
    href: "/docs/quickstart/backend/aspnet-core-webapi"
  }, {
    img: "python.svg",
    label: "Python",
    href: "/docs/quickstart/backend/python"
  }];
  return <section className="max-w-[962px] mx-auto py-12 px-8 lg:px-0">
      <h2 className="font-inter !font-medium text-[24px] text-gray-900 dark:text-white mb-6">
        Get started with authentication
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {languages.map((lang, idx) => <a key={idx} href={lang.href} className="flex flex-col items-center justify-center px-8 py-4 rounded-2xl 
                      bg-white/60 dark:bg-neutral-900/60 
                      border border-gray-200 dark:border-white/10 
                      shadow-sm hover:shadow-md 
                      hover:border-black dark:hover:border-white 
                      transition">
            <img noZoom src={`/docs/images/icons/light/${lang.img}`} alt={lang.label} className="h-8 w-8 mb-4 block dark:hidden" />
            <img noZoom src={`/docs/images/icons/dark/${lang.img}`} alt={lang.label} className="h-8 w-8 mb-4 hidden dark:block" />
            <span className="font-inter text-base text-gray-900 dark:text-white">{lang.label}</span>
          </a>)}
      </div>
    </section>;
};

```

--------------------------------

### Install Express and Auth0 SDK

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Installs the necessary npm packages for an Express.js application with Auth0 authentication. This includes express, express-openid-connect for Auth0 integration, and dotenv for managing environment variables.

```bash
npm install express express-openid-connect dotenv
```

--------------------------------

### Create and Configure Flutter Project

Source: https://auth0.com/docs/quickstart/native/flutter

This snippet demonstrates how to create a new Flutter project, navigate into its directory, and open it in VS Code. It assumes you have the Flutter SDK installed and configured.

```shellscript
# Create new Flutter project
flutter create auth0_flutter_sample

# Navigate into project directory
cd auth0_flutter_sample

# Open in VS Code
code .
```

--------------------------------

### Install Auth0 OIDC Client SDK using .NET CLI

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Installs the Auth0 OIDC Client SDK for .NET mobile applications using the .NET CLI. This command-line approach is an alternative to using the Package Manager Console.

```bash
dotnet add package Auth0.OidcClient.AndroidX
dotnet add package Auth0.OidcClient.iOS
dotnet add package Auth0.OidcClient.MAUI
```

--------------------------------

### Update package.json Scripts

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Updates the scripts section in the package.json file to include commands for starting the application. 'start' uses node, and 'dev' uses nodemon for development.

```json
{
  "name": "auth0-express",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "express-openid-connect": "^2.17.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
```

--------------------------------

### Install Auth0 SPA SDK

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Provides methods to install the Auth0 SPA SDK via npm or include it via CDN for browser-based projects.

```bash
npm install @auth0/auth0-spa-js
```

```html
<script src="https://cdn.auth0.com/js/auth0-spa-js/2.4/auth0-spa-js.production.js"></script>
```

--------------------------------

### Install Auth0 Angular SDK and Dependencies

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Installs the Auth0 Angular SDK and any other necessary npm packages. It also runs 'npm install' to ensure all project dependencies are met.

```bash
npm install @auth0/auth0-angular && npm install
```

--------------------------------

### Webhook Environment and Testing Setup

Source: https://auth0.com/docs/deploy-monitor/events/create-an-event-stream

Commands to generate a secure API token for the webhook, start the Node.js server, and expose the local endpoint via ngrok for testing.

```bash
API_TOKEN=`openssl rand -hex 32`
echo "API_TOKEN=$API_TOKEN" > .env
node webhook.js
ngrok http 3000
```

--------------------------------

### Main Application Setup with Auth0 in Go

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

Sets up the main application entry point, loads environment variables, initializes the Auth0 authenticator, and starts the HTTP server. It depends on 'net/http', 'log', 'github.com/joho/godotenv', and custom packages for authenticator and router.

```go
// Save this file in ./main.go

package main

import (
	"log"
	"net/http"

	"github.com/joho/godotenv"

	"01-Login/platform/authenticator"
	"01-Login/platform/router"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}
```

--------------------------------

### Install Auth0 UWP Package

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

Command to install the necessary NuGet package for Auth0 OIDC support in UWP applications.

```powershell
Install-Package Auth0.OidcClient.UWP
```

--------------------------------

### Start Node.js Webhook Server

Source: https://auth0.com/docs/customize/events/create-an-event-stream

This command starts the Node.js webhook server. Ensure you have installed the necessary dependencies (`express`, `dotenv`) and configured your `.env` file with the `API_TOKEN` before running this command.

```bash
node webhook.js
```

--------------------------------

### macOS Callback URL Configuration

Source: https://auth0.com/docs/quickstart/native/flutter

This example illustrates the Allowed Callback URLs for a macOS application, similar to iOS. Ensure `{yourDomain}` and `{yourBundleIdentifier}` are correctly substituted.

```text
https://{yourDomain}/macos/{yourBundleIdentifier}/callback,
{yourBundleIdentifier}://{yourDomain}/macos/{yourBundleIdentifier}/callback
```

--------------------------------

### Verify Auth0 Python SDK Installation

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Checks if the auth0-server-python package is installed in the current Python environment. This command lists all installed packages and filters for those containing 'auth0'.

```bash
pip list | grep auth0
```

--------------------------------

### Install Auth0 OIDC Client SDK using Package Manager Console

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Installs the Auth0 OIDC Client SDK for .NET mobile applications via the Package Manager Console in Visual Studio. This SDK simplifies OAuth 2.0 and OIDC protocol handling.

```bash
Install-Package Auth0.OidcClient.AndroidX
Install-Package Auth0.OidcClient.iOS
Install-Package Auth0.OidcClient.MAUI
```

--------------------------------

### Create Project Files

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Standard commands to create the necessary boilerplate files for a vanilla JavaScript application.

```bash
touch index.html app.js style.css
```

--------------------------------

### Example Get User Implementation (JavaScript)

Source: https://auth0.com/docs/authenticate/database-connections/custom-db/templates/get-user

A pseudo-JavaScript example demonstrating how to implement the 'getUser' function. It shows how to call an external API to search for a user by email and use the callback to return the user's profile or an error.

```javascript
function getUser(email, callback) {
  // Send user identifier to external database API
  let options = {
    url: "https://example.com/api/search-users",
    body: {
      email: email
    }
  };

  send(options, (err, profileData) => {
    // Return error in callback if there was an issue finding the user
    if (err) {
      return callback(new Error("Could not determine if user exists or not."));
    } else {
      // Return null in callback if user was not found, return profile data in callback if user was found
      if (!profileData) {
        return callback(null);
      } else {
        let profile = {
          email: profileData.email,
          user_id: profileData.userId
        };

        return callback(null, profile);
      }
    }
  });
}
```

--------------------------------

### Build Application with Maven

Source: https://auth0.com/docs/quickstart/webapp/java/index

This command uses Maven to clean the project, compile the source code, and package the application into a WAR file. This is a standard procedure for building Java web applications for deployment.

```bash
mvn clean compile war:war

```

--------------------------------

### Request Authorization Code (Node.js)

Source: https://auth0.com/docs/manage-users/my-account-api

This Node.js example utilizes the Axios library to make a GET request to the Auth0 authorization endpoint. It configures the request with query parameters for the authorization code grant flow. Remember to install Axios (`npm install axios`) and replace the placeholder values.

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://{yourDomain}/authorize',
  params: {
    response_type: 'code',
    client_id: '{yourClientId}',
    redirect_uri: '{yourRedirectUri}',
    scope: 'create:me:authentication_methods',
    offline_access: '',
    audience: 'https://{yourDomain}/me/'
  }
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### GET /api Example

Source: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/call-your-api-using-the-authorization-code-flow

Examples of making a GET request to a generic API endpoint '/api' with authorization headers.

```APIDOC
## GET /api

### Description
This endpoint retrieves data from the API. It requires an access token for authentication.

### Method
GET

### Endpoint
/api

### Parameters
#### Query Parameters
None

#### Request Body
None

#### Headers
- **Authorization** (string) - Required - Bearer token for authentication (e.g., `Bearer {accessToken}`)
- **Content-Type** (string) - Required - Specifies the format of the request body (e.g., `application/json`)

### Request Example
```bash
curl -X GET \
  https://myapi.com/api \
  -H 'Authorization: Bearer {accessToken}' \
  -H 'Content-Type: application/json'
```

### Response
#### Success Response (200)
- **data** (object) - The retrieved data from the API.

#### Response Example
```json
{
  "message": "Success"
}
```
```

--------------------------------

### Auth0 Flutter SDK Dependency in pubspec.yaml

Source: https://auth0.com/docs/quickstart/native/flutter

This snippet shows how the `auth0_flutter` package is added to your `pubspec.yaml` file after running the installation command. This is a declarative way to manage project dependencies.

```yaml
dependencies:
  auth0_flutter: ^2.0.0-beta.1
```

--------------------------------

### Initialize Flask Project Environment

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Commands to create a project directory and set up a Python virtual environment for the Flask application.

```shell
mkdir auth0-flask-app && cd auth0-flask-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

--------------------------------

### Android Callback URL Configuration

Source: https://auth0.com/docs/quickstart/native/flutter

This is an example of an Allowed Callback URL for an Android application. Replace `{yourDomain}` with your Auth0 domain and `{yourPackageName}` with your Android app's package name.

```text
https://{yourDomain}/android/{yourPackageName}/callback
```

--------------------------------

### Initialize Auth0 MCP Server for Claude Desktop

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command initializes the Auth0 MCP Server for use with Claude Desktop, which is the default client. Ensure Node.js v18 or higher is installed.

```javascript
npx @auth0/auth0-mcp-server init
```

--------------------------------

### Install Auth0 Flutter SDK

Source: https://auth0.com/docs/quickstart/native/flutter

This command adds the Auth0 Flutter SDK to your project's dependencies. Ensure you are within your Flutter project directory when running this command. The SDK requires Flutter 3.24.0+ and Dart 3.5.0+.

```shellscript
flutter pub add auth0_flutter
```

--------------------------------

### Initialize Auth0 MCP Server for Windsurf

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command initializes the Auth0 MCP Server for use with the Windsurf AI client. Ensure Node.js v18 or higher is installed on your system.

```javascript
npx @auth0/auth0-mcp-server init --client windsurf
```

--------------------------------

### Initialize Node.js Project

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Initializes a new Node.js project in the current directory using npm. This command creates a package.json file to manage project dependencies and scripts.

```bash
npm init -y
```

--------------------------------

### Build and Run .NET Mobile Applications

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Commands for building and running .NET Android and iOS applications using the .NET CLI.

```bash
# For Android
dotnet build -f net8.0-android
dotnet run -f net8.0-android

# For iOS
dotnet build -f net8.0-ios
dotnet run -f net8.0-ios
```

--------------------------------

### Auth0 Quick Setup for Vite

Source: https://auth0.com/docs/quickstart/spa/react/interactive

This command initiates the Auth0 setup process for a Vite project. It handles authentication, creates a Single Page Application in Auth0, and generates a .env file with necessary credentials. Ensure you are logged into Auth0 before running.

```bash
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Create Auth0 Application via CLI (macOS)

Source: https://auth0.com/docs/quickstart/webapp/hono

Automates the creation of an Auth0 application and generates a .env file with necessary credentials using the Auth0 CLI on macOS. It requires Homebrew to be installed and the Auth0 CLI to be tapped and installed.

```shellscript
AUTH0_APP_NAME="Hono Quickstart" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:3000/auth/callback -l http://localhost:3000 -o http://localhost:3000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" > auth0-app-details.json && CLIENT_ID=$(jq -r '.client_id' auth0-app-details.json) && CLIENT_SECRET=$(jq -r '.client_secret' auth0-app-details.json) && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && SECRET=$(openssl rand -hex 32) && echo "AUTH0_DOMAIN=${DOMAIN}" > .env && echo "AUTH0_CLIENT_ID=${CLIENT_ID}" >> .env && echo "AUTH0_CLIENT_SECRET=${CLIENT_SECRET}" >> .env && echo "BASE_URL=http://localhost:3000" >> .env && echo "AUTH0_SESSION_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env && rm auth0-app-details.json && cat .env
```

--------------------------------

### Auth0 App Setup with CLI (Shell)

Source: https://auth0.com/docs/quickstart/spa/vanillajs

Commands to set up a new Auth0 application and generate a `.env` file using the Auth0 CLI. This process is supported on both macOS and Windows, including instructions for installing the CLI if it's not already present.

```shellscript
# Install Auth0 CLI (if not already installed)
brew tap auth0/auth0-cli && brew install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

```powershell
# Install Auth0 CLI (if not already installed)
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### GitHub Quickstart Buttons with Download Functionality

Source: https://auth0.com/docs/fr-ca/quickstart/backend/nodejs/interactive

This React component, QuickstartButtons, displays GitHub and download sample buttons. It supports multiple languages for button text and includes functionality to parse GitHub URLs and trigger a sample download via a window.Auth0DocsUI interface. It handles potential URL parsing errors and download failures.

```javascript
export const QuickstartButtons = ({githubLink, lang = "en"}) => {
  const translations = {
    en: {
      viewOnGithub: "View On GitHub",
      loginAndDownload: "Download Sample"
    },
    "fr-ca": {
      viewOnGithub: "Afficher sur GitHub",
      loginAndDownload: "Télécharger un exemple"
    },
    "ja-jp": {
      viewOnGithub: "Githubで表示",
      loginAndDownload: "サンプルをダウンロード"
    }
  };
  const text = translations[lang] || translations.en;
  const parseGithubUrl = url => {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split("/").filter(Boolean);
      if (pathParts.length >= 4 && pathParts[2] === "tree") {
        const repoName = pathParts[1];
        const branch = pathParts[3];
        const path = pathParts.slice(4).join("/") || undefined;
        return {
          repo: repoName,
          branch,
          path
        };
      }
      console.warn("Could not parse GitHub URL:", url);
      return null;
    } catch (error) {
      console.error("Error parsing GitHub URL:", error);
      return null;
    }
  };
  const handleDownload = async () => {
    const params = parseGithubUrl(githubLink);
    if (!params) {
      console.error("Invalid GitHub URL format");
      return;
    }
    try {
      await window.Auth0DocsUI?.getSample(params);
    } catch (error) {
      console.error("Failed to download sample:", error);
    }
  };
  return <div className="quickstart_buttons flex flex-wrap gap-3 mb-4">
      <a href={githubLink} target="_blank" rel="noopener noreferrer" className="no_external_icon quickstart_button inline-flex items-center justify-center px-6 py-3 text-sm font-medium rounded-[18px] bg-black dark:bg-white !text-white dark:!text-black hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors">
        {text.viewOnGithub}
      </a>
      <button onClick={handleDownload} type="button" className="no_external_icon quickstart_button inline-flex items-center justify-center px-6 py-3 text-sm font-medium rounded-[18px] border border-gray-300 dark:border-[#454545] bg-white dark:bg-[#272728] !text-black dark:!text-white hover:bg-gray-50 dark:hover:bg-neutral-800 transition-colors">
        {text.loginAndDownload}
      </button>
    </div>;
};
```

--------------------------------

### Install Auth0 Express Agent Skill

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Installs the Auth0 agent skill for Express.js applications using npx. This skill helps in automatically adding Auth0 authentication to your Express app.

```bash
npx skills add https://github.com/auth0/agent-skills --skill auth0-express
```

--------------------------------

### Secure Credential Access with Biometrics

Source: https://auth0.com/docs/quickstart/native/flutter

Provides functionality to enable and utilize biometric authentication (Face ID, Touch ID, Fingerprint) for accessing user credentials stored locally. Requires platform-specific setup.

```dart
class SecureAuthService {
    final auth0 = Auth0('{yourDomain}', '{yourClientId}');
    
    Future<void> enableBiometrics() async {
      // Enable local authentication (Face ID, Touch ID, Fingerprint)
      await auth0.credentialsManager.enableLocalAuthentication(
        title: 'Authenticate to access your account',
        cancelTitle: 'Cancel',
        fallbackTitle: 'Use passcode',
      );
    }
    
    Future<Credentials> getCredentialsWithBiometrics() async {
      // This will now require biometric authentication
      return await auth0.credentialsManager.credentials();
    }
  }
```

--------------------------------

### Create Auth0 Application via CLI (Windows)

Source: https://auth0.com/docs/quickstart/webapp/hono

Automates the creation of an Auth0 application and generates a .env file with necessary credentials using the Auth0 CLI on Windows. It uses winget for installation and PowerShell for command execution.

```powershell
$AppName = "Hono Quickstart"; winget install Auth0.CLI; auth0 login --no-input; auth0 apps create -n "$AppName" -t regular -c http://localhost:3000/callback -l http://localhost:3000 -o http://localhost:3000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" | Set-Content -Path auth0-app-details.json; $ClientId = (Get-Content -Raw auth0-app-details.json | ConvertFrom-Json).client_id; $ClientSecret = (Get-Content -Raw auth0-app-details.json | ConvertFrom-Json).client_secret; $Domain = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name; $Secret = [System.Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)).ToLower(); Set-Content -Path .env -Value "AUTH0_DOMAIN=$Domain"; Add-Content -Path .env -Value "AUTH0_CLIENT_ID=$ClientId"; Add-Content -Path .env -Value "AUTH0_CLIENT_SECRET=$ClientSecret"; Add-Content -Path .env -Value "AUTH0_SECRET=$Secret"; Add-Content -Path .env -Value "BASE_URL=http://localhost:3000"; Remove-Item auth0-app-details.json; Write-Output ".env file created with your Auth0 details:"; Get-Content .env
```

--------------------------------

### Create Auth0 App and .env using PowerShell (Windows)

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This PowerShell command creates a new Auth0 application, sets up callback and logout URLs, and generates a .env file with Auth0 configuration. It uses `ConvertFrom-Json` and `ForEach-Object` for processing and `[guid]::NewGuid()` for generating a secret.

```powershell
$appName = "My Express App"
auth0 apps create -n $appName -t regular `
  --callbacks http://localhost:3000 `
  --logout-urls http://localhost:3000 `
  --json | ConvertFrom-Json | ForEach-Object {
    "ISSUER_BASE_URL=https://$($_.domain)`nCLIENT_ID=$($_.client_id)`nSECRET=$([guid]::NewGuid().ToString())`nBASE_URL=http://localhost:3000"
  } | Out-File .env -Encoding utf8
```

--------------------------------

### Calling Protected APIs with Access Tokens in Node.js

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This example demonstrates how to use the obtained access token to call a protected external API. It includes logic for checking token expiration and refreshing it if necessary before making the API request.

```javascript
app.get('/api-data', requiresAuth(), async (req, res) => {
  try {
    let { token_type, access_token, isExpired, refresh } = req.oidc.accessToken;

    // Refresh the token if expired
    if (isExpired()) {
      const refreshed = await refresh();
      access_token = refreshed.access_token;
    }

    // Call your protected API
    const response = await fetch('https://your-api.example.com/data', {
      headers: {
        Authorization: `${token_type} ${access_token}`,
      },
    });

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('API call failed:', error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});
```

--------------------------------

### Retrieve Auth0 Client Details (Go)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Shows how to retrieve Auth0 client details using Go's standard `net/http` package. This example makes a GET request and prints the response body.

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("authorization", "Bearer {yourMgmtApiAccessToken}")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

--------------------------------

### Build and Deploy Application

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

Shell commands to build the application using Maven or Gradle and deploy the resulting WAR file to a Tomcat servlet container.

```bash
# Maven Build
mvn clean compile war:war

# Maven Deploy
cp target/auth0-servlet-app.war $CATALINA_HOME/webapps/ROOT.war

# Gradle Build
gradle clean build

# Gradle Deploy
cp build/libs/auth0-servlet-app.war $CATALINA_HOME/webapps/

# Start Tomcat
$CATALINA_HOME/bin/startup.sh
```

--------------------------------

### Start Vite Development Server

Source: https://auth0.com/docs/quickstart/spa/vanillajs

Checks for custom port configurations in .env.local and starts the Vite server accordingly.

```bash
grep -q "VITE_DEV_PORT" .env.local 2>/dev/null && echo "Custom port detected" || echo "Using default port"

# Default
npm run dev

# Custom
npm run dev -- --port 5174
```

--------------------------------

### Initialize and Start Go Web Server

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

Configures environment variables, initializes the authentication provider, and starts the HTTP server on port 3000. It serves as the entry point for the application.

```go
package main

import (
	"log"
	"net/http"
	"github.com/joho/godotenv"
	"01-Login/platform/authenticator"
	"01-Login/platform/router"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}
```

--------------------------------

### Manage GitHub sample downloads

Source: https://auth0.com/docs/quickstart/backend/django/interactive

The QuickstartButtons component provides UI elements to link to GitHub repositories and trigger sample application downloads. It includes logic to parse GitHub URLs and interact with the Auth0DocsUI global service for file retrieval.

```javascript
export const QuickstartButtons = ({githubLink, lang = "en"}) => {
  const translations = {
    en: { viewOnGithub: "View On GitHub", loginAndDownload: "Download Sample" },
    "fr-ca": { viewOnGithub: "Afficher sur GitHub", loginAndDownload: "Télécharger un exemple" },
    "ja-jp": { viewOnGithub: "Githubで表示", loginAndDownload: "サンプルをダウンロード" }
  };
  const text = translations[lang] || translations.en;
  const parseGithubUrl = url => {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split("/").filter(Boolean);
      if (pathParts.length >= 4 && pathParts[2] === "tree") {
        return { repo: pathParts[1], branch: pathParts[3], path: pathParts.slice(4).join("/") || undefined };
      }
      return null;
    } catch (error) { return null; }
  };
  const handleDownload = async () => {
    const params = parseGithubUrl(githubLink);
    if (params) await window.Auth0DocsUI?.getSample(params);
  };
  return <div className="quickstart_buttons">
      <a href={githubLink} target="_blank" rel="noopener noreferrer">{text.viewOnGithub}</a>
      <button onClick={handleDownload} type="button">{text.loginAndDownload}</button>
    </div>;
};
```

--------------------------------

### Make Authenticated API Request (Node.js)

Source: https://auth0.com/docs/ja-jp/quickstart/backend/nodejs/interactive

This Node.js example uses the Axios library to make an authenticated GET request. It configures the request method, URL, and authorization header, then handles the response or any errors. Ensure Axios is installed via npm.

```javascript
var axios = require("axios").default;
var options = {
method: 'get',
url: 'http:///%7ByourDomain%7D/api_path',
headers: {authorization: 'Bearer YOUR_ACCESS_TOKEN_HERE'}
};
axios.request(options).then(function (response) {
console.log(response.data);
}).catch(function (error) {
console.error(error);
});
```

--------------------------------

### Install FastAPI Dependencies

Source: https://auth0.com/docs/quickstart/backend/fastapi

Defines the required packages for a FastAPI application with Auth0 support and installs them via pip.

```bash
cat > requirements.txt << 'EOF'
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
auth0-fastapi-api>=1.0.0b5
python-dotenv>=1.0.0
EOF
pip install -r requirements.txt
```

--------------------------------

### Run FastAPI Development Server

Source: https://auth0.com/docs/quickstart/webapp/fastapi

Demonstrates how to programmatically start the Uvicorn server within a Python script.

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
```

--------------------------------

### Start PHP Development Server

Source: https://auth0.com/docs/quickstart/webapp/php

This shell command starts a local PHP development server on port 3000, allowing the application to be accessed via the browser.

```bash
php -S 127.0.0.1:3000 index.php
```

--------------------------------

### Create ASP.NET MVC Project and Install Auth0 SDK

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core

This snippet shows how to create a new ASP.NET Core MVC project and install the necessary Auth0 authentication SDK using the .NET CLI.

```shellscript
dotnet new mvc -n SampleMvcApp
cd SampleMvcApp
dotnet add package Auth0.AspNetCore.Authentication
```

--------------------------------

### POST /passwordless/start

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates the passwordless authentication process by requesting a verification code to be sent to the specified connection (e.g., SMS).

```APIDOC
## POST /passwordless/start

### Description
Initiates a passwordless authentication flow. This endpoint triggers the delivery of a verification code to the user via the specified connection.

### Method
POST

### Endpoint
https://{yourDomain}/passwordless/start

### Parameters
#### Request Body
- **client_id** (string) - Required - Your Auth0 application client ID.
- **client_secret** (string) - Required - Your Auth0 application client secret.
- **connection** (string) - Required - The connection type, e.g., "sms".
- **phone_number** (string) - Required - The user's phone number to receive the code.
- **send** (string) - Required - The action to perform, e.g., "code".

### Request Example
{
  "client_id": "{yourClientId}",
  "client_secret": "{yourClientSecret}",
  "connection": "sms",
  "phone_number": "{userPhoneNumber}",
  "send": "code"
}

### Response
#### Success Response (200)
- **status** (string) - Indicates the request was successful.

#### Response Example
{
  "status": "ok"
}
```

--------------------------------

### Install Auth0 SDK for Expo

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

Adds the Auth0 React Native SDK to your Expo project. Using `npx expo install` is recommended as it ensures version compatibility with your current Expo SDK. The SDK is designed to auto-configure using the Expo plugin system.

```bash
npx expo install react-native-auth0
```

--------------------------------

### Install Dependencies from requirements.txt (Bash)

Source: https://auth0.com/docs/quickstart/backend/fastapi

This command installs all the Python dependencies listed in the requirements.txt file using pip. It assumes the requirements.txt file is in the current directory.

```bash
pip install -r requirements.txt
```

--------------------------------

### Check if Auth0 MCP Server is Running

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command checks if the Auth0 MCP Server process is actively running on your system. It's a crucial step for troubleshooting connection failures. If the server is not running, you may need to restart it or re-initialize the installation.

```bash
ps aux | grep auth0-mcp
```

--------------------------------

### Start Laravel development server

Source: https://auth0.com/docs/quickstart/backend/laravel/interactive

Launch the local development server to begin accepting requests.

```bash
php artisan serve
```

--------------------------------

### Install and initialize Auth0 SDK

Source: https://auth0.com/docs/quickstart/native/android-facebook-login

Provides instructions for adding the Auth0 dependency to Gradle, configuring domain and client ID in strings.xml, and initializing the Auth0 client in the activity.

```kotlin
dependencies {
    implementation("com.auth0.android:auth0:3.+")
}
```

```xml
<resources>
    <string name="com_auth0_domain">{yourDomain}</string>
    <string name="com_auth0_client_id">{yourClientId}</string>
</resources>
```

```kotlin
private val account: Auth0 by lazy {
    Auth0.getInstance(
        getString(R.string.com_auth0_client_id),
        getString(R.string.com_auth0_domain)
    )
}

private val authenticationApiClient: AuthenticationAPIClient by lazy {
    AuthenticationAPIClient(account)
}
```

--------------------------------

### Get All Applications (Auth0 Management API v2)

Source: https://auth0.com/docs/secure/tokens/access-tokens/management-api-access-tokens/get-management-api-access-tokens-for-production

Provides examples for retrieving all applications from the Auth0 Management API v2. It demonstrates how to authenticate and make a GET request to the '/api/v2/clients' endpoint. Ensure you replace placeholders like {yourDomain} and {yourAccessToken} with your actual values.

```bash
curl --request GET \
  --url 'https://{yourDomain}/api/v2/clients' \
  --header 'authorization: Bearer {yourAccessToken}' \
  --header 'content-type: application/json'
```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/clients");
var request = new RestRequest(Method.GET);
request.AddHeader("content-type", "application/json");
request.AddHeader("authorization", "Bearer {yourAccessToken}");
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/clients"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("content-type", "application/json")
	req.Header.Add("authorization", "Bearer {yourAccessToken}")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/clients")
  .header("content-type", "application/json")
  .header("authorization", "Bearer {yourAccessToken}")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://{yourDomain}/api/v2/clients',
  headers: {'content-type': 'application/json', authorization: 'Bearer {yourAccessToken}'}
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objc
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"content-type": @"application/json",
                             @"authorization": @"Bearer {yourAccessToken}" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/clients"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/api/v2/clients",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer {yourAccessToken}",
    "content-type: application/json"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:";
  echo $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("{yourDomain}")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer {yourAccessToken}"
    }

conn.request("GET", "/api/v2/clients", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/clients")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

# Further implementation for request and response handling would follow here.
```

--------------------------------

### Handle Quickstart Repository Actions

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/java/interactive

The QuickstartButtons component provides UI for viewing GitHub repositories and downloading sample applications. It includes logic to parse GitHub URLs and trigger sample retrieval via the Auth0DocsUI global interface.

```javascript
const parseGithubUrl = url => {
  try {
    const urlObj = new URL(url);
    const pathParts = urlObj.pathname.split("/").filter(Boolean);
    if (pathParts.length >= 4 && pathParts[2] === "tree") {
      return { repo: pathParts[1], branch: pathParts[3], path: pathParts.slice(4).join("/") || undefined };
    }
    return null;
  } catch (error) {
    return null;
  }
};

const handleDownload = async (githubLink) => {
  const params = parseGithubUrl(githubLink);
  if (params) {
    await window.Auth0DocsUI?.getSample(params);
  }
};
```

--------------------------------

### Install EAS CLI for Production Builds

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

This command installs the EAS CLI globally, which is required for building your React Native application for production using Expo Application Services (EAS).

```bash
npm install -g eas-cli
```

--------------------------------

### Install Auth0 Agent Skills (Bash)

Source: https://auth0.com/docs/quickstart/webapp/fastify

Command to install Auth0 agent skills for AI integration. This command uses npm to add the necessary skills for quickstart and Fastify integration.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-fastify
```

--------------------------------

### Initialize and Install Laravel and Auth0 SDK

Source: https://auth0.com/docs/quickstart/backend/laravel/interactive

Commands to create a new Laravel project, install the Auth0 Laravel SDK, and publish the necessary configuration files.

```bash
composer create-project --prefer-dist laravel/laravel auth0-laravel-api ^9.0
cd auth0-laravel-api
composer require auth0/login:^7.8 --update-with-all-dependencies
php artisan vendor:publish --tag auth0
```

--------------------------------

### Create Express Project Directory

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Creates a new directory for an Express.js application and navigates into it. This is the first step in setting up a new project.

```bash
mkdir auth0-express && cd auth0-express
```

--------------------------------

### Return User Profile Example (JavaScript)

Source: https://auth0.com/docs/authenticate/database-connections/custom-db/templates/get-user

An example of how to use the callback function to return a user's profile data. This includes standard fields and optional metadata fields like 'user_metadata' and 'app_metadata'.

```javascript
return callback(null, {
    username: "username",
    user_id: "my-custom-db|username@domain.com",
    email: "username@domain.com",
    email_verified: false,
    user_metadata: {
        language: "en"
    },
    app_metadata: {
        plan: "full"
    },
    mfa_factors: [
      {
        phone: {
          value: "+15551234567"
        }
      },
    ]
});
```

--------------------------------

### Language Grid for Authentication Quickstarts

Source: https://auth0.com/docs

Renders a grid of programming languages and frameworks for users to find authentication quickstart guides. It dynamically generates links based on language icons and hrefs.

```javascript
export const LanguageGrid = () => {
  const languages = [{
    img: "react.svg",
    label: "React",
    href: "/docs/quickstart/spa/react"
  }, {
    img: "angular.svg",
    label: "Angular",
    href: "/docs/quickstart/spa/angular"
  }, {
    img: "nextjs.svg",
    label: "Next.js",
    href: "/docs/quickstart/webapp/nextjs"
  }, {
    img: "apple.svg",
    label: "iOS",
    href: "/docs/quickstart/native/ios-swift"
  }, {
    img: "android.svg",
    label: "Android",
    href: "/docs/quickstart/native/android"
  }, {
    img: "java.svg",
    label: "Java",
    href: "/docs/quickstart/backend/java-spring-security5/interactive"
  }, {
    img: "dotnet.svg",
    label: ".NET",
    href: "/docs/quickstart/backend/aspnet-core-webapi"
  }, {
    img: "python.svg",
    label: "Python",
    href: "/docs/quickstart/backend/python"
  }];
  return <section className="max-w-[962px] mx-auto py-12 px-8 lg:px-0">
      <h2 className="font-inter !font-medium text-[24px] text-gray-900 dark:text-white mb-6">
        Get started with authentication
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {languages.map((lang, idx) => <a key={idx} href={lang.href} className="flex flex-col items-center justify-center px-8 py-4 rounded-2xl 
                      bg-white/60 dark:bg-neutral-900/60 
                      border border-gray-200 dark:border-white/10 
                      shadow-sm hover:shadow-md 
                      hover:border-black dark:hover:border-white 
                      transition">
            <img noZoom src={`/docs/images/icons/light/${lang.img}`} alt={lang.label} className="h-8 w-8 mb-4 block dark:hidden" />
            <img noZoom src={`/docs/images/icons/dark/${lang.img}`} alt={lang.label} className="h-8 w-8 mb-4 hidden dark:block" />
            <span className="font-inter text-base text-gray-900 dark:text-white">{lang.label}</span>
          </a>)}
      </div>
    </section>;
};

```

--------------------------------

### User Signup with Database Connection using auth0.js

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

Provides an example of signing up a new user to a database connection using the `signup` method. It includes sample HTML for a signup form and JavaScript to handle the form submission and call the `webAuth.signup` function with user details and metadata.

```html
<h2>Signup Database Connection</h2>
<input class="signup-email" />
<input type="password" class="signup-password" />
<input type="button" class="signup-db" value="Signup!" />
<script type="text/javascript">
    $('.signup-db').click(function (e) {
        e.preventDefault();
        webAuth.signup({
            connection: 'Username-Password-Authentication',
            email: $('.signup-email').val(),
            password: $('.signup-password').val(),
            user_metadata: { plan: 'silver', team_id: 'a111' }
        }, function (err) {
            if (err) return alert('Something went wrong: ' + err.message);
            return alert('success signup without login!')
        });
    });
</script>
```

--------------------------------

### Index HTML Page

Source: https://auth0.com/docs/quickstart/webapp/java/index

This HTML file serves as the landing page for the application. It provides a brief description of the example and a prominent 'Login with Auth0' button that initiates the authentication flow. The page includes basic styling for a welcoming user experience.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Auth0 Java Servlet Example</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 40px;
        background-color: #f8f9fa;
      }
      .container {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
        background-color: white;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }
      .login-btn {
        background-color: #007bff;
        color: white;
        padding: 12px 30px;
        text-decoration: none;
        border-radius: 5px;
        display: inline-block;
        font-size: 16px;
        margin-top: 20px;
        transition: background-color 0.3s;
      }
      .login-btn:hover {
        background-color: #0056b3;
      }
      h1 {
        color: #333;
      }
      p {
        color: #666;
        line-height: 1.6;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Auth0 Java Servlet Example</h1>
      <p>
        This example demonstrates how to add authentication to a Java servlet
        application using the Auth0 Java MVC Commons SDK.
      </p>
      <p>
        Click the button below to authenticate with Auth0 and access your
        profile.
      </p>

      <a href="/login" class="login-btn">Login with Auth0</a>
    </div>
  </body>
</html>

```

--------------------------------

### Install Auth0 FastAPI SDK

Source: https://auth0.com/docs/quickstart/backend/fastapi

Instructions to install the Auth0 FastAPI API SDK using pip. This is necessary for Python applications using FastAPI to integrate with Auth0.

```bash
# Activate your virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install the SDK
pip install auth0-fastapi-api

# Verify installation
pip show auth0-fastapi-api
```

--------------------------------

### Initialize Gradle Project

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

Creates a new directory named 'auth0-servlet-app' and initializes a Java application project using Gradle. This command sets up the basic structure and build files for a Gradle-based Java project.

```bash
mkdir auth0-servlet-app && cd auth0-servlet-app
gradle init --type java-application
```

--------------------------------

### Install Auth0.js SDK

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

Methods to add the auth0-js library to your project using package managers or a CDN script tag.

```bash
npm install auth0-js
yarn add auth0-js
```

```javascript
import auth0 from 'auth0-js';
```

```html
<script src="https://cdn.auth0.com/js/auth0/9.18/auth0.min.js"></script>
```

--------------------------------

### Complete Express API authentication setup

Source: https://auth0.com/docs/quickstart/backend

A comprehensive example of an Express server configured with JWT authentication, scope protection, and custom error handling for Auth0 integration.

```javascript
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { 
  auth, 
  requiredScopes, 
  claimCheck,
  UnauthorizedError,
  InsufficientScopeError,
} = require('express-oauth2-jwt-bearer');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const checkJwt = auth({
  issuerBaseURL: `https://${process.env.AUTH0_DOMAIN}`,
  audience: process.env.AUTH0_AUDIENCE,
});

app.get('/api/admin', 
  checkJwt, 
  requiredScopes('admin:access'),
  claimCheck((claims) => claims.role === 'admin'),
  (req, res) => {
    res.json({ message: 'Admin access granted' });
  }
);

app.use((err, req, res, next) => {
  if (err instanceof InsufficientScopeError) {
    return res.status(403).json({ error: 'insufficient_scope', message: 'Missing required permissions' });
  }
  if (err instanceof UnauthorizedError) {
    return res.status(err.status).json({ error: err.code || 'unauthorized', message: 'Authentication required' });
  }
  res.status(500).json({ error: 'server_error', message: 'An unexpected error occurred' });
});

app.listen(port);
```

--------------------------------

### GET /v2/connections-directory-provisionings

Source: https://auth0.com/docs/api/management/v2/connections-directory-provisionings/get-connections-directory-provisionings

Retrieves a list of directory provisioning configurations for a tenant. You can specify the starting point and the number of results per page.

```APIDOC
## GET /v2/connections-directory-provisionings

### Description
Retrieve a list of directory provisioning configurations of a tenant.

### Method
GET

### Endpoint
/v2/connections-directory-provisionings

### Scopes
read:directory_provisionings

### Query Parameters
- **from** (string) - Optional - Id from which to start selection.
- **take** (integer) - Optional - Number of results per page. Defaults to 50.

### Response
#### Success Response (200)
- **directory_provisionings** (object[]) - Required - List of directory provisioning configurations.
  - **connection_id** (string) - Required - The connection's identifier.
  - **connection_name** (string) - Required - The connection's name.
  - **strategy** (string) - Required - The connection's strategy.
  - **mapping** (object[]) - Required - The mapping between Auth0 and IDP user attributes.
    - **auth0** (string) - Required - The field location in the Auth0 schema.
    - **idp** (string) - Required - The field location in the IDP schema.
    - **synchronize_automatically** (boolean) - Required - Whether periodic automatic synchronization is enabled.
    - **synchronize_groups** (string) - Optional - Group synchronization configuration. Possible values: `all`, `off`.
  - **created_at** (string) - Required - The timestamp at which the directory provisioning configuration was created (format: date-time).
  - **updated_at** (string) - Required - The timestamp at which the directory provisioning configuration was last updated (format: date-time).
  - **last_synchronization_at** (string) - Optional - The timestamp at which the connection was last synchronized (format: date-time).
  - **last_synchronization_status** (string) - Optional - The status of the last synchronization.
  - **last_synchronization_error** (string) - Optional - The error message of the last synchronization, if any.
  - **next** (string) - Optional - The cursor to be used as the "from" query parameter for the next page of results.

#### Error Response
- **400** - Invalid pagination cursor
- **400** - Invalid request query string.
- **400** - Invalid query string paging options.
- **401** - Invalid token.
- **401** - Invalid signature received for JSON Web Token validation.
- **401** - Client is not global.
- **403** - The inbound directory provisioning feature is not enabled for this tenant.
- **403** - Insufficient scope; expected any of: read:directory_provisionings.
- **429** - Too many requests.

### Request Example
```json
{
  "example": "request body"
}
```

### Response Example
```json
{
  "directory_provisionings": [
    {
      "connection_id": "con_abc123",
      "connection_name": "MyDirectory",
      "strategy": "ad",
      "mapping": [
        {
          "auth0": "email",
          "idp": "userPrincipalName",
          "synchronize_automatically": true,
          "synchronize_groups": "all"
        }
      ],
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T10:00:00Z",
      "last_synchronization_at": "2023-10-27T10:05:00Z",
      "last_synchronization_status": "success",
      "next": "cursor_xyz789"
    }
  ]
}
```

### cURL Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/connections-directory-provisionings' \
-H 'Accept: application/json'
```
```

--------------------------------

### Protecting All Routes Under a Path with Express Router and requiresAuth()

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This example demonstrates how to protect all routes defined within an Express Router instance using the `requiresAuth()` middleware. This is useful for grouping protected routes under a common base path.

```javascript
const protectedRouter = express.Router();

// All routes in this router require authentication
protectedRouter.use(requiresAuth());

protectedRouter.get('/dashboard', (req, res) => {
  res.send('Protected dashboard');
});

protectedRouter.get('/settings', (req, res) => {
  res.send('Protected settings');
});

app.use('/app', protectedRouter);
// Routes: /app/dashboard, /app/settings are all protected
```

--------------------------------

### Build and Run Android Application

Source: https://auth0.com/docs/quickstart/native/android/interactive

Standard Gradle commands to clean, build, and install the Android application on a connected device or emulator.

```bash
# Sync project with Gradle files (or use Android Studio's "Sync Now")
./gradlew clean build

# Build and install on connected device or emulator
./gradlew installDebug
```

--------------------------------

### Create New Java Web Project (Maven)

Source: https://auth0.com/docs/quickstart/webapp/java/index

Generates a new Java web application project using the Maven archetype. This command initializes the project structure for a web application.

```bash
mvn archetype:generate \
  -DgroupId=com.auth0.example \
  -DartifactId=auth0-servlet-app \
  -DarchetypeArtifactId=maven-archetype-webapp \
  -DinteractiveMode=false

cd auth0-servlet-app
```

--------------------------------

### Create Hono Application

Source: https://auth0.com/docs/quickstart/webapp/hono

Initializes a new Hono application project using the create-hono utility. This command sets up the basic project structure for a Hono application.

```shellscript
npm create hono@latest auth0-hono-app && cd auth0-hono-app
```

--------------------------------

### Scaffold Project Structure

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Creates the necessary directory structure and empty files for a Flask application using Auth0 authentication.

```bash
mkdir templates static && touch app.py auth.py templates/index.html templates/profile.html static/style.css
```

--------------------------------

### Configuring Custom Redis Session Store with Auth0 in Node.js

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This example shows how to configure the Auth0 SDK to use Redis as a custom session store. It involves creating a Redis client and integrating it into the session configuration, which is crucial for scalability and persistence.

```javascript
const { auth } = require('express-openid-connect');
const { createClient } = require('redis');
const RedisStore = require('connect-redis').default;

// Create Redis client
const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
});
redisClient.connect().catch(console.error);

const config = {
  authRequired: false,
  auth0Logout: true,
  secret: process.env.SECRET,
  baseURL: process.env.BASE_URL,
  clientID: process.env.CLIENT_ID,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
  session: {
    store: new RedisStore({ client: redisClient }),
  },
};

app.use(auth(config));
```

--------------------------------

### Retrieve Auth0 Client Details (Java)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Provides a Java example using the Unirest library to fetch Auth0 client information. It sets the GET request URL and authorization header.

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true")
  .header("authorization", "Bearer {yourMgmtApiAccessToken}")
  .asString();
```

--------------------------------

### Install Auth0 SDK Dependencies

Source: https://auth0.com/docs/quickstart/native/ios-swift-siwa

Configuration files for various package managers to include the Auth0 SDK in your project.

```Podfile
platform :ios, '14.0'
use_frameworks!

target 'YourApp' do
  pod 'Auth0', '~> 2.0'
end
```

```Cartfile
github "auth0/Auth0.swift" ~> 2.0
```

```Shell
pod install

carthage update --platform iOS --use-xcframeworks
```

--------------------------------

### GET /api/v2/connections/{id}

Source: https://auth0.com/docs/fr-ca/authenticate/identity-providers/pass-parameters-to-idps

Retrieves a specific connection by its ID. This example shows how to make the request using Ruby and Swift, including setting the necessary authorization and content-type headers.

```APIDOC
## GET /api/v2/connections/{id}

### Description
Retrieves a specific connection by its ID. This endpoint requires an authorization header with a Management API access token.

### Method
GET

### Endpoint
`/api/v2/connections/{id}`

### Parameters
#### Path Parameters
- **id** (string) - Required - The ID of the connection to retrieve.

#### Query Parameters
None

#### Request Body
None

### Request Example (Ruby)
```ruby
require 'net/http'
require 'uri'

url = URI.parse("https://{yourDomain}/api/v2/connections/%7ByourWordpressConnectionId%7D")
request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer {yourMgmtApiAccessToken}'
request["content-type"] = 'application/json'

response = http.request(request)
puts response.read_body
```

### Request Example (Swift)
```swift
import Foundation

let headers = [
  "authorization": "Bearer {yourMgmtApiAccessToken}",
  "content-type": "application/json"
]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/connections/%7ByourWordpressConnectionId%7D")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                      timeoutInterval: 10.0)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

### Response
#### Success Response (200)
- **connection** (object) - Details of the retrieved connection.

#### Response Example
```json
{
  "id": "{yourWordpressConnectionId}",
  "name": "your-wordpress-connection",
  "strategy": "wordpress",
  "options": {
    "domain": "your-wordpress-blog.com"
  },
  "enabled_clients": [],
  "created_at": "2023-01-01T10:00:00.000Z",
  "updated_at": "2023-01-01T10:00:00.000Z"
}
```
```

--------------------------------

### AD/LDAP Configuration Example

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/active-directory-ldap/ad-ldap-connector/install-configure-ad-ldap-connector

A JSON configuration template for the AD/LDAP connector, defining connection parameters such as LDAP URL, base DN, and bind credentials.

```json
{
   "LDAP_URL": "ldap://{yourLdapServerFqdn}",
   "LDAP_BASE": "dc={yourDomain},dc=com",
   "LDAP_BIND_USER":"{yourLdapUser}",
   "LDAP_BIND_PASSWORD":"{yourLdapUserPassword}"
}
```

--------------------------------

### Create Project Files

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Creates the main application file (index.js) and the environment variable file (.env) for the Express.js project. These files are essential for running the application.

```bash
touch index.js .env
```

--------------------------------

### Create .NET MAUI, Android, or iOS Project

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Instructions for creating a new .NET MAUI, .NET Android, or .NET iOS project using Visual Studio. These projects serve as the foundation for integrating Auth0 authentication.

```text
1. **File** → **New** → **Project**
2. Select **.NET MAUI App** or **Android App (.NET)** or **iOS App (.NET)** template
3. Configure your project name and framework (.NET 8.0 or later)
4. Click **Create**
```

--------------------------------

### Call API Endpoint with GET Request (Multiple Languages)

Source: https://auth0.com/docs/customize/integrations/google-cloud-endpoints

This snippet shows how to make an unauthenticated GET request to an API endpoint. It includes examples for cURL, C#, Go, Java, Node.js, Obj-C, PHP, Python, Ruby, and Swift. These examples are useful for verifying API functionality after deployment or changes.

```bash
curl --request GET \
    --url 'https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO'
```

```csharp
var client = new RestClient("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO");
var request = new RestRequest(Method.GET);
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://%7ByourGceProject%7D.appspot.com/airportName',
  params: {iataCode: 'SFO'}
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objc
#import <Foundation/Foundation.h>

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO"] 
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy 
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request 
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("")

conn.request("GET", "%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let request = NSMutableURLRequest(url: NSURL(string: "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                      timeoutInterval: 10.0)
request.httpMethod = "GET"

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### Troubleshooting and Debugging Commands

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

Utility commands for managing the Auth0 MCP server, including viewing help documentation, verifying process status, and enabling debug logging.

```bash
npx @auth0/auth0-mcp-server help
```

```bash
ps aux | grep auth0-mcp
```

```bash
export DEBUG=auth0-mcp
```

--------------------------------

### Implement Login Method

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Handles the login process by invoking the Auth0 client and processing the result, including access and identity tokens.

```csharp
public async Task LoginAsync()
{
    var loginResult = await auth0Client.LoginAsync();

    if (!loginResult.IsError)
    {
        var accessToken = loginResult.AccessToken;
        var idToken = loginResult.IdentityToken;
    }
}
```

--------------------------------

### Setup Auth0 App via CLI

Source: https://auth0.com/docs/quickstart/spa/react

Automated setup of an Auth0 application using the Auth0 CLI for different operating systems.

```shellscript
# Mac
brew tap auth0/auth0-cli && brew install auth0
auth0 qs setup --type vite -n "My App" -p 5173
```

```powershell
# Windows
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### AI Prompt for Auth0 Integration in Cap'n Web

Source: https://auth0.com/docs/quickstart/spa/capn-web

This markdown snippet is designed for AI code assistants to guide the integration of Auth0 authentication into a Cap'n Web RPC application. It outlines a step-by-step execution flow, including project setup, dependency installation, Auth0 configuration, server-side JWT validation, and client-side integration. It emphasizes security requirements and specific behavioral instructions for the AI.

```markdown
Integrate Auth0 authentication into a Cap'n Web RPC application

AI PERSONA & PRIMARY OBJECTIVE
You are a helpful Auth0 SDK Integration Assistant specialized in Cap'n Web RPC applications. Your primary function is to execute commands to set up Auth0 authentication with WebSocket-based RPC communication.

CRITICAL BEHAVIORAL INSTRUCTIONS
1. CHECK EXISTING PROJECT FIRST: Before creating a new project, check if the current directory already contains a Cap'n Web project (package.json with capnweb dependencies).
2. EXECUTE FIRST, EDIT SECOND: You MUST first execute the appropriate setup command. Do not show, suggest, or create any files until the setup is complete.
3. NO PLANNING: DO NOT propose a directory structure. Your first action must be to run the appropriate command.
4. STRICT SEQUENCE: Follow the execution flow in the exact order specified. 
5. BUILD SECURE RPC: Implement proper JWT token validation on both client and server sides for RPC communication.

EXECUTION FLOW

Step 1: Create Cap'n Web Project
mkdir capnweb-auth0-app && cd capnweb-auth0-app
npm init -y && npm pkg set type="module"
mkdir -p client server && touch server/index.js client/index.html client/app.js .env

Step 2: Install Dependencies
npm install capnweb ws dotenv
npm install @auth0/auth0-spa-js @auth0/auth0-api-js
npm pkg set scripts.start="node server/index.js"

Step 3: Setup Auth0 App (use CLI command from Step 3 in the quickstart)

Step 4: Configure Auth0 Application and API
- Create Auth0 Application (SPA type)
- Create Auth0 API with required scopes
- Set callback URLs and origins

Step 5: Implement Server with JWT Validation
- Create WebSocket server with Cap'n Web RPC
- Extend RpcTarget class for ProfileService
- Validate JWT tokens from Auth0 for each RPC call
- Use newWebSocketRpcSession() to handle WebSocket connections
- Implement secure profile management endpoints

Step 6: Implement Client with Auth0 Integration
- Initialize Auth0 SPA client with refresh tokens enabled
- Use newWebSocketRpcSession() from capnweb for RPC
- Connect to WebSocket only after authentication is confirmed
- Handle login/logout flows
- Send JWT tokens with RPC calls
- Build modern UI with authentication state

Step 7: Run the Application
npm run start

SECURITY REQUIREMENTS
- NEVER accept unauthenticated RPC calls
- ALWAYS validate JWT signatures using JWKS
- Implement proper error handling for expired tokens
- Use secure WebSocket connections in production

Step 3: Setup Auth0 Application and API
AFTER the commands in Steps 1 and 2 have successfully executed, you will perform the Auth0 configuration.

🚨 DIRECTORY NAVIGATION RULES:
1. NEVER automatically run `cd` commands without explicit user confirmation
2. ALWAYS check current directory with `pwd` before proceeding
3. If working with existing project: Stay in current directory
4. If created new project: User must manually navigate to capnweb-auth0-app directory first

```

--------------------------------

### Implement Enterprise Federation with login_hint

Source: https://auth0.com/docs/authenticate/identity-providers/social-identity-providers/google-native

This snippet demonstrates how to handle enterprise federation by redirecting users to the web-based flow. It passes the user's email as a login_hint to streamline the authentication process.

```go
if (error.isAccessDenied && reason == "Enterprise Domain") {
	WebAuthProvider.login(account)
		.withParameters(mapOf("login_hint" to email))
		.start(...)
}
```

--------------------------------

### Actions: Log Hello World

Source: https://auth0.com/docs/troubleshoot/customer-support/auth0-changelog

A simple JavaScript example demonstrating how to log a 'Hello world!' message using `console.log` within an Auth0 Action. This log output can be viewed in the Actions Logs in the Auth0 Dashboard.

```javascript
console.log("Hello world!");
```

--------------------------------

### Add Auth0 SDK via CocoaPods

Source: https://auth0.com/docs/quickstart/native/ios-swift/interactive

Integrates the Auth0 SDK into your Xcode project using CocoaPods. Requires a Podfile and the 'pod install' command.

```ruby
platform :ios, '14.0' # Or platform :osx, '11.0' for macOS
use_frameworks!

target 'YourApp' do
  pod 'Auth0', '~> 2.0'
end

```

```bash
pod install
```

--------------------------------

### Manage GitHub Sample Downloads

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/java-ee/interactive

The QuickstartButtons component provides localized links to GitHub repositories and triggers sample downloads via the Auth0DocsUI interface. It parses GitHub URLs to extract repository, branch, and path information.

```javascript
export const QuickstartButtons = ({githubLink, lang = "en"}) => {
  const translations = {
    en: { viewOnGithub: "View On GitHub", loginAndDownload: "Download Sample" },
    "fr-ca": { viewOnGithub: "Afficher sur GitHub", loginAndDownload: "Télécharger un exemple" },
    "ja-jp": { viewOnGithub: "Githubで表示", loginAndDownload: "サンプルをダウンロード" }
  };
  const text = translations[lang] || translations.en;
  const parseGithubUrl = url => {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split("/").filter(Boolean);
      if (pathParts.length >= 4 && pathParts[2] === "tree") {
        return { repo: pathParts[1], branch: pathParts[3], path: pathParts.slice(4).join("/") || undefined };
      }
      return null;
    } catch (error) { return null; }
  };
  const handleDownload = async () => {
    const params = parseGithubUrl(githubLink);
    if (params) await window.Auth0DocsUI?.getSample(params);
  };
  return <div className="quickstart_buttons">
      <a href={githubLink}>{text.viewOnGithub}</a>
      <button onClick={handleDownload}>{text.loginAndDownload}</button>
    </div>;
};
```

--------------------------------

### Auth0 Rule: Configuration-Based URL Example

Source: https://auth0.com/docs/dev-lifecycle/set-up-multiple-environments

This JavaScript code snippet shows a recommended Auth0 rule implementation that uses a configuration variable for a URL. This makes the rule portable and easier to manage across different environments (development, staging, production).

```javascript
function(user, context, callback){
      var log_url = configuration.log_url;
      ...
    }
```

--------------------------------

### Activate Virtual Environment and Install SDK

Source: https://auth0.com/docs/quickstart/webapp/python

Commands to activate the Python virtual environment and install the required Auth0 server SDK and dependencies.

```bash
source venv/bin/activate
# or
venv\Scripts\activate

pip install auth0-server-python "flask[async]" python-dotenv

pip list | grep auth0
```

--------------------------------

### Initialize ASWebAuthenticationSessionBrowser

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Initializes the ASWebAuthenticationSessionBrowser with the option to prefer ephemeral browser sessions. This is a common setup for handling web-based authentication flows in applications.

```swift
Browser = new ASWebAuthenticationSessionBrowser
{
    PrefersEphemeralWebBrowserSession = false
}
);
```

--------------------------------

### Configure Environment Variables

Source: https://auth0.com/docs/quickstart/webapp/php

An example .env file structure containing the required Auth0 credentials and application configuration. This file should be stored in the project root and accessed by the application at runtime.

```env
# Your Auth0 application's Client ID
AUTH0_CLIENT_ID={yourClientId}

# The URL of your Auth0 tenant domain
AUTH0_DOMAIN={yourDomain}

# Your Auth0 application's Client Secret
AUTH0_CLIENT_SECRET={yourClientSecret}

# A long, secret value used to encrypt the session cookie.
# This can be generated using `openssl rand -hex 32` from your shell.
AUTH0_COOKIE_SECRET=

# A url your application is accessible from. Update this as appropriate.
AUTH0_BASE_URL=http://127.0.0.1:3000
```

--------------------------------

### Create New Java Web Project with Maven

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

Generates a new Java web application project using the Maven archetype 'maven-archetype-webapp'. This command initializes a basic web application structure suitable for further development.

```bash
mvn archetype:generate \
  -DgroupId=com.auth0.example \
  -DartifactId=auth0-servlet-app \
  -DarchetypeArtifactId=maven-archetype-webapp \
  -DinteractiveMode=false
```

--------------------------------

### Set API Key for Airtable Connection

Source: https://auth0.com/docs/api/management/v2/flows/post-flows-vault-connections

This example shows the structure for creating an Airtable connection. It requires a connection name, the 'AIRTABLE' app ID, and a setup object with the API key type and the actual API key.

```json
{
  "name": "string",
  "app_id": "AIRTABLE",
  "setup": {
    "type": "API_KEY",
    "api_key": "string"
  }
}
```

--------------------------------

### Render Quickstart Action Buttons

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

The QuickstartButtons component renders GitHub link and download buttons. It parses GitHub URLs to trigger sample downloads via the Auth0DocsUI interface and supports multi-language labels.

```javascript
export const QuickstartButtons = ({githubLink, lang = "en"}) => {
  const translations = {
    en: { viewOnGithub: "View On GitHub", loginAndDownload: "Download Sample" },
    "fr-ca": { viewOnGithub: "Afficher sur GitHub", loginAndDownload: "Télécharger un exemple" },
    "ja-jp": { viewOnGithub: "Githubで表示", loginAndDownload: "サンプルをダウンロード" }
  };
  const text = translations[lang] || translations.en;
  // ... parsing and rendering logic
  return <div className="quickstart_buttons">...</div>;
};
```

--------------------------------

### Start Server via Command Line

Source: https://auth0.com/docs/quickstart/webapp/fastapi

Shell commands to launch the FastAPI application using Uvicorn, either via the CLI or by executing the Python script directly.

```bash
# Using Uvicorn CLI
uvicorn main:app --reload --port 3000

# Using Python execution
python main.py
```

--------------------------------

### Navigate to Project Directory

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

Changes the current directory to the 'auth0-servlet-app' project folder. This is a standard command-line operation to access the project's files.

```bash
cd auth0-servlet-app
```

--------------------------------

### Install Flask Async Dependencies

Source: https://auth0.com/docs/quickstart/webapp/python

Command to install Flask with necessary asynchronous support to resolve event loop runtime errors.

```bash
pip install "flask[async]"
```

--------------------------------

### POST /u/login/signup

Source: https://auth0.com/docs/secure/attack-protection/configure-akamai-supplemental-signals

Initiates the user signup process.

```APIDOC
## POST /u/login/signup

### Description
Registers a new user account via the Universal Login flow.

### Method
POST

### Endpoint
/u/login/signup

### Parameters
#### Request Body
- **email** (array) - Required - User email address.
- **password** (array) - Required - User password.

### Request Example
{
  "email": ["user@example.com"],
  "password": ["securepassword123"]
}

### Response
#### Success Response (200)
- **status** (string) - Success message.
```

--------------------------------

### Initialize Auth0 SDK and Router (PHP)

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/php/interactive

Initializes the Auth0 SDK with provided credentials and sets up a basic router. This script is typically the entry point for the application, configuring the SDK and then passing control to the router.

```php
<?php

  declare(strict_types=1);

  require('vendor/autoload.php');

  use Auth0\SDK\Auth0;
  use Auth0\SDK\Configuration\SdkConfiguration;

  $configuration = new SdkConfiguration(
    domain: '{yourDomain}',
    clientId: '{yourClientId}',
    clientSecret: '{yourClientSecret}',
    redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
    cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
  );

  $sdk = new Auth0($configuration);

  require('router.php');
        
```

--------------------------------

### Implement User Signup

Source: https://auth0.com/docs/libraries/auth0js/v7

Shows how to register a new user against a database connection using the webAuth.signup method. Includes an example of capturing form input and passing user_metadata attributes.

```javascript
$('.signup-db').click(function (e) {
    e.preventDefault();
    webAuth.signup({
        connection: 'Username-Password-Authentication',
        email: $('.signup-email').val(),
        password: $('.signup-password').val(),
        user_metadata: { plan: 'silver', team_id: 'a111' }
    }, function (err) {
        if (err) return alert('Something went wrong: ' + err.message);
        return alert('success signup without login!')
    });
});
```

--------------------------------

### Clone and Run Auth0 Java EE Sample Application (Bash)

Source: https://auth0.com/docs/quickstart/webapp/java-ee

Provides commands to clone the Auth0 Java EE sample application from GitHub and set it up for execution. This includes cloning the repository, navigating to the sample directory, and running the application using Maven and WildFly. It guides users through the initial setup process to test Auth0 integration.

```bash
git clone https://github.com/auth0-samples/auth0-java-ee-sample.git
cd auth0-java-ee-sample/01-Login
./mvnw clean wildfly:run
```

--------------------------------

### Create New Angular Project

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Creates a new Angular project with routing and CSS styling enabled. This is the initial step for setting up the application.

```bash
npx @angular/cli@latest new auth0-angular --routing=true --style=css
```

--------------------------------

### Start development server

Source: https://auth0.com/docs/quickstart/spa/vuejs

Command to initialize the local development environment. Includes guidance on handling port conflicts by specifying an alternative port.

```shellscript
npm run dev
# To specify a custom port:
npm run dev -- --port 5174
```

--------------------------------

### GET /userinfo

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

Retrieves the user profile information using a valid access token obtained after authentication.

```APIDOC
## GET /userinfo

### Description
Fetches the user's profile information using an access token returned from the authentication flow.

### Method
GET

### Endpoint
webAuth.client.userInfo

### Parameters
#### Query Parameters
- **accessToken** (String) - Required - The access token received from the authentication result.

### Response
#### Success Response (200)
- **sub** (String) - Unique identifier for the user.
- **nickname** (String) - User's nickname.
- **email** (String) - User's email address.

#### Response Example
{
  "sub": "auth0|123456789012345678901234",
  "nickname": "johnfoo",
  "name": "johnfoo@gmail.com",
  "picture": "https://gravatar.com/avatar/example.png",
  "email": "johnfoo@gmail.com"
}
```

--------------------------------

### Install Auth0 CLI on Linux

Source: https://auth0.com/docs/deploy-monitor/auth0-cli

Installs the Auth0 CLI on Linux by downloading and executing an installation script. The script fetches the latest version and installs it to a specified binary path.

```bash
curl -sSfL https://raw.githubusercontent.com/auth0/auth0-cli/main/install.sh | sh -s -- -b /usr/local/bin
```

--------------------------------

### Auth0 React SDK Basic Setup

Source: https://auth0.com/docs/libraries/auth0-react

Example of setting up the Auth0Provider component to wrap a React application. This provides the necessary context for authentication across the app. Requires domain and clientId from Auth0.

```javascript
import React from 'react';
    import ReactDOM from 'react-dom';
    import { Auth0Provider } from '@auth0/auth0-react';
    import App from './App';
    ReactDOM.render(
      <Auth0Provider
        domain="{yourDomain}"
        clientId="{yourClientId}"
        authorizationParams={{
          redirect_uri: window.location.origin
        }}
    >
      <App />
    </Auth0Provider>,
    document.getElementById('app')
 );
```

--------------------------------

### Get User by Email (JavaScript)

Source: https://auth0.com/docs/authenticate/database-connections/custom-db/templates/get-user

A JavaScript example for the `getByEmail` function, which retrieves a user profile from a custom database. It outlines the three possible outcomes: user found, user not found, or an error during database access.

```javascript
function getByEmail(email, callback) {
  // This script should retrieve a user profile from your existing database,
  // without authenticating the user.
  // It is used to check if a user exists before executing flows that do not
  // require authentication (signup and password reset).
  //
  // There are three ways this script can finish:
  // 1. A user was successfully found. The profile should be in the following
  // format: https://auth0.com/docs/users/normalized/auth0/normalized-user-profile-schema.
  //     callback(null, profile);
  // 2. A user was not found
  //     callback(null);
  // 3. Something went wrong while trying to reach your database:
  //     callback(new Error("my error message"));
  const msg = 'Please implement the Get User script for this database connection ' +
    'at https://manage.auth0.com/#/connections/database';
  return callback(new Error(msg));
}
```

--------------------------------

### Signup

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

Sign up a new user for database connections using the `signup` method with user credentials and metadata.

```APIDOC
## Signup

### Description
Use the `signup` method to create a new user account for database connections. It accepts user credentials and optional metadata.

### Method
`webAuth.signup(options, callback)`

### Parameters
#### Options Object
- **email** (string) - Required - The user's email address.
- **password** (string) - Required - The user's desired password.
- **username** (string) - Required* - The user's desired username. Required if using a database connection with **Requires Username** enabled.
- **connection** (string) - Required - The name of the database connection to use for account creation.
- **user_metadata** (object) - Optional - Additional attributes for user information, stored in `user_metadata`.

### Request Example
```html
<h2>Signup Database Connection</h2>
<input type="email" class="signup-email" placeholder="Email">
<input type="password" class="signup-password" placeholder="Password">
<input type="button" class="signup-db" value="Signup!">

<script type="text/javascript">
    $('.signup-db').click(function (e) {
        e.preventDefault();
        webAuth.signup({
            connection: 'Username-Password-Authentication',
            email: $('.signup-email').val(),
            password: $('.signup-password').val(),
            user_metadata: { plan: 'silver', team_id: 'a111' }
        }, function (err) {
            if (err) return alert('Something went wrong: ' + err.message);
            return alert('Success signup without login!');
        });
    });
</script>
```

### Response
#### Success Response (Callback)
- **err** (object) - If an error occurs during signup, this object will contain error details. If successful, `err` will be null.
```

--------------------------------

### Install Auth0 SDK via Gradle

Source: https://auth0.com/docs/libraries/auth0-android

Adds the Auth0 Android library dependency to the application's build.gradle file. This is required to access Auth0 Authentication and Management APIs.

```kotlin
dependencies {
  // Add the Auth0 Android SDK
  implementation 'com.auth0.android:auth0:2.+'
}
```

--------------------------------

### Install and Configure Auth0 CLI (Windows PowerShell)

Source: https://auth0.com/docs/quickstart/spa/svelte

Installs the Auth0 CLI on Windows using Scoop and then uses it to set up a new Auth0 application for a Vite project. This command generates a .env file with necessary credentials.

```powershell
# Install Auth0 CLI if not already installed
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Launch development server

Source: https://auth0.com/docs/quickstart/spa/react/index

Command to start the local development environment. Includes instructions for handling port conflicts by specifying an alternative port.

```shellscript
npm run dev
# To specify a port:
npm run dev -- --port 5174
```

--------------------------------

### Automate Auth0 Configuration with CLI

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

A shell script to create an Auth0 application, retrieve credentials, and generate a .env file for local development.

```shell
AUTH0_APP_NAME="My Flask App" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:5000/callback -l http://localhost:5000 -o http://localhost:5000 --reveal-secrets --json > app-details.json && CLIENT_ID=$(python3 -c "import json; print(json.load(open('app-details.json'))['client_id'])") && CLIENT_SECRET=$(python3 -c "import json; print(json.load(open('app-details.json'))['client_secret'])") && DOMAIN=$(auth0 tenants list --json | python3 -c "import sys, json; print([t['name'] for t in json.load(sys.stdin) if t.get('active')][0])") && SECRET=$(openssl rand -hex 64) && echo "AUTH0_DOMAIN=${DOMAIN}" > .env && echo "AUTH0_CLIENT_ID=${CLIENT_ID}" >> .env && echo "AUTH0_CLIENT_SECRET=${CLIENT_SECRET}" >> .env && echo "AUTH0_SECRET=${SECRET}" >> .env && echo "AUTH0_REDIRECT_URI=http://localhost:5000/callback" >> .env && rm app-details.json && echo ".env file created with your Auth0 details:" && cat .env
```

--------------------------------

### Create Auth0 App and .env using Shell (macOS/Linux)

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This shell command creates a new Auth0 application, configures its callback and logout URLs, and generates a .env file with necessary Auth0 credentials and base URLs. It uses `jq` for JSON parsing and `openssl` for generating a secret.

```shell
AUTH0_APP_NAME="My Express App" && \
auth0 apps create -n "${AUTH0_APP_NAME}" -t regular \
  --callbacks http://localhost:3000 \
  --logout-urls http://localhost:3000 \
  --json | jq -r '"ISSUER_BASE_URL=https://\(.domain)\nCLIENT_ID=\(.client_id)\nSECRET='$(openssl rand -hex 32)'\nBASE_URL=http://localhost:3000"' > .env
```

--------------------------------

### Perform Auth0 Authorization Request

Source: https://auth0.com/docs/fr-ca/manage-users/my-account-api

Demonstrates how to construct and execute an HTTP GET request to the Auth0 authorize endpoint. The Ruby example focuses on SSL configuration and basic request execution, while the Swift example utilizes URLSession to handle asynchronous network requests.

```ruby
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/authorize?response_type=code&client_id={yourClientId}&redirect_uri=%7ByourRedirectUri%7D&scope=create%3Ame%3Aauthentication_methods&offline_access=&audience=https%3A%2F%2F{yourDomain}%2Fme%2F")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "GET"

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### Perform Authenticated GET Request

Source: https://auth0.com/docs/quickstart/backend/rails/interactive

Demonstrates how to send an HTTP GET request with a Bearer token in the Authorization header. These snippets handle connection setup, header configuration, and response logging for different environments.

```Objective-C
#import <Foundation/Foundation.h>
NSDictionary *headers = @{ @"authorization": @"Bearer YOUR_ACCESS_TOKEN_HERE" };
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http:///{yourDomain}/api_path"]
                                                cachePolicy:NSURLRequestUseProtocolCachePolicy
                                            timeoutInterval:10.0];
[request setHTTPMethod:@"get"];
[request setAllHTTPHeaderFields:headers];
NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                            if (error) {
                                                NSLog(@"%@", error);
                                            } else {
                                                NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                NSLog(@"%@", httpResponse);
                                            }
                                        }];
[dataTask resume];
```

```Python
import http.client
conn = http.client.HTTPConnection("")
headers = { 'authorization': "Bearer YOUR_ACCESS_TOKEN_HERE" }
conn.request("get", "/{yourDomain}/api_path", headers=headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

```Ruby
require 'uri'
require 'net/http'
url = URI("http:///{yourDomain}/api_path")
http = Net::HTTP.new(url.host, url.port)
request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer YOUR_ACCESS_TOKEN_HERE'
response = http.request(request)
puts response.read_body
```

```Swift
import Foundation
let headers = ["authorization": "Bearer YOUR_ACCESS_TOKEN_HERE"]
let request = NSMutableURLRequest(url: NSURL(string: "http:///{yourDomain}/api_path")! as URL,
                                    cachePolicy: .useProtocolCachePolicy,
                                timeoutInterval: 10.0)
request.httpMethod = "get"
request.allHTTPHeaderFields = headers
let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
    if (error != nil) {
        print(error!)
    } else {
        let httpResponse = response as? HTTPURLResponse
        print(httpResponse!)
    }
})
dataTask.resume()
```

--------------------------------

### Create and Navigate React Project

Source: https://auth0.com/docs/quickstart/spa/react/index

Initializes a new React project using Vite and navigates into the project directory. This sets up the basic structure for the React application.

```shellscript
npm create vite@latest auth0-react -- --template react-ts
cd auth0-react
```

--------------------------------

### Calling Protected APIs with Auth0

Source: https://auth0.com/docs/quickstart/spa/react/index

Shows how to configure the Auth0Provider with an API audience and retrieve access tokens to authorize requests. The implementation includes both the provider setup and a component example using fetch with an Authorization header.

```jsx
import { Auth0Provider } from '@auth0/auth0-react';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Auth0Provider
    domain={import.meta.env.VITE_AUTH0_DOMAIN}
    clientId={import.meta.env.VITE_AUTH0_CLIENT_ID}
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "YOUR_API_IDENTIFIER"
    }}
  >
    <App />
  </Auth0Provider>
);
```

```jsx
import { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function ApiCall() {
  const { getAccessTokenSilently } = useAuth0();
  const [apiResponse, setApiResponse] = useState(null);

  const callProtectedApi = async () => {
    try {
      const token = await getAccessTokenSilently();
      
      const response = await fetch('/api/protected', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      setApiResponse(data);
    } catch (error) {
      console.error('API call failed:', error);
    }
  };

  return (
    <div>
      <button onClick={callProtectedApi}>Call API</button>
      {apiResponse && <pre>{JSON.stringify(apiResponse, null, 2)}</pre>}
    </div>
  );
}

export default ApiCall;
```

--------------------------------

### Initialize Auth0 SDK for Account Management

Source: https://auth0.com/docs/troubleshoot/product-lifecycle/past-migrations/link-user-accounts-with-access-tokens-migration

Configures the Auth0 WebAuth and Management SDK instances for user authentication and identity management. These examples show the setup for both ID token-based and Access token-based workflows.

```javascript
// get an ID Token
var webAuth = new auth0.WebAuth({
  clientID: '{yourClientId}',
  domain: '{yourDomain}',
  redirectUri: 'https://{yourApp}/callback',
  scope: 'openid',
  responseType: 'id_token'
});
// create a new instance
var auth0Manage = new auth0.Management({
  domain: '{yourDomain}',
  token: '{yourIdToken}'
});
```

```javascript
// get an Access Token
  var webAuth = new auth0.WebAuth({
    clientID: '{yourClientId}',
    domain: '{yourDomain}',
    redirectUri: 'https://{yourApp}/callback',
    audience: 'https://{yourDomain}/api/v2/',
    scope: 'update:current_user_identities',
    responseType: 'token id_token'
  });
  // create a new instance
  var auth0Manage = new auth0.Management({
    domain: '{yourDomain}',
    token: '{yourMgmtApiAccessToken}'
  });
```

--------------------------------

### Initialize and Configure Go Project

Source: https://auth0.com/docs/quickstart/backend/golang/interactive

Commands to set up a new Go project directory, initialize a module, and install necessary Auth0 and environment dependencies. It also provides the resulting go.mod file structure.

```bash
mkdir myapi && cd myapi
go mod init github.com/yourorg/myapi
go get github.com/auth0/go-jwt-middleware/v3
go get github.com/joho/godotenv
go mod download
```

```go
// go.mod
module github.com/yourorg/myapi

go 1.24

require (
    github.com/auth0/go-jwt-middleware/v3 v3.0.0
    github.com/joho/godotenv v1.5.1
)
```

--------------------------------

### GET /api/v2/clients

Source: https://auth0.com/docs/customize/custom-domains/configure-features-to-use-custom-domains

Example of calling the Management API using an Access Token obtained via a custom domain.

```APIDOC
## GET /api/v2/clients

### Description
Retrieves client information from the Management API using a custom domain.

### Method
GET

### Endpoint
https://{yourCustomDomain}/api/v2/clients

### Parameters
#### Headers
- **Authorization** (string) - Required - Bearer <access_token>

### Request Example
GET https://mycustomdomain.com/api/v2/clients
Authorization: Bearer <access_token>

### Response
#### Success Response (200)
- **clients** (array) - List of client applications.
```

--------------------------------

### OIDC Authorization Request with prompt=login

Source: https://auth0.com/docs/authenticate/login/max-age-reauthentication

An example of an HTTP GET request to the Auth0 authorize endpoint including the prompt=login parameter to force user re-authentication.

```http
https://mydomain.auth0.com/authorize?
client_id=abcd1234
&redirect_uri= https://mydomain.com/callback
&scope=openid profile
&response_type=id_token
&prompt=login
```

--------------------------------

### POST /u/signup

Source: https://auth0.com/docs/secure/attack-protection/configure-akamai-supplemental-signals

Configures the user signup endpoint for Universal Login on Akamai.

```APIDOC
## POST /u/signup

### Description
Handles user registration requests within the Universal Login flow.

### Method
POST

### Endpoint
/u/signup

### Request Body
- **requestBody** (object) - Required - The payload containing signup details as defined by the application schema.

### Request Example
{
  "requestBody": { "content": { "application/x-www-form-urlencoded": { "schema": { "type": "object" } } } }
}

### Response
#### Success Response (200)
- **status** (string) - Indicates successful processing of the signup request.
```

--------------------------------

### Set up ASP.NET Core MVC Project and Install Auth0 SDK

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core/interactive

This snippet demonstrates how to check for an existing ASP.NET Core project and either create a new one or install the Auth0 SDK into an existing project. It ensures the necessary package is available for authentication.

```bash
# Check if .NET SDK is available
dotnet --version

# Check for existing .NET project
if ls *.csproj 1> /dev/null 2>&1; then
  echo "Found .csproj file, checking project type..."
  ls *.csproj
else
  echo "No .csproj found, will create new project"
fi

# Install Auth0 SDK (example for existing project)
dotnet add package Auth0.AspNetCore.Authentication

# Create new project and install SDK (example)
dotnet new mvc -n Auth0MvcApp && cd Auth0MvcApp && dotnet add package Auth0.AspNetCore.Authentication
```

--------------------------------

### Initialize FastAPI Project Environment

Source: https://auth0.com/docs/quickstart/backend/fastapi

Commands to verify the environment, create a virtual environment, and prepare the project structure for FastAPI development.

```bash
python3 --version && pip --version
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "app.py" ]; then
  echo "Found existing Python project"
  ls -la
else
  mkdir my-fastapi-api && cd my-fastapi-api && python3 -m venv venv && source venv/bin/activate
fi
```

--------------------------------

### Set up Main Application View

Source: https://auth0.com/docs/quickstart/spa/flutter/interactive

Replaces the default main.dart content to set up the root of the Flutter Web application. It imports necessary packages and initializes the MaterialApp widget.

```dart
import 'package:flutter/material.dart';
import 'package:auth0_flutter/auth0_flutter_web.dart';
import 'auth0_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Auth0 Flutter Web',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),

```

--------------------------------

### Troubleshooting and Maintenance Commands

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

Essential commands for cleaning native project artifacts, updating CocoaPods, and resolving common build-time errors.

```bash
# Clean and regenerate native projects
npx expo prebuild --clean

# Update iOS dependencies
cd ios
pod install --repo-update
cd ..
```

--------------------------------

### Initialize Auth0 MCP Server for AI Clients

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

Commands to initialize the Auth0 MCP server for supported AI clients. These commands automate the configuration process for Claude Desktop, Cursor, and Windsurf.

```bash
npx @auth0/auth0-mcp-server init
```

```bash
npx @auth0/auth0-mcp-server init --client cursor
```

```bash
npx @auth0/auth0-mcp-server init --client windsurf
```

--------------------------------

### GET Pet Information Response Body

Source: https://auth0.com/docs/customize/integrations/aws/aws-api-gateway-delegation/aws-api-gateway-delegation-1

The expected JSON response structure when querying the GET method after successfully posting pet data. It returns a list of pet objects currently stored in the system.

```json
[
  {
    "id": 1,
    "price": 249.99,
    "type": "dog"
  },
  {
    "id": 2,
    "price": 124.99,
    "type": "cat"
  }
]
```

--------------------------------

### Create React Native Project

Source: https://auth0.com/docs/quickstart/native/react-native/index

Initializes a new React Native project and navigates into the project directory. This step ensures the project is set up with the necessary structure for development. It requires Node.js and npm to be installed.

```bash
npx @react-native-community/cli init Auth0ReactNativeSample
cd Auth0ReactNativeSample
```

--------------------------------

### Install and Configure Auth0 CLI (macOS)

Source: https://auth0.com/docs/quickstart/spa/svelte

Installs the Auth0 CLI on macOS using Homebrew and then uses it to set up a new Auth0 application for a Vite project. This command generates a .env file with necessary credentials.

```bash
# Install Auth0 CLI if not already installed
brew tap auth0/auth0-cli && brew install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Initialize Fastify Project

Source: https://auth0.com/docs/quickstart/backend/fastify

Commands to create a new project directory, initialize a Node.js project, and set up the initial file structure.

```shellscript
mkdir auth0-fastify-api && cd auth0-fastify-api
npm init -y
touch server.js .env
```

--------------------------------

### Get User Authentication Methods (PHP)

Source: https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authentication-methods-with-management-api

This PHP example uses cURL to make a GET request to the Auth0 Management API to fetch user authentication methods. It configures cURL options for the request, including the authorization header.

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://%7ByourDomain%7D/api/v2/users/%7BuserId%7D/authentication-methods",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer {yourMgmtApiAccessToken}"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

--------------------------------

### Get User Authentication Methods (Node.js)

Source: https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authentication-methods-with-management-api

This Node.js example uses the Axios library to make a GET request to the Auth0 Management API to fetch a user's authentication methods. It includes the necessary headers with the access token.

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://%7ByourDomain%7D/api/v2/users/%7BuserId%7D/authentication-methods',
  headers: {authorization: 'Bearer {yourMgmtApiAccessToken}'}
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### Initialize Auth0 Client for Mobile

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Configures the Auth0Client instance for Android and iOS platforms. Requires domain and client ID parameters to establish secure communication with Auth0.

```csharp
using Auth0.OidcClient;
using Android.App;
using Android.Content;

[Activity(Label = "Auth0Sample", MainLauncher = true, Icon = "@drawable/icon",
    LaunchMode = LaunchMode.SingleTask)]
[IntentFilter(
    new[] { Intent.ActionView },
    Categories = new[] { Intent.CategoryDefault, Intent.CategoryBrowsable },
    DataScheme = "YOUR_ANDROID_PACKAGE_NAME",
    DataHost = "{yourDomain}",
    DataPathPrefix = "/android/YOUR_ANDROID_PACKAGE_NAME/callback")]
public class MainActivity : Activity
{
    private Auth0Client auth0Client;

    protected override void OnCreate(Bundle savedInstanceState)
    {
        base.OnCreate(savedInstanceState);

        auth0Client = new Auth0Client(new Auth0ClientOptions
        {
            Domain = "{yourDomain}",
            ClientId = "{yourClientId}"
        }, this);
    }

    protected override async void OnNewIntent(Intent intent)
    {
        base.OnNewIntent(intent);
        Auth0.OidcClient.ActivityMediator.Instance.Send(intent.DataString);
    }
}
```

```csharp
using Auth0.OidcClient;
using Foundation;
using UIKit;

[Register("AppDelegate")]
public class AppDelegate : UIApplicationDelegate
{
    private Auth0Client auth0Client;

    public override bool FinishedLaunching(UIApplication application, NSDictionary launchOptions)
    {
        auth0Client = new Auth0Client(new Auth0ClientOptions
        {
            Domain = "{yourDomain}",
            ClientId = "{yourClientId}"
        });

        return true;
    }

    public override bool OpenUrl(UIApplication application, NSUrl url,
        string sourceApplication, NSObject annotation)
    {
        ActivityMediator.Instance.Send(url.AbsoluteString);
        return true;
    }
}
```

--------------------------------

### Auth0 CLI Setup for Next.js

Source: https://auth0.com/docs/quickstart/webapp/nextjs

Commands to install and use the Auth0 CLI to set up a new Auth0 application for a Next.js project. This process automatically generates a `.env.local` file with required configuration.

```shellscript
# Install Auth0 CLI (if not already installed)
brew tap auth0/auth0-cli && brew install auth0

# Set up Auth0 app and generate .env.local file
auth0 qs setup --type nextjs -n "My App" -p 3000
```

```powershell
# Install Auth0 CLI (if not already installed)
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0

# Set up Auth0 app and generate .env.local file
auth0 qs setup --type nextjs -n "My App" -p 3000
```

--------------------------------

### Retrieve Airport Name via GET Request

Source: https://auth0.com/docs/customize/integrations/google-cloud-endpoints

Demonstrates how to perform a GET request to the /airportName endpoint across multiple programming languages. Each example passes an IATA code as a query parameter to fetch the corresponding airport name.

```bash
curl --request GET \
  --url 'https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO'
```

```csharp
var client = new RestClient("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO");
var request = new RestRequest(Method.GET);
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://%7ByourGceProject%7D.appspot.com/airportName',
  params: {iataCode: 'SFO'}
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objective-c
#import <Foundation/Foundation.h>

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO"]
                                                       cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                   timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                            completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                if (error) {
                                                    NSLog(@"%@", error);
                                                } else {
                                                    NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                    NSLog(@"%@", httpResponse);
                                                }
                                            }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("")

conn.request("GET", "%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let request = NSMutableURLRequest(url: NSURL(string: "https://%7ByourGceProject%7D.appspot.com/airportName?iataCode=SFO")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "GET"

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### Create New ASP.NET Core Web API and Install SDK

Source: https://auth0.com/docs/quickstart/backend/aspnet-core-webapi

This command creates a new ASP.NET Core Web API project named 'Auth0Api' and then installs the Auth0 SDK. It's used when starting a new project. The commands first create the project, navigate into its directory, and then add the necessary package.

```bash
dotnet new webapi -n Auth0Api && cd Auth0Api && dotnet add package Auth0.AspNetCore.Authentication.Api
```

--------------------------------

### Initialize Auth0 SDK Configuration

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/php/interactive

Sets up the Auth0 SDK instance with required credentials and configuration parameters. This is the entry point for all authentication operations.

```php
require('vendor/autoload.php');

use Auth0\SDK\Auth0;
use Auth0\SDK\Configuration\SdkConfiguration;

$configuration = new SdkConfiguration(
  domain: '{yourDomain}',
  clientId: '{yourClientId}',
  clientSecret: '{yourClientSecret}',
  redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
  cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
);

$sdk = new Auth0($configuration);
```

--------------------------------

### Create New Svelte Project and Install Auth0 SDK (npx)

Source: https://auth0.com/docs/quickstart/spa/svelte

Creates a new minimal Svelte project with TypeScript support and installs the Auth0 SPA JS SDK. This command also navigates into the project directory and installs project dependencies.

```bash
npx sv create auth0-svelte --template minimal --types ts --no-add-ons --no-install && cd auth0-svelte && npm install && npm install @auth0/auth0-spa-js
```

--------------------------------

### Navigate to Project Directory and Run Dev Server (Bash)

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Ensures the terminal is in the correct project directory before running the development server. This is crucial for commands like `npm run dev` to execute successfully.

```bash
cd auth0-vanillajs && npm run dev
```

--------------------------------

### Get User Authentication Methods (Ruby)

Source: https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authentication-methods-with-management-api

This Ruby example uses the Net::HTTP library to perform a GET request to the Auth0 Management API for fetching user authentication methods. It configures the HTTP request with the necessary authorization header.

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://%7ByourDomain%7D/api/v2/users/%7BuserId%7D/authentication-methods")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer {yourMgmtApiAccessToken}'

response = http.request(request)
puts response.read_body
```

--------------------------------

### Install Auth0 Flutter SDK and Dependencies

Source: https://auth0.com/docs/quickstart/spa/flutter/interactive

Adds the Auth0 Flutter SDK to the project and includes the necessary Auth0 SPA JS library in the web application's index.html. The SPA JS library is crucial for the Flutter Web SDK's functionality.

```shell
flutter pub add auth0_flutter
```

```html
<!DOCTYPE html>
<html>
<head>
  <!-- ... existing head content ... -->
</head>
<body>
  <!-- ... existing body content ... -->

  <!-- Add this before closing body tag -->
  <script src="https://cdn.auth0.com/js/auth0-spa-js/2.9/auth0-spa-js.production.js" defer></script>
</body>
</html>

```

--------------------------------

### Server Startup and Logging (JavaScript)

Source: https://auth0.com/docs/quickstart/spa/capn-web

This snippet demonstrates the server startup process and logs essential information to the console. It includes the server's listening port, Auth0 configuration details (domain, client ID, audience), and a list of available RPC methods. This is useful for monitoring and debugging the server's operational status.

```javascript
      });

    server.listen(PORT, () => {
      console.log('🚀 Cap'n Web Auth0 Server Started');
      console.log('📍 Server running on http://localhost:' + PORT);
      console.log('🔐 Auth0 Domain:', AUTH0_DOMAIN);
      console.log('🆔 Client ID:', AUTH0_CLIENT_ID.substring(0, 8) + '...');
      console.log('🎯 API Audience:', AUTH0_AUDIENCE);
      console.log('
📋 Available RPC Methods:');
      console.log('   - getProfile (authenticated)');
      console.log('   - updateProfile (authenticated)');
      console.log('   - getPublicData (public)');
    });
```

--------------------------------

### Auth0 CLI Setup - Windows

Source: https://auth0.com/docs/quickstart/spa/capn-web

This script sets up Auth0 for a new Cap'n Web application on Windows using PowerShell. It installs the Auth0 CLI via winget, logs in, creates an API and a SPA application, configures environment variables in a .env file, and cleans up temporary files. It uses ConvertFrom-Json and Where-Object for data manipulation.

```powershell
$AppName = "My Cap'n Web App"; $ApiName = "Cap'n Web API"; $ApiIdentifier = "https://capnweb-api.$((Get-Date).Ticks).com"; winget install Auth0.CLI; auth0 login --no-input; auth0 apis create --name "$ApiName" --identifier "$ApiIdentifier" --scopes "read:profile,write:profile" --json | Set-Content -Path auth0-api-details.json; auth0 apps create -n "$AppName" -t spa -c http://localhost:3000 -l http://localhost:3000 -o http://localhost:3000 --json | Set-Content -Path auth0-app-details.json; $ClientId = (Get-Content -Raw auth0-app-details.json | ConvertFrom-Json).client_id; $Domain = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name; Set-Content -Path .env -Value "AUTH0_DOMAIN=$Domain"; Add-Content -Path .env -Value "AUTH0_CLIENT_ID=$ClientId"; Add-Content -Path .env -Value "AUTH0_AUDIENCE=$ApiIdentifier"; Add-Content -Path .env -Value "PORT=3000"; Add-Content -Path .env -Value "NODE_ENV=development"; Remove-Item auth0-app-details.json, auth0-api-details.json; Write-Output ".env file created with your Auth0 details:"; Get-Content .env
```

--------------------------------

### Get Access Token for API Calls (JavaScript)

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Retrieves an access token from Auth0 for making authenticated requests to a protected API. It includes specifying the audience and scope for the token.

```javascript
async function getAccessToken() {
  try {
    const token = await auth0Client.getTokenSilently({
      authorizationParams: {
        audience: 'YOUR_API_IDENTIFIER',
        scope: 'read:messages'
      }
    });
    
    const response = await fetch('/api/protected', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error getting token:', error);
  }
}
```

--------------------------------

### Install Auth0 Agent Skills (Bash)

Source: https://auth0.com/docs/quickstart/spa/react/index

This bash command installs the necessary Auth0 agent skills for integrating authentication into an application. It uses `npx` to execute the `skills` command and adds specific skills like `auth0/agent-skills`, `auth0-quickstart`, and `auth0-react`.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-react

```

--------------------------------

### Initialize Server

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/golang/interactive

The main entry point that loads environment variables, initializes the Auth0 authenticator, sets up the router, and starts the HTTP server.

```golang
func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)
	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}
```

--------------------------------

### Sign In Link Example

Source: https://auth0.com/docs/get-started/applications/dynamic-client-registration

An HTML anchor tag example that constructs the authorization URL for initiating the sign-in process with specific scopes and audience.

```APIDOC
## HTML Link for Sign In

### Description
Provides an example of an HTML anchor tag that directs users to the Auth0 authorization endpoint to initiate the sign-in process.

### Method
GET (via link click)

### Endpoint
`https://{yourDomain}/authorize` (constructed within the `href` attribute)

### Request Example
```html
<a href="https://{yourDomain}/authorize?scope=appointments%20contacts&audience=appointments:api&response_type=id_token%20token&client_id={yourClientId}&redirect_uri={https://yourApp/callback}">
  Sign In
</a>
```
```

--------------------------------

### Initialize Auth0 Client

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

Instantiate the Auth0Client with your specific domain and client ID configuration.

```csharp
using Auth0.OidcClient;

var client = new Auth0Client(new Auth0ClientOptions
{
    Domain = "{yourDomain}",
    ClientId = "{yourClientId}"
});
```

--------------------------------

### Configure Auth0 SDK in web.xml

Source: https://auth0.com/docs/quickstart/webapp/java/index

Sets up the Auth0 SDK configuration within the web.xml file for a Java servlet application. This includes context parameters for Auth0 credentials and settings.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
             version="3.1">

    <display-name>Auth0 Servlet Example</display-name>

    <!-- Auth0 Configuration -->
    <context-param>

```

--------------------------------

### Manual Setup Instructions for Auth0

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core/interactive

These are manual steps required to set up your application in the Auth0 dashboard. This includes creating a new application, configuring its name, type, and callback URLs, and updating your application's configuration file with Auth0 credentials.

```bash
echo "📋 MANUAL SETUP REQUIRED:"
  echo "1. Go to https://manage.auth0.com/dashboard/"
  echo "2. Navigate to Applications → Applications"
  echo "3. Click 'Create Application'"
  echo "4. Set Name: 'My MVC App'"
  echo "5. Select 'Regular Web Applications'"
  echo "6. In Settings, set Allowed Callback URLs: https://localhost:5001/callback"
  echo "7. Set Allowed Logout URLs: https://localhost:5001/"
  echo "8. Update appsettings.json with your Domain, Client ID, and Client Secret"
```

--------------------------------

### User Identifier Configuration Example

Source: https://auth0.com/docs/authenticate/enterprise-connections/user-attribute-profile

An example demonstrating the configuration of the user identifier, including default mappings and strategy overrides for different identity providers.

```APIDOC
## User Identifier Example

```json
"user_id": {
  "oidc_mapping": "sub",
  "saml_mapping": [
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
  ],
  "scim_mapping": "externalId",
  "strategy_overrides": {
    "waad": {
      "oidc_mapping": "oid"
    },
    "samlp": {
      "scim_mapping": "userName"
    },
    "google-apps": {
      "oidc_mapping": "email"
    }
  }
}
```

* **Default identifier**: `externalId` via SCIM.
* **SAML**: Multiple identifier URIs supported.
* **OIDC**: Uses `sub`.
* **Overrides**: SAML and WAAD customize mappings.
```

--------------------------------

### Implement Authentication Login and Logout

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Demonstrates how to handle user authentication states using the Auth0Client. The login flow triggers the system browser, while the logout method clears the session.

```csharp
public async Task LogoutAsync()
{
	var logoutResult = await auth0Client.LogoutAsync();

	if (logoutResult == BrowserResultType.Success)
	{
		Console.WriteLine("Logged out successfully");
	}
}
```

--------------------------------

### Event Listeners Setup for Auth0 Class

Source: https://auth0.com/docs/quickstart/spa/capn-web

Configures event listeners for buttons within an Auth0-related class, including login, logout, get profile, update profile, and get public data. These listeners trigger corresponding methods within the class.

```javascript
setupEventListeners() {
  document.getElementById('login-btn').addEventListener('click', () => this.login());
  document.getElementById('logout-btn').addEventListener('click', () => this.logout());
  document.getElementById('get-profile-btn').addEventListener('click', () => this.getProfile());
  document.getElementById('update-profile-btn').addEventListener('click', () => this.updateProfile());
  document.getElementById('get-public-btn').addEventListener('click', () => this.getPublicData());
}
```

--------------------------------

### Install Auth0 Agent Skills (Bash)

Source: https://auth0.com/docs/quickstart/spa/react

This bash command installs the necessary Auth0 agent skills for integrating authentication into an application. It uses the 'npx skills add' command to fetch and install the 'auth0/agent-skills' package, along with specific skills like 'auth0-quickstart' and 'auth0-react'.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-react
```

--------------------------------

### Install iOS Pods and Run Development Build

Source: https://auth0.com/docs/quickstart/native/react-native-expo

This sequence of commands first navigates to the iOS directory, installs or updates the CocoaPods dependencies, and then runs the iOS development build. This is often necessary to resolve Pod-related errors during iOS builds.

```bash
cd ios
pod install --repo-update
cd ..
npx expo run:ios
```

--------------------------------

### Get User Authentication Methods (C#)

Source: https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authentication-methods-with-management-api

This C# example demonstrates how to fetch a user's authentication methods using the RestSharp library. It makes a GET request to the Auth0 Management API endpoint and requires the domain, user ID, and an access token.

```csharp
var client = new RestClient("https://%7ByourDomain%7D/api/v2/users/%7BuserId%7D/authentication-methods");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer {yourMgmtApiAccessToken}");
IRestResponse response = client.Execute(request);
```

--------------------------------

### Make GET Request to Auth0 API in Ruby

Source: https://auth0.com/docs/fr-ca/authenticate/identity-providers/pass-parameters-to-idps

This Ruby snippet shows how to construct and send a GET request to the Auth0 Management API. It sets the 'authorization' and 'content-type' headers before sending the request and printing the response body. Ensure you have the Net::HTTP library available.

```ruby
request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer {yourMgmtApiAccessToken}'
request["content-type"] = 'application/json'

response = http.request(request)
puts response.read_body
```

--------------------------------

### Example Auth0 Quota Headers

Source: https://auth0.com/docs/fine-grained-m2m-token-quotas-early-access

This snippet shows an example of the Auth0-Client-Quota-Limit and Auth0-Organization-Quota-Limit headers returned in Auth0 responses. These headers provide information about quota consumption in different time buckets (per_hour, per_day).

```text
Auth0-Client-Quota-Limit: b=per_hour;q=10;r=7;t=3540,b=per_day;q=50;r=47;t=43200
Auth0-Organization-Quota-Limit: b=per_hour;q=50;r=47;t=3540,b=per_day;q=250;r=247;t=43200
```

--------------------------------

### Install Auth0 React SDK and Dependencies

Source: https://auth0.com/docs/quickstart/spa/react/index

Installs the Auth0 React SDK and any other necessary project dependencies. This command ensures that the Auth0 SDK is available for use within the React application.

```shellscript
npm add @auth0/auth0-react && npm install
```

--------------------------------

### Send SMS Passwordless Code (Go)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using Go's standard net/http package. No external dependencies beyond standard libraries. Input includes domain, client ID, client secret, and user's phone number. Outputs HTTP response and body.

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/passwordless/start"

	payload := strings.NewReader("{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("content-type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

--------------------------------

### Get User by Email (ASP.NET Membership Provider - Universal Providers)

Source: https://auth0.com/docs/authenticate/database-connections/custom-db/templates/get-user

An example using Node.js with the 'tedious' library to connect to a SQL Server database for retrieving user information based on email. It handles connection, query execution, and user profile mapping.

```javascript
function getByEmail(email, callback) {
  const sqlserver = require('tedious@1.11.0');
  const Connection = sqlserver.Connection;
  const Request = sqlserver.Request;
  const TYPES = sqlserver.TYPES;
  const connection = new Connection({
    userName: 'the username',
    password: 'the password',
    server: 'the server',
    options: {
      database: 'the db name',
      encrypt: true // for Windows Azure
    }
  });
  connection.on('debug', function(text) {
    // if you have connection issues, uncomment this to get more detailed info
    //console.log(text);
  }).on('errorMessage', function(text) {
    // this will show any errors when connecting to the SQL database or with the SQL statements
    console.log(JSON.stringify(text));
  });
  connection.on('connect', function(err) {
    if (err) return callback(err);
    var user = {};
    const query =
      'SELECT Memberships.UserId, Email, Users.UserName ' +
      'FROM Memberships INNER JOIN Users ' +
      'ON Users.UserId = Memberships.UserId ' +
      'WHERE Memberships.Email = @Username OR Users.UserName = @Username';
    const getMembershipQuery = new Request(query, function(err, rowCount) {
      if (err) return callback(err);
      if (rowCount < 1) return callback();
      callback(null, user);
    });
    getMembershipQuery.addParameter('Username', TYPES.VarChar, email);
    getMembershipQuery.on('row', function(fields) {
      user = {
        user_id: fields.UserId.value,
        nickname: fields.UserName.value,
        email: fields.Email.value
      };
    });
    connection.execSql(getMembershipQuery);
  });
}
```

--------------------------------

### Auth0 CLI Setup - macOS

Source: https://auth0.com/docs/quickstart/spa/capn-web

This script sets up Auth0 for a new Cap'n Web application on macOS. It installs the Auth0 CLI, logs in, creates an API and a SPA application, configures environment variables in a .env file, and cleans up temporary files. Dependencies include Homebrew and jq.

```bash
AUTH0_APP_NAME="My Cap'n Web App" && AUTH0_API_NAME="Cap'n Web API" && AUTH0_API_IDENTIFIER="https://capnweb-api.$(date +%s).com" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apis create --name "${AUTH0_API_NAME}" --identifier "${AUTH0_API_IDENTIFIER}" --scopes "read:profile,write:profile" --json > auth0-api-details.json && auth0 apps create -n "${AUTH0_APP_NAME}" -t spa -c http://localhost:3000 -l http://localhost:3000 -o http://localhost:3000 --json > auth0-app-details.json && CLIENT_ID=$(jq -r '.client_id' auth0-app-details.json) && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && echo "AUTH0_DOMAIN=${DOMAIN}" > .env && echo "AUTH0_CLIENT_ID=${CLIENT_ID}" >> .env && echo "AUTH0_AUDIENCE=${AUTH0_API_IDENTIFIER}" >> .env && echo "PORT=3000" >> .env && echo "NODE_ENV=development" >> .env && rm auth0-app-details.json auth0-api-details.json && echo ".env file created with your Auth0 details:" && cat .env
```

--------------------------------

### Example Connection Response JSON

Source: https://auth0.com/docs/authenticate/passwordless/authentication-methods/use-sms-gateway-passwordless

A sample JSON response structure returned by the GET connections endpoint, showing the schema for an SMS connection including its ID and configuration options.

```JSON
[
    {
        "id": "con_UX85K7K0N86INi9U",
        "options": {
            "disable_signup": false,
            "name": "sms",
            "twilio_sid": "TWILIO_SID",
            "twilio_token": "TWILIO_AUTH_TOKEN",
            "from": "+15555555555",
            "syntax": "md_with_macros",
            "template": "Your SMS verification code is: @@password@@",
            "totp": {
                "time_step": 300,
                "length": 6
            },
            "messaging_service_sid": null,
            "brute_force_protection": true
        },
        "strategy": "sms",
        "name": "sms",
        "is_domain_connection": false,
        "realms": [
            "sms"
        ]
    }
]
```

--------------------------------

### Web Callback URL Configuration

Source: https://auth0.com/docs/quickstart/native/flutter

This is the Allowed Callback URL for a web application during development. It specifies the local development server address.

```text
http://localhost:3000
```

--------------------------------

### Create Auth0 API and Configure Environment (Shellscript)

Source: https://auth0.com/docs/quickstart/backend/fastapi

This script automates the creation of an Auth0 API and configures the environment variables (AUTH0_DOMAIN and AUTH0_AUDIENCE) in a .env file. It requires the Auth0 CLI and jq to be installed.

```shellscript
AUTH0_API_NAME="My FastAPI API" && AUTH0_API_IDENTIFIER="https://my-fastapi-api" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apis create --name "${AUTH0_API_NAME}" --identifier "${AUTH0_API_IDENTIFIER}" --signing-alg RS256 --no-input && echo "AUTH0_DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name')\nAUTH0_AUDIENCE=${AUTH0_API_IDENTIFIER}" > .env
```

--------------------------------

### Check for Project Configuration

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Checks for the existence of a package.json file in the current directory to determine if a project is already initialized.

```bash
if [ -f "package.json" ]; then
  echo "Found package.json, checking for dependencies..."
  cat package.json
else
  echo "No package.json found, will create new project"
fi
```

--------------------------------

### Get User Attribute Profile Templates

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/okta

Retrieves a list of default user attribute profile templates. These can be used as a starting point for creating custom user attribute profiles.

```APIDOC
## GET /api/v2/user-attribute-profiles/templates

### Description
Retrieves default templates for user attribute profiles.

### Method
GET

### Endpoint
/api/v2/user-attribute-profiles/templates

### Parameters
N/A

### Request Example
(No request body for GET requests)

### Response
#### Success Response (200 OK)
- **templates** (array) - An array of user attribute profile template objects.

#### Response Example
```json
{
  "templates": [
    {
      "name": "Default Template",
      "attributes": [
        {
          "key": "email",
          "value": ""
        },
        {
          "key": "name",
          "value": ""
        }
      ]
    }
  ]
}
```
```

--------------------------------

### Install Auth0 Vue SDK and Dependencies

Source: https://auth0.com/docs/quickstart/spa/vuejs

Installs the Auth0 Vue SDK and any other necessary npm packages, followed by running a general npm install to ensure all dependencies are met.

```shellscript
npm add @auth0/auth0-vue && npm install
```

--------------------------------

### Handle Login Requests with LoginServlet

Source: https://auth0.com/docs/quickstart/webapp/java/index

A servlet that initiates the Auth0 authentication flow by constructing the authorization URL and redirecting the user to the Auth0 login page.

```java
@WebServlet(urlPatterns = {"/login"})
public class LoginServlet extends HttpServlet {
    private AuthenticationController authenticationController;

    @Override
    public void init(ServletConfig config) throws ServletException {
        super.init(config);
        authenticationController = AuthenticationControllerProvider.getInstance(config);
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        String redirectUri = req.getScheme() + "://" + req.getServerName() + ":" + req.getServerPort() + "/callback";
        String authorizeUrl = authenticationController.buildAuthorizeUrl(req, res, redirectUri).build();
        res.sendRedirect(authorizeUrl);
    }
}
```

--------------------------------

### Home Servlet Example (Java)

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/java/interactive

A basic Java servlet example for the home page, typically used after successful authentication. This snippet shows the structure of a servlet that might be used to render the main content of the application.

```java
@WebServlet(urlPatterns = {"/portal/home"})
public class HomeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {

```

--------------------------------

### Router Setup (router.go)

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/golang/interactive

This Go snippet sets up the router for the application using the Gin framework. It configures session management using cookie-based sessions and initializes the Authenticator. It also imports middleware and handlers for various authentication-related routes.

```golang
// Save this file in ./platform/router/router.go

package router

import (
	"encoding/gob"
	"net/http"

	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"

	"01-Login/platform/authenticator"
	"01-Login/platform/middleware"

```

--------------------------------

### Configure Auth0 Client with Custom Scopes

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Initializes the Auth0Client with specific scopes to request additional user profile information.

```csharp
var auth0Client = new Auth0Client(new Auth0ClientOptions
{
	Domain = "{yourDomain}",
	ClientId = "{yourClientId}",
	Scope = "openid profile email offline_access read:posts"
});
```

--------------------------------

### Initialize and Continue Phone Enrollment (TypeScript)

Source: https://auth0.com/docs/libraries/acul/js-sdk/Screens/classes/PhoneIdentifierEnrollment

Demonstrates how to initialize the PhoneIdentifierEnrollment class and initiate the phone enrollment process. This example shows the basic setup and the call to continuePhoneEnrollment with a specified type.

```typescript
import PhoneIdentifierEnrollment from '@auth0/auth0-acul-js/phone-identifier-enrollment';

const phoneIdentifierEnrollment = new PhoneIdentifierEnrollment();
phoneIdentifierEnrollment.continuePhoneEnrollment({
    type: "text" | "voice"
});
```

--------------------------------

### Auth0 Rule: Hardcoded URL Example

Source: https://auth0.com/docs/dev-lifecycle/set-up-multiple-environments

This JavaScript code snippet demonstrates a basic Auth0 rule where a URL is hardcoded. This approach is not recommended for production environments as it makes migration difficult when the URL changes.

```javascript
function(user, context, callback){
      var log_url = 'https://someurl/log';
      ...
    }
```

--------------------------------

### Authentication Methods JSON Example

Source: https://auth0.com/docs/customize/rules/context-object

Provides an example of the JSON structure for authentication methods completed during a user's session. This includes the name of the method (e.g., 'pwd', 'mfa') and a timestamp.

```json
[
  {
    "name": "pwd",
    "timestamp": 1434454643024
  },
  {
    "name": "mfa",
    "timestamp": 1534454643881
  }
]
```

--------------------------------

### Start HTTP Server with Router

Source: https://auth0.com/docs/quickstart/webapp/golang/interactive

Initializes a new router and starts an HTTP server on port 3000. It logs the server's listening address and handles potential errors during server startup. This snippet assumes the 'router' and 'auth' packages are available.

```go
rtr := router.New(auth)

log.Print("Server listening on http://localhost:3000/")
if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
	log.Fatalf("There was an error with the http server: %v", err)
}
```

--------------------------------

### Implement Pre User Registration logic

Source: https://auth0.com/docs/customize/actions/migrate/migrate-from-hooks-to-actions

Demonstrates how to handle user registration conditions such as success or failure. The examples show the transition from the legacy Hook callback-based approach to the modern asynchronous Actions API.

```javascript
// Pre User Registration Hook
module.exports = function (user, context, cb) {
	if (user.app_metadata.condition === "success") {
      var response = {};
      response.user = { user_metadata: { favorite_color: "purple" } };
      // This Hook succeeded, proceed with the next Hook.
	  return callback(null, response);
	}

	if (user.app_metadata.condition === "failure") {
		// This Hook failed, stop the login with an error response.
		return callback(new Error("Failure message"));
	}

	// ... additional code
};
```

```javascript
// Pre User Registration Action
exports.onExecutePreUserRegistration = async (event, api) => {
	if (event.user.app_metadata.condition === "success") {
		// This Action succeeded, proceed with next Action.
		api.user.setUserMetadata("favorite_color", "purple");
		return;
	}

	if (event.user.app_metadata.condition === "failure") {
		// This Action failed, stop the call with an error response.
		return api.access.deny("Failure message");
	}

	// ... additional code
};
```

--------------------------------

### Get User Attribute Profile Templates

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/okta

This GET request retrieves default templates for User Attribute Profiles. These templates can be used as a starting point when creating a custom User Attribute Profile via the Management API. This is useful for setting up custom profiles for Okta OIN Express Configuration if no existing profiles are suitable.

```bash
GET /api/v2/user-attribute-profiles/templates
```

--------------------------------

### Initialize Auth0 MCP Server for Cursor

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command initializes the Auth0 MCP Server specifically for integration with the Cursor AI client. Node.js v18 or higher is required.

```javascript
npx @auth0/auth0-mcp-server init --client cursor
```

--------------------------------

### Configure Android MainActivity for Biometrics

Source: https://auth0.com/docs/quickstart/native/flutter

Updates the MainActivity to extend FlutterFragmentActivity, which is a prerequisite for using biometric authentication features in the Auth0 Flutter SDK.

```kotlin
import io.flutter.embedding.android.FlutterFragmentActivity

class MainActivity: FlutterFragmentActivity() {
}
```

--------------------------------

### Go: Router Setup

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

This Go code snippet initializes the router for a Gin application. It includes necessary imports for session management and HTTP handling. The snippet is incomplete but sets the stage for defining routes and middleware.

```go
// Save this file in ./platform/router/router.go

package router

import (
	"encoding/gob"
	"net/http"

	"github.com/gin-contrib/sessions"

```

--------------------------------

### GET /api/v2/clients/{clientId}

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Retrieves details for a specific client, identified by its ID. You can specify query parameters to include or exclude specific fields.

```APIDOC
## GET /api/v2/clients/{clientId}

### Description
Retrieves details for a specific client, identified by its ID. You can specify query parameters to include or exclude specific fields.

### Method
GET

### Endpoint
`https://{yourDomain}/api/v2/clients/%7ByourClientId%7D`

### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include in the response.
- **include_fields** (boolean) - Optional - If true, only the fields specified in the `fields` parameter will be returned. Defaults to true.

### Headers
- **authorization** (string) - Required - Bearer token for authentication. Example: `Bearer {yourMgmtApiAccessToken}`

### Request Example
```bash
curl --request GET \
  --url 'https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true' \
  --header 'authorization: Bearer {yourMgmtApiAccessToken}'
```

### Response
#### Success Response (200)
- **client_id** (string) - The unique identifier for the client.
- **name** (string) - The name of the client.
- **is_first_party** (boolean) - Indicates if the client is a first-party application.

#### Response Example
```json
{
  "client_id": "{yourClientId}",
  "name": "My Application",
  "is_first_party": true
}
```
```

--------------------------------

### Install Auth0.swift with Carthage

Source: https://auth0.com/docs/libraries/auth0-swift

Instructions for adding the Auth0.swift SDK to your project using Carthage. This involves adding the Auth0.swift GitHub repository to your Cartfile and running 'carthage bootstrap'.

```bash
github "auth0/Auth0.swift" ~> 2.0
```

--------------------------------

### Make GET Request to Auth0 API in Swift

Source: https://auth0.com/docs/fr-ca/authenticate/identity-providers/pass-parameters-to-idps

This Swift code demonstrates making a GET request to a specific Auth0 API endpoint using URLSession. It configures the request with authorization and content-type headers. The code handles potential errors and prints the HTTP response. This requires the Foundation framework.

```swift
import Foundation

let headers = [
  "authorization": "Bearer {yourMgmtApiAccessToken}",
  "content-type": "application/json"
]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/connections/%7ByourWordpressConnectionId%7D")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                      timeoutInterval: 10.0)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### React: Auth0 SDK Quickstart Buttons Component

Source: https://auth0.com/docs/ja-jp/quickstart/backend/php/interactive

This React component displays buttons for viewing a GitHub repository and downloading a sample application. It parses GitHub URLs to extract repository details and uses the Auth0DocsUI API to handle sample downloads. It supports multiple languages for button text.

```javascript
export const QuickstartButtons = ({githubLink, lang = "en"}) => {
  const translations = {
    en: {
      viewOnGithub: "View On GitHub",
      loginAndDownload: "Download Sample"
    },
    "fr-ca": {
      viewOnGithub: "Afficher sur GitHub",
      loginAndDownload: "Télécharger un exemple"
    },
    "ja-jp": {
      viewOnGithub: "Githubで表示",
      loginAndDownload: "サンプルをダウンロード"
    }
  };
  const text = translations[lang] || translations.en;
  const parseGithubUrl = url => {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split("/").filter(Boolean);
      if (pathParts.length >= 4 && pathParts[2] === "tree") {
        const repoName = pathParts[1];
        const branch = pathParts[3];
        const path = pathParts.slice(4).join("/") || undefined;
        return {
          repo: repoName,
          branch,
          path
        };
      }
      console.warn("Could not parse GitHub URL:", url);
      return null;
    } catch (error) {
      console.error("Error parsing GitHub URL:", error);
      return null;
    }
  };
  const handleDownload = async () => {
    const params = parseGithubUrl(githubLink);
    if (!params) {
      console.error("Invalid GitHub URL format");
      return;
    }
    try {
      await window.Auth0DocsUI?.getSample(params);
    } catch (error) {
      console.error("Failed to download sample:", error);
    }
  };
  return <div className="quickstart_buttons flex flex-wrap gap-3 mb-4">
      <a href={githubLink} target="_blank" rel="noopener noreferrer" className="no_external_icon quickstart_button inline-flex items-center justify-center px-6 py-3 text-sm font-medium rounded-[18px] bg-black dark:bg-white !text-white dark:!text-black hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors">
        {text.viewOnGithub}
      </a>
      <button onClick={handleDownload} type="button" className="no_external_icon quickstart_button inline-flex items-center justify-center px-6 py-3 text-sm font-medium rounded-[18px] border border-gray-300 dark:border-[#454545] bg-white dark:bg-[#272728] !text-black dark:!text-white hover:bg-gray-50 dark:hover:bg-neutral-800 transition-colors">
        {text.loginAndDownload}
      </button>
    </div>;
};

```

--------------------------------

### Install FastAPI and Auth0 Dependencies (Text)

Source: https://auth0.com/docs/quickstart/backend/fastapi

This snippet lists the necessary Python dependencies for a FastAPI project with Auth0 integration, including fastapi, uvicorn, auth0-fastapi-api, and python-dotenv. It's intended to be saved in a requirements.txt file.

```txt
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
auth0-fastapi-api>=1.0.0b5
python-dotenv>=1.0.0
```

--------------------------------

### Get Active Users Count (cURL)

Source: https://auth0.com/docs/api/management/v2/stats/get-active-users

This cURL command retrieves the number of active users who logged in during the last 30 days. It requires the tenant domain and an 'Accept' header for JSON response. No specific authentication is shown in this example, but it's typically handled via headers.

```bash
curl -L -g 'https://{tenantDomain}/api/v2/stats/active-users' \
-H 'Accept: application/json'
```

--------------------------------

### Configure Auth0 App via Auth0 CLI (Windows)

Source: https://auth0.com/docs/quickstart/spa/react/index

Installs the Auth0 CLI on Windows using Scoop and then uses it to set up a new Auth0 application and generate a `.env` file. This automates the Auth0 configuration process.

```shellscript
# Install Auth0 CLI (if not already installed)
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Implement Authentication Service for Flutter

Source: https://auth0.com/docs/quickstart/native/flutter

Provides methods for handling user login and logout flows. Includes platform-specific implementations for mobile/macOS and web environments.

```dart
import 'package:auth0_flutter/auth0_flutter.dart';

class AuthService {
  final auth0 = Auth0('{yourDomain}', '{yourClientId}');
  
  Future<Credentials> login() async {
    final credentials = await auth0.webAuthentication().login(useHTTPS: true);
    return credentials;
  }

  Future<void> logout() async {
    await auth0.webAuthentication().logout(useHTTPS: true);
  }
}
```

```dart
import 'package:auth0_flutter/auth0_flutter_web.dart';

class WebAuthService {
  final auth0Web = Auth0Web('{yourDomain}', '{yourClientId}');
  
  Future<void> initialize() async {
    final credentials = await auth0Web.onLoad();
  }
  
  Future<void> login() async {
    await auth0Web.loginWithRedirect(redirectUrl: 'http://localhost:3000');
  }

  Future<void> logout() async {
    await auth0Web.logout(returnToUrl: 'http://localhost:3000');
  }
}
```

--------------------------------

### Get Connection Profile Templates (curl)

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/okta/express-configuration

Retrieves default templates for Connection Profiles. This allows developers to start with predefined settings before creating a custom connection profile. No input parameters are needed.

```curl
GET /api/v2/connection-profiles/templates
```

--------------------------------

### Initialize Auth0 SDK and Configuration

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/php/interactive

Sets up the Auth0 SDK configuration with domain, client credentials, and redirect URIs. This is the entry point for integrating Auth0 into a PHP application.

```php
<?php

declare(strict_types=1);

require('vendor/autoload.php');

use Auth0\SDK\Auth0;
use Auth0\SDK\Configuration\SdkConfiguration;

$configuration = new SdkConfiguration(
  domain: '{yourDomain}',
  clientId: '{yourClientId}',
  clientSecret: '{yourClientSecret}',
  redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
  cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
);

$sdk = new Auth0($configuration);

require('router.php');
```

--------------------------------

### Use Auth0 CLI for Scripting with JSON Output

Source: https://auth0.com/docs/deploy-monitor/auth0-cli

Illustrates how to use the Auth0 CLI with the `--json` flag to get machine-readable output for scripting and automation. Examples include fetching application details and capturing output to a file.

```bash
# Get application details as JSON
auth0 apps show <app-id> --json
```

```bash
# Create an app and capture the output
auth0 apps create --name "My App" --type spa --json > app-details.json
```

--------------------------------

### Create Auth0 API and Configure Environment (PowerShell)

Source: https://auth0.com/docs/quickstart/backend/fastapi

This PowerShell script automates the creation of an Auth0 API and configures the environment variables (AUTH0_DOMAIN and AUTH0_AUDIENCE) in a .env file. It requires the Auth0 CLI to be installed.

```powershell
$ApiName = "My FastAPI API"; $ApiIdentifier = "https://my-fastapi-api"; auth0 login --no-input; auth0 apis create -n $ApiName -i $ApiIdentifier --signing-alg RS256 --no-input; $ActiveTenant = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name; "AUTH0_DOMAIN=$ActiveTenant`nAUTH0_AUDIENCE=$ApiIdentifier" | Out-File -FilePath .env -Encoding utf8
```

--------------------------------

### Construct Authorization Request with ACR Values

Source: https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication/configure-step-up-authentication-for-web-apps

An example of an HTTP GET request to the Auth0 /authorize endpoint, including the acr_values parameter to explicitly request MFA authentication.

```http
https://{yourDomain}/authorize?
        audience=https://{yourDomain}/userinfo&
        scope=openid&
        response_type=code&
        client_id={yourClientId}&
        redirect_uri={https://yourApp/callback}&
        state={yourOpaqueValue}&
        acr_values=http://schemas.openid.net/pape/policies/2007/06/multi-factor
```

--------------------------------

### Initialize Gin Server and Routes

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

The main entry point loads environment variables, initializes the Auth0 authenticator, and starts the Gin HTTP server. It serves as the orchestration layer for the application.

```golang
func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}
```

--------------------------------

### Initialize Auth0 Client Logic

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Implements the Auth0 SPA SDK initialization, including environment variable validation and handling of authentication redirects.

```javascript
import { createAuth0Client } from '@auth0/auth0-spa-js';

const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorDetails = document.getElementById('error-details');
const app = document.getElementById('app');
const loggedOutSection = document.getElementById('logged-out');
const loggedInSection = document.getElementById('logged-in');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const profileContainer = document.getElementById('profile');

let auth0Client;

async function initAuth0() {
  try {
    const domain = import.meta.env.VITE_AUTH0_DOMAIN;
    const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID;

    if (!domain || !clientId) {
      throw new Error('Auth0 configuration missing. Please check your .env.local file for VITE_AUTH0_DOMAIN and VITE_AUTH0_CLIENT_ID');
    }

    auth0Client = await createAuth0Client({
      domain: domain,
      clientId: clientId,
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    });

    if (window.location.search.includes('code=') && window.location.search.includes('state=')) {
      await handleRedirectCallback();
    }
  } catch (err) {
    console.error(err);
  }
}
```

--------------------------------

### Retrieve Auth0 Client Details (C#)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Demonstrates fetching Auth0 client information using C# with the RestSharp library. It constructs a GET request with the necessary authorization header and endpoint URL.

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer {yourMgmtApiAccessToken}");
IRestResponse response = client.Execute(request);
```

--------------------------------

### Install Auth0 Deploy CLI

Source: https://auth0.com/docs/extensions/deploy-cli-tool/create-and-configure-the-deploy-cli-application-manually

Installs the Auth0 Deploy CLI globally on the system to enable standalone command-line usage.

```bash
npm install -g auth0-deploy-cli
```

--------------------------------

### Configure Auth0 Routes and Middleware in Express

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Sets up the Auth0 OIDC middleware, defines a public home route with authentication status, and creates a protected profile route. It utilizes environment variables for configuration and provides server startup logic.

```javascript
require('dotenv').config();
const express = require('express');
const { auth, requiresAuth } = require('express-openid-connect');

const app = express();
const port = process.env.PORT || 3000;

const config = {
  authRequired: false,
  auth0Logout: true,
  secret: process.env.SECRET,
  baseURL: process.env.BASE_URL,
  clientID: process.env.CLIENT_ID,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
};

app.use(auth(config));

app.get('/', (req, res) => {
  const isAuthenticated = req.oidc.isAuthenticated();
  res.send(`<html><body><h1>Auth0 Express Quickstart</h1><nav>${isAuthenticated ? '<a href="/profile">Profile</a> | <a href="/logout">Logout</a>' : '<a href="/login">Login</a>'}</nav></body></html>`);
});

app.get('/profile', requiresAuth(), (req, res) => {
  const user = req.oidc.user;
  res.send(`<h1>User Profile</h1><pre>${JSON.stringify(user, null, 2)}</pre>`);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

--------------------------------

### Build and Run Expo Native Projects

Source: https://auth0.com/docs/quickstart/native/react-native-expo/interactive

Commands to generate and execute native iOS and Android builds required for Auth0 SDK functionality, which cannot run in Expo Go.

```bash
npx expo prebuild
npx expo run:ios
npx expo run:android
```

--------------------------------

### Example Connection Profile JSON Configuration

Source: https://auth0.com/docs/authenticate/enterprise-connections/connection-profile

An example JSON object representing a Connection Profile configuration. This includes settings for organization display, connection name templates, and enabled features.

```json
{
  "organization": {
    "show_as_button": "none",
    "assign_membership_on_login": "none"
  },
  "connection_name_prefix_template": "ec-{org_id}-",
  "enabled_features": [
    "scim",
    "universal_logout"
  ]
}
```

--------------------------------

### Run Development Server

Source: https://auth0.com/docs/quickstart/spa/react

Command to start the local development server for the Auth0 application. Includes instructions for handling port conflicts.

```shellscript
npm run dev
# If port 5173 is in use:
npm run dev -- --port 5174
```

--------------------------------

### Scaffold New Project

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Creates a new directory and initializes a Vite project with the necessary Auth0 dependencies for MacOS/Linux and Windows.

```bash
mkdir auth0-vanillajs && cd auth0-vanillajs && npm init -y && npm install --save-dev vite && npm install @auth0/auth0-spa-js && touch index.html app.js style.css
```

```powershell
mkdir auth0-vanillajs; cd auth0-vanillajs; npm init -y; npm install --save-dev vite; npm install @auth0/auth0-spa-js; New-Item -ItemType File -Path index.html, app.js, style.css
```

--------------------------------

### Web Authentication Login with Organization ID

Source: https://auth0.com/docs/quickstart/native/flutter

Facilitates web authentication for users belonging to a specific organization, identified by its unique ID. This is useful for B2B or enterprise scenarios.

```dart
Future<Credentials> loginWithOrganization(String organizationId) async {
    return await auth0.webAuthentication().login(
      useHTTPS: true,
      organizationId: organizationId,
    );
  }
```

--------------------------------

### Retrieve Auth0 Client Details (Python)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Demonstrates fetching Auth0 client information using Python's `http.client` module. This snippet sets up an HTTPS connection and sends a GET request with the authorization header.

```python
import http.client

conn = http.client.HTTPSConnection("")

headers = { 'authorization': "Bearer {yourMgmtApiAccessToken}" }

conn.request("GET", "/{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

--------------------------------

### Handle Mobile/macOS Authentication Errors

Source: https://auth0.com/docs/quickstart/native/flutter

Illustrates how to handle authentication errors specifically on mobile and macOS platforms. It includes checks for user cancellation and other potential login failures.

```dart
import 'package:auth0_flutter/auth0_flutter.dart';

Future<void> login() async {
  try {
    final credentials = await auth0.webAuthentication().login(useHTTPS: true);
    // Handle successful login
  } on WebAuthenticationException catch (e) {
    if (e.code == 'USER_CANCELLED') {
      // User cancelled the login
      print('Login cancelled by user');
    } else {
      // Handle other errors
      print('Login error: ${e.message}');
    }
  }
}
```

--------------------------------

### Create Flutter Web Project

Source: https://auth0.com/docs/quickstart/spa/flutter/interactive

Creates a new Flutter Web application using the Flutter CLI. This is the initial step for setting up the project.

```shell
flutter create --platforms=web auth0_flutter_web
cd auth0_flutter_web
```

--------------------------------

### Install Auth0 Vue SDK and Capacitor Plugins

Source: https://auth0.com/docs/quickstart/native/ionic-vue/interactive

Commands to install the required Auth0 Vue SDK and the necessary Capacitor plugins for browser interaction and app event handling.

```bash
npm install @auth0/auth0-vue
npm install @capacitor/browser @capacitor/app
```

--------------------------------

### Initialize and Develop ACUL Projects with Auth0 CLI

Source: https://auth0.com/docs/customize/login-pages/advanced-customizations/acul-use-cases/migrate-classic-universal-login

Commands to initialize a new ACUL project with specific screens and start a local development server for customization. These commands require the Auth0 CLI to be installed and configured.

```bash
auth0 acul init acul-login --screens login-id,login-password
```

```bash
auth0 acul dev
```

--------------------------------

### Create Svelte Project and Install Dependencies

Source: https://auth0.com/docs/quickstart/spa/svelte

Commands to create a new Svelte project using Vite and install the Auth0 SPA JS SDK. This sets up the basic project structure and adds the necessary authentication library.

```shellscript
npx sv create auth0-svelte --template minimal --types ts --no-add-ons --no-install
cd auth0-svelte
npm install && npm install @auth0/auth0-spa-js
```

--------------------------------

### Email Attribute Configuration Example

Source: https://auth0.com/docs/authenticate/enterprise-connections/user-attribute-profile

An example illustrating the configuration for the email attribute, including its description, label, and specific mappings for different protocols and strategy overrides.

```APIDOC
## Email Attribute Example

```json
"email": {
  "description": "Email",
  "label": "Email",
  "profile_required": true,
  "auth0_mapping": "email",
  "scim_mapping": "emails[primary eq true].value",
  "oidc_mapping": {
    "mapping": "${context.tokenset.email}",
    "display_name": "email"
  },
  "saml_mapping": [
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
  ],
  "strategy_overrides": {
    "waad": {
      "scim_mapping": "emails[type eq \"work\"].value"
    }
  }
}
```

* Suggested for most profiles.
* Unified across Auth0, OIDC, SAML and SCIM.
* WAAD override ensures correct mapping to work emails.
```

--------------------------------

### Install ASP.NET Core Authentication Packages

Source: https://auth0.com/docs/get-started/architecture-scenarios/sso-for-regular-web-apps/implementation-aspnetcore

Installs the required NuGet packages for cookie and OpenID Connect authentication in ASP.NET Core applications.

```bash
Install-Package Microsoft.AspNetCore.Authentication.Cookies
Install-Package Microsoft.AspNetCore.Authentication.OpenIdConnect
```

--------------------------------

### POST /me/v1/authentication-methods

Source: https://auth0.com/docs/api/myaccount/create-authentication-method

Starts the enrollment of a supported authentication method for a user.

```APIDOC
## POST /me/v1/authentication-methods

### Description
Starts the enrollment of a supported authentication method.

### Method
POST

### Endpoint
https://auth0.auth0.com/me/v1/authentication-methods

### Parameters
#### Query Parameters
- **scopes** (string) - Required - Scopes for the request, e.g., `create:me:authentication_methods`

#### Request Body
- **connection** (string) - Required - Connection name
- **identity_user_id** (string) - Required - The ID of the user identity linked with the authentication method
- **email** (string) - Required - The email address to use for sending one-time codes.
- **phone_number** (string) - Required - The destination phone number used to send verification codes via text and voice.
- **preferred_authentication_method** (PhoneAuthenticationMethodEnum) - Optional - Preferred authentication method for phone-based authentication. Possible values: `sms`, `voice`

### Request Example
```json
{
  "connection": "your_connection_name",
  "identity_user_id": "user_id_from_identity",
  "email": "user@example.com",
  "phone_number": "+15551234567",
  "preferred_authentication_method": "sms"
}
```

### Response
#### Success Response (200)
- **object** (object) - Details of the started enrollment process.

#### Response Example
```json
{
  "enrollment_id": "enrollment_abc123",
  "status": "pending"
}
```
```

--------------------------------

### Configure Tailwind CSS and Run Application

Source: https://auth0.com/docs/quickstart/webapp

Provides the necessary CSS configuration for Tailwind and the command to start the development server.

```css
@import "tailwindcss";
```

```bash
npm run dev
```

--------------------------------

### Initialize ACUL Project with Auth0 CLI

Source: https://auth0.com/docs/customize/login-pages/advanced-customizations/quickstart

Initializes a new ACUL project directory using the Auth0 CLI. This command sets up the project structure for React-based authentication screens.

```bash
auth0 acul init "Your_App_Name"
```

--------------------------------

### Handle Credentials Manager Errors

Source: https://auth0.com/docs/quickstart/native/flutter

Demonstrates error handling for the Credentials Manager, specifically addressing scenarios where no credentials are found or token renewal fails, requiring user re-authentication.

```dart
Future<Credentials> getCredentials() async {
  try {
    return await auth0.credentialsManager.credentials();
  } on CredentialsManagerException catch (e) {
    if (e.isNoCredentialsFound) {
      // No stored credentials, user needs to log in
      throw Exception('Please log in first');
    } else if (e.isTokenRenewFailed) {
      // Refresh token expired, re-authentication required

```

--------------------------------

### Run FastAPI Application with Uvicorn

Source: https://auth0.com/docs/quickstart/backend/fastapi

This command starts the FastAPI application using Uvicorn, a high-performance ASGI server. Ensure your virtual environment is activated before running this command. The `--reload` flag enables hot-reloading for development.

```bash
uvicorn app:app --reload
```

--------------------------------

### Fetch Auth0 Clients with Swift

Source: https://auth0.com/docs/secure/tokens/access-tokens/management-api-access-tokens/get-management-api-access-tokens-for-production

This Swift code example shows how to fetch client data from the Auth0 Management API v2. It defines request headers, creates an NSMutableURLRequest for the '/clients' endpoint, sets the HTTP method to GET, and configures the request headers. It then uses URLSession to execute the request and prints the HTTP response.

```swift
import Foundation

let headers = [
  "content-type": "application/json",
  "authorization": "Bearer {yourAccessToken}"
]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/clients")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                      timeoutInterval: 10.0)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### GET /v2/prompts/rendering

Source: https://auth0.com/docs/customize/login-pages/advanced-customizations/reference

Retrieves the configuration for all Universal Login screens.

```APIDOC
## GET /v2/prompts/rendering

### Description
Retrieves the rendering configurations for all available Universal Login screens in the tenant.

### Method
GET

### Endpoint
/v2/prompts/rendering

### Response
#### Success Response (200)
- **screens** (array) - A list of all screen configurations.

#### Response Example
{
  "screens": [
    { "prompt": "login", "screen": "identifier-first", "rendering": {} }
  ]
}
```

--------------------------------

### iOS Callback URL Configuration

Source: https://auth0.com/docs/quickstart/native/flutter

This snippet shows the Allowed Callback URLs for an iOS application. It includes both HTTPS and custom scheme formats. Replace `{yourDomain}` and `{yourBundleIdentifier}` accordingly.

```text
https://{yourDomain}/ios/{yourBundleIdentifier}/callback,
{yourBundleIdentifier}://{yourDomain}/ios/{yourBundleIdentifier}/callback
```

--------------------------------

### Install Auth0 CLI on Windows

Source: https://auth0.com/docs/deploy-monitor/auth0-cli

Installs the Auth0 CLI on Windows using Scoop. This requires adding the Auth0 CLI repository to Scoop and then installing the package.

```powershell
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0
```

--------------------------------

### Perform Authenticated API Requests

Source: https://auth0.com/docs/quickstart/backend/django/interactive

Demonstrates how to send an HTTP GET request with an Authorization Bearer token to an Auth0-protected endpoint. Examples are provided for PHP, Python, Ruby, Swift, and Objective-C.

```Objective-C
NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
NSLog(@"%@", httpResponse);
[dataTask resume];
```

```PHP
$curl = curl_init();
curl_setopt_array($curl, [
	CURLOPT_URL => "http:///{yourDomain}.com/api_path",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_HTTPHEADER => ["authorization: Bearer YOUR_ACCESS_TOKEN_HERE"]
]);
$response = curl_exec($curl);
curl_close($curl);
echo $response;
```

```Python
import http.client
conn = http.client.HTTPConnection("")
headers = { 'authorization': "Bearer YOUR_ACCESS_TOKEN_HERE" }
conn.request("get", "/{yourDomain}.com/api_path", headers=headers)
res = conn.getresponse()
print(res.read().decode("utf-8"))
```

```Ruby
require 'uri'
require 'net/http'
url = URI("http:///{yourDomain}.com/api_path")
http = Net::HTTP.new(url.host, url.port)
request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer YOUR_ACCESS_TOKEN_HERE'
response = http.request(request)
puts response.read_body
```

```Swift
let headers = ["authorization": "Bearer YOUR_ACCESS_TOKEN_HERE"]
let request = NSMutableURLRequest(url: NSURL(string: "http:///{yourDomain}.com/api_path")! as URL)
request.httpMethod = "get"
request.allHTTPHeaderFields = headers
let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
	let httpResponse = response as? HTTPURLResponse
	print(httpResponse)
})
dataTask.resume()
```

--------------------------------

### Run Development Server with Custom Port (npm)

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Command to run the Vite development server on a custom port. This is an alternative to the default port if needed.

```bash
npm run dev -- --port 5174
```

--------------------------------

### Configure Auth0 SDK in web.xml

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

Sets up the Auth0 SDK configuration within the `web.xml` deployment descriptor for a Java servlet application. It requires replacing placeholder values with your Auth0 application's domain, client ID, and client secret.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
         http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">

    <display-name>Auth0 Servlet Example</display-name>

    <!-- Auth0 Configuration -->
    <context-param>
        <param-name>com.auth0.domain</param-name>
        <param-value>YOUR_AUTH0_DOMAIN</param-value>
    </context-param>
    <context-param>
        <param-name>com.auth0.clientId</param-name>
        <param-value>YOUR_AUTH0_CLIENT_ID</param-value>
    </context-param>
    <context-param>
        <param-name>com.auth0.clientSecret</param-name>
        <param-value>YOUR_AUTH0_CLIENT_SECRET</param-value>
    </context-param>
</web-app>
```

--------------------------------

### React Component for Displaying Auth0 Quickstart Information

Source: https://auth0.com/docs/quickstarts

This React component, `SectionCard`, is designed to display information about an Auth0 quickstart. It takes an `item` object as a prop, which contains details like name, subtext, logo, links to GitHub, sample apps, quickstarts, and documentation. It conditionally renders elements based on the presence of these details and handles image sources for light and dark modes. It also formats and displays badges and dates.

```javascript
export const SectionCard = ({item}) => {
  if (!item) return null;
  const getLink = (item, label) => item.links?.find(l => l.label?.toLowerCase() === label.toLowerCase());
  const github = getLink(item, "github");
  const sample = getLink(item, "sample app");
  const quickstart = getLink(item, "quickstart");
  const docs = getLink(item, "Get started");
  const title = item?.name ?? "";
  const subtext = item?.subtext ?? "";
  const badge = item?.badge ?? "";
  const date = item?.date ?? "";
  const isHttpsLogo = typeof item?.logo === "string" && (/^https:\/\//i).test(item.logo);
  const src = isHttpsLogo ? item.logo : `/docs/images/icons/light/${item?.logo}`;
  const srcDark = isHttpsLogo ? item.logo : `/docs/images/icons/dark/${item?.logo}`;
  const imgClass = "!my-0 w-8 h-8 object-contain shrink-0 " + (isHttpsLogo ? "mint-filter mint-grayscale" : "");
  const tertiary = quickstart || docs;
  const tertiaryLabel = quickstart ? "Quickstart" : docs ? "Get started" : "";
  return <article className="
      libraries_card mb-[16px]
      rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow
      border-gray-200 dark:border-gray-800 dark:bg-black
    ">
      <div className="px-4 md:px-5 pt-4 md:pt-5 pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex gap-3 min-w-0">
            {item?.logo && <>
                <img noZoom src={src} alt={title} className={`${imgClass} mint-block dark:mint-hidden`} />
                <img noZoom src={srcDark} alt={title} className={`${imgClass} mint-hidden dark:mint-block`} />
              </>}

            <div className="min-w-0">
              <h4 className="text-base md:text-lg font-semibold text-gray-900 dark:text-white truncate !m-0 leading-snug">
                {title}
              </h4>
              {!!subtext && <p className="text-xs text-gray-500 dark:text-gray-400 truncate !m-0 leading-tight">{subtext}</p>}
            </div>
          </div>

          <div className="flex flex-col items-end gap-0.5 shrink-0">
            {!!badge && <span className="
                  inline-flex items-center rounded-full px-1.5 py-[0.5px] text-[10px] font-medium
                  border border-emerald-700 text-emerald-700 bg-emerald-200
                  dark:border-emerald-400 dark:text-emerald-300 dark:bg-emerald-900/30
                ">
                {badge}
              </span>}
            {!!date && <span className="mr-[5px] text-[10px] text-gray-500 dark:text-gray-400">
                on {date.replace(/^on\s+/i, "")}
              </span>}
          </div>
        </div>
      </div>

      <div className="h-px mx-3 bg-gray-200 dark:bg-gray-800" />

      <div className="px-4 md:px-5 py-3">
        <div className="libraries_cards flex items-center justify-between w-full gap-3">
          {github && <a href={github.url} target="_blank" rel="noopener noreferrer" className="
                no_external_icon inline-flex items-center gap-1.5 text-xs font-medium
                !text-black dark:!text-white
                !no-underline !border-0
                transition-colors duration-200
                hover:!text-neutral-700 dark:hover:!text-neutral-200
              " style={{
    borderBottom: "none !important"
  }}>
              <Icon icon="github" className="w-3 h-3 shrink-0" />
              <span className="leading-none">Github</span>
            </a>}

          {sample && <a href={sample.url} target="_blank" rel="noopener noreferrer" className="
                no_external_icon inline-flex items-center gap-1.5 text-xs font-medium
                !text-black dark:!text-white
                !no-underline !border-0
                transition-colors duration-200
                hover:!text-neutral-700 dark:hover:!text-neutral-200
              " style={{
    borderBottom: "none !important"
  }}>
              <Icon icon="download" className="w-3 h-3 shrink-0" />
              <span className="leading-none">Sample App</span>
            </a>}

          {tertiary && <a href={tertiary.url} className="
                no_external_icon inline-flex items-center gap-1.5 text-xs font-medium
                !text-black dark:!text-white
                !no-underline !border-0
                transition-colors duration-200
                hover:!text-neutral-700 dark:hover:!text-neutral-200
              " style={{
    borderBottom: "none !important"
  }}>
              {tertiaryLabel === "Quickstart" ? <Icon icon="play" className="w-3 h-3 shrink-0" /> : <Icon icon="file-lines" className="w-3 h-3 shrink-0" />}
              <span className="leading-none">{tertiaryLabel}</span>
            </a>}
        </div>
      </div>
    </article>;
};
```

--------------------------------

### Authenticate via Passwordless OTP using Auth0 API

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

These snippets demonstrate how to perform a POST request to the Auth0 /oauth/token endpoint to exchange a phone-based OTP for an authentication token. Each implementation handles JSON serialization of parameters and sets the necessary headers for the request.

```Objective-C
NSDictionary *parameters = @{@"grant_type": @"http://auth0.com/oauth/grant-type/passwordless/otp",
                                @"client_id": @"{yourClientId}",
                                @"client_secret": @"{yourClientSecret}",
                                @"username": @"USER_PHONE_NUMBER",
                                @"otp": @"code",
                                @"realm": @"sms",
                                @"audience": @"your-api-audience",
                                @"scope": @"openid profile email" };

  NSData *postData = [NSJSONSerialization dataWithJSONObject:parameters options:0 error:nil];

  NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/oauth/token"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
  [request setHTTPMethod:@"POST"];
  [request setAllHTTPHeaderFields:headers];
  [request setHTTPBody:postData];

  NSURLSession *session = [NSURLSession sharedSession];
  NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
  [dataTask resume];
```

```PHP
$curl = curl_init();

  curl_setopt_array($curl, [
    CURLOPT_URL => "https://{yourDomain}/oauth/token",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CUSTOMREQUEST => "POST",
    CURLOPT_POSTFIELDS => "{\"grant_type\": \"http://auth0.com/oauth/grant-type/passwordless/otp\", \"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"username\": \"USER_PHONE_NUMBER\", \"otp\": \"code\", \"realm\": \"sms\", \"audience\": \"your-api-audience\",\"scope\": \"openid profile email\"}",
    CURLOPT_HTTPHEADER => ["content-type: application/json"]
  ]);

  $response = curl_exec($curl);
  $err = curl_error($curl);
  curl_close($curl);
```

```Python
import http.client

conn = http.client.HTTPSConnection("")
payload = "{\"grant_type\": \"http://auth0.com/oauth/grant-type/passwordless/otp\", \"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"username\": \"USER_PHONE_NUMBER\", \"otp\": \"code\", \"realm\": \"sms\", \"audience\": \"your-api-audience\",\"scope\": \"openid profile email\"}"
headers = { 'content-type': "application/json" }

conn.request("POST", "/{yourDomain}/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
```

```Ruby
require 'uri'
require 'net/http'

url = URI("https://{yourDomain}/oauth/token")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["content-type"] = 'application/json'
request.body = "{\"grant_type\": \"http://auth0.com/oauth/grant-type/passwordless/otp\", \"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"username\": \"USER_PHONE_NUMBER\", \"otp\": \"code\", \"realm\": \"sms\", \"audience\": \"your-api-audience\",\"scope\": \"openid profile email\"}"

response = http.request(request)
```

```Swift
import Foundation

let parameters = [
  "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
  "client_id": "{yourClientId}",
  "client_secret": "{yourClientSecret}",
  "username": "USER_PHONE_NUMBER",
  "otp": "code",
  "realm": "sms",
  "audience": "your-api-audience",
  "scope": "openid profile email"
]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])
let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/oauth/token")! as URL)
request.httpMethod = "POST"
request.allHTTPHeaderFields = ["content-type": "application/json"]
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest) { (data, response, error) in ... }
```

--------------------------------

### Handle Web Authentication Exceptions

Source: https://auth0.com/docs/quickstart/native/flutter

Implements a login function that catches and prints specific `WebException` errors that may occur during the web authentication process. This aids in debugging and user feedback.

```dart
Future<void> login() async {
    try {
      await auth0Web.loginWithRedirect(redirectUrl: 'http://localhost:3000');
    } on WebException catch (e) {
      print('Login error: ${e.message}');
    }
  }
```

--------------------------------

### Call Protected API with Bearer Token

Source: https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow/call-your-api-using-the-client-credentials-flow

Demonstrates how to perform an authenticated GET request to an API endpoint. Each example sets the 'Authorization' header to 'Bearer ACCESS_TOKEN' and the 'Content-Type' to 'application/json'.

```bash
curl --request GET \
  --url https://myapi.com/api \
  --header 'authorization: Bearer ACCESS_TOKEN' \
  --header 'content-type: application/json'
```

```csharp
var client = new RestClient("https://myapi.com/api");
var request = new RestRequest(Method.GET);
request.AddHeader("content-type", "application/json");
request.AddHeader("authorization", "Bearer ACCESS_TOKEN");
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://myapi.com/api"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("content-type", "application/json")
	req.Header.Add("authorization", "Bearer ACCESS_TOKEN")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse response = Unirest.get("https://myapi.com/api")
  .header("content-type", "application/json")
  .header("authorization", "Bearer ACCESS_TOKEN")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://myapi.com/api',
  headers: {'content-type': 'application/json', authorization: 'Bearer ACCESS_TOKEN'}
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objc
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"content-type": @"application/json",
                           @"authorization": @"Bearer ACCESS_TOKEN" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://myapi.com/api"]
                                                       cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                   timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                            completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                if (error) {
                                                    NSLog(@"%@", error);
                                                } else {
                                                    NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                    NSLog(@"%@", httpResponse);
                                                }
                                            }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://myapi.com/api",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer ACCESS_TOKEN",
    "content-type: application/json"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("myapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer ACCESS_TOKEN"
    }

conn.request("GET", "/api", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://myapi.com/api")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["content-type"] = 'application/json'
request["authorization"] = 'Bearer ACCESS_TOKEN'

response = http.request(request)
puts response.read_body
```

--------------------------------

### Manual MCP Server Configuration

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

JSON configuration schema for integrating the Auth0 MCP server with generic MCP-compatible clients. This configuration defines the command, arguments, and environment variables required for the server to run.

```json
{
  "mcpServers": {
    "auth0": {
      "command": "npx",
      "args": ["-y", "@auth0/auth0-mcp-server", "run"],
      "capabilities": ["tools"],
      "env": {
        "DEBUG": "auth0-mcp"
      }
    }
  }
}
```

--------------------------------

### Install Auth0 React Native SDK

Source: https://auth0.com/docs/quickstart/native/react-native/index

Installs the Auth0 React Native SDK using npm and then installs native dependencies for iOS using CocoaPods. This makes the Auth0 authentication functionalities available in the project. Ensure you are in the project's root directory.

```bash
npm install react-native-auth0
cd ios && pod install && cd ..
```

--------------------------------

### Install Auth0 Guardian SDK using npm

Source: https://auth0.com/docs/secure/multi-factor-authentication/multi-factor-authentication-developer-resources/install-guardian-sdk

Installs the Auth0 Guardian SDK, a UI-less client for Guardian, using npm. This is the first step to integrate Guardian's multi-factor authentication capabilities.

```bash
npm install auth0-guardian-js
```

--------------------------------

### Install Auth0 Nuxt SDK

Source: https://auth0.com/docs/quickstart/webapp/nuxt

Installs the official Auth0 SDK for Nuxt.js and resolves project dependencies.

```shellscript
npm add @auth0/auth0-nuxt && npm install
```

--------------------------------

### Authentication Service Implementation (Swift)

Source: https://auth0.com/docs/quickstart/native/ios-swift/interactive

A Swift class using Combine and the Auth0 SDK to manage authentication state, user information, and handle login/logout flows. It checks authentication status on initialization and provides methods for user interaction.

```swift
import Foundation
import Auth0
import Combine

@MainActor
class AuthenticationService: ObservableObject {
    @Published var isAuthenticated = false
    @Published var user: User?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let credentialsManager = CredentialsManager(authentication: Auth0.authentication())
    
    init() {
        Task {
            await checkAuthenticationStatus()
        }
    }
    
    private func checkAuthenticationStatus() async {
        isLoading = true
        defer { isLoading = false }
        
        guard let credentials = try? await credentialsManager.credentials() else {
            isAuthenticated = false
            return
        }
        
        isAuthenticated = true
        // Get user info from the ID token
        user = credentials.user
    }
    
    func login() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }
        
        do {
            let credentials = try await Auth0
                .webAuth()
                .scope("openid profile email offline_access")

```

--------------------------------

### Configure Auth0 App via Auth0 CLI (Mac)

Source: https://auth0.com/docs/quickstart/spa/react/index

Installs the Auth0 CLI on macOS and then uses it to set up a new Auth0 application and generate a `.env` file. This is a convenient way to configure Auth0 for your project.

```shellscript
# Install Auth0 CLI (if not already installed)
brew tap auth0/auth0-cli && brew install auth0

# Set up Auth0 app and generate .env file
auth0 qs setup --type vite -n "My App" -p 5173
```

--------------------------------

### Web Authentication Login with HTTPS

Source: https://auth0.com/docs/quickstart/native/flutter

Initiates the web authentication flow using Auth0, ensuring HTTPS is used for the connection. This is a common method for initiating user login via a web browser.

```dart
return await auth0.webAuthentication().login(useHTTPS: true);
```

--------------------------------

### Start Development Server (Shell Command)

Source: https://auth0.com/docs/quickstart/spa/capn-web

Command to start the local development server for the project. This is typically used during development to serve the application and allow for testing.

```bash
    npm run start

```

--------------------------------

### Install Capacitor Plugins

Source: https://auth0.com/docs/quickstart/native/ionic-angular/interactive

Installs essential Capacitor plugins for interacting with the device's system browser and handling app events, crucial for Auth0 authentication callbacks.

```bash
npm install @capacitor/browser @capacitor/app
```

--------------------------------

### Include Auth0 SPA SDK for Web

Source: https://auth0.com/docs/quickstart/native/flutter

Adds the Auth0 Single Page Application SDK script tag to the HTML head section to enable authentication capabilities in web-based Flutter apps.

```html
<head>
  <!-- ... other head content ... -->
  <script src="https://cdn.auth0.com/js/auth0-spa-js/2.9/auth0-spa-js.production.js" defer></script>
</head>
```

--------------------------------

### Example Section Data Structure

Source: https://auth0.com/docs/quickstart/native/ionic-vue/interactive

This JavaScript array defines the structure for sections within a guide or recipe. Each object in the array represents a section and contains an 'id' and a 'title'. This data is likely used to dynamically generate navigation or content sections.

```javascript
export const sections = [{
  id: "getting-started",
  title: "Getting started"
}, {
  id: "configure-auth0",
  title: "Configure Auth0"
}, {
  id: "install-the-auth0-vue-sdk",
  title: "Install the Auth0 Vue SDK"
}, {
  id: "configure-the-createauht0-plugin",
  title: "Configure the CreateAuht0 plugin"
}, {
  id: "add-login-to-your-application",
  title: "Add login to your application"
}, {
  id: "handle-the-login-callback",
  title: "Handle the login callback"
}, {
  id: "add-logout-to-your-application",
  title: "Add logout to your application"
}, {
  id: "show-the-user-profile",
  title: "Show the user profile"
}];
```

--------------------------------

### Initiate Silent Authentication Request (Auth0 API)

Source: https://auth0.com/docs/authenticate/login/configure-silent-authentication

This example shows how to construct a GET request to the Auth0 `/authorize` endpoint with the `prompt=none` parameter to initiate a silent authentication flow. It includes common parameters like `response_type`, `client_id`, `redirect_uri`, and `state`.

```json
GET https://{yourDomain}/authorize
    ?response_type=id_token token&
    client_id=...
    redirect_uri=...
    state=...
    scope=openid...
    nonce=...
    audience=...
    response_mode=...
    prompt=none
```

--------------------------------

### Install Auth0 SDK

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server/interactive

Installs the required Auth0 ASP.NET Core authentication package via the .NET CLI.

```bash
dotnet add package Auth0.AspNetCore.Authentication
```

--------------------------------

### Project Configuration and Scripts

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

The package.json file configuration required to manage dependencies and development scripts for the Auth0 Vanilla JS project using Vite.

```json
{
  "name": "auth0-vanillajs",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@auth0/auth0-spa-js": "^2.4.1"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

--------------------------------

### Minimal Universal Login Page Template Example (HTML)

Source: https://auth0.com/docs/manage-users/sessions/configure-keep-me-signed-in-sessions

A basic HTML template for Auth0's Universal Login page. This example includes styling for a background image and centers the widget. It's designed to be used with the Auth0 CLI's template update command.

```html
<!DOCTYPE html>
<html lang="{{locale}}">
  <head>
    {%- auth0:head -%}
    <style>
      body {
        background-image: url("https://images.unsplash.com/photo-1643916861364-02e63ce3e52f");
        background-size: cover;
        background-position: center;
      }
      .prompt-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.3);
      }
    </style>
    <title>{{ prompt.screen.texts.pageTitle }}</title>
  </head>
  <body class="_widget-auto-layout">
    {% if prompt.name == "login" or prompt.name == "signup" %}
      <div class="prompt-wrapper">
        {%- auth0:widget -%}
      </div>
    {% else %}
      {%- auth0:widget -%}
    {% endif %}
  </body>
</html>
```

--------------------------------

### Start Development Server

Source: https://auth0.com/docs/quickstart/spa/capn-web

Command to launch the application locally for testing the Auth0 integration.

```shellscript
npm run start
```

--------------------------------

### Build and Run Auth0 Java EE Sample Application

Source: https://auth0.com/docs/quickstart/webapp/java-ee/interactive

These commands build the cloned Auth0 Java EE sample application using Maven and then run it on a WildFly server. Ensure your Auth0 configuration values in `src/main/webapp/WEB-INF/web.xml` are updated before running.

```bash
./mvnw clean wildfly:run
```

--------------------------------

### Angular Development Server Command

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Command to start the Angular development server for the Auth0 project. This command compiles the Angular application and serves it locally, typically on port 4200. It also provides instructions for changing the port if the default is in use and updating the Auth0 application's callback URLs accordingly.

```bash
ng serve

If port 4200 is in use, run: `ng serve --port 4201` and update your Auth0 app’s callback URLs to `http://localhost:4201`
```

--------------------------------

### Install Routing Library via Composer

Source: https://auth0.com/docs/quickstart/backend/php/interactive

Installs the simple-php-router library to manage application routes efficiently.

```bash
composer require steampixel/simple-php-router
```

--------------------------------

### Render Authentication Quickstart Grid

Source: https://auth0.com/docs/ja-jp

This component maps over an array of language objects to generate a grid of clickable cards. Each card links to specific authentication quickstart documentation and displays light/dark mode compatible icons.

```jsx
const languages = [{ img: "apple.svg", label: "iOS", href: "/docs/quickstart/native/ios-swift" }, { img: "android.svg", label: "Android", href: "/docs/quickstart/native/android" }];

export const AuthQuickstartGrid = () => (
  <section className="grid grid-cols-2 md:grid-cols-4 gap-6">
    {languages.map((lang, idx) => (
      <a key={idx} href={lang.href} className="flex flex-col items-center">
        <img src={`/docs/images/icons/light/${lang.img}`} alt={lang.label} className="h-8 w-8 dark:hidden" />
        <img src={`/docs/images/icons/dark/${lang.img}`} alt={lang.label} className="h-8 w-8 hidden dark:block" />
        <span>{lang.label}</span>
      </a>
    ))}
  </section>
);
```

--------------------------------

### Initialize and use SignupId manager in TypeScript

Source: https://auth0.com/docs/libraries/acul/js-sdk/Screens/classes/SignupId

Demonstrates how to instantiate the SignupId class, retrieve required and optional identifiers for the signup flow, and execute the signup process with provided parameters.

```typescript
import SignupId from "@auth0/auth0-acul-js/signup-id";
const signupIdManager = new SignupId();
const { transaction } = signupIdManager;
//get mandatory & optional identifiers required for signup
const mandatoryIdentifier = transaction.getRequiredIdentifiers(); // eg: email
const optionalIdentifiers = transaction.getOptionalIdentifiers() // eg: phone
const signupParams = {
 email : "testEmail",
 phone : "+91923456789"
};
signupIdManager.signup(signupParams);
```

--------------------------------

### Cocoapods Installation for Lock.swift

Source: https://auth0.com/docs/libraries/lock-swift

Instructions for installing the Lock.swift library using Cocoapods. This involves adding a specific line to your Podfile and running the 'pod install' command.

```ruby
pod 'Lock', '~> 2.0'
```

--------------------------------

### Initiate Auth0 Login Flow in Java Servlet

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/java-ee/interactive

Handles the initial GET request to the `/login` endpoint to start the Auth0 authentication process. It constructs the callback URL based on the incoming request's scheme, server name, and port. This servlet then prepares the authorization URL to redirect the user to Auth0 for login.

```java
// src/main/java/com/auth0/example/web/LoginServlet.java

        @WebServlet(urlPatterns = "/login")
        public class LoginServlet extends HttpServlet {
            private final Auth0AuthenticationConfig config;
            private final AuthenticationController authenticationController;

            @Inject
            LoginServlet(Auth0AuthenticationConfig config, AuthenticationController authenticationController) {
                this.config = config;
                this.authenticationController = authenticationController;
            }

            @Override
            public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
                // URL where the application will receive the authorization code (e.g., http://localhost:3000/callback)
                String callbackUrl = String.format(
                        "%s://%s:%s/callback",
                        request.getScheme(),
                        request.getServerName(),
                        request.getServerPort()
                );

                // Create the authorization URL to redirect the user to, to begin the authentication flow.

```

--------------------------------

### Send SMS Passwordless Code (Java)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using the Unirest library. Requires the Unirest library. Input includes domain, client ID, client secret, and user's phone number. Outputs an HttpResponse.

```java
HttpResponse<String> response = Unirest.post("https://{yourDomain}/passwordless/start")
  .header("content-type", "application/json")
  .body("{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}")
  .asString();
```

--------------------------------

### Android Manifest Placeholders for Auth0

Source: https://auth0.com/docs/quickstart/native/flutter

This Groovy code snippet shows how to add manifest placeholders for your Auth0 domain and scheme in the `android/app/build.gradle` file. This configuration is necessary for the Auth0 SDK to function correctly on Android.

```groovy
android {
    // ...
    defaultConfig {
        // Add the following line
        manifestPlaceholders += [auth0Domain: "{yourDomain}", auth0Scheme: "https"]
    }
    // ...
}
```

--------------------------------

### Debugging Environment Variable Loading

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Provides a JavaScript code snippet for debugging environment variable loading issues. It logs the presence of essential configuration variables, helping to identify if they are correctly loaded from the .env file.

```javascript
// Debug: Log config values (remove in production!)
console.log('Config check:', {
  hasSecret: !!process.env.SECRET,
  hasClientID: !!process.env.CLIENT_ID,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
});
```

--------------------------------

### Automate Auth0 API Setup via CLI

Source: https://auth0.com/docs/quickstart/backend/python

Shell scripts to programmatically create an Auth0 API and generate a .env configuration file for Mac and Windows environments.

```shellscript
AUTH0_API_NAME="My Flask API" && AUTH0_API_IDENTIFIER="https://my-flask-api" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apis create --name "${AUTH0_API_NAME}" --identifier "${AUTH0_API_IDENTIFIER}" --signing-alg RS256 --json > auth0-api-details.json && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && AUDIENCE=$(jq -r '.identifier' auth0-api-details.json) && echo "AUTH0_DOMAIN=${DOMAIN}" > .env && echo "AUTH0_AUDIENCE=${AUDIENCE}" >> .env && rm auth0-api-details.json && echo ".env file created with your Auth0 API details:" && cat .env
```

```shellscript
$ApiName = "My Flask API"; $ApiIdentifier = "https://my-flask-api"; winget install Auth0.CLI; auth0 login --no-input; auth0 apis create -n "$ApiName" -i "$ApiIdentifier" --signing-alg RS256 --json | Set-Content -Path auth0-api-details.json; $Domain = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name; $Audience = (Get-Content -Raw auth0-api-details.json | ConvertFrom-Json).identifier; Set-Content -Path .env -Value "AUTH0_DOMAIN=$Domain"; Add-Content -Path .env -Value "AUTH0_AUDIENCE=$Audience"; Remove-Item auth0-api-details.json; Write-Output ".env file created with your Auth0 API details:"; Get-Content .env
```

--------------------------------

### Initialize Auth0 Server Client

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Configures the Auth0 ServerClient with environment variables and custom in-memory stores for session and transaction management. This implementation is intended for development purposes only and requires persistent storage for production environments.

```python
import os
from auth0_server_python.auth_server.server_client import ServerClient
from dotenv import load_dotenv

load_dotenv()

class MemoryStateStore:
    """In-memory state store for session data (development only)"""
    def __init__(self):
        self._data = {}
    
    async def get(self, key, options=None):
        return self._data.get(key)
    
    async def set(self, key, value, options=None):
        self._data[key] = value
    
    async def delete(self, key, options=None):
        self._data.pop(key, None)
    
    async def delete_by_logout_token(self, claims, options=None):
        pass

class MemoryTransactionStore:
    """In-memory transaction store for OAuth flows (development only)"""
    def __init__(self):
        self._data = {}
    
    async def get(self, key, options=None):
        return self._data.get(key)
    
    async def set(self, key, value, options=None):
        self._data[key] = value
    
    async def delete(self, key, options=None):
        self._data.pop(key, None)

state_store = MemoryStateStore()
transaction_store = MemoryTransactionStore()

auth0 = ServerClient(
    domain=os.getenv('AUTH0_DOMAIN'),
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    secret=os.getenv('AUTH0_SECRET'),
    redirect_uri=os.getenv('AUTH0_REDIRECT_URI'),
    state_store=state_store,
    transaction_store=transaction_store,
    authorization_params={
        'scope': 'openid profile email',
        'audience': os.getenv('AUTH0_AUDIENCE', '')
    }
)
```

--------------------------------

### Run Auth0 MCP Server in Debug Mode

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

Executes the Auth0 MCP server with debug logging enabled. This helps capture detailed diagnostic information during server execution.

```bash
DEBUG=auth0-mcp npx @auth0/auth0-mcp-server run
```

--------------------------------

### GET /v2/prompts/rendering

Source: https://auth0.com/docs/api/management/v2/prompts/get-all-rendering

Retrieves a list of render setting configurations for all screens. Supports pagination, filtering, and field selection.

```APIDOC
## GET /v2/prompts/rendering

### Description
Get render setting configurations for all screens. This endpoint requires the `read:prompts` scope.

### Method
GET

### Endpoint
/v2/prompts/rendering

### Parameters
#### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include or exclude.
- **include_fields** (boolean) - Optional - Whether specified fields are to be included (default: true) or excluded (false).
- **page** (integer) - Optional - Page index of the results to return (starts at 0).
- **per_page** (integer) - Optional - Number of results per page (max 100, default 50).
- **include_totals** (boolean) - Optional - Return results inside an object with total count (true) or as an array (false).
- **prompt** (string) - Optional - Name of the prompt to filter by.
- **screen** (string) - Optional - Name of the screen to filter by.
- **rendering_mode** (string) - Optional - Rendering mode to filter by (`advanced` or `standard`).

### Request Example
GET /v2/prompts/rendering?prompt=login&per_page=10

### Response
#### Success Response (200)
- **tenant** (string) - Tenant ID
- **prompt** (string) - Name of the prompt
- **screen** (string) - Name of the screen
- **rendering_mode** (string) - Rendering mode (`advanced` or `standard`)
- **context_configuration** (array) - Context values to make available

#### Response Example
[
  {
    "tenant": "my-tenant",
    "prompt": "login",
    "screen": "identifier-first",
    "rendering_mode": "advanced",
    "context_configuration": ["tenant.name"]
  }
]
```

--------------------------------

### Bcrypt Password Hashing Example (Conceptual)

Source: https://auth0.com/docs/manage-users/user-accounts/user-profiles/user-profile-structure

Conceptual example demonstrating the use of bcrypt for password hashing, as used by Auth0 for user imports. Compatible hashes should use '$2a$' or '$2b$' and have 10 salt rounds. This is used for initial user import and cannot be updated later.

```javascript
// Example using a hypothetical bcrypt library
// const bcrypt = require('bcrypt');
// const saltRounds = 10;
// const hashedPassword = bcrypt.hashSync('userPassword', saltRounds);
// console.log(hashedPassword); // Example output: $2b$10$...
```

--------------------------------

### Install Auth0.swift with Cocoapods

Source: https://auth0.com/docs/libraries/auth0-swift

Instructions for adding the Auth0.swift SDK to your project using Cocoapods. This involves adding the 'Auth0' pod to your Podfile and running 'pod install'.

```bash
pod 'Auth0', '~> 2.0'
```

--------------------------------

### Initialize Auth0 Client with Environment Variables (JavaScript)

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Initializes the Auth0 client using environment variables for domain and client ID, and includes essential authorization parameters for the redirect URI. This ensures secure credential management and proper login flow.

```javascript
import { createAuth0Client } from '@auth0/auth0-spa-js';

const auth0Client = await createAuth0Client({
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin
  }
});
```

--------------------------------

### Allow MFA Authentication Request (Swift)

Source: https://auth0.com/docs/secure/multi-factor-authentication/auth0-guardian/guardian-for-ios-sdk

Provides an example of how to allow an MFA authentication request using the Guardian SDK. It involves specifying the tenant domain, the authenticated device, and the notification, then starting the authentication process.

```swift
Guardian
        .authentication(forDomain: "{yourTenantDomain}", device: device)
        .allow(notification: notification)
        .start { result in
            switch result {
            case .success:
                // the auth request was successfuly allowed
            case .failure(let cause):
                // something failed, check cause to see what went wrong
            }
        }
```

--------------------------------

### Send SMS Passwordless Code (Python)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using Python's http.client. No external dependencies. Input includes domain, client ID, client secret, and user's phone number. Outputs the decoded response.

```python
import http.client

conn = http.client.HTTPSConnection("{yourDomain}")

payload = "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/passwordless/start", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

--------------------------------

### Running the Next.js Development Server

Source: https://auth0.com/docs/quickstart/webapp/nextjs/interactive

Command to start the Next.js development server. It also provides instructions on how to change the port if 3000 is already in use and how to update Auth0 callback URLs accordingly. This command initiates the local development environment for the application.

```bash
npm run dev

# If port 3000 is in use:
npm run dev -- --port 3001
```

--------------------------------

### Create Custom Domain with Auth0 Management API (Node.js)

Source: https://auth0.com/docs/customize/custom-domains/multiple-custom-domains

This Node.js example uses the Axios library to send a POST request to the Auth0 Management API for creating a custom domain. It configures the request method, URL, headers, and the JSON data payload. The code includes handling both successful responses and errors. Make sure Axios is installed (`npm install axios`).

```javascript
var axios = require("axios").default;

var options = {
  method: 'POST',
  url: 'https://{yourDomain}/api/v2/custom-domains',
  headers: {
    authorization: 'Bearer {yourMgmtApiAccessToken}',
    'content-type': 'application/json',
    accept: 'application/json'
  },
  data: {
    domain: 'your.example-custom-domain.com',
    type: 'auth0_managed_certs',
    tls_policy: 'recommended',
    custom_client_ip_header: 'true-client-ip',
    domain_metadata: {environment: 'development'}
  }
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### Quickstart Buttons Component (Placeholder)

Source: https://auth0.com/docs/quickstart/native/ionic-angular/interactive

A placeholder component for rendering quickstart buttons, likely linking to external resources like GitHub repositories. It accepts a 'githubLink' prop.

```jsx
<QuickstartButtons githubLink="https://github.com/auth0-samples/auth0-ionic-samples/tree/main/angular" />
```

--------------------------------

### Carthage Installation for Lock.swift

Source: https://auth0.com/docs/libraries/lock-swift

Instructions for installing the Lock.swift library using Carthage. This involves adding a specific line to your Cartfile and running the 'carthage bootstrap' command.

```ruby
github "auth0/Lock.swift" ~> 2.0
```

--------------------------------

### Configure iOS Browser with Custom Presentation in C#

Source: https://auth0.com/docs/quickstart/native/net-android-ios

This C# code snippet shows how to configure the iOS browser using SFSafariViewController with custom presentation options. It initializes the Auth0Client with specific options for the iOS browser component.

```cs
var auth0Client = new Auth0Client(new Auth0ClientOptions
{
    Domain = "{yourDomain}",
    ClientId = "{yourClientId}",
```

--------------------------------

### Make Authenticated API Request (PHP)

Source: https://auth0.com/docs/ja-jp/quickstart/backend/nodejs/interactive

This PHP snippet shows how to make an authenticated GET request using cURL. It sets the authorization header and retrieves the response. Ensure the cURL extension is enabled in your PHP installation.

```php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http:///%7ByourDomain%7D/api_path");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
$headers = array();
$headers[] = "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE";
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$result = curl_exec($ch);
if (curl_errno($ch)) {
    echo 'Error:' . curl_error($ch);
}
curl_close($ch);
echo $result;
```

--------------------------------

### Example User Tokensets Response

Source: https://auth0.com/docs/fr-ca/secure/tokens/token-vault/configure-token-vault

An example JSON response when successfully retrieving a user's tokensets. It lists details for each tokenset, including the connection, ID, issue time, expiration time, last used time, and scope.

```json
Status Code: 200
[
{
  "connection": "google-oauth2",
  "id": "some-unique-tokenset-id1",
  "issued_at": 1733455897,
  "expires_at": 1733455897,
  "last_used_at": 1733453897,
  "scope": "https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events",
},
{
  "id": "some-unique-tokenset-id2",
  "connection": "google-oauth2",
  "issued_at": 1733455897,
  "expires_at": 1733455897,
  "last_used_at": 1733453897,
  "scope": "https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events",
},
{
  "connection": "google-oauth2",
  "issued_at": 1733455897,
  "id": "some-unique-tokenset-id3",
  "expires_at": 1733455897,
 "last_used_at": 1733453897,
  "scope": "Calendar.Read Calendar.Write",
}]

```

--------------------------------

### Make Authenticated API Request (C#)

Source: https://auth0.com/docs/ja-jp/quickstart/backend/nodejs/interactive

This C# snippet uses the RestSharp library to perform a GET request to an API endpoint. It includes setting the authorization header with a Bearer token. Ensure RestSharp is installed in your project.

```csharp
var client = new RestClient("http:///%7ByourDomain%7D/api_path");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer YOUR_ACCESS_TOKEN_HERE");
IRestResponse response = client.Execute(request);
```

--------------------------------

### Auth0 PHP SDK Installation and Configuration

Source: https://auth0.com/docs/quickstart/webapp/php/interactive

This section outlines the initial steps for integrating the Auth0 PHP SDK into your project. It details the necessity of configuring Auth0 in the Auth0 Dashboard, setting up callback and logout URLs, and defining allowed web origins for secure authentication flows.

```php
<?php

// Example of SDK usage (actual code would be more extensive)
require 'vendor/autoload.php';

use Auth0\SDK\Auth0;

$config = [
    'domain' => 'YOUR_AUTH0_DOMAIN',
    'client_id' => 'YOUR_CLIENT_ID',
    'client_secret' => 'YOUR_CLIENT_SECRET',
    'redirect_uri' => 'http://localhost:3000/callback',
    'audience' => 'YOUR_API_AUDIENCE',
    'scope' => 'openid profile email',
];

$auth0 = new Auth0($config);

// ... rest of the PHP application logic ...
?>

<!-- Example HTML for login button -->
<a href="<?php echo htmlspecialchars($auth0->login()); ?>">Login</a>
```

--------------------------------

### Iterate Through User Claims

Source: https://auth0.com/docs/quickstart/native/net-android-ios

Iterates through all available claims associated with the authenticated user profile.

```csharp
if (!loginResult.IsError)
{
	foreach (var claim in loginResult.User.Claims)
	{
		Console.WriteLine($"{claim.Type}: {claim.Value}");
	}
}
```

--------------------------------

### Manage Partials with Auth0 Management API

Source: https://auth0.com/docs/customize/universal-login-pages/customize-signup-and-login-prompts

This snippet demonstrates how to use the Auth0 Management API to retrieve all existing partials for a specific prompt. It requires a GET request to the `/v2/prompts/{prompts_name}/partials` endpoint. The response includes a JSON object mapping entry points to their respective HTML or Liquid content.

```bash
GET /api/v2/prompts/signup-id/partials
# response
# success code: 200
# not found code: 404
body: {
  "signup-id": {
    "form-content-start": "<div>HTML or Liquid</div>",
    "form-content-end": "<div>HTML or Liquid</div>"
  }
}
```

--------------------------------

### Verify Node.js and npm Installation

Source: https://auth0.com/docs/quickstart/spa/angular

These commands verify that Node.js and npm are installed and check their versions. This is a prerequisite for using Auth0 integration tools.

```bash
node --version && npm --version
```

--------------------------------

### Programmatic Auth0 Configuration for Login and Logout

Source: https://auth0.com/docs/quickstart/native/ios-swift/interactive

Demonstrates how to initialize Auth0 web authentication dynamically using client ID and domain, replacing static plist configurations. Includes async implementations for both login and logout flows with error handling.

```swift
func login() async {
    isLoading = true
    errorMessage = nil
    defer { isLoading = false }
    
    do {
        let credentials = try await Auth0
            .webAuth(clientId: "{yourClientId}", domain: "{yourDomain}")
            .scope("openid profile email offline_access")
            .start()
        
        _ = credentialsManager.store(credentials: credentials)
        isAuthenticated = true
        user = credentials.user
    } catch {
        errorMessage = "Login failed: \(error.localizedDescription)"
    }
}

func logout() async {
    isLoading = true
    defer { isLoading = false }
    
    do {
        try await Auth0.webAuth(clientId: "{yourClientId}", domain: "{yourDomain}").clearSession()
        _ = credentialsManager.clear()
        isAuthenticated = false
        user = nil
    } catch {
        errorMessage = "Logout failed: \(error.localizedDescription)"
    }
}
```

--------------------------------

### Web Authentication Login with Custom Scopes and Audience

Source: https://auth0.com/docs/quickstart/native/flutter

Performs web authentication, requesting specific scopes (permissions) and an audience (the API the user is accessing). It also includes a 'prompt' parameter to force a login interaction.

```dart
return await auth0.webAuthentication().login(
      useHTTPS: true,
      scopes: {'openid', 'profile', 'email', 'offline_access', 'read:posts'},
      audience: 'https://myapi.example.com',
      parameters: {'prompt': 'login'},
    );
```

--------------------------------

### Install Auth0 CLI on macOS

Source: https://auth0.com/docs/deploy-monitor/auth0-cli

Installs the Auth0 CLI on macOS using Homebrew. This involves tapping the Auth0 CLI repository and then installing the package.

```bash
brew tap auth0/auth0-cli
brew install auth0
```

--------------------------------

### Debug with MCP Inspector

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

Launches the MCP Inspector tool with the Auth0 MCP server, allowing for interactive debugging and inspection of protocol messages. Requires the debug environment variable to be set.

```bash
npx @modelcontextprotocol/inspector -e DEBUG='auth0-mcp' @auth0/auth0-mcp-server run
```

--------------------------------

### Configure systemd Service for Auth0 AD/LDAP Connector

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/active-directory-ldap/ad-ldap-connector/install-configure-ad-ldap-connector

This bash script configures a systemd service to run the Auth0 AD/LDAP Connector as a background process on Ubuntu Xenial. It ensures the service starts automatically and restarts if it fails.

```bash
[Unit]
Description=Auth0 AD LDAP Agent
After=network.target

[Service]
Type=simple
Restart=always
User=ubuntu
WorkingDirectory=/opt/auth0-adldap
ExecStart=/usr/bin/node server.js

[Install]
WantedBy=multi-user.target
```

--------------------------------

### Initialize Auth0 Server with Gin

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

Sets up the main entry point for the application, loading environment variables and initializing the router with the Auth0 authenticator. It uses the standard net/http server to listen on port 3000.

```golang
package main

import (
	"log"
	"net/http"

	"github.com/joho/godotenv"

	"01-Login/platform/authenticator"
	"01-Login/platform/router"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}
```

--------------------------------

### Create New Application and Post Messages in React

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

Creates a new application with a given name, updates the application list, saves it, and then selects the new application and navigates to the 'integrate' route. It also posts an 'APPS_UPDATED' message.

```javascript
const onCreate = name => {
      const id = uid();
      const next = [...apps, {
        id,
        name: name || "Untitled"
      }];
      setApps(next);
      saveApps(next);
      bc.postMessage({
        type: "APPS_UPDATED"
      });
      selectApp(id);
      nav("integrate");
    };
```

--------------------------------

### Define Authentication UI Structure

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Provides the HTML boilerplate for the application, including placeholders for loading, error, logged-out, and logged-in states.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Auth0 Vanilla JS</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="app-container">
      <div id="loading" class="loading-state">
        <div class="loading-text">Loading...</div>
      </div>
      <div id="error" class="error-state" style="display: none;">
        <div class="error-title">Oops!</div>
        <div class="error-message">Something went wrong</div>
        <div id="error-details" class="error-sub-message"></div>
      </div>
      <div id="app" class="main-card-wrapper" style="display: none;">
        <img src="https://cdn.auth0.com/quantum-assets/dist/latest/logos/auth0/auth0-lockup-en-ondark.png" alt="Auth0 Logo" class="auth0-logo" />
        <h1 class="main-title">Welcome to Sample0</h1>
        <div id="logged-out" class="action-card">
          <p class="action-text">Get started by signing in to your account</p>
          <button id="login-btn" class="button login">Log In</button>
        </div>
        <div id="logged-in" class="logged-in-section" style="display: none;">
          <div class="logged-in-message">✅ Successfully authenticated!</div>
          <h2 class="profile-section-title">Your Profile</h2>
          <div id="profile" class="profile-card"></div>
          <button id="logout-btn" class="button logout">Log Out</button>
        </div>
      </div>
    </div>
    <script type="module" src="app.js"></script>
  </body>
</html>
```

--------------------------------

### Add Auth0 SDK via Carthage

Source: https://auth0.com/docs/quickstart/native/ios-swift/interactive

Integrates the Auth0 SDK into your Xcode project using Carthage. Requires a Cartfile, the 'carthage update' command, and manual framework addition.

```bash
github "auth0/Auth0.swift" ~> 2.0
```

```bash
carthage update --platform iOS --use-xcframeworks
```

--------------------------------

### GET /v2/prompts/{prompt}/screen/{screen}/rendering

Source: https://auth0.com/docs/customize/login-pages/advanced-customizations/reference

Retrieves the specific configuration for a single Universal Login screen.

```APIDOC
## GET /v2/prompts/{prompt}/screen/{screen}/rendering

### Description
Retrieves the current rendering configuration for a specific screen within a given prompt.

### Method
GET

### Endpoint
/v2/prompts/{prompt}/screen/{screen}/rendering

### Parameters
#### Path Parameters
- **prompt** (string) - Required - The identifier of the prompt.
- **screen** (string) - Required - The identifier of the screen.

### Response
#### Success Response (200)
- **rendering** (object) - The configuration object for the specified screen.

#### Response Example
{
  "rendering": {
    "template": "<html>...</html>",
    "metadata": {}
  }
}
```

--------------------------------

### Install Auth0 Agent Skills (Bash)

Source: https://auth0.com/docs/quickstart/spa/vuejs

Installs the Auth0 agent skills for automatic integration into your application. This command uses npx to add the specified skills. Ensure you have Node.js and npm installed.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-vue
```

--------------------------------

### Main Application Entry Point with Auth0

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/golang/interactive

This Go program serves as the main entry point for the application, initializing the environment variables, the Auth0 authenticator, and the router. It then starts an HTTP server listening on port 3000, logging any fatal errors during startup or server operation.

```golang
// Save this file in ./main.go

package main

import (
	"log"
	"net/http"

	"github.com/joho/godotenv"

	"01-Login/platform/authenticator"
	"01-Login/platform/router"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	auth, err := authenticator.New()
	if err != nil {
		log.Fatalf("Failed to initialize the authenticator: %v", err)
	}

	rtr := router.New(auth)

	log.Print("Server listening on http://localhost:3000/")
	if err := http.ListenAndServe("0.0.0.0:3000", rtr); err != nil {
		log.Fatalf("There was an error with the http server: %v", err)
	}
}

```

--------------------------------

### Configure Auth0 Organization Support

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Shows how to initialize the Auth0 client with organization-specific parameters. This ensures the authentication flow is scoped to a particular organization ID.

```javascript
auth0Client = await createAuth0Client({
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin,
    organization: 'YOUR_ORGANIZATION_ID'
  }
});
```

--------------------------------

### Setup Blazor Server Project and Auth0 SDK (Bash)

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server/interactive

This snippet demonstrates how to check for an existing .NET project and either create a new Blazor Server project or add the Auth0 SDK package to an existing one. It's designed for Unix-like systems.

```bash
if ls *.csproj 1> /dev/null 2>&1; then
  echo "Found .csproj file, checking project type..."
  ls *.csproj
else
  echo "No .csproj found, will create new project"
fi
dotnet new blazor -n SampleBlazorApp --interactivity Server && cd SampleBlazorApp && dotnet add package Auth0.AspNetCore.Authentication
```

--------------------------------

### Install Auth0 Agent Skills CLI

Source: https://auth0.com/docs/quickstart/spa/angular

This command installs the Auth0 agent skills for AI integration. It requires npm to be installed.

```bash
npx skills add auth0/agent-skills --skill auth0-quickstart --skill auth0-angular
```

--------------------------------

### Metadata Merge Example (Node.js SDK)

Source: https://auth0.com/docs/manage-users/user-accounts/user-account-linking/suggested-account-linking-server-side-implementation

Example demonstrating how to merge user_metadata and app_metadata from a secondary account into a primary account using the Node.js Auth0 SDK.

```APIDOC
## Metadata merge example

### Description
The following example shows explicitly how the `user_metadata` and `app_metadata` from the secondary account gets merged into the primary account using the [Node.js Auth0 SDK for API V2](https://github.com/auth0/node-auth0).

### Method
N/A (Illustrative example of SDK usage)

### Endpoint
N/A

### Parameters
N/A

### Request Example
N/A

### Response
N/A

### Code Example (JavaScript)
```javascript
/*
 * Recursively merges user_metadata and app_metadata from secondary into primary user.
 * Data of primary user takes preponderance.
 * Array fields are joined.
 */
async function mergeMetadata(primaryUserId, secondaryUserId) {
  // load both users with metedata.
  const [primaryUser, secondaryUser] = await Promise.all(
    [primaryUserId, secondaryUserId].map((uid) => auth0Client.getUser(uid))
  );

  const customizerCallback = function (objectValue, sourceValue) {
    if (_.isArray(objectValue)) {
      return sourceValue.concat(objectValue);
    }
  };
  const mergedUserMetadata = _.merge(
    {},
    secondaryUser.user_metadata,
    primaryUser.user_metadata,
    customizerCallback
  );
  const mergedAppMetadata = _.merge(
    {},
    secondaryUser.app_metadata,
    primaryUser.app_metadata,
    customizerCallback
  );
  await auth0Client.updateUser(primaryUserId, {
    user_metadata: mergedUserMetadata,
    app_metadata: mergedAppMetadata,
  });
}
```
```

--------------------------------

### Install Auth0-PHP SDK using Composer

Source: https://auth0.com/docs/libraries/auth0-php

This command installs the Auth0 PHP SDK and its dependencies using Composer, the standard PHP dependency manager. Ensure Composer is installed and accessible in your project directory before running this command.

```shell
composer require auth0/auth0-php

```

--------------------------------

### Web Authentication Login with Organization Name

Source: https://auth0.com/docs/quickstart/native/flutter

Enables web authentication by specifying the organization's name, allowing users to log in within a designated enterprise context. This method prompts the user to select an organization if multiple are available.

```dart
Future<Credentials> loginWithOrganizationName(String organizationName) async {
    return await auth0.webAuthentication().login(
      useHTTPS: true,
      organizationName: organizationName,
    );
  }
```

--------------------------------

### Example Office 365 Deep Link URL

Source: https://auth0.com/docs/customize/integrations/office-365-custom-provisioning

An example of a fully constructed deep link URL for Office 365, demonstrating the usage of the custom domain and an encoded SharePoint Online URL.

```http
https://login.microsoftonline.com/login.srf?wa=wsignin1.0&whr=travel0.com&wreply=https%3A%2F%2Ftravel0%2Esharepoint%2Ecom
```

--------------------------------

### Create Auth0 App and Environment File (Mac)

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Automates the creation of an Auth0 application and generates an environment file for Angular with the necessary Auth0 configuration details. This script is for macOS users.

```bash
AUTH0_APP_NAME="My Angular App" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apps create -n "${AUTH0_APP_NAME}" -t spa -c http://localhost:4200 -l http://localhost:4200 -o http://localhost:4200 --json --metadata created_by="quickstart-docs-cli" > auth0-app-details.json && CLIENT_ID=$(jq -r '.client_id' auth0-app-details.json) && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && mkdir -p src/environments && echo "export const environment = { production: false, auth0: { domain: '${DOMAIN}', clientId: '${CLIENT_ID}' } };" > src/environments/environment.ts && rm auth0-app-details.json && echo "Environment file created at src/environments/environment.ts with your Auth0 details:" && cat src/environments/environment.ts
```

--------------------------------

### Install Auth0 Lock

Source: https://auth0.com/docs/libraries/lock

Commands to install the Auth0 Lock library using package managers or including it via CDN.

```bash
npm install auth0-lock
bower install auth0-lock
```

```html
<script src="https://cdn.auth0.com/js/lock/11.x/lock.min.js"></script>
```

--------------------------------

### Auth0 CLI command to set up Next.js app

Source: https://auth0.com/docs/quickstart/webapp/nextjs/interactive

This command initializes Auth0 for a Next.js project, creates a new Auth0 application, and generates a .env.local file with necessary authentication credentials.

```bash
auth0 qs setup --type nextjs -n "My App" -p 3000
```

--------------------------------

### Monitor MCP Server Logs

Source: https://auth0.com/docs/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

Displays the last 20 lines of the Claude MCP log file and follows new entries in real-time. Useful for monitoring server activity and identifying runtime errors.

```bash
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

--------------------------------

### POST /u/signup

Source: https://auth0.com/docs/secure/attack-protection/configure-akamai-supplemental-signals

Endpoint for user signup. Requires email and password in the request body.

```APIDOC
## POST /u/signup

### Description
Endpoint for user signup. Requires email and password in the request body.

### Method
POST

### Endpoint
/u/signup

### Parameters
#### Request Body
- **email** (array[string]) - Required - Maximum 256 items
- **password** (array[string]) - Required - Maximum 256 items

### Request Example
```json
{
  "email": ["user@example.com"],
  "password": ["securepassword123"]
}
```

### Response
#### Success Response (200)
- **message** (string) - Confirmation message

#### Response Example
```json
{
  "message": "User registered successfully"
}
```
```

--------------------------------

### GET /v2/guardian/factors/duo/settings

Source: https://auth0.com/docs/api/management/v2/guardian/get-factor-duo-settings

Retrieves the DUO account and factor configuration settings for the tenant.

```APIDOC
## GET /v2/guardian/factors/duo/settings

### Description
Retrieves the DUO account and factor configuration, including the integration keys and host information.

### Method
GET

### Endpoint
/v2/guardian/factors/duo/settings

### Parameters
#### Path Parameters
- None

#### Query Parameters
- None

#### Request Body
- None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/duo/settings' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **ikey** (string) - The integration key for DUO.
- **skey** (string) - The secret key for DUO.
- **host** (string) - The DUO API host.

#### Response Example
{
  "ikey": "DIXXXXXXXXXXXXXXXXXX",
  "skey": "secret-key-value",
  "host": "api-xxxxxxxx.duosecurity.com"
}
```

--------------------------------

### Check Project Prerequisites and Dependencies (Shell)

Source: https://auth0.com/docs/quickstart/spa/svelte

Verifies if Node.js and npm are installed and checks for an existing package.json file to determine if a Svelte project is present. This helps in deciding whether to create a new project or proceed with SDK installation.

```shell
# Check if Node.js and npm are available
node --version && npm --version

# Check for existing Svelte project
if [ -f "package.json" ]; then
  echo "Found package.json, checking for Svelte dependencies..."
  cat package.json
else
  echo "No package.json found, will create new project"
fi
```

--------------------------------

### Full Passwordless Implementation

Source: https://auth0.com/docs/libraries/lock

A complete example showing how to configure Passwordless options including authentication parameters and initializing the Lock instance.

```javascript
var passwordlessOptions = {
  allowedConnections: ['email'],
  passwordlessMethod: 'code',
  auth: {
    redirectUrl: 'http://localhost:3000/callback',   
    responseType: 'token id_token',
    params: {
      scope: 'openid email'               
    }          
  }
}

var lockPasswordless = new Auth0LockPasswordless(
 '{yourClientId}',
 '{yourDomain}',
 passwordlessOptions
);
```

--------------------------------

### Initialize Nuxt.js Project

Source: https://auth0.com/docs/quickstart/webapp/nuxt

Commands to scaffold a new Nuxt.js application and navigate into the project directory.

```shellscript
npx nuxi@latest init auth0-nuxt-app
cd auth0-nuxt-app
```

--------------------------------

### Start Development Server

Source: https://auth0.com/docs/manage-users/cookies/spa-authenticate-with-cookies

Command to initialize the application development environment after configuration.

```shell
npm run dev
```

--------------------------------

### List MFA Authenticators using C#

Source: https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authenticator-factors-mfa-api

This C# code example shows how to fetch MFA authenticators using the RestSharp library. It constructs a GET request to the Auth0 MFA Authenticators endpoint, including the necessary authorization header.

```csharp
var client = new RestClient("https://{yourDomain}/mfa/authenticators");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer MFA_TOKEN");
IRestResponse response = client.Execute(request);
```

--------------------------------

### Retrieve Auth0 Client Details (cURL)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Uses cURL to make a GET request to the Auth0 Management API to retrieve specific client details. Requires your Auth0 domain, client ID, and a Management API access token.

```bash
curl --request GET \
    --url 'https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true' \
    --header 'authorization: Bearer {yourMgmtApiAccessToken}'
```

--------------------------------

### Navigate to Project Directory

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Changes the current directory to the newly created Angular project. This command is necessary to execute subsequent project-specific commands.

```bash
cd auth0-angular
```

--------------------------------

### Configure Auth0 App and .env File (Dashboard)

Source: https://auth0.com/docs/quickstart/webapp/python

Manually sets up the Auth0 application through the Auth0 Dashboard and creates a `.env` file with placeholder values. Requires manual replacement of placeholders with actual Auth0 tenant details.

```bash
# Auth0 Configuration
AUTH0_DOMAIN=YOUR_AUTH0_DOMAIN
AUTH0_CLIENT_ID=YOUR_CLIENT_ID
AUTH0_CLIENT_SECRET=YOUR_CLIENT_SECRET
AUTH0_SECRET=YOUR_GENERATED_SECRET
AUTH0_REDIRECT_URI=http://localhost:5000/callback
```

--------------------------------

### Install Auth0 Angular SDK

Source: https://auth0.com/docs/quickstart/native/ionic-angular/interactive

Installs the Auth0 Angular SDK, which provides modules and services for integrating Auth0 authentication into an Angular application.

```bash
npm install @auth0/auth0-angular
```

--------------------------------

### Complete Adaptive MFA Login Log Example

Source: https://auth0.com/docs/secure/multi-factor-authentication/adaptive-mfa/adaptive-mfa-log-events

A comprehensive example of a successful login log entry in Auth0, demonstrating how risk assessment data is integrated alongside standard session and user metadata.

```json
{
  "date": "2020-06-24T20:24:39.412Z",
  "type": "s",
  "description": "Successful login",
  "connection": "Username-Password-Authentication",
  "connection_id": "con_16Tpc6YqlWZ4HCut",
  "client_id": "9ZteveEZ8CqSLtCNXgvhoCJQ0jt2xSxe",
  "client_name": "jwt.io",
  "ip": "10.12.13.1",
  "client_ip": null,
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
  "details": {
    "prompts": [
      {
        "name": "prompt-authenticate",
        "initiatedAt": null,
        "completedAt": 1593030278513,
        "connection": "Username-Password-Authentication",
        "connection_id": null,
        "strategy": "auth0",
        "identity": "5ee10b1ca85332004e44ce3e",
        "stats": {
          "loginsCount": 66
        },
        "elapsedTime": null
      },
      {
        "name": "login",
        "flow": "universal-login",
        "initiatedAt": 1593030268561,
        "completedAt": 1593030278558,
        "timers": {
          "rules": 336
        },
        "user_id": "auth0|5ee10b1ca85332004e44ce3e",
        "user_name": "user@josh.local.dev.auth0.com",
        "elapsedTime": 9997
      }
    ],
    "initiatedAt": 1593030268550,
    "completedAt": 1593030279374,
    "elapsedTime": 10824,
    "session_id": "dKvR03IjVSNLPaVLqVS-FBuX87z0bBoE",
    "riskAssessment": {
      "confidence": "medium",
      "assessments": {
        "UntrustedIP": {
          "confidence": "high",
          "code": "ip_not_found"
        },
        "NewDevice": {
          "confidence": "medium",
          "code": "match_useragent",
          "details": {
            "device": "unknown",
            "useragent": "known"
          }
        },
        "ImpossibleTravel": {
          "confidence": "low",
          "code": "missing_geoip"
        }
      }
    },
    "stats": {
      "loginsCount": 66
    }
  },
  "hostname": "josh.local.dev.auth0.com",
  "user_id": "auth0|5ee10b1ca85332004e44ce3e",
  "user_name": "user@josh.local.dev.auth0.com",
  "strategy": "auth0",
  "strategy_type": "database"
}
```

--------------------------------

### Install Flask and Auth0 Dependencies

Source: https://auth0.com/docs/quickstart/backend/python/interactive

Defines the required dependencies in a requirements.txt file and provides the command to install them via pip.

```text
flask>=3.0
auth0-api-python
python-dotenv
```

```shell
pip install -r requirements.txt
```

--------------------------------

### Initialize and Enroll Device with Guardian.swift

Source: https://auth0.com/docs/secure/multi-factor-authentication/auth0-guardian/guardian-for-ios-sdk

Demonstrates how to import the Guardian library, set the tenant domain, and perform device enrollment. Enrollment requires an enrollment URI, APNS token, and an RSA key pair to link the device to an Auth0 account.

```swift
import Guardian

let domain = "<tenant>.<region>.auth0.com"

Guardian
        .enroll(forDomain: "{yourTenantDomain}",
                usingUri: "{enrollmentUri}",
                notificationToken: "{apnsToken}",
                signingKey: signingKey,
                verificationKey: verificationKey
                )
        .start { result in
            switch result {
            case .success(let enrolledDevice):
                // success, we have the enrollment device data available
            case .failure(let cause):
                // something failed, check cause to see what went wrong
            }
        }
```

--------------------------------

### Request Authorization Code (C#)

Source: https://auth0.com/docs/manage-users/my-account-api

This C# code snippet demonstrates requesting an authorization code using the RestSharp library. It configures a GET request to the Auth0 authorization endpoint. Make sure to install the RestSharp NuGet package and replace the placeholder values.

```csharp
var client = new RestClient("https://{yourDomain}/authorize?response_type=code&client_id={yourClientId}&redirect_uri=%7ByourRedirectUri%7D&scope=create%3Ame%3Aauthentication_methods&offline_access=&audience=https%3A%2F%2F{yourDomain}%2Fme%2F");
var request = new RestRequest(Method.GET);
IRestResponse response = client.Execute(request);
```

--------------------------------

### React Component for Auth0 Quickstart Banner

Source: https://auth0.com/docs/quickstarts

This React component, `QuickstartBanner`, is a simple functional component that renders a banner. It is intended to be used for promoting Auth0 quickstarts. The component currently returns a div element with basic styling for centering content and adding top margin.

```javascript
export const QuickstartBanner = () => {
  return <div className="w-full flex justify-center px-4 mt-10">

```

--------------------------------

### Install Auth0 CLI (Windows)

Source: https://auth0.com/docs/quickstart/webapp/nextjs/index

Installs the Auth0 Command Line Interface (CLI) on Windows using Scoop. This CLI facilitates the management of Auth0 applications and settings directly from the command prompt.

```powershell
# Install Auth0 CLI (if not already installed)
scoop bucket add auth0 https://github.com/auth0/scoop-auth0-cli.git
scoop install auth0
```

--------------------------------

### HTTP Redirect Examples for Authorization Response Modes

Source: https://auth0.com/docs/protocols/oauth2

Examples of HTTP 302 Found responses demonstrating how authorization codes and access tokens are returned via query parameters or URL fragments.

```HTTP
HTTP/1.1 302 Found
Location: https://my-redirect-uri.callback?code=js89p2x1
```

```HTTP
HTTP/1.1 302 Found
Location: https://my-redirect-uri/callback#access_token=eyB…78f&token_type=Bearer&expires_in=3600
```

--------------------------------

### Calling an API with Auth0 Access Token (cURL)

Source: https://auth0.com/docs/flows/guides/device-auth/call-api-device-auth

To call a protected API after obtaining an Access Token, include the token in the `Authorization` header as a Bearer token. This example demonstrates the cURL command for making a GET request to a sample API endpoint.

```bash
curl --request GET \
  --url https://myapi.com/api \
  --header 'authorization: Bearer ACCESS_TOKEN' \
  --header 'content-type: application/json'
```

--------------------------------

### Environment Configuration (Placeholder)

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Defines the environment-specific configuration for Auth0, including the domain and client ID. This is a placeholder and should be replaced with actual values.

```typescript
export const environment = {
  production: false,
  auth0: {
    domain: {yourDomain},
    clientId: {yourClientId}
  }
};
```

--------------------------------

### Install Auth0 SPA JS SDK (npm)

Source: https://auth0.com/docs/quickstart/spa/svelte

Installs the Auth0 SPA JavaScript SDK into an existing Svelte project. This SDK is essential for handling authentication flows, token management, and user sessions.

```bash
npm install @auth0/auth0-spa-js
```

--------------------------------

### Auth0 Management API Pagination Response Example

Source: https://auth0.com/docs/deploy-monitor/logs/log-search-query-syntax

This JSON structure represents a paginated response from the Auth0 Management API when fetching logs with the 'include_totals' parameter. It includes metadata about the results such as the number of items returned, the limit per page, the start index, and the total number of available logs.

```json
{
  "length": 5,
  "limit": 5,
  "logs": [...],
  "start": 0,
  "total": 5
}
```

--------------------------------

### Initialize Auth0 SDK Configuration

Source: https://auth0.com/docs/fr-ca/quickstart/webapp/php/interactive

This snippet shows how to configure the Auth0 SDK with your domain, client ID, client secret, and redirect URI. It sets up the necessary parameters for authentication and session management.

```php
<?php

  declare(strict_types=1);

  require('vendor/autoload.php');

  use Auth0SDK\Auth0;
  use Auth0SDK\Configuration\SdkConfiguration;

  $configuration = new SdkConfiguration(
    domain: '{yourDomain}',
    clientId: '{yourClientId}',
    clientSecret: '{yourClientSecret}',
    redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
    cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
  );

  $sdk = new Auth0($configuration);

```

--------------------------------

### Retrieve API Access Tokens with Auth0 Python SDK

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Demonstrates how to fetch an access token for a protected API using the Auth0 SDK. It requires setting the audience in the environment and including the offline_access scope.

```python
@app.route('/api-call')
@require_auth
async def api_call():
    try:
        access_token = await auth0.get_access_token(
            audience='https://your-api.example.com',
            store_options=g.store_options
        )
        return f"Access token retrieved: {access_token[:20]}..."
    except Exception as e:
        return f"Error getting access token: {str(e)}", 500
```

```python
authorization_params={
    'scope': 'openid profile email offline_access',
    'audience': os.getenv('AUTH0_AUDIENCE')
}
```

--------------------------------

### Render Sign-Up Call-to-Action

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

Displays a promotional component encouraging users to sign up or log in to their Auth0 account. It includes an image and interactive buttons for authentication actions.

```jsx
function SignUpFormInternal() {
  return (
    <div className="flex flex-col gap-2 items-center h-full">
      <img src="/docs/img/quickstarts/action_hero_dashboard.svg" alt="Sign up" style={{ width: "250px", height: "250px" }} />
      <button onClick={() => console.log("sign up")} className="bg-primary text-white px-4 py-2 rounded-md mt-4">
        Sign up
      </button>
    </div>
  );
}
```

--------------------------------

### GET /login/callback

Source: https://auth0.com/docs/troubleshoot/customer-support/auth0-changelog

Initiate a SAML IDP-initiated login flow with optional organization context.

```APIDOC
## GET /login/callback

### Description
Initiates a SAML IDP-initiated login flow. When using the Organizations feature, you can append the organization ID to ensure the user is directed to the correct organization context.

### Method
GET

### Endpoint
https://YOUR_DOMAIN/login/callback

### Parameters
#### Query Parameters
- **connection** (string) - Required - The name of the SAML Enterprise connection.
- **organization** (string) - Optional - The unique identifier of the customer's organization.

### Request Example
https://YOUR_DOMAIN/login/callback?connection=my-saml-connection&organization=org_12345

### Response
#### Success Response (302)
- **Redirect** - Redirects the user to the Auth0 login page with the specified connection and organization context applied.

#### Response Example
{
  "status": "redirecting to authentication provider"
}
```

--------------------------------

### Authorization URL Example

Source: https://auth0.com/docs/get-started/authentication-and-authorization-flow/hybrid-flow/call-api-hybrid-flow

An example of an HTML anchor tag to initiate the authorization code flow.

```APIDOC
## GET /authorize

### Description
Initiates the authorization code flow by redirecting the user to the Auth0 authorization server.

### Method
GET

### Endpoint
`https://{yourDomain}/authorize`

### Query Parameters
- **response_type** (string) - Required - Specifies the grant type. Common values include `code`, `id_token`, `token`, or combinations like `code id_token token`.
- **client_id** (string) - Required - Your Auth0 application's client ID.
- **redirect_uri** (string) - Required - The URL to which Auth0 will redirect the user after authentication.
- **scope** (string) - Optional - A space-separated list of scopes to request. Example: `appointments%20contacts`.
- **audience** (string) - Optional - The identifier of the API you want to access. Example: `appointments:api`.
- **state** (string) - Recommended - An opaque value used to maintain state between the request and callback. Helps prevent cross-site request forgery (CSRF) attacks.
- **nonce** (string) - Recommended - A string value used to associate a client session with an ID token and to mitigate replay attacks. Required when using `id_token` in `response_type`.

### Request Example
```html
<a href="https://{yourDomain}/authorize?response_type=code id_token token&client_id={yourClientId}&redirect_uri={https://yourApp/callback}&scope=appointments%20contacts&audience=appointments:api&state=xyzABC123&nonce=eq...hPmz">
  Sign In
</a>
```

### Response
#### Success Response (302 Found)
Auth0 redirects the user's browser with an HTTP 302 Found status. The response body is form-urlencoded and contains the following parameters:
- **code** (string) - An authorization code. Present if `response_type` includes `code`.
- **id_token** (string) - An OpenID Connect ID Token. Present if `response_type` includes `id_token`.
- **access_token** (string) - An access token. Present if `response_type` includes `token`.
- **expires_in** (integer) - The lifetime in seconds of the access token. Present if `access_token` is returned.
- **token_type** (string) - The type of the token, typically `Bearer`. Present if `access_token` is returned.
- **state** (string) - The value of the `state` parameter sent in the request.

#### Response Example
```json
HTTP/1.1 302 Found
Content-Type: application/x-www-form-urlencoded
code=AUTHORIZATION_CODE&access_token=ey...MhPw&expires_in=7200&token_type=Bearer&id_token=eyJ...acA&state=xyzABC123
```

### Notes
- The `c_hash` claim in the ID Token should be validated if an ID Token is issued along with a `code`.
- The Access Token received in this step is intended for immediate use and should not be used to call APIs directly. It's recommended to use the Access Token obtained in the subsequent token exchange step for API calls.
```

--------------------------------

### Enable Debug Mode for Auth0 MCP Server

Source: https://auth0.com/docs/ja-jp/get-started/auth0-mcp-server/getting-started-with-auth0-mcp-server

This command enables debug mode for the Auth0 MCP Server by setting the DEBUG environment variable. This will provide more detailed logs, which are essential for diagnosing complex issues and API errors.

```bash
export DEBUG=auth0-mcp
```

--------------------------------

### Initialize and Apply Terraform Configuration (Bash)

Source: https://auth0.com/docs/customize/events/create-an-event-stream

Commands to initialize the Terraform environment, plan the changes for creating an event stream, and apply those changes. Requires setting the webhook endpoint URL as a variable.

```bash
terraform init

URL="<your-ngrok-url>/webhook"
terraform plan -var="webhook_endpoint_url=${URL}"

terraform apply -var="webhook_endpoint_url=https://<your-ngrok-url>/webhook"
```

--------------------------------

### Exchange Authorization Code for Access Token

Source: https://auth0.com/docs/secure/tokens/refresh-tokens/get-refresh-tokens

Demonstrates how to send a POST request to the OAuth 2.0 token endpoint with the required grant type, client credentials, and authorization code. The examples handle the 'application/x-www-form-urlencoded' content type and output the resulting access token.

```Objective-C
[request setHTTPMethod:@"POST"];
[request setAllHTTPHeaderFields:headers];
[request setHTTPBody:postData];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                            completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                if (error) {
                                                    NSLog(@"%@", error);
                                                } else {
                                                    NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                    NSLog(@"%@", httpResponse);
                                                }
                                            }];
[dataTask resume];
```

```PHP
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/oauth/token",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "grant_type=authorization_code&client_id={yourClientId}&client_secret={yourClientSecret}&code={yourAuthorizationCode}&redirect_uri={https://yourApp/callback}",
  CURLOPT_HTTPHEADER => ["content-type: application/x-www-form-urlencoded"]
]);

$response = curl_exec($curl);
curl_close($curl);
```

```Python
import http.client

conn = http.client.HTTPSConnection("")
payload = "grant_type=authorization_code&client_id={yourClientId}&client_secret={yourClientSecret}&code={yourAuthorizationCode}&redirect_uri={https://yourApp/callback}"
headers = { 'content-type': "application/x-www-form-urlencoded" }

conn.request("POST", "/{yourDomain}/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

```Ruby
require 'uri'
require 'net/http'

url = URI("https://{yourDomain}/oauth/token")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["content-type"] = 'application/x-www-form-urlencoded'
request.body = "grant_type=authorization_code&client_id={yourClientId}&client_secret={yourClientSecret}&code={yourAuthorizationCode}&redirect_uri={https://yourApp/callback}"

response = http.request(request)
puts response.read_body
```

```Swift
let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/oauth/token")! as URL)
request.httpMethod = "POST"
request.allHTTPHeaderFields = ["content-type": "application/x-www-form-urlencoded"]
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) { print(error!) }
  else { print(response as? HTTPURLResponse) }
})
dataTask.resume()
```

--------------------------------

### Create React Project with Vite

Source: https://auth0.com/docs/quickstart/spa

Creates a new React project using Vite with a TypeScript template. This command initializes a new project directory named 'auth0-react' and sets up the basic structure for a React application.

```bash
npm create vite@latest auth0-react -- --template react-ts
```

--------------------------------

### Get Directory Provisioning Configurations (cURL)

Source: https://auth0.com/docs/api/management/v2/connections-directory-provisionings/get-connections-directory-provisionings

This snippet demonstrates how to retrieve a list of directory provisioning configurations using cURL. It includes the GET endpoint and necessary headers for authentication and content negotiation. The `from` and `take` query parameters can be added for pagination.

```bash
curl -L -g 'https://{tenantDomain}/api/v2/connections-directory-provisionings' \
-H 'Accept: application/json'
```

--------------------------------

### Send SMS Passwordless Code (C#)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using RestSharp. Requires the RestSharp library. Input includes domain, client ID, client secret, and user's phone number. Outputs an IRestResponse.

```csharp
var client = new RestClient("https://{yourDomain}/passwordless/start");
var request = new RestRequest(Method.POST);
request.AddHeader("content-type", "application/json");
request.AddParameter("application/json", "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}", ParameterType.RequestBody);
IRestResponse response = client.Execute(request);
```

--------------------------------

### Initialize Blazor Server Project

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server/interactive

Commands to create a new Blazor Server project and navigate into the project directory.

```bash
dotnet new blazor -n SampleBlazorApp --interactivity Server
cd SampleBlazorApp
```

--------------------------------

### Retrieve Refresh Token Metadata using Auth0 Management API (Bash)

Source: https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-metadata/configure-refresh-token-metadata

This example shows how to retrieve existing refresh token metadata by making a GET request to the `/api/v2/refresh-tokens/{id}` endpoint of the Auth0 Management API. This requires an access token with the `update:refresh_tokens` scope.

```bash
GET /api/v2/refresh-tokens/{id}
```

--------------------------------

### GET /v2/connections-scim-configurations

Source: https://auth0.com/docs/api/management/v2/connections-scim-configurations/get-connections-scim-configurations

Retrieves a list of SCIM configurations for the tenant, supporting pagination via query parameters.

```APIDOC
## GET /v2/connections-scim-configurations

### Description
Retrieve a list of SCIM configurations of a tenant. Requires the `read:scim_config` scope.

### Method
GET

### Endpoint
/v2/connections-scim-configurations

### Parameters
#### Query Parameters
- **from** (string) - Optional - Id from which to start selection.
- **take** (integer) - Optional - Number of results per page. Defaults to 50.

### Request Example
```
GET /v2/connections-scim-configurations?take=10
```

### Response
#### Success Response (200)
- **scim_configurations** (object[]) - List of SCIM configurations
  - **connection_id** (string) - The connection's identifier
  - **connection_name** (string) - The connection's name
  - **strategy** (string) - The connection's strategy
  - **tenant_name** (string) - The tenant's name
  - **user_id_attribute** (string) - User ID attribute for generating unique user ids
  - **mapping** (object[]) - The mapping between auth0 and SCIM
  - **created_at** (string) - ISO 8601 date and time created
  - **updated_on** (string) - ISO 8601 date and time last updated
  - **next** (string) - The cursor for the next page of results

#### Response Example
{
  "scim_configurations": [
    {
      "connection_id": "con_12345",
      "connection_name": "my-scim-connection",
      "strategy": "scim",
      "tenant_name": "my-tenant",
      "user_id_attribute": "userName",
      "mapping": [],
      "created_at": "2023-01-01T00:00:00.000Z",
      "updated_on": "2023-01-01T00:00:00.000Z"
    }
  ]
}
```

--------------------------------

### Verify OTP and Get Auth Tokens (Node.js)

Source: https://auth0.com/docs/secure/multi-factor-authentication/authenticate-using-ropg-flow-with-mfa/enroll-and-challenge-otp-authenticators

This Node.js example uses the Axios library to send a POST request to the Auth0 Token endpoint for OTP verification. It requires the client ID, client secret, MFA token, and user OTP, formatted as URL-encoded form data.

```javascript
var axios = require("axios").default;

var options = {
  method: 'POST',
  url: 'https://{yourDomain}/oauth/token',
  headers: {'content-type': 'application/x-www-form-urlencoded'},
  data: new URLSearchParams({
    grant_type: 'http://auth0.com/oauth/grant-type/mfa-otp',
    client_id: '{yourClientId}',
    client_secret: '{yourClientSecret}',
    mfa_token: '{mfaToken}',
    otp: '{userOtpCode}'
  })
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### Configure Auth0 CLI and Application

Source: https://auth0.com/docs/quickstart/backend/laravel/interactive

Commands to install the Auth0 CLI, authenticate, and programmatically create the application and API definitions required for the SDK.

```bash
curl -sSfL https://raw.githubusercontent.com/auth0/auth0-cli/main/install.sh | sh -s -- -b .
./auth0 login
./auth0 apps create --name "My Laravel Backend" --type "regular" --auth-method "post" --callbacks "http://localhost:8000/callback" --logout-urls "http://localhost:8000" --reveal-secrets --no-input --json > .auth0.app.json
./auth0 apis create --name "My Laravel Backend API" --identifier "https://github.com/auth0/laravel-auth0" --offline-access --no-input --json > .auth0.api.json
```

--------------------------------

### Application Metadata Example (JSON)

Source: https://auth0.com/docs/customize/login-pages/universal-login/customize-templates

Example of application metadata, which can store custom attributes and values for your Auth0 application. This is typically a JSON object.

```json
{
  "attribute1": "value",
  "attribute2": "value",
  "attribute3": "value"
}
```

--------------------------------

### Install Auth0 Agent Skills via CLI

Source: https://auth0.com/docs/troubleshoot/customer-support/auth0-changelog

Command to initialize Auth0 Agent Skills, which provides AI coding assistants with structured guidance for implementing Auth0 authentication across various frameworks.

```bash
npx skills add auth0/agent-skills
```

--------------------------------

### Environment Variables for Auth0 API Access

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This snippet lists the necessary environment variables required for the Auth0 SDK to obtain access tokens for protected APIs. These variables should be set in your `.env` file.

```dotenv
CLIENT_SECRET=your_client_secret_from_dashboard
API_AUDIENCE=https://your-api.example.com
```

--------------------------------

### Send SMS Passwordless Code (PHP)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using PHP's cURL. No external dependencies. Input includes domain, client ID, client secret, and user's phone number. Outputs the response or a cURL error.

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/passwordless/start",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}",
  CURLOPT_HTTPHEADER => [
    "content-type: application/json"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:";
} else {
  echo $response;
}
```

--------------------------------

### Initialize Auth0 Instance in Activity

Source: https://auth0.com/docs/quickstart/native/android

Demonstrates the import statements and class structure required to initialize the Auth0 SDK within an Android Activity.

```kotlin
import com.auth0.android.Auth0
import com.auth0.android.authentication.AuthenticationException
import com.auth0.android.callback.Callback
import com.auth0.android.provider.WebAuthProvider
import com.auth0.android.result.Credentials

class MainActivity : ComponentActivity() {
    private lateinit var auth0: Auth0
}
```

--------------------------------

### Send SMS Passwordless Code (Objective-C)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using Objective-C's NSURLSession. No external dependencies. Input includes domain, client ID, client secret, and user's phone number. Outputs the HTTP response or an error.

```objectivec
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"content-type": @"application/json" };
NSDictionary *parameters = @{ @"client_id": @"{yourClientId}",
                                @"client_secret": @"{yourClientSecret}",
                                @"connection": @"sms",
                                @"phone_number": @"{userPhoneNumber}",
                                @"send": @"code" };

NSData *postData = [NSJSONSerialization dataWithJSONObject:parameters options:0 error:nil];

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/passwordless/start"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"POST"];
[request setAllHTTPHeaderFields:headers];
[request setHTTPBody:postData];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

--------------------------------

### Initialize Auth0 Client in C#

Source: https://auth0.com/docs/fr-ca/quickstart/native/wpf-winforms/interactive

Initializes the Auth0 client with domain and client ID. Sets the PostLogoutRedirectUri. Requires the Auth0.OidcClient NuGet package.

```csharp
using Auth0.OidcClient;

public partial class MainWindow : Window
{
    private Auth0Client client;

    private void InitializeClient()
    {
        Auth0ClientOptions clientOptions = new Auth0ClientOptions
        {
            Domain = "{yourDomain}",
            ClientId = "{yourClientId}"
        };
        client = new Auth0Client(clientOptions);
        clientOptions.PostLogoutRedirectUri = clientOptions.RedirectUri;
    }
}
```

--------------------------------

### Akamai API Resource Configuration for /u/signup

Source: https://auth0.com/docs/secure/attack-protection/configure-akamai-supplemental-signals

Defines the configuration for the '/u/signup' API resource within Akamai. This specifies how the API should handle undefined parameters, the path, and the allowed HTTP methods.

```text
API undefined parameters: Specific (Request body)
Path: /signup
Methods: POST
```

--------------------------------

### Send SMS Passwordless Code (Node.js)

Source: https://auth0.com/docs/ja-jp/authenticate/passwordless/implement-login/embedded-login/webapps

Initiates passwordless authentication by sending an SMS code using the Axios library. Requires the Axios library. Input includes domain, client ID, client secret, and user's phone number. Outputs the response data or an error.

```javascript
var axios = require("axios").default;

var options = {
  method: 'POST',
  url: 'https://{yourDomain}/passwordless/start',
  headers: {'content-type': 'application/json'},
  data: {
    client_id: '{yourClientId}',
    client_secret: '{yourClientSecret}',
    connection: 'sms',
    phone_number: '{userPhoneNumber}',
    send: 'code'
  }
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### Retrieve Auth0 Client Details (Swift)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Provides a Swift example for fetching Auth0 client information using `NSMutableURLRequest`. This snippet initializes the request with the URL and sets the authorization header.

```swift
import Foundation

let headers = ["authorization": "Bearer {yourMgmtApiAccessToken}"]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true")! as URL,

```

--------------------------------

### Create FastAPI Project and Virtual Environment (Bash)

Source: https://auth0.com/docs/quickstart/backend/fastapi

This snippet shows how to create a new directory for a FastAPI project, navigate into it, and set up a Python virtual environment. It includes commands for both Linux/macOS and Windows.

```bash
mkdir my-fastapi-api
cd my-fastapi-api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

--------------------------------

### Perform GET Request with Query Parameters

Source: https://auth0.com/docs/api/authentication?javascript=

Demonstrates the standard format for passing parameters in a GET request via the URL query string.

```http
GET https://${account.namespace}/some-endpoint?param=value&param=value
```

--------------------------------

### Initialize, Plan, and Apply Terraform Configuration

Source: https://auth0.com/docs/customize/events/create-an-event-stream

These bash commands are used to manage Terraform resources. 'terraform init' initializes the backend and providers, 'terraform plan' shows the proposed changes, and 'terraform apply' creates or updates the resources defined in your Terraform files.

```bash
terraform init
```

```bash
terraform plan
```

```bash
terraform apply
```

--------------------------------

### Initialize Auth0 WebAuth Instance

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

How to instantiate the WebAuth class using your Auth0 domain and client ID to enable authentication services.

```javascript
var webAuth = new auth0.WebAuth({
  domain:       '{yourDomain}',
  clientID:     '{yourClientId}'
});
```

--------------------------------

### Deploy TikTok Integration Proxy for Token Endpoint

Source: https://auth0.com/docs/authenticate/identity-providers/social-identity-providers/tiktok

This example demonstrates a Node.js server setup for proxying token requests to TikTok. It includes a '/proxy/token' POST route that appends the 'client_key' parameter programmatically. This is required because custom parameters cannot be directly passed to the Authentication API's /token endpoint.

```javascript
import express from 'express';
import { request } from 'undici';

const app = express();

app.use(express.json());

app.post('/proxy/token', async (req, res) => {
  const { code, redirect_uri, grant_type } = req.body;
  const clientKey = req.headers['x-client-key']; // Assuming client_key is passed as a header

  if (!code || !redirect_uri || !grant_type || !clientKey) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const tiktokTokenEndpoint = 'https://open.tiktokapis.com/oauth2/token/'; // Replace with actual TikTok token endpoint
    const response = await request(tiktokTokenEndpoint, {
      method: 'POST',
      body: JSON.stringify({
        code: code,
        redirect_uri: redirect_uri,
        grant_type: grant_type,
        client_key: clientKey // Append client_key here
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.body.json();
    res.json(data);
  } catch (error) {
    console.error('Error proxying token request:', error);
    res.status(500).json({ error: 'Failed to proxy token request' });
  }
});

const port = 3333;
app.listen(port, () => {
  console.log(`Proxy server running on http://localhost:${port}`);
});

```

--------------------------------

### Retrieve Auth0 Client Details (Ruby)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Shows how to retrieve Auth0 client details using Ruby's `Net::HTTP` library. This example constructs a URI, sets up an HTTP request with SSL, and includes the authorization header.

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer {yourMgmtApiAccessToken}'

response = http.request(request)
puts response.read_body
```

--------------------------------

### Configure Hono Auth0 Middleware

Source: https://auth0.com/docs/quickstart/webapp/hono

Initializes the Hono application with Auth0 authentication middleware. It demonstrates how to set up public routes, protect specific paths using requiresAuth, and retrieve user session data.

```typescript
import 'dotenv/config';
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { auth, requiresAuth, Auth0Exception, type OIDCEnv } from '@auth0/auth0-hono';

const app = new Hono<OIDCEnv>();

app.use(
  auth({
    domain: process.env.AUTH0_DOMAIN,
    clientID: process.env.AUTH0_CLIENT_ID,
    clientSecret: process.env.AUTH0_CLIENT_SECRET,
    baseURL: process.env.BASE_URL,
    authRequired: false,
    session: {
      secret: process.env.AUTH0_SESSION_ENCRYPTION_KEY,
    },
  })
);

app.get('/', (c) => c.text('Public — no login required'));

app.use('/profile/*', requiresAuth());

app.get('/profile', async (c) => {
  const session = await c.var.auth0Client?.getSession(c);
  const user = session?.user;
  return c.json({ message: 'Protected profile', user });
});

const port = Number(process.env.PORT) || 3000;
serve({ fetch: app.fetch, port }, (info) => {
    console.log(`Server is running on http://localhost:${info.port}`);
  }
);
```

--------------------------------

### Example cURL Request to Get Log Stream by ID

Source: https://auth0.com/docs/api/management/v2/log-streams/get-log-streams-by-id

This snippet demonstrates how to retrieve a specific log stream using its ID via a cURL command. It includes necessary headers for authentication and content negotiation. Ensure you replace `{tenantDomain}` and `:id` with your actual tenant domain and log stream ID.

```bash
curl -L -g 'https://{tenantDomain}/api/v2/log-streams/:id' \
-H 'Accept: application/json'
```

--------------------------------

### Install Auth0 PHP SDK and Dependencies

Source: https://auth0.com/docs/quickstart/backend/php/interactive

Installs the Auth0 PHP SDK and necessary PSR-17/PSR-18 compatible HTTP libraries using Composer. Ensure you are in your project's root directory before running these commands.

```bash
cd <your-project-directory>
composer require symfony/http-client nyholm/psr7
composer require auth0/auth0-php
```

--------------------------------

### AWS IAM Policy for S3 Bucket Access

Source: https://auth0.com/docs/customize/extensions/authorization-extension/install-authorization-extension

This JSON policy grants an IAM user the necessary permissions to manage objects within a specified S3 bucket, which is required for the Auth0 Authorization Extension when using Amazon S3 for data storage. Ensure you replace '{nameOfYourBucket}' with your actual bucket name.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::{nameOfYourBucket}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{nameOfYourBucket}"
            ],
            "Condition": {}
        }
    ]
}
```

--------------------------------

### Implement Custom Login Parameters

Source: https://auth0.com/docs/quickstart/spa/flutter/interactive

Shows how to pass specific authorization parameters to the login flow, such as forcing a specific connection or requesting custom scopes.

```Dart
Future<void> _loginWithGoogle() async {
  await auth0Service.auth0Web.loginWithRedirect(
    redirectUrl: 'http://localhost:3000',
    authorizationParams: AuthorizationParams(
      connection: 'google-oauth2', // Force Google login
      screen_hint: 'signup',       // Show signup screen
    ),
  );
}

Future<void> _loginWithCustomScope() async {
  await auth0Service.auth0Web.loginWithRedirect(
    redirectUrl: 'http://localhost:3000',
    authorizationParams: AuthorizationParams(
      scope: 'openid profile email read:messages',
      audience: 'https://your-api.example.com',
    ),
  );
}
```

--------------------------------

### GET /v2/prompts

Source: https://auth0.com/docs/api/management/v2/prompts/get-prompts

Retrieve the current Universal Login configuration for the tenant, including feature flags for authentication flows.

```APIDOC
## GET /v2/prompts

### Description
Retrieve details of the Universal Login configuration of your tenant. This includes the Identifier First Authentication and WebAuthn with Device Biometrics for MFA features.

### Method
GET

### Endpoint
https://{tenantDomain}/api/v2/prompts

### Parameters
#### Path Parameters
- None

#### Query Parameters
- None

#### Request Body
- None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/prompts' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **universal_login_experience** (string) - Which login experience to use (new or classic).
- **identifier_first** (boolean) - Whether identifier first is enabled or not.
- **webauthn_platform_first_factor** (boolean) - Use WebAuthn with Device Biometrics as the first authentication factor.

#### Response Example
{
  "universal_login_experience": "new",
  "identifier_first": true,
  "webauthn_platform_first_factor": false
}
```

--------------------------------

### Get Pet Information Lambda Function (Node.js)

Source: https://auth0.com/docs/customize/integrations/aws/aws-api-gateway-delegation/aws-api-gateway-delegation-1

This Node.js Lambda function retrieves pet information for a default user from a DynamoDB table named 'Pets'. It handles errors and returns the pet data or an empty object if no data is found. Dependencies include the AWS SDK and 'dynamodb-doc'.

```javascript
var AWS = require('aws-sdk');
var DOC = require('dynamodb-doc');
var dynamo = new DOC.DynamoDB();

exports.handler = function(event, context) {
   var cb = function(err, data) {
      if(err) {
         console.log('error on GetPetsInfo: ',err);
         context.done('Unable to retrieve pet information', null);
      } else {
         if(data.Item && data.Item.pets) {
             context.done(null, data.Item.pets);
         } else {
              context.done(null, {});
         }
      }
   };

   dynamo.getItem({TableName:"Pets", Key:{username:"default"}}, cb);
};
```

--------------------------------

### Create New Application Handler (JavaScript)

Source: https://auth0.com/docs/quickstart/native/windows-uwp-csharp/interactive

Handles the creation of a new application. It generates a unique ID, updates the application list, saves the list, notifies other components via broadcast channel, selects the new app, and navigates to the integrate page.

```javascript
const onCreate = name => {
  const id = uid();
  const next = [...apps, {
    id,
    name: name || "Untitled"
  }];
  setApps(next);
  saveApps(next);
  bc.postMessage({
    type: "APPS_UPDATED"
  });
  selectApp(id);
  nav("integrate");
};
```

--------------------------------

### Set Custom Text for Prompt - Management API Examples

Source: https://auth0.com/docs/customize/login-pages/universal-login/customize-text-elements

Examples demonstrating how to set custom text for a specific prompt and screen using the Auth0 Management API. These examples cover cURL, C#, Go, Java, and Node.js, showing how to make a PUT request to update prompt configurations. Ensure you have the necessary Management API access token with 'read:prompts' and 'update:prompts' scopes.

```bash
curl --request PUT \
  --url 'https://{yourDomain}/api/v2/prompts/login/custom-text/en' \
  --header 'authorization: Bearer {yourMgmtApiAccessToken}' \
  --header 'content-type: application/json' \
  --data '{ "login": { "description": "Login to ACME's Website" } }'
```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/prompts/login/custom-text/en");
var request = new RestRequest(Method.PUT);
request.AddHeader("content-type", "application/json");
request.AddHeader("authorization", "Bearer {yourMgmtApiAccessToken}");
request.AddParameter("application/json", "{ \"login\": { \"description\": \"Login to ACME's Website\" } }", ParameterType.RequestBody);
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/prompts/login/custom-text/en"

	payload := strings.NewReader("{ \"login\": { \"description\": \"Login to ACME's Website\" } }")

	req, _ := http.NewRequest("PUT", url, payload)

	req.Header.Add("content-type", "application/json")
	req.Header.Add("authorization", "Bearer {yourMgmtApiAccessToken}")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.put("https://{yourDomain}/api/v2/prompts/login/custom-text/en")
  .header("content-type", "application/json")
  .header("authorization", "Bearer {yourMgmtApiAccessToken}")
  .body("{ \"login\": { \"description\": \"Login to ACME's Website\" } }")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'PUT',
  url: 'https://{yourDomain}/api/v2/prompts/login/custom-text/en',
  headers: {
    'content-type': 'application/json',
    authorization: 'Bearer {yourMgmtApiAccessToken}'
  },
  data: {login: {description: 'Login to ACME\'s Website'}}
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

--------------------------------

### Retrieve Users by Name using Swift

Source: https://auth0.com/docs/manage-users/user-search/user-search-query-syntax

This Swift code snippet shows how to construct and execute an HTTP GET request to the Auth0 API to search for users whose names start with 'john'. It includes setting the request URL, HTTP method, headers, and handling the response. Dependencies include Foundation and URLSession.

```swift
let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/users?q=name%3Ajohn*&search_engine=v3")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                      timeoutInterval: 10.0)
  request.httpMethod = "GET"
  request.allHTTPHeaderFields = headers

  let session = URLSession.shared
  let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
    if (error != nil) {
      print(error)
    } else {
      let httpResponse = response as? HTTPURLResponse
      print(httpResponse)
    }
  })

  dataTask.resume()
```

--------------------------------

### HTML: Quickstart Buttons Component

Source: https://auth0.com/docs/quickstart/webapp/aspnet-owin/interactive

A placeholder for a component that displays quickstart buttons, likely linking to a GitHub repository for sample code. This component is not defined in the provided JavaScript but is referenced in the HTML structure.

```html
<QuickstartButtons githubLink="https://github.com/auth0-samples/auth0-aspnet-owin-mvc-samples/tree/master/Quickstart/Sample" />
```

--------------------------------

### Example tenant.yaml configuration structure

Source: https://auth0.com/docs/extensions/bitbucket-deploy

An excerpt of a YAML file generated by the Auth0 Deploy CLI, demonstrating how rules and resource servers are represented in the exported configuration.

```yaml
rules:
  - name: custom-claims
    script: ./rules/custom-claims.js
    stage: login_success
    enabled: true
    order: 1
resourceServers:
  - name: ZeroHR API
    identifier: 'https://api.dev.zerohr.app/'
    allow_offline_access: false
    signing_alg: RS256
    skip_consent_for_verifiable_first_party_clients: true
    token_lifetime: 86400
    token_lifetime_for_web: 7200
```

--------------------------------

### Get User Permissions via Management API (Multiple Languages)

Source: https://auth0.com/docs/manage-users/access-control/configure-core-rbac/rbac-users/view-user-permissions

This snippet shows how to fetch a user's permissions from the Auth0 Management API. It requires the user's ID and a Management API access token. The examples cover cURL, C#, Go, Java, Node.js, Objective-C, PHP, Python, Ruby, and Swift.

```bash
curl --request GET \
    --url 'https://{yourDomain}/api/v2/users/USER_ID/permissions' \
    --header 'authorization: Bearer MGMT_API_ACCESS_TOKEN'
```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/users/USER_ID/permissions");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer MGMT_API_ACCESS_TOKEN");
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/users/USER_ID/permissions"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("authorization", "Bearer MGMT_API_ACCESS_TOKEN")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/users/USER_ID/permissions")
  .header("authorization", "Bearer MGMT_API_ACCESS_TOKEN")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
    method: 'GET',
    url: 'https://{yourDomain}/api/v2/users/USER_ID/permissions',
    headers: {authorization: 'Bearer MGMT_API_ACCESS_TOKEN'}
};
axios.request(options).then(function (response) {
    console.log(response.data);
}).catch(function (error) {
    console.error(error);
});
```

```objc
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"authorization": @"Bearer MGMT_API_ACCESS_TOKEN" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/users/USER_ID/permissions"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/api/v2/users/USER_ID/permissions",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer MGMT_API_ACCESS_TOKEN"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:";
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("{yourDomain}")

headers = { 'authorization': "Bearer MGMT_API_ACCESS_TOKEN" }

conn.request("GET", "/api/v2/users/USER_ID/permissions", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/users/USER_ID/permissions")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer MGMT_API_ACCESS_TOKEN'

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let headers = ["authorization": "Bearer MGMT_API_ACCESS_TOKEN"]

let url = URL(string: "https://{yourDomain}/api/v2/users/USER_ID/permissions")!
var request = URLRequest(url: url)
request.httpMethod = "GET"
headers.forEach { key, value in
    request.setValue(value, forHTTPHeaderField: key)
}

let task = URLSession.shared.dataTask(with: request) { data, response, error in
    guard let data = data else { return }
    print(String(data: data, encoding: .utf8))
}
task.resume()
```

--------------------------------

### Install Auth0 PHP SDK and Dependencies

Source: https://auth0.com/docs/quickstart/backend/php

Commands to install the Auth0 PHP SDK, Guzzle HTTP client for PSR-17/PSR-18 compliance, and a dotenv loader for environment variable management.

```bash
composer require guzzlehttp/guzzle guzzlehttp/psr7 http-interop/http-factory-guzzle
composer require auth0/auth0-php
composer require vlucas/phpdotenv
```

--------------------------------

### Apply Production Security Best Practices

Source: https://auth0.com/docs/quickstart/backend/nodejs/interactive

Implements essential security headers using Helmet and configures Express to trust proxies. Also demonstrates tuning SDK settings like clockTolerance for production environments.

```javascript
const helmet = require('helmet');

app.use(helmet());
app.enable('trust proxy');

const checkJwt = auth({
  issuerBaseURL: `https://${process.env.AUTH0_DOMAIN}`,
  audience: process.env.AUTH0_AUDIENCE,
  clockTolerance: 10,
});
```

--------------------------------

### Install Auth0 MAUI SDK using .NET CLI

Source: https://auth0.com/docs/quickstart/native/maui/interactive

Installs the Auth0 OIDC Client SDK for MAUI applications using the .NET command-line interface. This is an alternative to using the NuGet Package Manager.

```bash
dotnet add package Auth0.OidcClient.MAUI
```

--------------------------------

### Retrieve User Import Job Error Details (cURL)

Source: https://auth0.com/docs/users/guides/bulk-user-imports

This snippet shows how to make a GET request to the Auth0 Management API to retrieve error details for a failed user import job. It requires your Management API Access Token and the specific Job ID. The response will contain details about users that failed to import and the reasons for failure. Sensitive fields are redacted in the example response.

```cURL
curl --request GET \
  --url 'https://{yourDomain}/api/v2/jobs/JOB_ID/errors' \
  --header 'authorization: Bearer MGMT_API_ACCESS_TOKEN' \
  --header 'content-type: application/json'
```

--------------------------------

### Create Project Directories and Files (Windows)

Source: https://auth0.com/docs/quickstart/webapp/nextjs/index

PowerShell commands to create the necessary directories (`src/lib`, `src/components`) and files (`auth0.ts`, `proxy.ts`, `LoginButton.tsx`, `LogoutButton.tsx`, `Profile.tsx`) for Auth0 integration on Windows systems.

```powershell
New-Item -ItemType Directory -Force -Path src/lib, src/components
New-Item -ItemType File -Path src/lib/auth0.ts, src/proxy.ts, src/components/LoginButton.tsx, src/components/LogoutButton.tsx, src/components/Profile.tsx
```

--------------------------------

### Get User Roles using Management API (Multiple Languages)

Source: https://auth0.com/docs/manage-users/access-control/configure-core-rbac/rbac-users/view-user-roles

This snippet shows how to retrieve a user's roles using the Auth0 Management API. It requires the user's ID and a Management API access token. The examples cover cURL, C#, Go, Java, Node.js, Objective-C, PHP, Python, Ruby, and Swift.

```bash
curl --request GET \
    --url 'https://{yourDomain}/api/v2/users/USER_ID/roles' \
    --header 'authorization: Bearer MGMT_API_ACCESS_TOKEN'
```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/users/USER_ID/roles");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer MGMT_API_ACCESS_TOKEN");
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/users/USER_ID/roles"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("authorization", "Bearer MGMT_API_ACCESS_TOKEN")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/users/USER_ID/roles")
  .header("authorization", "Bearer MGMT_API_ACCESS_TOKEN")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
    method: 'GET',
    url: 'https://{yourDomain}/api/v2/users/USER_ID/roles',
    headers: {authorization: 'Bearer MGMT_API_ACCESS_TOKEN'}
};
axios.request(options).then(function (response) {
    console.log(response.data);
}).catch(function (error) {
    console.error(error);
});
```

```objective-c
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"authorization": @"Bearer MGMT_API_ACCESS_TOKEN" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/users/USER_ID/roles"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/api/v2/users/USER_ID/roles",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer MGMT_API_ACCESS_TOKEN"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("")

headers = { 'authorization': "Bearer MGMT_API_ACCESS_TOKEN" }

conn.request("GET", "/{yourDomain}/api/v2/users/USER_ID/roles", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/users/USER_ID/roles")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer MGMT_API_ACCESS_TOKEN'

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let headers = ["authorization": "Bearer MGMT_API_ACCESS_TOKEN"]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/users/USER_ID/roles")! as URL,

```

--------------------------------

### POST /passwordless/start

Source: https://auth0.com/docs/libraries/auth0js/migration-guide

Initiates the passwordless authentication process by sending a code or link to the user via email or SMS.

```APIDOC
## POST /passwordless/start

### Description
Initiates the passwordless authentication process. Exactly one of `phoneNumber` or `email` must be provided.

### Method
POST

### Endpoint
webAuth.passwordlessStart

### Parameters
#### Request Body
- **connection** (String) - Required - Specifies delivery method: 'email' or 'sms'.
- **send** (String) - Required - Specifies content: 'code' or 'link'.
- **phoneNumber** (String) - Optional - User's phone number for SMS delivery.
- **email** (String) - Optional - User's email address for email delivery.

### Request Example
{
  "connection": "email",
  "send": "code",
  "email": "foo@bar.com"
}
```

--------------------------------

### Deploy Auth0 Action using cURL

Source: https://auth0.com/docs/api/management/v2/actions/post-deploy-action

This snippet demonstrates how to deploy an Auth0 Action using the cURL command-line tool. It requires the action's ID and your tenant domain. Ensure you have the necessary API token and permissions to execute this request.

```bash
curl -L -g -X POST 'https://{tenantDomain}/api/v2/actions/actions/:id/deploy' \
-H 'Accept: application/json'
```

--------------------------------

### Perform Exact Match User Search via Auth0 API

Source: https://auth0.com/docs/manage-users/user-search/user-search-query-syntax

This snippet shows how to query the Auth0 API to find users with an exact name match. It utilizes the 'q' parameter with double quotes for precise matching. The examples demonstrate making a GET request to the /api/v2/users endpoint, requiring an authorization header with a Management API access token.

```bash
curl --request GET \
    --url 'https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3' \
    --header 'authorization: Bearer {yourMgmtApiAccessToken}'
```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer {yourMgmtApiAccessToken}");
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("authorization", "Bearer {yourMgmtApiAccessToken}")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3")
  .header("authorization", "Bearer {yourMgmtApiAccessToken}")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://{yourDomain}/api/v2/users',
  params: {q: 'name:"jane smith"', search_engine: 'v3'},
  headers: {authorization: 'Bearer {yourMgmtApiAccessToken}'}
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objc
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"authorization": @"Bearer {yourMgmtApiAccessToken}" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3"] 
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy 
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer {yourMgmtApiAccessToken}"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("")

headers = { 'authorization': "Bearer {yourMgmtApiAccessToken}" }

conn.request("GET", "/{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["authorization"] = 'Bearer {yourMgmtApiAccessToken}'

response = http.request(request)
puts response.read_body
```

```swift
import Foundation

let headers = ["authorization": "Bearer {yourMgmtApiAccessToken}"]

let request = NSMutableURLRequest(url: NSURL(string: "https://{yourDomain}/api/v2/users?q=name%3A%22jane%20smith%22&search_engine=v3")! as URL,

```

--------------------------------

### Retrieve Auth0 Universal Login Branding Template (cURL, C#, Go, Java, Node.js, Obj-C)

Source: https://auth0.com/docs/customize/login-pages/universal-login/customize-templates

These code examples demonstrate how to retrieve the current Auth0 Universal Login branding template. They all use the GET method on the specified API endpoint and require an 'authorization' header with a Bearer token. The response typically contains the HTML content of the template.

```bash
curl --request GET \
  --url 'https://{yourDomain}/api/v2/branding/templates/universal-login' \
  --header 'authorization: Bearer MGMT_API_ACCESS_TOKEN'

```

```csharp
var client = new RestClient("https://{yourDomain}/api/v2/branding/templates/universal-login");
var request = new RestRequest(Method.GET);
request.AddHeader("authorization", "Bearer MGMT_API_ACCESS_TOKEN");
IRestResponse response = client.Execute(request);

```

```go
package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/api/v2/branding/templates/universal-login"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("authorization", "Bearer MGMT_API_ACCESS_TOKEN")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}

```

```java
HttpResponse<String> response = Unirest.get("https://{yourDomain}/api/v2/branding/templates/universal-login")
  .header("authorization", "Bearer MGMT_API_ACCESS_TOKEN")
  .asString();

```

```javascript
var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://{yourDomain}/api/v2/branding/templates/universal-login',
  headers: {authorization: 'Bearer MGMT_API_ACCESS_TOKEN'}
};
axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});

```

```objectivec
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"authorization": @"Bearer MGMT_API_ACCESS_TOKEN" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/branding/templates/universal-login"] 
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy 
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request

```

--------------------------------

### Configure Auth0.swift SDK Programmatically

Source: https://auth0.com/docs/libraries/auth0-swift

Code examples demonstrating how to configure the Auth0.swift SDK programmatically for different use cases: Web Auth, Authentication API client, and Management API client. Requires your Auth0 Client ID and Domain.

```swift
Auth0
    .webAuth(clientId: "{yourAuth0ClientID}", domain: "{yourAuth0Domain}")
    // ...
```

```swift
Auth0
    .authentication(clientId: "{yourAuth0ClientID}", domain: "{yourAuth0Domain}")
    // ...
```

```swift
Auth0
    .users(token: credentials.accessToken, domain: "{yourAuth0Domain}")
    // ...
```

--------------------------------

### Implement AuthenticationController Provider

Source: https://auth0.com/docs/quickstart/webapp/java/index

A singleton provider class that initializes the Auth0 AuthenticationController using parameters from the ServletContext. It ensures a single instance is used throughout the application lifecycle.

```java
package com.auth0.example;

import com.auth0.AuthenticationController;
import com.auth0.jwk.JwkProvider;
import com.auth0.jwk.JwkProviderBuilder;
import javax.servlet.ServletConfig;
import java.io.UnsupportedEncodingException;

public class AuthenticationControllerProvider {
    private AuthenticationControllerProvider() {}
    private static AuthenticationController INSTANCE;

    public static synchronized AuthenticationController getInstance(ServletConfig config) throws UnsupportedEncodingException {
        if (INSTANCE == null) {
            String domain = config.getServletContext().getInitParameter("com.auth0.domain");
            String clientId = config.getServletContext().getInitParameter("com.auth0.clientId");
            String clientSecret = config.getServletContext().getInitParameter("com.auth0.clientSecret");
            JwkProvider jwkProvider = new JwkProviderBuilder(domain).build();
            INSTANCE = AuthenticationController.newBuilder(domain, clientId, clientSecret)
                    .withJwkProvider(jwkProvider)
                    .build();
        }
        return INSTANCE;
    }
}
```

--------------------------------

### Install Auth0 Gem for Rails

Source: https://auth0.com/docs/quickstart/webapp/rails/interactive

Add the `omniauth-rails_csrf_protection` gem to your Gemfile to prevent forged authentication requests. After adding the gem, run `bundle install` to install it.

```ruby
gem 'omniauth-rails_csrf_protection', '~> 1.0'
```

--------------------------------

### Implement Login and Logout with Auth0 SDK

Source: https://auth0.com/docs/quickstart/native/ios-swift/interactive

Provides Swift functions for handling user login and logout using the Auth0 SDK. It includes storing and clearing credentials, managing authentication state, and error handling for login and logout operations.

```swift
import Auth0
import SwiftUI

class AuthenticationService: ObservableObject {
    @Published var isAuthenticated = false
    @Published var user: User? = nil
    @Published var errorMessage: String? = nil
    @Published var isLoading = false
    
    private let credentialsManager = CredentialsManager(secureStorage: KeychainStorage())

    func login() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let credentials = try await Auth0
              .webAuth()
              .scope("openid profile email offline_access")
              .start()
            
            _ = credentialsManager.store(credentials: credentials)
            isAuthenticated = true
            // Get user info from the ID token
            user = credentials.user
        } catch {
            errorMessage = "Login failed: (error.localizedDescription)"
        }
    }
    
    func logout() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            try await Auth0
              .webAuth()
              .clearSession()
            _ = credentialsManager.clear()
            isAuthenticated = false
            user = nil
        } catch {
            errorMessage = "Logout failed: (error.localizedDescription)"
        }
    }
}
```

--------------------------------

### Initiate Passwordless SMS Code via API (Multiple Languages)

Source: https://auth0.com/docs/authenticate/passwordless/implement-login/embedded-login/webapps

These examples demonstrate how to send a POST request to the Auth0 passwordless start endpoint to initiate an SMS-based passwordless login. They require your Auth0 domain, client ID, client secret, and the user's phone number. The API returns a response indicating the success or failure of the operation.

```csharp
var client = new RestClient("https://{yourDomain}/passwordless/start");
var request = new RestRequest(Method.POST);
request.AddHeader("content-type", "application/json");
request.AddParameter("application/json", "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}", ParameterType.RequestBody);
IRestResponse response = client.Execute(request);
```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "https://{yourDomain}/passwordless/start"

	payload := strings.NewReader("{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("content-type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```java
HttpResponse<String> response = Unirest.post("https://{yourDomain}/passwordless/start")
  .header("content-type", "application/json")
  .body("{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}")
  .asString();
```

```javascript
var axios = require("axios").default;

var options = {
  method: 'POST',
  url: 'https://{yourDomain}/passwordless/start',
  headers: {'content-type': 'application/json'},
  data: {
    client_id: '{yourClientId}',
    client_secret: '{yourClientSecret}',
    connection: 'sms',
    phone_number: '{userPhoneNumber}',
    send: 'code'
  }
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
```

```objectivec
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"content-type": @"application/json" };
NSDictionary *parameters = @{ @"client_id": @"{yourClientId}",
                              @"client_secret": @"{yourClientSecret}",
                              @"connection": @"sms",
                              @"phone_number": @"{userPhoneNumber}",
                              @"send": @"code" };

NSData *postData = [NSJSONSerialization dataWithJSONObject:parameters options:0 error:nil];

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/passwordless/start"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"POST"];
[request setAllHTTPHeaderFields:headers];
[request setHTTPBody:postData];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/passwordless/start",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}",
  CURLOPT_HTTPHEADER => [
    "content-type: application/json"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```python
import http.client

conn = http.client.HTTPSConnection("")

payload = "{\"client_id\": \"{yourClientId}\", \"client_secret\": \"{yourClientSecret}\", \"connection\": \"sms\", \"phone_number\": \"{userPhoneNumber}\",\"send\": \"code\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/{yourDomain}/passwordless/start", payload, headers)

res = conn.getresponse()
data = res.read()
```

--------------------------------

### Install and Enable NGINX njs Module

Source: https://auth0.com/docs/quickstart/webapp/nginx-plus/interactive

Commands to install the NGINX Plus njs module via yum and the configuration directive to load the module into the NGINX environment.

```sh
sudo yum install nginx-plus-module-njs jq
```

```conf
load_module modules/ngx_http_js_module.so;
```

--------------------------------

### Create and Send GET Request with Ruby

Source: https://auth0.com/docs/ja-jp/manage-users/my-account-api

Creates a new HTTP GET request object and sends it using the configured HTTP client. It then prints the response body.

```ruby
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

--------------------------------

### Clone and Run Sample Application

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server

Provides terminal commands to clone the Auth0 ASP.NET Core sample repository and execute the application.

```bash
git clone https://github.com/auth0-samples/auth0-aspnetcore-blazor-server-samples/tree/main/Quickstart/Sample

# Update appsettings.json with your Auth0 configuration
dotnet run
```

--------------------------------

### GET /api/v2/prompts/:prompt/screen/:screen/rendering

Source: https://auth0.com/docs/api/management/v2/prompts/get-rendering

Retrieves the rendering configuration for a specific prompt and screen within an Auth0 tenant.

```APIDOC
## GET /api/v2/prompts/:prompt/screen/:screen/rendering

### Description
Retrieves the rendering settings for a specified prompt and screen combination. This endpoint requires appropriate scopes and an active subscription for Advanced Customizations.

### Method
GET

### Endpoint
https://{tenantDomain}/api/v2/prompts/:prompt/screen/:screen/rendering

### Parameters
#### Path Parameters
- **prompt** (string) - Required - The identifier of the prompt (e.g., login, signup, mfa).
- **screen** (string) - Required - The identifier of the specific screen within the prompt.

### Request Example
```
curl -L -g 'https://{tenantDomain}/api/v2/prompts/login/screen/login-id/rendering' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **settings** (object) - The rendering configuration object for the requested screen.

#### Error Responses
- **400** - Invalid request URI.
- **401** - Invalid token or signature.
- **402** - Paid subscription required for Advanced Customizations.
- **403** - Insufficient scope (requires read:prompts) or feature not enabled for tenant.
- **404** - The specified prompt or screen does not exist.
- **429** - Too many requests (Rate limited).
```

--------------------------------

### Configure Auth0 Application Settings via CLI

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core

This snippet demonstrates how to automatically set up your Auth0 application and configure `appsettings.json` using the Auth0 CLI. It handles creating the application, retrieving secrets, and updating the configuration file. Dependencies include `jq` for JSON parsing on Linux/macOS and `auth0-cli`.

```shellscript
AUTH0_APP_NAME="My App" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:5000/callback -l http://localhost:5000 -o http://localhost:5000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" > auth0-app-details.json && CLIENT_ID=$(jq -r '.client_id' auth0-app-details.json) && CLIENT_SECRET=$(jq -r '.client_secret' auth0-app-details.json) && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && rm auth0-app-details.json && cat > appsettings.json << EOF
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Auth0": {
    "Domain": "${DOMAIN}",
    "ClientId": "${CLIENT_ID}",
    "ClientSecret": "${CLIENT_SECRET}"
  }
}
EOF
echo "appsettings.json created with your Auth0 details:" && cat appsettings.json
```

```powershell
$AUTH0_APP_NAME = "My MVC App"
$latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/auth0/auth0-cli/releases/latest"
$latestVersion = $latestRelease.tag_name
$version = $latestVersion -replace "^v"
Invoke-WebRequest -Uri "https://github.com/auth0/auth0-cli/releases/download/${latestVersion}/auth0-cli_${version}_Windows_x86_64.zip" -OutFile ".\auth0.zip"
Expand-Archive ".\auth0.zip" .\
[System.Environment]::SetEnvironmentVariable('PATH', $Env:PATH + ";${pwd}")
auth0 login --no-input
auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:5000/callback -l http://localhost:5000 -o http://localhost:5000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" | Set-Content -Path auth0-app-details.json
$AppDetails = Get-Content -Raw auth0-app-details.json | ConvertFrom-Json
$ClientId = $AppDetails.client_id
$ClientSecret = $AppDetails.client_secret
$Domain = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name
$Config = Get-Content -Raw appsettings.json | ConvertFrom-Json
if (-not $Config.Auth0) { $Config | Add-Member -MemberType NoteProperty -Name Auth0 -Value @{} }
$Config.Auth0.Domain = $Domain
$Config.Auth0.ClientId = $ClientId
$Config.Auth0.ClientSecret = $ClientSecret
$Config | ConvertTo-Json -Depth 10 | Set-Content appsettings.json
Remove-Item auth0-api-details.json
Write-Output "✅ appsettings.json updated with your Auth0 API details:"
Get-Content appsettings.json
```

--------------------------------

### Get User Permissions using cURL

Source: https://auth0.com/docs/api/management/v2/users/get-permissions

This cURL command demonstrates how to retrieve all permissions associated with a user. It targets the GET /v2/users/{id}/permissions endpoint and includes necessary headers.

```bash
curl -L -g 'https://{tenantDomain}/api/v2/users/:id/permissions' \
-H 'Accept: application/json'
```

--------------------------------

### Install auth0-js via npm or yarn

Source: https://auth0.com/docs/libraries/auth0js/v7

Installs the auth0-js module using either npm or yarn package managers. This is the recommended way to include the library in your project for managing dependencies.

```bash
npm install auth0-js

yarn add auth0-js
```

--------------------------------

### GET /v2/guardian/factors/phone/providers/twilio

Source: https://auth0.com/docs/api/management/v2/guardian/get-phone-twilio-factor-provider

Retrieves the configuration details for a Twilio phone provider.

```APIDOC
## GET /v2/guardian/factors/phone/providers/twilio

### Description
Retrieves configuration details for a Twilio phone provider that has been set up in your tenant.

### Method
GET

### Endpoint
/v2/guardian/factors/phone/providers/twilio

### Scopes
read:guardian_factors

### Response
#### Success Response (200)
- **from** (string) - From number
- **messaging_service_sid** (string) - Copilot SID
- **auth_token** (string) - Twilio Authentication token
- **sid** (string) - Twilio SID

#### Response Example
```json
{
  "from": "+15551234567",
  "messaging_service_sid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "auth_token": "your_twilio_auth_token",
  "sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

#### Error Responses
- **200** - Twilio Phone configuration successfully retrieved.
- **400** - Invalid input based on schemas.
- **401** - Token has expired or signature is invalid.
- **403** - Insufficient scope.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/phone/providers/twilio' \
-H 'Accept: application/json'
```
```

--------------------------------

### Initialize Lock with Options in Swift

Source: https://auth0.com/docs/libraries/lock-swift/lock-swift-configuration-options

Demonstrates how to initialize the Lock library and apply multiple configuration options such as closability, username style, and allowed screens.

```swift
Lock
  .classic()
  .withOptions {
    $0.closable = true
    $0.usernameStyle = [.Username]
    $0.allow = [.Login, .ResetPassword]
  }
  .present(from: self)
```

--------------------------------

### Construct Authorization URLs for Auth0

Source: https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication/configure-step-up-authentication-for-apis

Examples of OAuth 2.0 authorization request URLs used to initiate authentication. The difference between the two examples is the inclusion of the 'transfer:funds' scope, which triggers the MFA Action.

```text
https://{yourDomain}/authorize?
audience=https://my-banking-api&
scope=openid%20view:balance%20transfer:funds&
response_type=id_token%20token&
client_id={yourClientId}&
redirect_uri={https://yourApp/callback}&
nonce=NONCE&
state=OPAQUE_VALUE
```

```text
https://{yourDomain}/authorize?
audience=https://my-banking-api&
scope=openid%20view:balance&
response_type=id_token%20token&
client_id={yourClientId}&
redirect_uri={https://yourApp/callback}&
nonce=NONCE&
state=OPAQUE_VALUE
```

--------------------------------

### Multi-Factor Authentication (MFA) Setup

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/okta/express-configuration

This section details how to enable and configure multi-factor authentication for the Express Configuration flow using Post-Login Actions.

```APIDOC
## Multi-Factor Authentication (MFA) Setup

### Description
This Post-Login Action demonstrates how to conditionally challenge users for multi-factor authentication, such as WebAuthN or one-time password via email, during the Express Configuration flow. This requires enabling MFA factors in your Auth0 tenant and selecting the 'Customize MFA Factors using Actions' option.

### Method
Not Applicable (Code Snippet for Auth0 Action)

### Endpoint
Not Applicable (Auth0 Action)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None (This is a code snippet for an Auth0 Action)

### Request Example
```javascript
exports.onExecutePostLogin = async (event, api) => {
  if (event.resource_server && event.resource_server.identifier === "urn:auth0:express-configure") {
    api.multifactor.enable('any');
    api.authentication.challengeWith({ type: 'email' });

    if (!event.user.enrolledFactors.some(m => m.type === 'webauthn-platform')) {
      api.authentication.enrollWith({type: 'webauthn-platform'});
    } else {
      api.authentication.challengeWith({type: 'webauthn-platform'});
    }
  }
}
```

### Response
#### Success Response (200)
Not Applicable (Auth0 Action)

#### Response Example
Not Applicable (Auth0 Action)
```

--------------------------------

### GET /v2/supplemental-signals

Source: https://auth0.com/docs/api/management/v2/supplemental-signals/get-supplemental-signals

Retrieves the current supplemental signals configuration for the authenticated tenant.

```APIDOC
## GET /v2/supplemental-signals

### Description
Retrieves the supplemental signals configuration for a tenant, indicating whether Akamai headers are processed.

### Method
GET

### Endpoint
https://{tenantDomain}/api/v2/supplemental-signals

### Parameters
#### Path Parameters
- **tenantDomain** (string) - Required - The domain of your Auth0 tenant.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/supplemental-signals' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **akamai_enabled** (boolean) - Indicates if incoming Akamai Headers should be processed.

#### Response Example
{
  "akamai_enabled": true
}

### Error Handling
- **401**: Invalid token or signature.
- **403**: Insufficient scope (expected: read:attack_protection).
- **404**: Configuration not found.
- **429**: Too many requests.
```

--------------------------------

### Initialize and Configure Auth0 Client

Source: https://auth0.com/docs/ja-jp/quickstart/spa/vanillajs/interactive

Demonstrates how to initialize the Auth0 client using domain and client ID credentials. It sets up the redirect URI and provides a promise-based structure for handling authentication events.

```javascript
auth0.createAuth0Client({
  domain: "dev-s3674bdouue0bd73.us.auth0.com",
  clientId: "QqpqsvIQHjLodaUIPpabJcIHoG41tbAv",
  authorizationParams: {
    redirect_uri: window.location.origin
  }
}).then(async (auth0Client) => {
  // Implementation logic follows
});
```

--------------------------------

### GET /v2/self-service-profiles

Source: https://auth0.com/docs/api/management/v2/self-service-profiles/get-self-service-profiles

Retrieves a list of self-service profiles configured for the tenant.

```APIDOC
## GET /v2/self-service-profiles

### Description
Retrieves a list of self-service profiles. This endpoint requires the `read:self_service_profiles` scope.

### Method
GET

### Endpoint
/v2/self-service-profiles

### Parameters
#### Query Parameters
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page. Defaults to 50.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array of results (false, default).

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/self-service-profiles' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - The unique ID of the self-service Profile.
- **name** (string) - The name of the self-service Profile.
- **description** (string) - The description of the self-service Profile.
- **allowed_strategies** (string[]) - List of IdP strategies allowed for the flow.

#### Response Example
{
  "id": "ssp_12345",
  "name": "Example Profile",
  "description": "Standard SSO profile",
  "allowed_strategies": ["oidc", "samlp"]
}
```

--------------------------------

### Fastify Server Setup with Auth0

Source: https://auth0.com/docs/quickstart/webapp/fastify

Initializes a Fastify server, registers view engine and Auth0 authentication plugin, and defines a route for the home page. Requires environment variables for Auth0 configuration and a session secret.

```javascript
const fastify = require('fastify')({ logger: true });
const port = process.env.PORT || 3000;

await fastify.register(require('@fastify/view'), {
  engine: { ejs: require('ejs') },
  root: './views',
});

await fastify.register(require('fastify-auth0'), {
  domain: process.env.AUTH0_DOMAIN!,
  clientId: process.env.AUTH0_CLIENT_ID!,
  clientSecret: process.env.AUTH0_CLIENT_SECRET!,
  appBaseUrl: process.env.APP_BASE_URL!,
  sessionSecret: process.env.SESSION_SECRET!,
});

fastify.get('/', async (request, reply) => {
  const session = await fastify.auth0Client.getSession({ request, reply });
  return reply.view('views/home.ejs', {
    isAuthenticated: !!session,
  });
});

fastify.listen({ port: Number(port) });
```

--------------------------------

### Add Organization Support (JavaScript)

Source: https://auth0.com/docs/quickstart/spa/vanillajs

This example illustrates how to configure the Auth0 client to support organizations. It involves updating the `createAuth0Client` call with an `organization` parameter in the `authorizationParams`. This is useful for multi-tenant applications where users belong to specific organizations.

```javascript
auth0Client = await createAuth0Client({
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin,
    organization: 'YOUR_ORGANIZATION_ID' // or prompt user to select
  }
});
```

--------------------------------

### GET /v2/rules

Source: https://auth0.com/docs/api/management/v2/rules/get-rules

Retrieve a filtered list of rules defined in the Auth0 tenant.

```APIDOC
## GET /v2/rules

### Description
Retrieve a filtered list of rules. Accepts a list of fields to include or exclude.

### Method
GET

### Endpoint
/v2/rules

### Parameters
#### Query Parameters
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array of results (false, default).
- **enabled** (boolean) - Optional - Filter on whether a rule is enabled (true) or disabled (false).
- **fields** (string) - Optional - Comma-separated list of fields to include or exclude.
- **include_fields** (boolean) - Optional - Whether specified fields are to be included (true) or excluded (false).

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/rules' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **name** (string) - Name of this rule.
- **id** (string) - ID of this rule.
- **enabled** (boolean) - Whether the rule is enabled.
- **script** (string) - Code to be executed.
- **order** (number) - Execution order.
- **stage** (string) - Execution stage (login_success, login_failure, or pre_authorize).

#### Response Example
{
  "rules": [
    {
      "id": "rul_12345",
      "name": "My Rule",
      "enabled": true,
      "script": "function (user, context, callback) { ... }",
      "order": 1,
      "stage": "login_success"
    }
  ]
}
```

--------------------------------

### Configure Redis Custom Storage for Auth0 Sessions

Source: https://auth0.com/docs/quickstart/webapp/python/interactive

Shows how to implement a custom Redis-based state store for the Auth0 ServerClient. This is recommended for production environments requiring session sharing across multiple server instances.

```python
from auth0_server_python.stores.redis_state_store import RedisStateStore
import redis.asyncio as redis

redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
state_store = RedisStateStore(
    secret=os.getenv('AUTH0_SECRET'),
    redis_client=redis_client
)

auth0 = ServerClient(
    domain=os.getenv('AUTH0_DOMAIN'),
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    secret=os.getenv('AUTH0_SECRET'),
    redirect_uri=os.getenv('AUTH0_REDIRECT_URI'),
    state_store=state_store,
    authorization_params={'scope': 'openid profile email'}
)
```

--------------------------------

### Install Auth0 Next.js SDK

Source: https://auth0.com/docs/quickstart/webapp/nextjs/index

Installs the official Auth0 Next.js SDK using npm. This package provides the necessary tools and components for integrating Auth0 authentication into a Next.js application.

```shellscript
npm install @auth0/nextjs-auth0
```

--------------------------------

### GET /v2/keys/encryption

Source: https://auth0.com/docs/api/management/v2/keys/get-encryption-keys

Retrieve details of all the encryption keys associated with your Auth0 tenant.

```APIDOC
## GET /v2/keys/encryption

### Description
Retrieve details of all the encryption keys associated with your tenant. Requires the `read:encryption_keys` scope.

### Method
GET

### Endpoint
/v2/keys/encryption

### Parameters
#### Query Parameters
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page. Default value is 50, maximum value is 100.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array of results (false, default).

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/keys/encryption' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **kid** (string) - Key ID
- **type** (string) - Key type (customer-provided-root-key, environment-root-key, tenant-master-key, tenant-encryption-key)
- **state** (string) - Key state (pre-activation, active, deactivated, destroyed)
- **created_at** (string) - Key creation timestamp
- **updated_at** (string) - Key update timestamp
- **public_key** (string) - Public key in PEM format

#### Response Example
{
  "keys": [
    {
      "kid": "key_123",
      "type": "tenant-encryption-key",
      "state": "active",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

--------------------------------

### Auth0 React SDK Installation

Source: https://auth0.com/docs/libraries/auth0-react

Instructions for installing the Auth0 React SDK using npm or yarn package managers. This is a prerequisite for integrating Auth0 authentication into a React application.

```bash
npm install @auth0/auth0-react
```

```bash
yarn add @auth0/auth0-react
```

--------------------------------

### React Component for Displaying Section Cards

Source: https://auth0.com/docs/quickstarts

A React component designed to render a list of section cards, each containing details like name, subtext, logo, and links. This component is used to display quickstart options for various technologies. It takes an 'item' object as a prop to configure the card's content.

```jsx
const SectionCard = ({ item }) => (
  <a
    href={item.links[0].url}
    className="flex flex-col justify-between rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md dark:border-slate-700 dark:bg-black"
  >
    <div className="flex items-center gap-3">
      <img src={item.logo} alt={`${item.name} logo`} className="h-10 w-10 shrink-0 rounded-full bg-white p-2 dark:bg-slate-800" />
      <div>
        <p className="font-semibold leading-tight text-slate-800 dark:text-slate-200">
          {item.name}
        </p>
        <p className="mt-1 text-sm leading-snug text-slate-600 dark:text-slate-400">
          {item.subtext}
        </p>
      </div>
    </div>
    <div className="mt-4 flex items-center justify-between gap-3">
      <span className="text-sm text-slate-600 dark:text-slate-400">
        {item.date}
      </span>
      {item.badge && (
        <span className="inline-flex items-center rounded-full border border-indigo-200 bg-indigo-100 px-2.5 py-0.5 text-xs font-medium text-indigo-800 dark:border-indigo-500 dark:bg-indigo-900 dark:text-indigo-300">
          {item.badge}
        </span>
      )}
      <span className="text-sm font-medium text-indigo-600 hover:underline dark:text-indigo-400">
        {item.links[0].label}
      </span>
    </div>
  </a>
);
```

--------------------------------

### Set API Token Request Body Example

Source: https://auth0.com/docs/api/management/v2/network-acls/put-network-acls-by-id

Provides an example of a request body for setting an API token, including fields for description, active status, priority, rule configuration (action and match criteria), and scope. The `scope` field identifies the origin of the request.

```json
{
  "description": "string",
  "active": true,
  "priority": 0,
  "rule": {
    "action": {
      "block": true,
      "allow": true,
      "log": true,
      "redirect": true,
      "redirect_uri": "string"
    },
    "match": {
      "asns": [
        0
      ],
      "auth0_managed": [
        "string"
      ],
      "geo_country_codes": [
        "string"
      ],
      "geo_subdivision_codes": [
        "string"
      ],
      "ipv4_cidrs": [
        "198.51.100.42"
      ],
      "ipv6_cidrs": [
        "string"
      ],
      "ja3_fingerprints": [
        "string"
      ],
      "ja4_fingerprints": [
        "string"
      ],
      "user_agents": [
        "string"
      ]
    }
  },
  "scope": "management"
}
```

--------------------------------

### Install Auth0 Flutter SDK and Dependencies

Source: https://auth0.com/docs/quickstart/spa/flutter

Adds the Auth0 Flutter package to the project and includes the required Auth0 SPA JS library in the web index file.

```shellscript
flutter pub add auth0_flutter
```

```html
<!DOCTYPE html>
<html>
<head>
  <!-- ... existing head content ... -->
</head>
<body>
  <!-- ... existing body content ... -->

  <!-- Add this before closing body tag -->
  <script src="https://cdn.auth0.com/js/auth0-spa-js/2.9/auth0-spa-js.production.js" defer></script>
</body>
</html>
```

--------------------------------

### Automate Auth0 Application Setup via CLI

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server

Automated scripts to create an Auth0 application and populate the appsettings.json file with credentials.

```shellscript
AUTH0_APP_NAME="My Blazor App" && brew tap auth0/auth0-cli && brew install auth0 && auth0 login --no-input && auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:5000/callback -l http://localhost:5000 -o http://localhost:5000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" > auth0-app-details.json && CLIENT_ID=$(jq -r '.client_id' auth0-app-details.json) && CLIENT_SECRET=$(jq -r '.client_secret' auth0-app-details.json) && DOMAIN=$(auth0 tenants list --json | jq -r '.[] | select(.active == true) | .name') && rm auth0-app-details.json && cat > appsettings.json << EOF
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Auth0": {
    "Domain": "${DOMAIN}",
    "ClientId": "${CLIENT_ID}",
    "ClientSecret": "${CLIENT_SECRET}"
  }
}
EOF
```

```powershell
$AUTH0_APP_NAME = "My Blazor App"
$latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/auth0/auth0-cli/releases/latest"
$latestVersion = $latestRelease.tag_name
$version = $latestVersion -replace "^v"
Invoke-WebRequest -Uri "https://github.com/auth0/auth0-cli/releases/download/${latestVersion}/auth0-cli_${version}_Windows_x86_64.zip" -OutFile ".\auth0.zip"
Expand-Archive ".\auth0.zip" .\
[System.Environment]::SetEnvironmentVariable('PATH', $Env:PATH + ";${pwd}")
auth0 login --no-input
auth0 apps create -n "${AUTH0_APP_NAME}" -t regular -c http://localhost:5000/callback -l http://localhost:5000 -o http://localhost:5000 --reveal-secrets --json --metadata created_by="quickstart-docs-cli" | Set-Content -Path auth0-app-details.json
$AppDetails = Get-Content -Raw auth0-app-details.json | ConvertFrom-Json
$ClientId = $AppDetails.client_id
$ClientSecret = $AppDetails.client_secret
$Domain = (auth0 tenants list --json | ConvertFrom-Json | Where-Object { $_.active -eq $true }).name
$Config = Get-Content -Raw appsettings.json | ConvertFrom-Json
if (-not $Config.Auth0) { $Config | Add-Member -MemberType NoteProperty -Name Auth0 -Value @{} }
$Config.Auth0.Domain = $Domain
$Config.Auth0.ClientId = $ClientId
$Config.Auth0.ClientSecret = $ClientSecret
$Config | ConvertTo-Json -Depth 10 | Set-Content appsettings.json
Remove-Item auth0-app-details.json
```

--------------------------------

### Install Auth0 MAUI SDK using NuGet Package Manager

Source: https://auth0.com/docs/quickstart/native/maui/interactive

Installs the Auth0 OIDC Client SDK for MAUI applications. This SDK simplifies the integration of Auth0 authentication flows.

```powershell
Install-Package Auth0.OidcClient.MAUI
```

--------------------------------

### Initialize and Configure Blazor Server Project

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server

Commands to create a new Blazor Server project and install the necessary Auth0 authentication SDK package.

```shellscript
dotnet new blazor -n SampleBlazorApp --interactivity Server
cd SampleBlazorApp
dotnet add package Auth0.AspNetCore.Authentication
```

--------------------------------

### Configuring Auth0 SDK for API Access Tokens in Node.js

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This configuration snippet sets up the Auth0 SDK to request an access token for calling protected APIs. It includes essential parameters like `clientID`, `issuerBaseURL`, and `audience`, and specifies the desired scopes.

```javascript
const config = {
  authRequired: false,
  auth0Logout: true,
  secret: process.env.SECRET,
  baseURL: process.env.BASE_URL,
  clientID: process.env.CLIENT_ID,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
  clientSecret: process.env.CLIENT_SECRET,  // Required for code flow
  authorizationParams: {
    response_type: 'code',
    audience: process.env.API_AUDIENCE,     // Your API identifier
    scope: 'openid profile email read:data',
  },
};
```

--------------------------------

### Go Module Dependencies (Shell)

Source: https://auth0.com/docs/quickstart/webapp/golang/interactive

This command demonstrates how to initialize a Go module, which is essential for managing project dependencies. It creates a go.mod file to track the project's packages.

```shell
go mod init

# To integrate Auth0 in a Go application, add the `coreos/go-oidc/v3` and `x/oauth2`
# packages.

# In addition to the OIDC and OAuth2 packages, add `joho/godotenv`, `gin-gonic/gin`, and
# `gin-contrib/sessions`.
```

--------------------------------

### GET /v2/sessions/{id}

Source: https://auth0.com/docs/api/management/v2/sessions/get-session

Retrieves detailed information about a specific user session by its unique identifier.

```APIDOC
## GET /v2/sessions/{id}

### Description
Retrieve session information for a specific session ID. This endpoint requires the `read:sessions` scope.

### Method
GET

### Endpoint
/v2/sessions/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the session to retrieve

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/sessions/{id}' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - The ID of the session
- **user_id** (string) - ID of the user
- **created_at** (string/object) - Creation timestamp
- **device** (object) - Metadata related to the device used
- **clients** (object[]) - List of client details for the session
- **authentication** (object) - Details about authentication signals

#### Response Example
{
  "id": "sess_12345",
  "user_id": "auth0|5f8d...",
  "created_at": "2023-10-01T12:00:00Z",
  "device": {
    "initial_ip": "192.168.1.1"
  }
}
```

--------------------------------

### Example user profile object

Source: https://auth0.com/docs/libraries/auth0js/v7

A sample JSON structure representing the user information returned by the Auth0 /userinfo endpoint.

```json
{
    "sub": "auth0|123456789012345678901234",
    "nickname": "johnfoo",
    "name": "johnfoo@gmail.com",
    "picture": "https://gravatar.com/avatar/example.png",
    "updated_at": "2018-05-07T14:16:52.013Z",
    "email": "johnfoo@gmail.com",
    "email_verified": "false"
}
```

--------------------------------

### GET /v2/keys/custom-signing

Source: https://auth0.com/docs/api/management/v2/keys/get-custom-signing-keys

Retrieves the entire JWKS representation of custom signing keys.

```APIDOC
## GET /v2/keys/custom-signing

### Description
Retrieves the entire JWKS representation of custom signing keys.

### Method
GET

### Endpoint
/v2/keys/custom-signing

### Scopes
read:custom_signing_keys

### Response
#### Success Response (200)
- **keys** (object[]) - An array of custom public signing keys.
  - **kty** (string) - Key type. Possible values: [`EC`, `RSA`]
  - **kid** (string) - Key identifier
  - **use** (string) - Key use. Possible values: [`sig`]
  - **key_ops** (string[]) - Key operations
  - **alg** (string) - Key algorithm. Possible values: [`RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, `PS512`]
  - **n** (string) - Key modulus
  - **e** (string) - Key exponent
  - **crv** (string) - Curve. Possible values: [`P-256`, `P-384`, `P-521`]
  - **x** (string) - X coordinate
  - **y** (string) - Y coordinate
  - **x5u** (string) - X.509 URL
  - **x5c** (string[]) - X.509 certificate chain
  - **x5t** (string) - X.509 certificate SHA-1 thumbprint
  - **x5t#S256** (string) - X.509 certificate SHA-256 thumbprint

#### Response Example (200)
```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "some-key-id",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "..."
    }
  ]
}
```

#### Error Responses
- **401** - Invalid token.
- **401** - Invalid signature received for JSON Web Token validation.
- **403** - Insufficient scope; expected any of: read:custom_signing_keys.
- **404** - No custom signing keys found for this tenant. Upload custom signing keys first.
- **429** - Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/keys/custom-signing' \
-H 'Accept: application/json'
```
```

--------------------------------

### Configure Auth0 SDK

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/php/interactive

Initializes the Auth0 SDK with required credentials and configuration settings. This script acts as the entry point for the application's authentication setup.

```php
<?php

declare(strict_types=1);

require('vendor/autoload.php');

use Auth0\SDK\Auth0;
use Auth0\SDK\Configuration\SdkConfiguration;

$configuration = new SdkConfiguration(
  domain: '{yourDomain}',
  clientId: '{yourClientId}',
  clientSecret: '{yourClientSecret}',
  redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
  cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
);

$sdk = new Auth0($configuration);
```

--------------------------------

### Configure Auth0 Credentials in web.xml

Source: https://auth0.com/docs/quickstart/webapp/java/index

Defines the required Auth0 domain, client ID, and client secret as context parameters in the web.xml file. These values are used by the application to initialize the authentication controller.

```xml
<context-param>
    <param-name>com.auth0.domain</param-name>
    <param-value>YOUR_AUTH0_DOMAIN</param-value>
</context-param>
<context-param>
    <param-name>com.auth0.clientId</param-name>
    <param-value>YOUR_AUTH0_CLIENT_ID</param-value>
</context-param>
<context-param>
    <param-name>com.auth0.clientSecret</param-name>
    <param-value>YOUR_AUTH0_CLIENT_SECRET</param-value>
</context-param>
```

--------------------------------

### GET /v2/hooks/{id}

Source: https://auth0.com/docs/api/management/v2/hooks/get-hooks-by-id

Retrieve a hook by its ID. Accepts a list of fields to include in the result.

```APIDOC
## GET /v2/hooks/{id}

### Description
Retrieve a hook by its ID. Accepts a list of fields to include in the result.

### Method
GET

### Endpoint
/v2/hooks/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the hook to retrieve.

#### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include in the result. Leave empty to retrieve all fields.

### Request Example
```json
{
  "example": "(No request body for GET request)"
}
```

### Response
#### Success Response (200)
- **triggerId** (string) - Trigger ID
- **id** (string) - ID of this hook.
- **name** (string) - Name of this hook.
- **enabled** (boolean) - Whether this hook will be executed (true) or ignored (false).
- **script** (string) - Code to be executed when this hook runs.
- **dependencies** (object) - Dependencies of this hook used by webtask server.
  - **[key: string]** (string)

#### Response Example
```json
{
  "triggerId": "string",
  "id": "string",
  "name": "string",
  "enabled": true,
  "script": "string",
  "dependencies": {
    "key": "string"
  }
}
```

### Error Handling
- **400** Invalid request URI. The message will vary depending on the cause.
- **400** Invalid request query string. The message will vary depending on the cause.
- **401** Invalid token.
- **401** Client is not global.
- **401** Invalid signature received for JSON Web Token validation.
- **403** Insufficient scope; expected any of: read:hooks.
- **404** Hook not found.
- **429** Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.
```

--------------------------------

### Router Setup in Go (Gin)

Source: https://auth0.com/docs/quickstart/webapp/golang/interactive

Configures the Gin router, including session management with cookie stores, static file serving, HTML template loading, and defining routes for home, login, callback, user, and logout. It utilizes middleware for session handling and depends on custom packages for authentication and application handlers.

```go
package router

import (
	"encoding/gob"
	"net/http"

	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"

	"01-Login/platform/authenticator"
	"01-Login/platform/middleware"
	"01-Login/web/app/callback"
	"01-Login/web/app/login"
	"01-Login/web/app/logout"
	"01-Login/web/app/user"
)

// New registers the routes and returns the router.
func New(auth *authenticator.Authenticator) *gin.Engine {
	router := gin.Default()

	// To store custom types in our cookies,
	// we must first register them using gob.Register
	gob.Register(map[string]interface{}{})

	store := cookie.NewStore([]byte("secret"))
	router.Use(sessions.Sessions("auth-session", store))

	router.Static("/public", "web/static")
	router.LoadHTMLGlob("web/template/*")

	router.GET("/", func(ctx *gin.Context) {
		ctx.HTML(http.StatusOK, "home.html", nil)
	})
	router.GET("/login", login.Handler(auth))
	router.GET("/callback", callback.Handler(auth))
	router.GET("/user", user.Handler)
	router.GET("/logout", logout.Handler)

	return router
}
```

--------------------------------

### GET /v2/guardian/factors

Source: https://auth0.com/docs/api/management/v2/guardian/get-factors

Retrieve a list of all multi-factor authentication factors configured for the Auth0 tenant.

```APIDOC
## GET /v2/guardian/factors

### Description
Retrieve details of all multi-factor authentication factors associated with your tenant.

### Method
GET

### Endpoint
/v2/guardian/factors

### Scopes
- read:guardian_factors

### Response
#### Success Response (200)
- **enabled** (boolean) - Whether this factor is enabled (true) or disabled (false).
- **trial_expired** (boolean) - Whether trial limits have been exceeded.
- **name** (string) - Factor name (e.g., `push-notification`, `sms`, `email`, `duo`, `otp`, `webauthn-roaming`, `webauthn-platform`, `recovery-code`).

#### Response Example
[
  {
    "name": "push-notification",
    "enabled": true,
    "trial_expired": false
  }
]

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors' \
-H 'Accept: application/json'
```
```

--------------------------------

### Authenticator Service Setup (Go)

Source: https://auth0.com/docs/quickstart/webapp/golang/interactive

Initializes the Auth0 authenticator service. It uses the `oidc` and `oauth2` packages to configure the OpenID Connect provider and OAuth2 client based on environment variables for domain, client ID, client secret, and callback URL.

```Go
// Save this file in ./platform/authenticator/auth.go

package authenticator

import (
	"context"
	"errors"
	"os"

	"github.com/coreos/go-oidc/v3/oidc"
	"golang.org/x/oauth2"
)

// Authenticator is used to authenticate our users.
type Authenticator struct {
	*oidc.Provider
	oauth2.Config
}

// New instantiates the *Authenticator.
func New() (*Authenticator, error) {
	provider, err := oidc.NewProvider(
		context.Background(),
		"https://"+os.Getenv("AUTH0_DOMAIN")+"/",
	)
	if err != nil {
		return nil, err
	}

	conf := oauth2.Config{
		ClientID:     os.Getenv("AUTH0_CLIENT_ID"),
		ClientSecret: os.Getenv("AUTH0_CLIENT_SECRET"),
		RedirectURL:  os.Getenv("AUTH0_CALLBACK_URL"),
		Endpoint:     provider.Endpoint(),
		Scopes:       []string{oidc.ScopeOpenID, "profile"},
	}

	return &Authenticator{
		Provider: provider,
		Config:   conf,
	}, nil
}
```

--------------------------------

### GET /v2/groups

Source: https://auth0.com/docs/api/management/v2/groups/get-groups

Retrieves a list of all groups in the tenant, with support for filtering, pagination, and field selection.

```APIDOC
## GET /v2/groups

### Description
List all groups in your tenant. This endpoint supports filtering by connection, name, or external ID, and allows for pagination.

### Method
GET

### Endpoint
/v2/groups

### Parameters
#### Query Parameters
- **connection_id** (string) - Optional - Filter groups by connection ID.
- **name** (string) - Optional - Filter groups by name.
- **external_id** (string) - Optional - Filter groups by external ID.
- **fields** (string) - Optional - A comma separated list of fields to include or exclude.
- **include_fields** (boolean) - Optional - Whether specified fields are to be included (true) or excluded (false).
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page. Defaults to 50.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count.
- **from** (string) - Optional - Id from which to start selection.
- **take** (integer) - Optional - Number of results per page. Defaults to 50.

### Request Example
```
GET /v2/groups?per_page=10&include_totals=true
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the group.
- **name** (string) - Name of the group.
- **external_id** (string) - External identifier for the group.
- **created_at** (string) - Timestamp of creation.

#### Response Example
{
  "groups": [
    {
      "id": "grp_1234567890abcdef",
      "name": "Admins",
      "external_id": "ext_001",
      "created_at": "2023-01-01T00:00:00.000Z"
    }
  ],
  "total": 1
}
```

--------------------------------

### GET /v2/forms

Source: https://auth0.com/docs/api/management/v2/forms/get-forms

Retrieves a list of forms. Supports pagination and hydration with additional data.

```APIDOC
## GET /v2/forms

### Description
Retrieves a list of forms. Supports pagination and hydration with additional data.

### Method
GET

### Endpoint
/v2/forms

### Parameters
#### Query Parameters
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page. Defaults to 50.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array of results (false, default).
- **hydrate** (string[]) - Optional - Query parameter to hydrate the response with additional data. Possible values: [`flow_count`, `links`]

### Request Example
```json
{
  "example": ""
}
```

### Response
#### Success Response (200)
- **id** (string) - Required - Form ID. Format: `form-id`. Length: <= 30.
- **name** (string) - Required - Form name. Length: 1 to 150.
- **created_at** (string) - Required - Creation timestamp. Format: `date-time`.
- **updated_at** (string) - Required - Update timestamp. Format: `date-time`.
- **embedded_at** (string) - Optional - Embedding timestamp. Format: `date`.
- **submitted_at** (string) - Optional - Submission timestamp. Format: `date`.
- **start** (number) - Optional
- **limit** (number) - Optional
- **total** (number) - Optional
- **forms** (object[]) - Optional

#### Response Example
```json
{
  "forms": [
    {
      "id": "form-id-123",
      "name": "Example Form",
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T10:00:00Z",
      "embedded_at": "2023-10-27",
      "submitted_at": "2023-10-27"
    }
  ],
  "start": 0,
  "limit": 50,
  "total": 1
}
```

### Error Handling
- **400**: Invalid request query string.
- **400**: Invalid query string paging options.
- **401**: Invalid token.
- **401**: Invalid signature received for JSON Web Token validation.
- **401**: Client is not global.
- **403**: Insufficient scope; expected any of: `read:forms`.
- **429**: Too many requests.
```

--------------------------------

### Install Express and Authentication Dependencies

Source: https://auth0.com/docs/get-started/architecture-scenarios/server-application-api/api-implementation-nodejs

Installs the necessary Node.js modules for building an Express API, including body-parser for request handling and JWT/JWKS libraries for secure authentication.

```bash
npm install express express-jwt jwks-rsa body-parser --save
```

--------------------------------

### GET /v2/emails/provider

Source: https://auth0.com/docs/api/management/v2/emails/get-provider

Retrieves the details of the email provider currently configured in the Auth0 tenant.

```APIDOC
## GET /v2/emails/provider

### Description
Retrieve details of the email provider configuration in your tenant. A list of fields to include or exclude may also be specified.

### Method
GET

### Endpoint
/v2/emails/provider

### Parameters
#### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include or exclude from the result.
- **include_fields** (boolean) - Optional - Whether specified fields are to be included (true) or excluded (false).

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/emails/provider' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **name** (string) - Name of the email provider.
- **enabled** (boolean) - Whether the provider is enabled.
- **default_from_address** (string) - Email address to use as "from" when no other address specified.
- **credentials** (object) - Credentials required to use the provider.
- **settings** (object) - Specific provider settings.

#### Response Example
{
  "name": "smtp",
  "enabled": true,
  "default_from_address": "noreply@example.com",
  "credentials": {
    "smtp_host": "smtp.example.com",
    "smtp_port": 587
  }
}
```

--------------------------------

### Install Auth0 Laravel SDK

Source: https://auth0.com/docs/quickstart/webapp/laravel/interactive

Installs the Auth0 Laravel SDK using Composer. Ensure you are in your project's root directory. This command also updates all dependencies.

```sh
composer require auth0/login:^7.8 --update-with-all-dependencies
```

--------------------------------

### Retrieve Auth0 Client Details (Objective-C)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Shows how to retrieve Auth0 client information using Objective-C with `NSMutableURLRequest` and `NSURLSession`. This example sets up the request and handles the response.

```objectivec
#import <Foundation/Foundation.h>

NSDictionary *headers = @{ @"authorization": @"Bearer {yourMgmtApiAccessToken}" };

NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true"]
                                                         cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                     timeoutInterval:10.0];
[request setHTTPMethod:@"GET"];
[request setAllHTTPHeaderFields:headers];

NSURLSession *session = [NSURLSession sharedSession];
NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
                                              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                  if (error) {
                                                      NSLog(@"%@", error);
                                                  } else {
                                                      NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
                                                      NSLog(@"%@", httpResponse);
                                                  }
                                              }];
[dataTask resume];
```

--------------------------------

### Authorization Code Flow Request Examples

Source: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/call-your-api-using-the-authorization-code-flow

Examples of the Authorization Code Flow request URL and HTML anchor tag implementation. These examples use placeholders for domain, client ID, and other parameters that are dynamically replaced by the AuthCode components.

```http
https://{yourDomain}/authorize?
    response_type=code&
    client_id={yourClientId}&
    redirect_uri={https://yourApp/callback}&
    scope={scope}&
    audience={apiAudience}&
    state={state}
```

```html
<a href="https://{yourDomain}/authorize?
  response_type=code&
  client_id={yourClientId}&
  redirect_uri={https://yourApp/callback}&  
  scope=appointments%20contacts&
  audience=appointments:api&
  state=xyzABC123">
  Sign In
</a>
```

--------------------------------

### Configure Auth0 Middleware in Express.js

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This JavaScript code snippet demonstrates how to configure and apply the Auth0 middleware (`express-openid-connect`) to an Express.js application. It loads environment variables, defines the Auth0 configuration object, and applies the middleware to handle authentication routes.

```javascript
require('dotenv').config();
const express = require('express');
const { auth } = require('express-openid-connect');

const app = express();
const port = process.env.PORT || 3000;

// Auth0 configuration
const config = {
  authRequired: false,      // Allow public routes
  auth0Logout: true,        // Use Auth0 logout endpoint
  secret: process.env.SECRET,
  baseURL: process.env.BASE_URL,
  clientID: process.env.CLIENT_ID,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
};

// Apply the auth middleware
app.use(auth(config));

// Home route - public
app.get('/', (req, res) => {
  res.send(req.oidc.isAuthenticated() ? 'Logged in' : 'Logged out');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

```

--------------------------------

### Example Authorization URL

Source: https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers/active-directory-ldap/ad-ldap-connector/ad-ldap-connector-test-environment

An example URL for OAuth 2.0 authorization code flow, commonly used for integrating with services like Auth0. It includes parameters for response type, scope, client ID, redirect URI, and connection.

```text
https://{yourDomain}/authorize?response_type=token&scope=openid%20profile&client_id={yourClientId}&redirect_uri=http%3A%2F%2Fjwt.io&connection=auth0-test-ad
```

--------------------------------

### Run Flutter App Command

Source: https://auth0.com/docs/quickstart/spa/flutter/interactive

Command to run a Flutter Web application on port 3000. This is a standard command for launching Flutter web projects during development.

```bash
flutter run -d chrome --web-port 3000

```

--------------------------------

### GET /v2/users/{id}/permissions

Source: https://auth0.com/docs/api/management/v2/users/get-permissions

Retrieve all permissions associated with a specific user by their ID.

```APIDOC
## GET /v2/users/{id}/permissions

### Description
Retrieve all permissions associated with the user. Requires the 'read:users' scope.

### Method
GET

### Endpoint
/v2/users/{id}/permissions

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the user to retrieve the permissions for.

#### Query Parameters
- **per_page** (integer) - Optional - Number of results per page.
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array of results (false, default).

### Request Example
```
GET /v2/users/auth0|123456/permissions?include_totals=true
```

### Response
#### Success Response (200)
- **resource_server_identifier** (string) - Resource server (API) identifier that this permission is for.
- **permission_name** (string) - Name of this permission.
- **resource_server_name** (string) - Resource server (API) name this permission is for.
- **description** (string) - Description of this permission.

#### Response Example
{
  "permissions": [
    {
      "resource_server_identifier": "https://api.example.com",
      "permission_name": "read:data",
      "resource_server_name": "Example API",
      "description": "Read access to data"
    }
  ],
  "total": 1
}
```

--------------------------------

### POST /u/signup/password

Source: https://auth0.com/docs/secure/attack-protection/configure-akamai-supplemental-signals

Configures the password-based signup endpoint for Universal Login on Akamai.

```APIDOC
## POST /u/signup/password

### Description
Handles user registration requests specifically requiring password setup within the Universal Login flow.

### Method
POST

### Endpoint
/u/signup/password

### Request Body
- **requestBody** (object) - Required - The payload containing signup and password details.

### Request Example
{
  "requestBody": { "content": { "application/x-www-form-urlencoded": { "schema": { "type": "object" } } } }
}

### Response
#### Success Response (200)
- **status** (string) - Indicates successful processing of the signup request.
```

--------------------------------

### GET /v2/keys/signing

Source: https://auth0.com/docs/api/management/v2/keys/get-signing-keys

Retrieve a list of all application signing keys associated with your Auth0 tenant.

```APIDOC
## GET /v2/keys/signing

### Description
Retrieve details of all the application signing keys associated with your tenant.

### Method
GET

### Endpoint
https://{tenantDomain}/api/v2/keys/signing

### Parameters
#### Scopes
- **read:signing_keys** - Required

### Response
#### Success Response (200)
- **kid** (string) - The key id of the signing key
- **cert** (string) - The public certificate of the signing key
- **pkcs7** (string) - The public certificate of the signing key in pkcs7 format
- **current** (boolean) - True if the key is the current key
- **next** (boolean) - True if the key is the next key
- **previous** (boolean) - True if the key is the previous key
- **current_since** (string/object) - The date and time when the key became the current key
- **current_until** (string/object) - The date and time when the key became the current key
- **fingerprint** (string) - The cert fingerprint
- **thumbprint** (string) - The cert thumbprint
- **revoked** (boolean) - True if the key is revoked
- **revoked_at** (string/object) - The date and time when the key was revoked

#### Response Example
[
  {
    "kid": "key_123",
    "cert": "-----BEGIN CERTIFICATE-----...",
    "current": true,
    "fingerprint": "aa:bb:cc...",
    "thumbprint": "123456...",
    "revoked": false
  }
]
```

--------------------------------

### Install Auth0 SDK via Package Managers

Source: https://auth0.com/docs/quickstart/native/ios-swift/index

Configuration files for integrating the Auth0 SDK into an Apple project using CocoaPods or Carthage dependency managers.

```ruby
platform :ios, '14.0'
use_frameworks!

target 'YourApp' do
  pod 'Auth0', '~> 2.0'
end
```

```bash
pod install
```

```text
github "auth0/Auth0.swift" ~> 2.0
```

```bash
carthage update --platform iOS --use-xcframeworks
```

--------------------------------

### GET /v2/flows/{flow_id}/executions/{execution_id}

Source: https://auth0.com/docs/api/management/v2/flows/get-flows-executions-by-execution-id

Retrieves the details of a specific flow execution by its identifier.

```APIDOC
## GET /v2/flows/{flow_id}/executions/{execution_id}

### Description
Retrieves the details of a specific flow execution. This endpoint requires the `read:flows_executions` scope.

### Method
GET

### Endpoint
/v2/flows/{flow_id}/executions/{execution_id}

### Parameters
#### Path Parameters
- **flow_id** (string) - Required - Flow identifier
- **execution_id** (string) - Required - Flow execution identifier

#### Query Parameters
- **hydrate** (string[]) - Optional - Hydration parameter, e.g., `debug`

### Request Example
```
curl -L -g 'https://{tenantDomain}/api/v2/flows/:flow_id/executions/:execution_id' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - Flow execution identifier
- **trace_id** (string) - Trace id
- **journey_id** (string) - Journey id
- **status** (string) - Execution status
- **debug** (object) - Flow execution debug information
- **created_at** (string) - ISO 8601 creation date
- **updated_at** (string) - ISO 8601 update date
- **started_at** (string) - ISO 8601 start date
- **ended_at** (string) - ISO 8601 end date

#### Response Example
{
  "id": "exec_123",
  "trace_id": "trace_abc",
  "status": "success",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:05Z"
}
```

--------------------------------

### Configuring Auth0Provider and Calling Protected APIs

Source: https://auth0.com/docs/quickstart/spa/react/interactive

Demonstrates how to initialize the Auth0Provider with an API audience and retrieve a silent access token to authorize requests to protected backend endpoints.

```javascript
import { Auth0Provider } from '@auth0/auth0-react';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Auth0Provider
    domain={import.meta.env.VITE_AUTH0_DOMAIN}
    clientId={import.meta.env.VITE_AUTH0_CLIENT_ID}
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "YOUR_API_IDENTIFIER"
    }}
  >
    <App />
  </Auth0Provider>
);
```

```javascript
import { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function ApiCall() {
  const { getAccessTokenSilently } = useAuth0();
  const [apiResponse, setApiResponse] = useState(null);

  const callProtectedApi = async () => {
    try {
      const token = await getAccessTokenSilently();
      
      const response = await fetch('/api/protected', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      setApiResponse(data);
    } catch (error) {
      console.error('API call failed:', error);
    }
  };

  return (
    <div>
      <button onClick={callProtectedApi}>Call API</button>
      {apiResponse && <pre>{JSON.stringify(apiResponse, null, 2)}</pre>}
    </div>
  );
}
```

--------------------------------

### Create/Update User in Auth0 API (Ruby)

Source: https://auth0.com/docs/fr-ca/manage-users/user-accounts/metadata/manage-metadata-api

This Ruby code example demonstrates making a POST request to the Auth0 Management API using the `net/http` library. It sets up the request with the target URL, authorization, content type, and a JSON body representing the user data. SSL verification is disabled for simplicity.

```ruby
require 'uri'
require 'net/http'
require 'openssl'

url = URI("https://{yourDomain}/api/v2/users")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Post.new(url)
request["authorization"] = 'Bearer MGMT_API_ACCESS_TOKEN'
request["content-type"] = 'application/json'
request.body = "{\"email\": \"jane.doe@example.com\", \"user_metadata\": {\"hobby\": \"surfing\"}, \"app_metadata\": {\"plan\": \"full\"}}"

response = http.request(request)
puts response.read_body
```

--------------------------------

### Perform Popup-Based Login (JavaScript)

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Initiates the login process using a popup window for a smoother user experience. It handles potential errors, including the user closing the popup.

```javascript
async function login() {
  try {
    await auth0Client.loginWithPopup();
    await updateUI();
  } catch (err) {
    if (err.error !== 'popup_closed_by_user') {
      showError(err.message);
    }
  }
}
```

--------------------------------

### GET /v2/connections/{id}/keys

Source: https://auth0.com/docs/api/management/v2/connections/get-keys

Retrieves the connection keys for the Okta or OIDC connection strategy.

```APIDOC
## GET /v2/connections/{id}/keys

### Description
Gets the connection keys for the Okta or OIDC connection strategy. Requires the `read:connections_keys` scope.

### Method
GET

### Endpoint
/v2/connections/{id}/keys

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the connection

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/connections/:id/keys' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **kid** (string) - The key id of the signing key
- **cert** (string) - The public certificate of the signing key
- **pkcs** (string) - The public certificate of the signing key in pkcs7 format
- **current** (boolean) - True if the key is the current key
- **next** (boolean) - True if the key is the next key
- **previous** (boolean) - True if the key is the previous key
- **current_since** (string) - The date and time when the key became the current key
- **fingerprint** (string) - The cert fingerprint
- **thumbprint** (string) - The cert thumbprint
- **algorithm** (string) - Signing key algorithm
- **key_use** (string) - Signing key use (encryption or signing)
- **subject_dn** (string) - Subject distinguished name

#### Response Example
{
  "kid": "example-key-id",
  "cert": "-----BEGIN CERTIFICATE-----\\n...\\n-----END CERTIFICATE-----",
  "current": true,
  "fingerprint": "aa:bb:cc:dd",
  "thumbprint": "1234567890"
}
```

--------------------------------

### Using a Custom Session Store for Large Sessions

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

Illustrates how to configure a custom session store, such as Redis, to handle large user session data that might exceed default cookie size limits. This prevents 'Session too large / Cookie errors'.

```javascript
session: {
  store: new RedisStore({ client: redisClient }),
}
```

--------------------------------

### GET /v2/clients/{client_id}/credentials

Source: https://auth0.com/docs/api/management/v2/clients/get-credentials

Retrieves the details of a client credential for a specific Auth0 client.

```APIDOC
## GET /v2/clients/{client_id}/credentials

### Description
Get the details of a client credential. To enable credentials for client authentication or JWT-Secured Authorization, ensure the appropriate properties are set on the client.

### Method
GET

### Endpoint
/v2/clients/{client_id}/credentials

### Parameters
#### Path Parameters
- **client_id** (string) - Required - ID of the client.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/clients/:client_id/credentials' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - ID of the credential.
- **name** (string) - Name given to the credential.
- **kid** (string) - Key identifier.
- **alg** (string) - Algorithm (RS256, RS384, PS256).
- **credential_type** (string) - Type of credential (public_key, cert_subject_dn, x509_cert).
- **subject_dn** (string) - X509 certificate's Subject Distinguished Name.
- **thumbprint_sha256** (string) - X509 certificate's SHA256 thumbprint.
- **created_at** (string) - ISO 8601 creation date.
- **updated_at** (string) - ISO 8601 update date.
- **expires_at** (string) - ISO 8601 expiration date.

#### Response Example
{
  "id": "cred_123",
  "name": "my-credential",
  "kid": "key_abc",
  "alg": "RS256",
  "credential_type": "public_key",
  "created_at": "2023-01-01T00:00:00.000Z"
}
```

--------------------------------

### Run Vite Development Server

Source: https://auth0.com/docs/quickstart/spa/react/interactive

This command starts the Vite development server, allowing you to see your application running locally. If the default port 5173 is in use, you can specify an alternative port like 5174 and update your Auth0 callback URLs accordingly.

```bash
npm run dev
```

```bash
npm run dev -- --port 5174
```

--------------------------------

### Auth0 Authenticator Configuration Example

Source: https://auth0.com/docs/secure/multi-factor-authentication/authenticate-using-ropg-flow-with-mfa/enroll-and-challenge-push-authenticators

This JSON example shows the structure of a list of authenticators configured for an Auth0 user. It includes details such as the authenticator ID, type, active status, and specific properties like oob_channel for push authenticators.

```json
[
    {
        "id": "recovery-code|dev_Ahb2Tb0ujX3w7ilC",
        "authenticator_type": "recovery-code",
        "active": true
    },
    {
        "id": "push|dev_ZUla9SQ6tAIHSz6y",
        "authenticator_type": "oob",
        "active": true,
        "oob_channel": "auth0",
        "name": "user's device name"
    },
    {
        "id": "totp|dev_gJ6Y6vpSrjnKeT67",
        "authenticator_type": "otp",
        "active": true
    }
]
```

--------------------------------

### Generate a secure secret using OpenSSL

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This command generates a cryptographically secure random hexadecimal string of 32 bytes, suitable for use as a secret key for session encryption in the .env file.

```shell
openssl rand -hex 32
```

--------------------------------

### GET /v2/branding/templates/universal-login

Source: https://auth0.com/docs/api/management/v2/branding/get-universal-login

Retrieves the custom page template for the New Universal Login Experience.

```APIDOC
## GET /v2/branding/templates/universal-login

### Description
Retrieves the custom page template for the New Universal Login Experience.

### Method
GET

### Endpoint
/v2/branding/templates/universal-login

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/branding/templates/universal-login' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **body** (string) - The custom page template for the New Universal Login Experience.

#### Response Example
```json
{
  "body": "<html>...</html>"
}
```

#### Error Responses
- **401**: Invalid token or Invalid signature received for JSON Web Token validation.
- **402**: A paid subscription is required for this feature.
- **403**: Insufficient scope; expected: read:branding
- **404**: Template does not exist.
- **429**: Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.
```

--------------------------------

### usePrompt Hook Example

Source: https://auth0.com/docs/libraries/acul/react-sdk/API-Reference/Screens/interstitial-captcha

This example shows the usage of the `usePrompt` hook to access prompt configuration and flow settings within a React component. The hook is imported from '@auth0/auth0-acul-react/login-id'.

```jsx
import { usePrompt } from '@auth0/auth0-acul-react/login-id';
function FlowInfo() {
  const prompt = usePrompt();
}
```

--------------------------------

### Example Usage (JavaScript)

Source: https://auth0.com/docs/secure/tokens/refresh-tokens/disable-refresh-token-rotation

Example of how to configure Auth0 client to disable refresh token rotation.

```APIDOC
## JavaScript Example

### Description
This code snippet demonstrates how to initialize the Auth0 client with refresh token rotation disabled.

### Code
```javascript
const auth0 = await createAuth0Client({
  domain: '{yourDomain}',
  client_id: '{yourClientId}',
  audience: '{yourApiIdentifier}',
  useRefreshTokens: false
});
```
```

--------------------------------

### Parameter Handling

Source: https://auth0.com/docs/api/authentication/reference

Guidelines for passing parameters in GET and POST requests.

```APIDOC
## Parameters

For **GET** requests, parameters not in the path can be passed as a query string:
`GET https://${account.namespace}/some-endpoint?param=value&param=value`

For **POST** requests, parameters not in the URL should be encoded as JSON with `Content-Type: application/json`:
```curl
curl --request POST \
  --url 'https://${account.namespace}/some-endpoint' \
  --header 'content-type: application/json' \
  --data '{
  "param": "value",
  "param": "value"
}'
```

An exception is the SAML IdP-Initiated SSO Flow, which uses both query string parameters and `x-www-form-urlencoded` values.
```

--------------------------------

### Get Authentication Method by ID (cURL)

Source: https://auth0.com/docs/api/management/v2/users/get-authentication-methods-by-authentication-method-id

This cURL command demonstrates how to make a GET request to retrieve a specific authentication method for a user. It includes the necessary endpoint URL, headers, and placeholders for user and authentication method IDs.

```bash
curl -L -g 'https://{tenantDomain}/api/v2/users/:id/authentication-methods/:authentication_method_id' \
-H 'Accept: application/json'
```

--------------------------------

### Import Tenant Configuration using Auth0 Deploy CLI

Source: https://auth0.com/docs/extensions/deploy-cli-tool/install-and-configure-the-deploy-cli-tool

This command imports tenant configuration from a local YAML file into an Auth0 tenant. It requires a configuration file (e.g., config.json) and the input file path. This is essential for deploying configurations to a new or existing tenant.

```bash
a0deploy import --config_file=config.json --input_file local/tenant.yaml
```

--------------------------------

### Instantiate MfaPushWelcome and Enroll

Source: https://auth0.com/docs/libraries/acul/js-sdk/Screens/classes/MfaPushWelcome

Demonstrates how to create an instance of the MfaPushWelcome class and initiate the enrollment process. This is useful for starting the MFA enrollment flow for users.

```typescript
import MfaPushWelcome from '@auth0/auth0-acul-js/mfa-push-welcome';

const mfaPushWelcome = new MfaPushWelcome();
await mfaPushWelcome.enroll();
```

--------------------------------

### Initialize Auth0 AuthenticationController in Java

Source: https://auth0.com/docs/quickstart/webapp/java/interactive

This singleton provider manages the Auth0 AuthenticationController instance. It retrieves configuration parameters from the servlet context and initializes the JwkProvider required for RS256 token validation.

```java
package com.auth0.example;

import com.auth0.AuthenticationController;
import com.auth0.jwk.JwkProvider;
import com.auth0.jwk.JwkProviderBuilder;

import javax.servlet.ServletConfig;
import java.io.UnsupportedEncodingException;

/**
 * Manages a singleton instance of AuthenticationController for the application.
 */
public class AuthenticationControllerProvider {

    private AuthenticationControllerProvider() {}

    private static AuthenticationController INSTANCE;

    public static synchronized AuthenticationController getInstance(ServletConfig config)
            throws UnsupportedEncodingException {
        if (INSTANCE == null) {
            String domain = config.getServletContext().getInitParameter("com.auth0.domain");
            String clientId = config.getServletContext().getInitParameter("com.auth0.clientId");
            String clientSecret = config.getServletContext().getInitParameter("com.auth0.clientSecret");

            if (domain == null || clientId == null || clientSecret == null) {
                throw new IllegalArgumentException(
                    "Missing domain, clientId, or clientSecret. Check your web.xml configuration.");
            }

            // JwkProvider required for RS256 tokens
            JwkProvider jwkProvider = new JwkProviderBuilder(domain).build();
            INSTANCE = AuthenticationController.newBuilder(domain, clientId, clientSecret)
                    .withJwkProvider(jwkProvider)
                    .build();
        }
        return INSTANCE;
    }
}
```

--------------------------------

### Environment Configuration (Manual)

Source: https://auth0.com/docs/quickstart/spa/angular/interactive

Manually sets up the environment configuration for Auth0 in the Angular application. Replace placeholder values with your actual Auth0 domain and client ID.

```typescript
export const environment = {
  production: false,
  auth0: {
    domain: 'YOUR_AUTH0_APP_DOMAIN',
    clientId: 'YOUR_AUTH0_APP_CLIENT_ID'
  }
};
```

--------------------------------

### Initialize Auth0 SDK and Configure Routes (PHP)

Source: https://auth0.com/docs/ja-jp/quickstart/webapp/php/interactive

This snippet shows how to initialize the Auth0 SDK with your domain, client ID, client secret, and redirect URI. It also sets up basic routing for the application using the Steampixel/Route library, defining routes for the home page, login, callback, and logout.

```php
<?php

  declare(strict_types=1);

  require('vendor/autoload.php');

  use Auth0SDKAuth0;
  use Auth0SDKConfigurationSdkConfiguration;

  $configuration = new SdkConfiguration(
    domain: '{yourDomain}',
    clientId: '{yourClientId}',
    clientSecret: '{yourClientSecret}',
    redirectUri: 'http://' . $_SERVER['HTTP_HOST'] . '/callback',
    cookieSecret: '4f60eb5de6b5904ad4b8e31d9193e7ea4a3013b476ddb5c259ee9077c05e1457'
  );

  $sdk = new Auth0($configuration);

  require('router.php');

```

```php
<?php

  declare(strict_types=1);

  use SteampixelRoute;

  if ($_SERVER['HTTP_HOST'] !== 'localhost:3000') {
    die('<p>This quickstart is configured to be run from <a href="http://localhost:3000">http://localhost:3000</a>.</p>');
  }

  Route::add('/', function() use ($sdk) {
    require('profile.php');
  });

  Route::add('/login', function() use ($sdk) {
    require('login.php');
  });

  Route::add('/callback', function() use ($sdk) {
    require('callback.php');
  });

  Route::add('/logout', function() use ($sdk) {
    require('logout.php');
  });

  Route::run();

```

--------------------------------

### GET /v2/roles/{id}

Source: https://auth0.com/docs/api/management/v2/roles/get-roles-by-id

Retrieves the details of a specific role by its ID. Requires 'read:roles' scope.

```APIDOC
## GET /v2/roles/{id}

### Description
Retrieves details about a specific user role specified by ID.

### Method
GET

### Endpoint
/v2/roles/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the role to retrieve.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/roles/:id' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - ID for this role.
- **name** (string) - Name of this role.
- **description** (string) - Description of this role.

#### Response Example
```json
{
  "id": "role_id_string",
  "name": "role_name_string",
  "description": "role_description_string"
}
```

#### Error Responses
- **400**: Invalid request URI or Invalid request body.
- **401**: Invalid token or Invalid signature received for JSON Web Token validation.
- **403**: Insufficient scope; expected: read:roles.
- **404**: Role not found.
- **429**: Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.
```

--------------------------------

### GET /v2/guardian/factors/push-notification/providers/sns

Source: https://auth0.com/docs/api/management/v2/guardian/get-sns

Retrieves the configuration details for an AWS SNS push notification provider enabled for MFA.

```APIDOC
## GET /v2/guardian/factors/push-notification/providers/sns

### Description
Retrieve configuration details for an AWS SNS push notification provider that has been enabled for MFA.

### Method
GET

### Endpoint
/v2/guardian/factors/push-notification/providers/sns

### Scopes
- read:guardian_factors

### Response
#### Success Response (200)
- **aws_access_key_id** (string) - The AWS access key ID.
- **aws_secret_access_key** (string) - The AWS secret access key.
- **aws_region** (string) - The AWS region for the SNS service.
- **sns_apns_platform_application_arn** (string) - The ARN for the APNS platform application.
- **sns_gcm_platform_application_arn** (string) - The ARN for the GCM platform application.

#### Response Example
{
  "aws_access_key_id": "AKIA...",
  "aws_secret_access_key": "secret",
  "aws_region": "us-east-1",
  "sns_apns_platform_application_arn": "arn:aws:sns:...",
  "sns_gcm_platform_application_arn": "arn:aws:sns:..."
}

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/push-notification/providers/sns' \
-H 'Accept: application/json'
```
```

--------------------------------

### Get Push Notification Provider

Source: https://auth0.com/docs/api/management/v2/guardian/get-pn-providers

Retrieves the currently configured push notification provider for your tenant.

```APIDOC
## GET /v2/guardian/factors/push-notification/selected-provider

### Description
Retrieves the push notification provider configured for your tenant. This is useful for understanding the current MFA push notification setup.

### Method
GET

### Endpoint
/v2/guardian/factors/push-notification/selected-provider

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/push-notification/selected-provider' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **provider** (string) - The selected push notification provider. Possible values: `guardian`, `sns`, `direct`.

#### Response Example
```json
{
  "provider": "guardian"
}
```

### Error Handling
- **400**: Invalid input based on schemas.
- **401**: Token has expired or signature is invalid.
- **403**: Insufficient scope (requires `read:guardian_factors`).
```

--------------------------------

### Configure JWT Middleware with DPoP in Go

Source: https://auth0.com/docs/quickstart/backend/golang/interactive

Demonstrates how to initialize the JWT middleware with a validator, DPoP mode, and a logger. This setup ensures secure token handling and observability in Go applications.

```go
jwtmiddleware.WithValidator(jwtValidator),
jwtmiddleware.WithDPoPMode(jwtmiddleware.DPoPRequired),
jwtmiddleware.WithLogger(slog.Default()),
)
```

--------------------------------

### GET /v2/guardian/factors/sms/templates

Source: https://auth0.com/docs/api/management/v2/guardian/get-factor-sms-templates

Retrieves the SMS enrollment and verification templates configured for your tenant. This endpoint is deprecated.

```APIDOC
## GET /v2/guardian/factors/sms/templates

### Description
Retrieves the SMS enrollment and verification templates configured for your tenant. This endpoint is deprecated and has been replaced by the 'Retrieve enrollment and verification phone templates' endpoint.

### Method
GET

### Endpoint
/v2/guardian/factors/sms/templates

### Scopes
read:guardian_factors

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/sms/templates' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **enrollment_message** (string) - Message sent to the user when they are invited to enroll with a phone number.
- **verification_message** (string) - Message sent to the user when they are prompted to verify their account.

#### Success Response (204)
- **enrollment_message** (string) - Message sent to the user when they are invited to enroll with a phone number.
- **verification_message** (string) - Message sent to the user when they are prompted to verify their account.

#### Response Example (200)
```json
{
  "enrollment_message": "Your verification code is {{code}}",
  "verification_message": "Welcome! Your verification code is {{code}}."
}
```

#### Response Example (204)
```json
{
  "enrollment_message": "",
  "verification_message": ""
}
```

#### Error Responses
- **400**: Invalid input based on schemas.
- **401**: Token has expired or signature is invalid.
- **403**: Insufficient scope.
```

--------------------------------

### Example User Profile JSON after Simultaneous Metadata Update

Source: https://auth0.com/docs/manage-users/user-accounts/metadata/manage-metadata-rules

Demonstrates the JSON output for a user profile where both app and user metadata have been updated simultaneously, including roles and font size preferences.

```json
{
  "user_id": "jdoe",
  "email": "john.doe@example.com",
  "app_metadata": {
    "roles": [ "writer", "admin" ]
  },
  "user_metadata": {
    "preferences": {
      "color": "blue",
      "fontSize": 12
    }
  }
}
```

--------------------------------

### GET /v2/guardian/factors/phone/selected-provider

Source: https://auth0.com/docs/api/management/v2/guardian/get-guardian-phone-providers

Retrieves the details of the multi-factor authentication phone provider currently configured for the tenant.

```APIDOC
## GET /v2/guardian/factors/phone/selected-provider

### Description
Retrieve details of the multi-factor authentication phone provider configured for your tenant.

### Method
GET

### Endpoint
/v2/guardian/factors/phone/selected-provider

### Parameters
#### Path Parameters
- None

#### Query Parameters
- None

#### Request Body
- None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/phone/selected-provider' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **provider** (string) - The identifier of the selected phone provider. Possible values: `auth0`, `twilio`, `phone-message-hook`

#### Response Example
{
  "provider": "twilio"
}
```

--------------------------------

### Claim-Based Authorization with express-openid-connect

Source: https://auth0.com/docs/quickstart/webapp/express/interactive

This snippet illustrates how to protect routes based on user claims (e.g., roles, permissions) using helper functions like `claimEquals`, `claimIncludes`, and `claimCheck` provided by the `express-openid-connect` library.

```javascript
const { auth, requiresAuth, claimEquals, claimIncludes, claimCheck } = require('express-openid-connect');

app.use(auth({ authRequired: false }));

// Only users with role = 'admin'
app.get('/admin', claimEquals('role', 'admin'), (req, res) => {
  res.send('Admin dashboard');
});

// Users whose roles array includes 'editor'
app.get('/editor', claimIncludes('roles', 'editor'), (req, res) => {
  res.send('Editor dashboard');
});

// Custom claim check with logic
app.get('/premium', claimCheck((req, claims) => {
  return claims.subscription === 'premium' || claims.role === 'admin';
}), (req, res) => {
  res.send('Premium content');
});
```

--------------------------------

### Make GET Request with Headers in Swift

Source: https://auth0.com/docs/manage-users/organizations/configure-organizations/retrieve-organizations

This Swift code snippet demonstrates how to construct and execute an HTTP GET request using URLSession. It includes setting custom headers and handling the response, including potential errors. The request is configured with a specific timeout interval.

```swift
let request = NSMutableURLRequest(url: URL(string: "https://your.api.endpoint.com/resource")!)
  timeoutInterval: 10.0)
  request.httpMethod = "GET"
  request.allHTTPHeaderFields = headers

  let session = URLSession.shared
  let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
    if (error != nil) {
      print(error)
    } else {
      let httpResponse = response as? HTTPURLResponse
      print(httpResponse)
    }
  })

  dataTask.resume()
```

--------------------------------

### Retrieve Auth0 Client Details (PHP)

Source: https://auth0.com/docs/ja-jp/get-started/applications/confidential-and-public-applications/view-application-ownership

Provides a PHP example using cURL to fetch Auth0 client details. It configures the request options including the URL, method, and authorization header.

```php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://{yourDomain}/api/v2/clients/%7ByourClientId%7D?fields=is_first_party&include_fields=true",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "authorization: Bearer {yourMgmtApiAccessToken}"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

--------------------------------

### Manually Create appsettings.json for Auth0

Source: https://auth0.com/docs/quickstart/webapp/aspnet-core-blazor-server

This snippet provides the content for manually creating an appsettings.json file when automatic setup fails. It outlines the structure required for Auth0 configuration, including placeholders for Domain, ClientId, and ClientSecret. This method is a fallback for users who prefer manual configuration or encounter issues with automated scripts.

```bash
cat > appsettings.json << 'EOF'
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Auth0": {
    "Domain": "your-tenant.auth0.com",
    "ClientId": "YOUR_CLIENT_ID",
    "ClientSecret": "YOUR_CLIENT_SECRET"
  }
}
EOF
```

--------------------------------

### GET /v2/connections/{id}/scim-configuration/tokens

Source: https://auth0.com/docs/api/management/v2/connections/get-scim-tokens

Retrieves all SCIM tokens associated with a specific connection ID.

```APIDOC
## GET /v2/connections/{id}/scim-configuration/tokens

### Description
Retrieves all SCIM tokens by the connection's unique identifier. Requires the `read:scim_token` scope.

### Method
GET

### Endpoint
/v2/connections/{id}/scim-configuration/tokens

### Parameters
#### Path Parameters
- **id** (string) - Required - The id of the connection to retrieve its SCIM configuration.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/connections/{id}/scim-configuration/tokens' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **token_id** (string) - The token's identifier
- **scopes** (string[]) - The scopes of the scim token
- **created_at** (string) - The token's created at timestamp
- **valid_until** (string) - The token's valid until timestamp
- **last_used_at** (string) - The token's last used at timestamp

#### Response Example
[
  {
    "token_id": "scim_12345",
    "scopes": ["read", "write"],
    "created_at": "2023-01-01T00:00:00Z",
    "valid_until": "2024-01-01T00:00:00Z",
    "last_used_at": "2023-12-01T12:00:00Z"
  }
]
```

--------------------------------

### Auth0 Custom Phone Provider Handler Example (JavaScript)

Source: https://auth0.com/docs/customize/phone-messages/unified-phone/use-auth0s-unified-phone-experience-for-multi-factor-authentication

An example of the `onExecuteCustomPhoneProvider` handler function in JavaScript. This function is executed when sending a phone notification and receives event and API objects for customization. It requires the 'undici' package for fetching.

```javascript
const { fetch } = require('undici');
/**
* Handler to be executed while sending a phone notification
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {CustomPhoneProviderAPI} api - Methods and utilities to help change the behavior of sending a phone notification.
*/
exports.onExecuteCustomPhoneProvider = async (event, api) => {


```

--------------------------------

### Perform HTTP GET Request in Swift

Source: https://auth0.com/docs/secure/multi-factor-authentication/authenticate-using-ropg-flow-with-mfa/enroll-and-challenge-otp-authenticators

This Swift code snippet demonstrates how to create and execute an HTTP GET request using URLSession. It includes setting headers and handling the response, including potential errors. The primary dependency is the Foundation framework for URLSession.

```swift
let url = URL(string: "https://YOUR_DOMAIN/api/v2/authenticators")
let headers = [
  "authorization": "Bearer YOUR_API_TOKEN"
]
let request = NSMutableURLRequest(url: url!)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```

--------------------------------

### Example User Profile JSON

Source: https://auth0.com/docs/manage-users/user-accounts/metadata/manage-metadata-rules

Illustrates the JSON structure of a user profile after app and user metadata updates have been applied.

```json
{
  "user_id": "jdoe",
  "email": "john.doe@example.com",
  "app_metadata": {
    "roles": [ "writer", "administrator" ]
  },
  "user_metadata": {
    "preferences": {
      "color": "blue"
    }
  }
}
```

--------------------------------

### GET /v2/branding/phone/templates/{id}

Source: https://auth0.com/docs/api/management/v2/branding/get-phone-template

Retrieves the details of a specific phone notification template by its unique identifier.

```APIDOC
## GET /v2/branding/phone/templates/{id}

### Description
Retrieves a specific phone notification template by its ID. This endpoint requires the `read:phone_templates` scope.

### Method
GET

### Endpoint
/v2/branding/phone/templates/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the phone template.

### Response
#### Success Response (200)
- **id** (string) - Unique identifier of the template.
- **channel** (string) - The communication channel.
- **customizable** (boolean) - Whether the template can be customized.
- **tenant** (string) - The tenant identifier.
- **content** (object) - The template content structure.
  - **syntax** (string) - Template syntax.
  - **from** (string) - Default sender phone number.
  - **body** (object) - Content details.
    - **text** (string) - Text notification content.
    - **voice** (string) - Voice notification content.
- **type** (string) - Template type (e.g., otp_verify, otp_enroll, change_password).
- **disabled** (boolean) - Status of the template.

#### Response Example
{
  "id": "template_123",
  "channel": "sms",
  "customizable": true,
  "tenant": "my-tenant",
  "content": {
    "syntax": "liquid",
    "from": "+1555000111",
    "body": {
      "text": "Your code is {{code}}",
      "voice": "Your code is {{code}}"
    }
  },
  "type": "otp_verify",
  "disabled": false
}
```

--------------------------------

### Initialize MfaBeginEnrollOptions and Enroll MFA Factor (TypeScript)

Source: https://auth0.com/docs/libraries/acul/js-sdk/Screens/classes/MfaBeginEnrollOptions

Demonstrates how to create an instance of MfaBeginEnrollOptions and initiate the MFA enrollment process with a specified action, such as 'push-notification'. This is useful for integrating MFA into your application's authentication flow.

```typescript
import MfaBeginEnrollOptions from '@auth0/auth0-acul-js/mfa-begin-enroll-options';

const mfaBeginEnrollOptions = new MfaBeginEnrollOptions();
await mfaBeginEnrollOptions.enroll({
  action: 'push-notification'
});
```

--------------------------------

### GET /show-possible-types

Source: https://auth0.com/docs/api/management/v2/prompts/patch-bulk-rendering

Lists the available static and dynamic context types that can be injected into the Universal Login page templates.

```APIDOC
## GET /show-possible-types

### Description
Returns a list of supported context types, including static branding settings and dynamic metadata keys for users, clients, and organizations.

### Method
GET

### Endpoint
/show-possible-types

### Parameters
None

### Response
#### Success Response (200)
- **types** (array) - List of supported context keys.

#### Response Example
{
  "types": [
    "branding.settings",
    "client.logo_uri",
    "user.user_metadata.myKey",
    "organization.display_name"
  ]
}
```

--------------------------------

### Apply Modern Auth0 Styling

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Provides a clean, dark-themed CSS structure for the authentication interface using the Inter font family and responsive layout containers.

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  background-color: #1a1e27;
  color: #e2e8f0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 1rem;
}
```

--------------------------------

### POST /signup

Source: https://auth0.com/docs/libraries/auth0js/v7

Registers a new user in a database connection.

```APIDOC
## POST /signup

### Description
Creates a new user account within a specified database connection.

### Method
POST

### Parameters
#### Request Body
- **email** (string) - Required - User's email address.
- **password** (string) - Required - User's desired password.
- **connection** (string) - Required - The database connection name.
- **username** (string) - Optional - Required if 'Requires Username' is enabled.
- **user_metadata** (object) - Optional - Additional attributes for the user.

### Request Example
{
  "connection": "Username-Password-Authentication",
  "email": "user@example.com",
  "password": "secret123",
  "user_metadata": { "plan": "silver" }
}
```

--------------------------------

### Configure Auth0 Client ID and Domain with plist

Source: https://auth0.com/docs/libraries/auth0-swift

Example of an Auth0.plist file used to configure the Auth0.swift SDK with your application's Client ID and Domain. This method is suitable for most applications.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>ClientId</key>
    <string>{yourAuth0ClientId}</string>
    <key>Domain</key>
    <string>{yourAuth0Domain}</string>
</dict>
</plist>
```

--------------------------------

### WS-Fed (WIF) Configuration

Source: https://auth0.com/docs/api/management/v2/clients/patch-clients-by-id

Enable WS-Fed (WIF) addon. Actual configuration is stored in `callback` and `client_aliases` properties on the client.

```APIDOC
## WS-Fed (WIF) Configuration

### Description
Enable WS-Fed (WIF) addon. Actual configuration is stored in `callback` and `client_aliases` properties on the client.

### Method
N/A (Configuration Object)

### Endpoint
N/A

### Parameters
#### Request Body
(No specific fields for enabling WIF, configuration is managed elsewhere)

### Request Example
```json
{
  "wsfed": true
}
```

### Response
#### Success Response (200)
- **message** (string) - Configuration saved successfully.
```

--------------------------------

### UI Component Styling and Animations

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

A collection of CSS classes defining the visual appearance of the authentication interface, including card layouts, button states, and keyframe animations for smooth transitions.

```css
.main-card-wrapper {
  background-color: #262a33;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 3rem;
  max-width: 500px;
  width: 90%;
  animation: fadeInScale 0.8s ease-out forwards;
}

.button {
  padding: 1.1rem 2.8rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

--------------------------------

### Run and Test API via CLI

Source: https://auth0.com/docs/quickstart/backend/python

Commands to start the Flask development server and perform HTTP requests to test public and protected endpoints using cURL.

```bash
# Start the application
python app.py

# Test public endpoint
curl http://localhost:5000/api/public

# Test protected endpoint
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:5000/api/private
```

--------------------------------

### JSON User Profile Examples for Auth0 Account Linking

Source: https://auth0.com/docs/manage-users/user-accounts/user-account-linking

These JSON examples illustrate the structure of user profiles before and after account linking in Auth0. They show the primary account, secondary account, and the resulting linked profile, highlighting how identities and metadata are consolidated.

```json
{
  "email": "your0@email.com",
  "email_verified": true,
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "picture": "https://lh3.googleusercontent..../photo.jpg",
  "gender": "male",
  "locale": "en",
  "user_id": "google-oauth2|115015401343387192604",
  "identities": [
    {
      "provider": "google-oauth2",
      "user_id": "115015401343387192604",
      "connection": "google-oauth2",
      "isSocial": true
    }
  ],
  "user_metadata": {
    "color": "red"
  },
  "app_metadata": {
    "roles": [
      "Admin"
    ]
  },
  ...
}
```

```json
{
  "phone_number": "+14258831929",
  "phone_verified": true,
  "name": "+14258831929",
  "updated_at": "2015-10-08T18:35:18.102Z",
  "user_id": "sms|560ebaeef609ee1adaa7c551",
  "identities": [
    {
      "user_id": "560ebaeef609ee1adaa7c551",
      "provider": "sms",
      "connection": "sms",
      "isSocial": false
    }
  ],
  "user_metadata": {
    "color": "blue"
  },
  "app_metadata": {
    "roles": [
      "AppAdmin"
    ]
  },
  ...
}
```

```json
{
  "email": "your0@email.com",
  "email_verified": true,
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "picture": "https://lh3.googleusercontent..../photo.jpg",
  "gender": "male",
  "locale": "en",
  "user_id": "google-oauth2|115015401343387192604",
  "identities": [
    {
      "provider": "google-oauth2",
      "user_id": "115015401343387192604",
      "connection": "google-oauth2",
      "isSocial": true
    },
    {
      "profileData": {
        "phone_number": "+14258831929",
        "phone_verified": true,
        "name": "+14258831929"
      },
      "user_id": "560ebaeef609ee1adaa7c551",
      "provider": "sms",
      "connection": "sms",
      "isSocial": false
    }
  ],
  "user_metadata": {
    "color": "red"
  },
  "app_metadata": {
    "roles": [
      "Admin"
    ]
  },
  ...
}
```

--------------------------------

### Initialize Auth0 Client

Source: https://auth0.com/docs/libraries/auth0-spa-js

Demonstrates how to create an Auth0Client instance using the recommended createAuth0Client helper or the direct constructor. The helper method automatically handles session refreshing via getTokenSilently.

```javascript
import { createAuth0Client } from '@auth0/auth0-spa-js';

// Async/Await approach
const auth0 = await createAuth0Client({
  domain: '{yourDomain}',
  clientId: '{yourClientId}'
});

// Promise approach
createAuth0Client({
  domain: '{yourDomain}',
  clientId: '{yourClientId}'
}).then(auth0 => {
  //...
});

// Direct constructor approach
import { Auth0Client } from '@auth0/auth0-spa-js';
const auth0Direct = new Auth0Client({
  domain: '{yourDomain}',
  clientId: '{yourClientId}'
});
```

--------------------------------

### GET /api/v2/users

Source: https://auth0.com/docs/manage-users/user-search/retrieve-users-with-get-users-endpoint

Retrieves a list of users based on search criteria. Requires a Management API access token.

```APIDOC
## GET /api/v2/users

### Description
Search for users in your Auth0 tenant. This endpoint requires a Management API access token with appropriate scopes.

### Method
GET

### Endpoint
https://{yourDomain}/api/v2/users

### Parameters
#### Query Parameters
- **q** (string) - Required - The search query (e.g., email:"jane@exampleco.com").
- **search_engine** (string) - Required - The search engine version to use (e.g., v3).

### Request Example
GET https://{yourDomain}/api/v2/users?q=email:"jane@exampleco.com"&search_engine=v3

### Response
#### Success Response (200)
- **users** (array) - A list of user objects matching the search criteria.

#### Response Example
[
  {
    "user_id": "auth0|123456",
    "email": "jane@exampleco.com",
    "name": "Jane Doe"
  }
]
```

--------------------------------

### Render Auth0 Quickstart Card Component

Source: https://auth0.com/docs/ja-jp/quickstarts

A React component that maps item data to a styled card. It handles conditional rendering for logos, badges, and navigation links based on the provided item object structure.

```javascript
export const SectionCard = ({item}) => {
  if (!item) return null;
  const getLink = (item, label) => item.links?.find(l => l.label?.toLowerCase() === label.toLowerCase());
  const github = getLink(item, "github");
  const sample = getLink(item, "sample app");
  const quickstart = getLink(item, "quickstart");
  const docs = getLink(item, "Get started");
  const title = item?.name ?? "";
  const subtext = item?.subtext ?? "";
  const badge = item?.badge ?? "";
  const date = item?.date ?? "";
  const isHttpsLogo = typeof item?.logo === "string" && (/^https:\/\//i).test(item.logo);
  const src = isHttpsLogo ? item.logo : `/docs/images/icons/light/${item?.logo}`;
  const srcDark = isHttpsLogo ? item.logo : `/docs/images/icons/dark/${item?.logo}`;
  const imgClass = "!my-0 w-8 h-8 object-contain shrink-0 " + (isHttpsLogo ? "mint-filter mint-grayscale" : "");
  const tertiary = quickstart || docs;
  const tertiaryLabel = quickstart ? "Quickstart" : docs ? "Get started" : "";
  return <article className="libraries_card mb-[16px] rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow border-gray-200 dark:border-gray-800 dark:bg-black">
      <div className="px-4 md:px-5 pt-4 md:pt-5 pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex gap-3 min-w-0">
            {item?.logo && <>
                <img noZoom src={src} alt={title} className={`${imgClass} mint-block dark:mint-hidden`} />
                <img noZoom src={srcDark} alt={title} className={`${imgClass} mint-hidden dark:mint-block`} />
              </>}
            <div className="min-w-0">
              <h4 className="text-base md:text-lg font-semibold text-gray-900 dark:text-white truncate !m-0 leading-snug">
                {title}
              </h4>
              {!!subtext && <p className="text-xs text-gray-500 dark:text-gray-400 truncate !m-0 leading-tight">{subtext}</p>}
            </div>
          </div>
          <div className="flex flex-col items-end gap-0.5 shrink-0">
            {!!badge && <span className="inline-flex items-center rounded-full px-1.5 py-[0.5px] text-[10px] font-medium border border-emerald-700 text-emerald-700 bg-emerald-200 dark:border-emerald-400 dark:text-emerald-300 dark:bg-emerald-900/30">
                {badge}
              </span>}
            {!!date && <span className="mr-[5px] text-[10px] text-gray-500 dark:text-gray-400">
                on {date.replace(/^on\s+/i, "")}
              </span>}
          </div>
        </div>
      </div>
      <div className="h-px mx-3 bg-gray-200 dark:bg-gray-800" />
      <div className="px-4 md:px-5 py-3">
        <div className="libraries_cards flex items-center justify-between w-full gap-3">
          {github && <a href={github.url} target="_blank" rel="noopener noreferrer" className="no_external_icon inline-flex items-center gap-1.5 text-xs font-medium !text-black dark:!text-white !no-underline !border-0 transition-colors duration-200 hover:!text-neutral-700 dark:hover:!text-neutral-200" style={{borderBottom: "none !important"}}>
              <Icon icon="github" className="w-3 h-3 shrink-0" />
              <span className="leading-none">Github</span>
            </a>}
          {sample && <a href={sample.url} target="_blank" rel="noopener noreferrer" className="no_external_icon inline-flex items-center gap-1.5 text-xs font-medium !text-black dark:!text-white !no-underline !border-0 transition-colors duration-200 hover:!text-neutral-700 dark:hover:!text-neutral-200" style={{borderBottom: "none !important"}}>
              <Icon icon="download" className="w-3 h-3 shrink-0" />
              <span className="leading-none">Sample App</span>
            </a>}
          {tertiary && <a href={tertiary.url} className="no_external_icon inline-flex items-center gap-1.5 text-xs font-medium !text-black dark:!text-white !no-underline !border-0 transition-colors duration-200 hover:!text-neutral-700 dark:hover:!text-neutral-200" style={{borderBottom: "none !important"}}>
              {tertiaryLabel === "Quickstart" ? <Icon icon="play" className="w-3 h-3 shrink-0" /> : <Icon icon="file-lines" className="w-3 h-3 shrink-0" />}
              <span className="leading-none">{tertiaryLabel}</span>
            </a>}
        </div>
      </div>
    </article>;
};
```

--------------------------------

### Configure Auth0 Environment Variables

Source: https://auth0.com/docs/quickstart/spa/vanillajs/interactive

Defines the required environment variables for Auth0 integration. These should be placed in a .env.local file to securely manage your domain and client ID.

```env
VITE_AUTH0_DOMAIN=your-auth0-domain.auth0.com
VITE_AUTH0_CLIENT_ID=your-auth0-client-id
```

--------------------------------

### Configure environment variables and proxy settings

Source: https://auth0.com/docs/quickstart/backend/nodejs/interactive

Provides configuration snippets for environment variables and handling network proxies when the SDK cannot reach the Auth0 authorization server.

```bash
# Correct .env configuration
AUTH0_DOMAIN=dev-abc123.us.auth0.com
AUTH0_AUDIENCE=https://api.example.com
```

```javascript
const { HttpsProxyAgent } = require('https-proxy-agent');

const checkJwt = auth({
  issuerBaseURL: `https://${process.env.AUTH0_DOMAIN}`,
  audience: process.env.AUTH0_AUDIENCE,
  agent: new HttpsProxyAgent(process.env.HTTPS_PROXY),
});
```

--------------------------------

### GET /v2/users/{id}/federated-connections-tokensets

Source: https://auth0.com/docs/api/management/v2/users/get-federated-connections-tokensets

Retrieves a list of active federated connections tokensets for a provided user.

```APIDOC
## GET /v2/users/{id}/federated-connections-tokensets

### Description
Retrieves a list of active federated connections tokensets for a provided user.

### Method
GET

### Endpoint
/v2/users/{id}/federated-connections-tokensets

### Parameters
#### Path Parameters
- **id** (string) - Required - User identifier

#### Query Parameters
None

#### Request Body
None

### Request Example
```json
{
  "example": "No request body"
}
```

### Response
#### Success Response (200)
- **id** (string) - The user's ID.
- **connection** (string) - The name of the federated connection.
- **scope** (string) - The scopes associated with the token.
- **expires_at** (string) - The expiration time of the token (date-time format).
- **issued_at** (string) - The issuance time of the token (date-time format).
- **last_used_at** (string) - The last used time of the token (date-time format).

#### Response Example
```json
{
  "id": "auth0|user123",
  "connection": "google-oauth2",
  "scope": "openid profile email",
  "expires_at": "2023-10-27T10:00:00Z",
  "issued_at": "2023-10-27T09:00:00Z",
  "last_used_at": "2023-10-27T09:30:00Z"
}
```

#### Error Responses
- **401**: Invalid token.
- **401**: Invalid signature received for JSON Web Token validation.
- **401**: Client is not global.
- **403**: Insufficient scope; expected any of: read:federated_connections_tokens.
- **404**: The user does not exist.
- **429**: Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.
```

--------------------------------

### GET /v2/prompts/{prompt}/screen/{screen}/rendering

Source: https://auth0.com/docs/api/management/v2/prompts/get-rendering

Retrieves the rendering settings for a specific screen associated with a prompt.

```APIDOC
## GET /v2/prompts/{prompt}/screen/{screen}/rendering

### Description
Retrieves the current rendering configuration for a specific screen within a prompt, including context values, head tags, and filtering rules.

### Method
GET

### Endpoint
/v2/prompts/{prompt}/screen/{screen}/rendering

### Parameters
#### Path Parameters
- **prompt** (string) - Required - Name of the prompt
- **screen** (string) - Required - Name of the screen

### Request Example
```json
{}
```

### Response
#### Success Response (200)
- **tenant** (string) - Tenant ID
- **prompt** (string) - Name of the prompt
- **screen** (string) - Name of the screen
- **rendering_mode** (string) - Rendering mode (advanced or standard)
- **context_configuration** (array) - Context values to make available
- **default_head_tags_disabled** (boolean) - Override Universal Login default head tags
- **use_page_template** (boolean) - Use page template with ACUL
- **head_tags** (array) - An array of head tags

#### Response Example
```json
{
  "tenant": "my-tenant",
  "prompt": "login",
  "screen": "identifier-first",
  "rendering_mode": "advanced",
  "context_configuration": ["tenant.name"],
  "default_head_tags_disabled": false,
  "use_page_template": true,
  "head_tags": []
}
```
```

--------------------------------

### Connected Accounts Connections List (JSON)

Source: https://auth0.com/docs/secure/tokens/token-vault/connected-accounts-for-token-vault

Example JSON response listing available connected account connections. Each connection object includes its name, strategy, and the scopes granted.

```json
{
  "connections": [
    {
      "name": "google-oauth2",
      "strategy": "google-oauth2",
      "scopes": [
        "email",
        "profile",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/calendar.addons.execute",
        "https://www.googleapis.com/auth/calendar.events.readonly",
        "https://www.googleapis.com/auth/calendar.settings.readonly",
        "openid"
      ]
    },
    {
      "name": "custom",
      "strategy": "oauth2",
      "scopes": [
        "openid"
      ]
    }
  ]
}
```

--------------------------------

### Get Active Users Count

Source: https://auth0.com/docs/api/management/v2/stats/get-active-users

Retrieves the number of active users who have logged in during the last 30 days.

```APIDOC
## GET /v2/stats/active-users

### Description
Retrieve the number of active users that logged in during the last 30 days.

### Method
GET

### Endpoint
/v2/stats/active-users

### Scopes
read:stats

### Response
#### Success Response (200)
- **number** (number) - Number of active users in the last 30 days.

#### Response Example
```json
1500
```

### Error Responses
- **401**: Invalid token.
- **401**: Client is not global.
- **401**: Invalid signature received for JSON Web Token validation.
- **403**: Insufficient scope; expected any of: read:stats.
- **429**: Too many requests. Check the X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset headers.
```

--------------------------------

### Composant React pour la gestion des applications et configurations

Source: https://auth0.com/docs/fr-ca/quickstart/native/wpf-winforms/interactive

Ce composant React gère le chargement, la sauvegarde et la synchronisation des applications et de leurs configurations à l'aide du stockage local et de BroadcastChannel. Il inclut des fonctions utilitaires pour générer des identifiants uniques et charger/sauvegarder des données.

```javascript
export const LoggedInForm = ({sampleApp}) => {
  const LS_APPS_KEY = "auth_demo_apps";
  const LS_APP_CFG_KEY = "auth_demo_app_cfg";
  const CHANNEL = "auth_flows_sync_v1";
  const mkChannel = () => new BroadcastChannel(CHANNEL);
  function uid() {
    return Math.random().toString(36).slice(2) + Date.now().toString(36);
  }
  function loadApps() {
    const raw = localStorage.getItem(LS_APPS_KEY);
    if (raw) return JSON.parse(raw);
    const seeded = [{
      id: "{yourClientId}",
      name: "Default App"
    }];
    localStorage.setItem(LS_APPS_KEY, JSON.stringify(seeded));
    return seeded;
  }
  function saveApps(apps) {
    localStorage.setItem(LS_APPS_KEY, JSON.stringify(apps));
  }
  function loadCfg() {
    const raw = localStorage.getItem(LS_APP_CFG_KEY);
    return raw ? JSON.parse(raw) : {};
  }
  function saveCfg(cfg) {
    localStorage.setItem(LS_APP_CFG_KEY, JSON.stringify(cfg));
  }
  // ... autres fonctions et JSX
  return (
    // JSX pour le composant
    <div></div>
  );
};
```

--------------------------------

### GET /v2/organizations/{id}

Source: https://auth0.com/docs/api/management/v2/organizations/get-organizations-by-id

Retrieves details for a specific organization using its ID. Requires 'read:organizations' or 'read:organizations_summary' scope.

```APIDOC
## GET /v2/organizations/{id}

### Description
Retrieves details about a single Organization specified by ID.

### Method
GET

### Endpoint
/v2/organizations/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the organization to retrieve.

#### Query Parameters
None

#### Request Body
None

### Request Example
```curl
curl -L -g 'https://{tenantDomain}/api/v2/organizations/:id' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - Organization identifier.
- **name** (string) - The name of this organization.
- **display_name** (string) - Friendly name of this organization.
- **branding** (object) - Theme defines how to style the login pages.
  - **logo_url** (string) - URL of logo to display on login page.
  - **colors** (object) - Color scheme used to customize the login pages.
    - **primary** (string) - HEX Color for primary elements.
    - **page_background** (string) - HEX Color for background.
- **metadata** (object) - Metadata associated with the organization.
- **token_quota** (object) - Token quota configuration.
  - **client_credentials** (object) - The token quota configuration.
    - **enforce** (boolean) - If enabled, the quota will be enforced.
    - **per_day** (integer) - Maximum number of issued tokens per day.
    - **per_hour** (integer) - Maximum number of issued tokens per hour.

#### Response Example
```json
{
  "id": "org_abcdef1234567890",
  "name": "Example Org",
  "display_name": "Example Organization",
  "branding": {
    "logo_url": "https://example.com/logo.png",
    "colors": {
      "primary": "#000000",
      "page_background": "#FFFFFF"
    }
  },
  "metadata": {
    "custom_key": "custom_value"
  },
  "token_quota": {
    "client_credentials": {
      "enforce": true,
      "per_day": 1000,
      "per_hour": 100
    }
  }
}
```

#### Error Responses
- **400**: Invalid request query string.
- **401**: Invalid token or signature.
- **403**: Insufficient scope.
- **429**: Too many requests.
```

--------------------------------

### Configure Lock widget behavior with withOptions

Source: https://auth0.com/docs/libraries/lock-ios

Shows how to control the functional behavior of the Lock widget, such as enabling closability, restricting input types to usernames, and filtering visible screens.

```Swift
Lock
  .classic()
  .withOptions {
    $0.closable = true
    $0.usernameStyle = [.Username]
    $0.allow = [.Login, .ResetPassword]
  }
```

--------------------------------

### GET /v2/organizations/{id}/invitations/{invitation_id}

Source: https://auth0.com/docs/api/management/v2/organizations/get-invitations-by-invitation-id

Retrieves details for a specific invitation to an organization. Requires `read:organization_invitations` scope.

```APIDOC
## GET /v2/organizations/{id}/invitations/{invitation_id}

### Description
Retrieves details for a specific invitation to an organization.

### Method
GET

### Endpoint
`/v2/organizations/{id}/invitations/{invitation_id}`

### Parameters
#### Path Parameters
- **id** (string) - Required - Organization identifier.
- **invitation_id** (string) - Required - The id of the user invitation.

#### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include or exclude. Leave empty to retrieve all fields.
- **include_fields** (boolean) - Optional - Whether specified fields are to be included (true) or excluded (false). Defaults to true.

### Request Example
```json
{
  "example": "(No request body for GET request)"
}
```

### Response
#### Success Response (200)
- **id** (string) - The id of the user invitation.
- **organization_id** (string) - Organization identifier.
- **inviter** (object) - Information about the inviter.
  - **name** (string) - The inviter's name.
- **invitee** (object) - Information about the invitee.
  - **email** (string) - The invitee's email.
- **invitation_url** (string) - The invitation url to be send to the invitee.
- **created_at** (string) - The ISO 8601 formatted timestamp representing the creation time of the invitation.
- **expires_at** (string) - The ISO 8601 formatted timestamp representing the expiration time of the invitation.
- **client_id** (string) - Auth0 client ID.
- **connection_id** (string) - The id of the connection to force invitee to authenticate with.
- **app_metadata** (object) - Data related to the user that does affect the application's core functionality.
- **user_metadata** (object) - Data related to the user that does not affect the application's core functionality.
- **roles** (string[]) - List of roles IDs to associated with the user.
- **ticket_id** (string) - The id of the invitation ticket.

#### Response Example
```json
{
  "id": "user-invitation-id",
  "organization_id": "organization-id",
  "inviter": {
    "name": "Inviter Name"
  },
  "invitee": {
    "email": "invitee@example.com"
  },
  "invitation_url": "https://example.com/invite",
  "created_at": "2023-10-27T10:00:00Z",
  "expires_at": "2023-10-27T11:00:00Z",
  "client_id": "client-id",
  "connection_id": "connection-id",
  "app_metadata": {},
  "user_metadata": {},
  "roles": [],
  "ticket_id": "ticket-id"
}
```

### Error Handling
- **400**: Invalid request query string.
- **401**: Client is not global, Invalid signature, or Invalid token.
- **403**: Insufficient scope; expected any of: read:organization_invitations.
- **404**: No organization found or invitation does not exist.
- **429**: Too many requests.
```

--------------------------------

### GET /v2/guardian/enrollments/{id}

Source: https://auth0.com/docs/api/management/v2/guardian/get-enrollments-by-id

Retrieves the details of a specific multi-factor authentication enrollment, including its status, type, and device information.

```APIDOC
## GET /v2/guardian/enrollments/{id}

### Description
Retrieve details, such as status and type, for a specific multi-factor authentication enrollment registered to a user account.

### Method
GET

### Endpoint
/v2/guardian/enrollments/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - ID of the enrollment to be retrieved.

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/enrollments/:id' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **id** (string) - ID for this enrollment.
- **status** (string) - Status of this enrollment (pending or confirmed).
- **name** (string) - Device name (only for push notification).
- **identifier** (string) - Device identifier.
- **phone_number** (string) - Phone number.
- **enrolled_at** (string) - Enrollment date and time.
- **last_auth** (string) - Last authentication date and time.

#### Response Example
{
  "id": "enrollment_123",
  "status": "confirmed",
  "name": "My iPhone",
  "identifier": "device_id_abc",
  "phone_number": "+15550101",
  "enrolled_at": "2023-01-01T00:00:00Z",
  "last_auth": "2023-01-02T12:00:00Z"
}
```

--------------------------------

### GET /v2/groups/{id}

Source: https://auth0.com/docs/api/management/v2/groups/get-group

Retrieves a group's metadata by its unique identifier. The member list is available via a separate endpoint.

```APIDOC
## GET /v2/groups/{id}

### Description
Retrieves a group's metadata by its unique identifier. The member list is available via a separate endpoint.

### Method
GET

### Endpoint
/v2/groups/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - Unique identifier for the group (service-generated).

#### Query Parameters
None

#### Request Body
None

### Request Example
None

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the group (service-generated).
- **name** (string) - Name of the group. Must be unique within its scope (connection, organization, or tenant). Must contain between 1 and 128 printable ASCII characters.
- **external_id** (string) - External identifier for the group, often used for SCIM synchronization. Max length of 256 characters.
- **connection_id** (string) - Identifier for the connection this group belongs to (if a connection group).
- **organization_id** (string) - Identifier for the organization this group belongs to (if an organization group).
- **tenant_name** (string) - Identifier for the tenant this group belongs to.
- **description** (string) - Description of the group. Max length of 512 characters.
- **created_at** (string) - Timestamp of when the group was created.
- **updated_at** (string) - Timestamp of when the group was last updated.

#### Response Example
```json
{
  "id": "gid:xxxxxxxxxxxxxxxxxxxxxxxx",
  "name": "Example Group",
  "external_id": "ext:12345",
  "connection_id": "cid:yyyyyyyyyyyyyyyyyyyyyyyy",
  "organization_id": "oid:zzzzzzzzzzzzzzzzzzzzzzzz",
  "tenant_name": "my-tenant",
  "description": "This is an example group.",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

#### Error Responses
- **400** - Invalid request query string.
- **401** - Invalid token or insufficient permissions.
- **403** - Insufficient scope; expected 'read:groups'.
- **404** - The group does not exist.
- **429** - Too many requests.
```

--------------------------------

### POST /api/v2/connections (Create Connection with Values)

Source: https://auth0.com/docs/connections/enterprise/saml

Creates a SAML connection by providing specific configuration values.

```APIDOC
## POST /api/v2/connections (Create Connection with Values)

### Description
Creates a SAML connection by providing specific configuration values such as sign-in URL, sign-out URL, and signing certificate.

### Method
POST

### Endpoint
`https://{yourDomain}/api/v2/connections`

### Parameters
#### Request Body
- **strategy** (string) - Required - The authentication strategy, should be 'samlp' for SAML connections.
- **name** (string) - Required - The name of the connection to be created.
- **options** (object) - Required - An object containing the connection's options.
  - **signInEndpoint** (string) - Required - The SAML single sign-on URL for the connection.
  - **signOutEndpoint** (string) - Required - The SAML single sign-out URL for the connection.
  - **signatureAlgorithm** (string) - Optional - The signature algorithm to use (e.g., 'rsa-sha256'). Defaults to 'rsa-sha256'.
  - **digestAlgorithm** (string) - Optional - The digest algorithm to use (e.g., 'sha256'). Defaults to 'sha256'.
  - **fieldsMap** (object) - Optional - A mapping for custom fields.
  - **signingCert** (string) - Required - The Base64-encoded X.509 signing certificate (PEM or CER format).

### Request Example
```json
{
  "strategy": "samlp",
  "name": "CONNECTION_NAME",
  "options": {
    "signInEndpoint": "SIGN_IN_ENDPOINT_URL",
    "signOutEndpoint": "SIGN_OUT_ENDPOINT_URL",
    "signatureAlgorithm": "rsa-sha256",
    "digestAlgorithm": "sha256",
    "fieldsMap": {},
    "signingCert": "BASE64_SIGNING_CERT"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - The unique identifier for the created connection.
- **strategy** (string) - The authentication strategy used.
- **name** (string) - The name of the connection.
- **options** (object) - The configuration options for the connection.

#### Response Example
```json
{
  "id": "con_abcdef1234567890",
  "strategy": "samlp",
  "name": "MySAMLConnection",
  "options": {
    "signInEndpoint": "https://idp.example.com/sso",
    "signOutEndpoint": "https://idp.example.com/slo",
    "signatureAlgorithm": "rsa-sha256",
    "digestAlgorithm": "sha256",
    "fieldsMap": {},
    "signingCert": "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----"
  }
}
```
```

--------------------------------

### Initialization Configuration

Source: https://auth0.com/docs/libraries/auth0js

Configuration parameters for the WebAuth instance instantiation.

```APIDOC
## Initialization Configuration

### Description
Defines the configuration object required when instantiating the `webAuth` client for Auth0 authentication flows.

### Parameters
#### Request Body
- **domain** (String) - Required - Your Auth0 account domain (ex. myaccount.auth0.com)
- **clientID** (String) - Required - Your Auth0 client ID
- **redirectUri** (String) - Optional - The default redirect URI used for authentication callbacks.
- **scope** (String) - Optional - The default scope(s) used by the application.
- **audience** (String) - Optional - The default audience to be used for requesting API access.
- **responseType** (String) - Optional - The default response type (code, token, id_token).
- **responseMode** (String) - Optional - The mode used to send the token or code (query, fragment, form_post).

### Request Example
{
  "domain": "myaccount.auth0.com",
  "clientID": "your_client_id",
  "redirectUri": "https://myapp.com/callback",
  "responseType": "code"
}
```

--------------------------------

### GET /v2/guardian/factors/push-notification/providers/apns

Source: https://auth0.com/docs/api/management/v2/guardian/get-apns

Retrieve the configuration details for the APNS push notification provider associated with the tenant.

```APIDOC
## GET /v2/guardian/factors/push-notification/providers/apns

### Description
Retrieve configuration details for the multi-factor authentication APNS provider associated with your tenant.

### Method
GET

### Endpoint
/v2/guardian/factors/push-notification/providers/apns

### Parameters
#### Path Parameters
- None

#### Query Parameters
- None

#### Request Body
- None

### Request Example
```bash
curl -L -g 'https://{tenantDomain}/api/v2/guardian/factors/push-notification/providers/apns' \
-H 'Accept: application/json'
```

### Response
#### Success Response (200)
- **bundle_id** (string) - The bundle ID for the APNS provider (1-20 characters).
- **sandbox** (boolean) - Indicates if the sandbox environment is enabled.
- **enabled** (boolean) - Indicates if the provider is enabled.

#### Response Example
{
  "bundle_id": "com.example.app",
  "sandbox": false,
  "enabled": true
}
```

--------------------------------

### GET /v2/flows/{flow_id}/executions

Source: https://auth0.com/docs/api/management/v2/flows/get-flows-executions

Retrieves a list of executions for a specific flow, supporting filtering and pagination options.

```APIDOC
## GET /v2/flows/{flow_id}/executions

### Description
Retrieves a list of flow executions for the specified flow ID. This endpoint supports pagination and can return results either as a direct array or as an object containing total result counts.

### Method
GET

### Endpoint
/v2/flows/{flow_id}/executions

### Parameters
#### Path Parameters
- **flow_id** (string) - Required - The unique identifier of the flow.

#### Query Parameters
- **page** (integer) - Optional - Page index of the results to return. First page is 0.
- **per_page** (integer) - Optional - Number of results per page. Defaults to 50.
- **include_totals** (boolean) - Optional - Return results inside an object that contains the total result count (true) or as a direct array (false, default).
- **from** (string) - Optional - Id from which to start selection.
- **take** (integer) - Optional - Number of results per page. Defaults to 50.

### Request Example
```
GET /v2/flows/my-flow-123/executions?page=0&per_page=10
```

### Response
#### Success Response (200)
- **id** (string) - Flow execution identifier.
- **trace_id** (string) - Trace id.
- **status** (string) - Execution status.
- **created_at** (string) - ISO 8601 date when created.
- **updated_at** (string) - ISO 8601 date when updated.

#### Response Example
{
  "id": "exec_12345",
  "trace_id": "trace_abc",
  "status": "success",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

--------------------------------

### GET /v2/flows/vault/connections/{id}

Source: https://auth0.com/docs/api/management/v2/flows/get-flows-vault-connections-by-id

Retrieves the details of a specific Flows Vault connection by its unique identifier.

```APIDOC
## GET /v2/flows/vault/connections/{id}

### Description
Retrieves the details of a specific Flows Vault connection by its unique identifier. Requires the `read:flows_vault_connections` scope.

### Method
GET

### Endpoint
/v2/flows/vault/connections/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - Flows Vault connection ID

### Response
#### Success Response (200)
- **id** (string) - Flows Vault Connection identifier
- **app_id** (string) - Flows Vault Connection app identifier
- **environment** (string) - Flows Vault Connection environment
- **name** (string) - Flows Vault Connection name
- **account_name** (string) - Flows Vault Connection custom account name
- **ready** (boolean) - Whether the Flows Vault Connection is configured
- **created_at** (string) - ISO 8601 date when created
- **updated_at** (string) - ISO 8601 date when updated
- **refreshed_at** (string) - ISO 8601 date when refreshed
- **fingerprint** (string) - Connection fingerprint

#### Response Example
{
  "id": "conn_12345",
  "app_id": "app_abc",
  "name": "My Connection",
  "ready": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "fingerprint": "abc-123"
}
```

--------------------------------

### Email Verification Output Example (JSON)

Source: https://auth0.com/docs/customize/forms/flows/integrations/data-verification

Examples of the JSON output object for email verification. The 'valid' property indicates if the email meets the criteria, and 'cause' provides a reason if validation fails.

```json
{
  "valid": false,
  "cause": "FREE_EMAIL"
}
```

```json
{
  "valid": true,
  "cause": null
}
```

--------------------------------

### GET /v2/branding/phone/templates

Source: https://auth0.com/docs/api/management/v2/branding/get-phone-templates

Retrieves a list of all phone notification templates. You can filter the results to include only disabled templates.

```APIDOC
## GET /v2/branding/phone/templates

### Description
Retrieves a list of all phone notification templates. You can filter the results to include only disabled templates.

### Method
GET

### Endpoint
/v2/branding/phone/templates

### Parameters
#### Query Parameters
- **disabled** (boolean) - Optional - Whether the template is enabled (false) or disabled (true).

### Request Example
```json
{
  "example": "GET /v2/branding/phone/templates?disabled=true"
}
```

### Response
#### Success Response (200)
- **templates** (object[]) - An array of phone notification template objects.
  - **id** (string) - Required - Unique identifier for the template.
  - **channel** (string) - The communication channel for the template.
  - **customizable** (boolean) - Indicates if the template is customizable.
  - **tenant** (string) - The tenant associated with the template.
  - **content** (object) - Required - The content of the notification template.
    - **syntax** (string) - The syntax used for the template content.
    - **from** (string) - Default phone number to be used as 'from' when sending a phone notification.
    - **body** (object) - The body of the notification.
      - **text** (string) - Content of the phone template for text notifications.
      - **voice** (string) - Content of the phone template for voice notifications.
    - **type** (string) - Required - The type of notification (e.g., 'otp_verify', 'change_password'). Possible values: [`otp_verify`, `otp_enroll`, `change_password`, `blocked_account`, `password_breach`].
    - **disabled** (boolean) - Required - Whether the template is enabled (false) or disabled (true).

#### Response Example
```json
{
  "example": {
    "templates": [
      {
        "id": "template_123",
        "channel": "sms",
        "customizable": true,
        "tenant": "my-tenant",
        "content": {
          "syntax": "plain",
          "from": "+15551234567",
          "body": {
            "text": "Your verification code is {{otp_code}}"
          },
          "type": "otp_verify",
          "disabled": false
        }
      }
    ]
  }
}
```

#### Error Responses
- **400**: Invalid request URI.
- **401**: Invalid token or insufficient permissions.
- **403**: Insufficient scope.
- **429**: Too many requests.
```

--------------------------------

### Build and Run Application with WildFly Maven Plugin (Command Line)

Source: https://auth0.com/docs/quickstart/webapp/java-ee/interactive

This command builds and runs the Java EE application using the WildFly Maven plugin. It cleans the project, compiles the code, and deploys it to a running WildFly instance. Ensure you have Maven and WildFly installed and configured. The output will indicate the URL where the application is accessible.

```bash
mvn clean wildfly:run
```

--------------------------------

### Configure WhatsApp Connection with Token

Source: https://auth0.com/docs/api/management/v2/flows/post-flows-vault-connections

This JSON structure defines how to set up a WhatsApp connection using a token. It includes the connection name, 'WHATSAPP' app ID, and a setup object specifying the token type and the token itself.

```json
{
  "name": "string",
  "app_id": "WHATSAPP",
  "setup": {
    "type": "TOKEN",
    "token": "string"
  }
}
```

--------------------------------

### Create Component Directories (Shell)

Source: https://auth0.com/docs/quickstart/webapp/nuxt

Creates the necessary directory structure for application components using the `mkdir` command. This ensures that the component files have a place to reside within the project.

```shell
mkdir -p app/components && touch app/components/LoginButton.vue && touch app/components/LogoutButton.vue && touch app/components/UserProfile.vue
```