// Mock for lucide-react icons
import React from 'react';

// Create a generic mock component for all icons
const MockIcon = ({ className, size, ...props }) => (
  React.createElement('svg', {
    className,
    width: size || 24,
    height: size || 24,
    'data-testid': 'mock-icon',
    ...props
  })
);

// Export commonly used icons
export const AlertCircle = MockIcon;
export const CheckCircle = MockIcon;
export const XCircle = MockIcon;
export const Info = MockIcon;
export const Send = MockIcon;
export const Loader = MockIcon;
export const User = MockIcon;
export const Calendar = MockIcon;
export const Mail = MockIcon;
export const Github = MockIcon;
export const MessageSquare = MockIcon;
export const Shield = MockIcon;
export const Key = MockIcon;
export const Settings = MockIcon;
export const Eye = MockIcon;
export const EyeOff = MockIcon;
export const Trash = MockIcon;
export const Edit = MockIcon;
export const Plus = MockIcon;
export const Minus = MockIcon;
export const ChevronDown = MockIcon;
export const ChevronUp = MockIcon;
export const ChevronLeft = MockIcon;
export const ChevronRight = MockIcon;
export const Download = MockIcon;
export const Upload = MockIcon;
export const Refresh = MockIcon;
export const Search = MockIcon;
export const Filter = MockIcon;
export const Clock = MockIcon;
export const Globe = MockIcon;
export const Lock = MockIcon;
export const Unlock = MockIcon;

// Default export
export default MockIcon;