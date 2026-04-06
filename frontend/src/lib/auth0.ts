// Mock auth0 for hackathon
export const auth0 = {
  getSession: () => Promise.resolve({
    user: {
      sub: 'mock-user-123',
      email: 'test@example.com',
      name: 'Test User'
    }
  })
};
