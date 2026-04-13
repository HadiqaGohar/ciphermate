
The log entry indicates a 500 Internal Server Error occurred during a POST request to /api/v1/auth/google/exchange-token . This error often points to a problem with the application's authentication process when trying to exchange a Google token.

This could be due to several reasons, including:

Incorrect redirect_uri configuration: The redirect_uri configured in your Google API project and the one used in your application might not match, causing the Google token endpoint to reject the request.
Invalid client credentials: There might be an issue with the client ID or client secret used by your application to authenticate with Google.
Network or connectivity issues: Although less likely for this specific error message, transient network problems between your Cloud Run service and Google's authentication servers could interfere.
To validate the root cause:

Check redirect_uri configuration: Verify that the redirect_uri registered in your Google Cloud Project's OAuth 2.0 client ID matches exactly the redirect_uri your application is using in the /api/v1/auth/google/exchange-token request. Any mismatch, even a trailing slash, can cause this error.
Inspect application logs for Google token exchange details: Look for more detailed error messages within your application logs (specifically, logs originating from the code that attempts to exchange the Google token) around the time of this error. These logs might provide a more specific reason for the redirect_uri_mismatch or other authentication failures.