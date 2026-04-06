import { getAccessToken } from '@auth0/nextjs-auth0';

export interface TokenVaultService {
  storeToken(service: string, token: string, scopes: string[]): Promise<void>;
  retrieveToken(service: string): Promise<string | null>;
  revokeToken(service: string): Promise<void>;
  listTokens(): Promise<Array<{ service: string; scopes: string[]; createdAt: string }>>;
}

class Auth0TokenVaultService implements TokenVaultService {
  private async getManagementToken(): Promise<string> {
    try {
      const accessToken = await getAccessToken();
      return accessToken as string;
    } catch (error) {
      console.error('Failed to get management token:', error);
      throw new Error('Unable to access Token Vault');
    }
  }

  async storeToken(service: string, token: string, scopes: string[]): Promise<void> {
    const managementToken = await this.getManagementToken();
    
    const response = await fetch('/api/token-vault/store', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${managementToken}`,
      },
      body: JSON.stringify({
        service,
        token,
        scopes,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to store token: ${response.statusText}`);
    }
  }

  async retrieveToken(service: string): Promise<string | null> {
    const managementToken = await this.getManagementToken();
    
    const response = await fetch(`/api/token-vault/retrieve/${service}`, {
      headers: {
        'Authorization': `Bearer ${managementToken}`,
      },
    });

    if (response.status === 404) {
      return null;
    }

    if (!response.ok) {
      throw new Error(`Failed to retrieve token: ${response.statusText}`);
    }

    const data = await response.json();
    return data.token;
  }

  async revokeToken(service: string): Promise<void> {
    const managementToken = await this.getManagementToken();
    
    const response = await fetch(`/api/token-vault/revoke/${service}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${managementToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to revoke token: ${response.statusText}`);
    }
  }

  async listTokens(): Promise<Array<{ service: string; scopes: string[]; createdAt: string }>> {
    const managementToken = await this.getManagementToken();
    
    const response = await fetch('/api/token-vault/list', {
      headers: {
        'Authorization': `Bearer ${managementToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to list tokens: ${response.statusText}`);
    }

    return response.json();
  }
}

export const tokenVaultService = new Auth0TokenVaultService();