/**
 * Biometric Authentication Integration
 * WebAuthn + Fingerprint/Face ID support
 * WINNING FEATURE: Most hackathons don't have this!
 */

import { useState, useEffect } from 'react';

export interface BiometricCredential {
  id: string;
  publicKey: ArrayBuffer;
  type: 'fingerprint' | 'face' | 'voice';
  deviceInfo: DeviceInfo;
}

export interface DeviceInfo {
  platform: string;
  userAgent: string;
  screenResolution: string;
  timezone: string;
  language: string;
  fingerprint: string;
}

export interface BiometricAuthResult {
  success: boolean;
  credential?: BiometricCredential;
  fallbackRequired?: boolean;
  error?: string;
}

class BiometricAuthManager {
  private isSupported: boolean = false;

  constructor() {
    this.checkSupport();
  }

  private checkSupport(): void {
    this.isSupported = !!(
      window.PublicKeyCredential &&
      window.navigator.credentials &&
      window.navigator.credentials.create
    );
  }

  /**
   * Check if biometric authentication is available
   */
  isAvailable(): boolean {
    return this.isSupported && this.hasRegisteredCredentials();
  }

  /**
   * Register biometric credential (fingerprint/face)
   */
  async registerBiometric(userId: string): Promise<BiometricAuthResult> {
    if (!this.isSupported) {
      return {
        success: false,
        fallbackRequired: true,
        error: 'Biometric authentication not supported on this device'
      };
    }

    try {
      const challenge = await this.generateChallenge();
      const deviceInfo = this.getDeviceFingerprint();

      const credential = await navigator.credentials.create({
        publicKey: {
          challenge: new TextEncoder().encode(challenge),
          rp: {
            name: "CipherMate AI Assistant",
            id: window.location.hostname,
          },
          user: {
            id: new TextEncoder().encode(userId),
            name: userId,
            displayName: "CipherMate User",
          },
          pubKeyCredParams: [
            { alg: -7, type: "public-key" }, // ES256
            { alg: -257, type: "public-key" }, // RS256
          ],
          authenticatorSelection: {
            authenticatorAttachment: "platform", // Built-in authenticators
            userVerification: "required",
            residentKey: "preferred"
          },
          timeout: 60000,
          attestation: "direct"
        }
      }) as PublicKeyCredential;

      if (credential) {
        const biometricCred: BiometricCredential = {
          id: credential.id,
          publicKey: (credential.response as AuthenticatorAttestationResponse).getPublicKey()!,
          type: this.detectBiometricType(),
          deviceInfo
        };

        // Store credential securely
        await this.storeCredential(biometricCred);

        return {
          success: true,
          credential: biometricCred
        };
      }

      throw new Error('Failed to create credential');

    } catch (error) {
      console.error('Biometric registration failed:', error);
      return {
        success: false,
        fallbackRequired: true,
        error: error instanceof Error ? error.message : 'Registration failed'
      };
    }
  }

  /**
   * Authenticate using biometric (fingerprint/face)
   */
  async authenticateWithBiometric(): Promise<BiometricAuthResult> {
    if (!this.isSupported || !this.hasRegisteredCredentials()) {
      return {
        success: false,
        fallbackRequired: true,
        error: 'No biometric credentials registered'
      };
    }

    try {
      const challenge = await this.generateChallenge();
      const credentialIds = this.getStoredCredentialIds();

      const assertion = await navigator.credentials.get({
        publicKey: {
          challenge: new TextEncoder().encode(challenge),
          allowCredentials: credentialIds.map(id => ({
            id: new TextEncoder().encode(id),
            type: "public-key"
          })),
          userVerification: "required",
          timeout: 60000
        }
      }) as PublicKeyCredential;

      if (assertion) {
        // Verify the assertion with backend
        const isValid = await this.verifyAssertion(assertion, challenge);
        
        if (isValid) {
          // Log successful biometric authentication
          await this.logBiometricAuth('success');
          
          return {
            success: true,
            credential: await this.getCredentialById(assertion.id)
          };
        }
      }

      throw new Error('Authentication failed');

    } catch (error) {
      console.error('Biometric authentication failed:', error);
      await this.logBiometricAuth('failed', error instanceof Error ? error.message : 'Unknown error');
      
      return {
        success: false,
        fallbackRequired: true,
        error: error instanceof Error ? error.message : 'Authentication failed'
      };
    }
  }

