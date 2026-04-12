
// Mock for @auth0/nextjs-auth0
const React = require('react');

const mockUseUser = jest.fn(() => ({
  user: null,
  error: null,
  isLoading: false,
}));

const mockUserProvider = ({ children }) => {
  return React.createElement('div', { 'data-testid': 'mock-user-provider' }, children);
};

const mockAuth0Provider = ({ children }) => {
  return React.createElement('div', { 'data-testid': 'mock-auth0-provider' }, children);
};

module.exports = {
  useUser: mockUseUser,
  UserProvider: mockUserProvider,
  Auth0Provider: mockAuth0Provider,
};