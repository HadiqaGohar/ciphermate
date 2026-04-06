// Mock for @auth0/nextjs-auth0/client
const React = require('react');

const mockUseUser = jest.fn(() => ({
  user: null,
  error: null,
  isLoading: false,
}));

const mockUserProvider = ({ children }) => {
  return React.createElement('div', { 'data-testid': 'mock-user-provider' }, children);
};

module.exports = {
  useUser: mockUseUser,
  UserProvider: mockUserProvider,
};