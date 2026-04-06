'use client';

import { Message } from './ChatInterface';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.type === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
      }`}>
        <div className="text-sm">
          {message.content}
        </div>
        
        {/* Show intent analysis for assistant messages */}
        {!isUser && message.intentAnalysis && message.intentAnalysis.intent_type !== 'GENERAL_QUERY' && (
          <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
            <div className="text-xs text-gray-600 dark:text-gray-400">
              <div className="flex items-center gap-2">
                <span className="font-medium">Intent:</span>
                <span className="capitalize">
                  {message.intentAnalysis.intent_type.toLowerCase().replace(/_/g, ' ')}
                </span>
                <span className={`px-1.5 py-0.5 rounded text-xs ${
                  message.intentAnalysis.confidence === 'HIGH' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : message.intentAnalysis.confidence === 'MEDIUM'
                    ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                    : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                }`}>
                  {message.intentAnalysis.confidence}
                </span>
              </div>
              
              {message.intentAnalysis.service_name && (
                <div className="mt-1">
                  <span className="font-medium">Service:</span> {message.intentAnalysis.service_name}
                </div>
              )}
              
              {message.intentAnalysis.required_permissions.length > 0 && (
                <div className="mt-1">
                  <span className="font-medium">Permissions:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {message.intentAnalysis.required_permissions.map((perm, index) => (
                      <span 
                        key={index}
                        className={`px-1.5 py-0.5 rounded text-xs ${
                          message.intentAnalysis?.has_permissions
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                        }`}
                      >
                        {perm}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Show error information */}
        {message.error && (
          <div className="mt-2 pt-2 border-t border-red-200 dark:border-red-600">
            <div className="text-xs text-red-600 dark:text-red-400">
              <span className="font-medium">Error:</span> {message.error}
            </div>
          </div>
        )}
        
        <div className="text-xs mt-1 opacity-70">
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </div>
  );
}