  /**
   * Generate device fingerprint for security
   */
  private getDeviceFingerprint(): DeviceInfo {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx!.textBaseline = 'top';
    ctx!.font = '14px Arial';
    ctx!.fillText('Device fingerprint', 2, 2);
    
    const fingerprint = [
      navigator.userAgent,
      navigator.language,
      screen.width + 'x' + screen.height,
      new Date().getTimezoneOffset(),
      navigator.hardwareConcurrency,
      canvas.toDataURL()
    ].join('|');

    return {
      platform: navigator.platform,
      userAgent: navigator.userAgent,
      screenResolution: `${screen.width}x${screen.height}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      language: navigator.language,
      fingerprint: btoa(fingerprint).slice(0, 32)
    };
  }

  /**
   * Detect biometric type based on authenticator
   */
  private detectBiometricType(): 'fingerprint' | 'face' | 'voice' {
    // Simple heuristic - in real implementation, use authenticator info
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
      return 'face'; // Face ID likely
    } else if (userAgent.includes('android')) {
      return 'fingerprint'; // Fingerprint likely
    }
    
    return 'fingerprint'; // Default
  }

  /**
   * Generate cryptographic challenge
   */
  private async generateChallenge(): Promise<string> {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return btoa(String.fromCharCode(...array));
  }

  /**
   * Store credential securely in IndexedDB
   */
  private async storeCredential(credential: BiometricCredential): Promise<void> {
    const db = await this.openDB();
    const transaction = db.transaction(['credentials'], 'readwrite');
    const store = transaction.objectStore('credentials');
    
    await store.put({
      id: credential.id,
      credential: credential,
      timestamp: Date.now()
    });
  }

  /**
   * Check if user has registered credentials
   */
  public hasRegisteredCredentials(): boolean {
    return localStorage.getItem('biometric_registered') === 'true';
  }

  /**
   * Get stored credential IDs
   */
  public getStoredCredentialIds(): string[] {
    const stored = localStorage.getItem('biometric_credential_ids');
    return stored ? JSON.parse(stored) : [];
  }

  /**
   * Get credential by ID
   */
  private async getCredentialById(id: string): Promise<BiometricCredential | undefined> {
    const db = await this.openDB();
    const transaction = db.transaction(['credentials'], 'readonly');
    const store = transaction.objectStore('credentials');
    const result = await store.get(id) as unknown as { id: string; credential: BiometricCredential; timestamp: number } | undefined;

    return result?.credential;
  }

  /**
   * Verify assertion with backend
   */
  private async verifyAssertion(assertion: PublicKeyCredential, challenge: string): Promise<boolean> {
    try {
      const response = await fetch('/api/auth/verify-biometric', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentialId: assertion.id,
          challenge: challenge,
          signature: Array.from(new Uint8Array((assertion.response as AuthenticatorAssertionResponse).signature)),
          authenticatorData: Array.from(new Uint8Array((assertion.response as AuthenticatorAssertionResponse).authenticatorData)),
          clientDataJSON: Array.from(new Uint8Array(assertion.response.clientDataJSON))
        })
      });

      return response.ok;
    } catch (error) {
      console.error('Biometric verification failed:', error);
      return false;
    }
  }

  /**
   * Log biometric authentication events
   */
  private async logBiometricAuth(status: 'success' | 'failed', error?: string): Promise<void> {
    try {
      await fetch('/api/auth/log-biometric', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status,
          error,
          timestamp: new Date().toISOString(),
          deviceInfo: this.getDeviceFingerprint()
        })
      });
    } catch (err) {
      console.error('Failed to log biometric auth:', err);
    }
  }

  /**
   * Open IndexedDB for credential storage
   */
  private async openDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('BiometricCredentials', 1);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains('credentials')) {
          db.createObjectStore('credentials', { keyPath: 'id' });
        }
      };
    });
  }

  /**
   * Remove all biometric credentials (logout/reset)
   */
  async clearCredentials(): Promise<void> {
    try {
      const db = await this.openDB();
      const transaction = db.transaction(['credentials'], 'readwrite');
      const store = transaction.objectStore('credentials');
      await store.clear();
      
      localStorage.removeItem('biometric_registered');
      localStorage.removeItem('biometric_credential_ids');
    } catch (error) {
      console.error('Failed to clear biometric credentials:', error);
    }
  }
}

// Export singleton instance
export const biometricAuth = new BiometricAuthManager();

// React hook for biometric authentication
export function useBiometricAuth() {
  const [isAvailable, setIsAvailable] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(false);

  useEffect(() => {
    setIsAvailable(biometricAuth.isAvailable());
    setIsRegistered(biometricAuth.hasRegisteredCredentials());
  }, []);

  const register = async (userId: string) => {
    const result = await biometricAuth.registerBiometric(userId);
    if (result.success) {
      setIsRegistered(true);
    }
    return result;
  };

  const authenticate = async () => {
    setIsAuthenticating(true);
    try {
      const result = await biometricAuth.authenticateWithBiometric();
      return result;
    } finally {
      setIsAuthenticating(false);
    }
  };

  const clear = async () => {
    await biometricAuth.clearCredentials();
    setIsRegistered(false);
  };

  return {
    isAvailable,
    isRegistered,
    isAuthenticating,
    register,
    authenticate,
    clear
  };
}