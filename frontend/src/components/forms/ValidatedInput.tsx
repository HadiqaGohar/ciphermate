'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  url?: boolean;
  custom?: (value: string) => string | null;
}

export interface ValidationResult {
  isValid: boolean;
  error?: string;
  warning?: string;
}

interface ValidatedInputProps {
  id: string;
  name: string;
  type?: 'text' | 'email' | 'url' | 'password' | 'textarea';
  label: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onValidation?: (result: ValidationResult) => void;
  rules?: ValidationRule;
  disabled?: boolean;
  className?: string;
  showValidation?: boolean;
  validateOnBlur?: boolean;
  validateOnChange?: boolean;
  rows?: number; // For textarea
}

export function ValidatedInput({
  id,
  name,
  type = 'text',
  label,
  placeholder,
  value,
  onChange,
  onValidation,
  rules = {},
  disabled = false,
  className = '',
  showValidation = true,
  validateOnBlur = true,
  validateOnChange = false,
  rows = 3
}: ValidatedInputProps) {
  const [validation, setValidation] = useState<ValidationResult>({ isValid: true });
  const [touched, setTouched] = useState(false);
  const [focused, setFocused] = useState(false);

  const validateValue = useCallback((val: string): ValidationResult => {
    // Required validation
    if (rules.required && !val.trim()) {
      return { isValid: false, error: `${label} is required` };
    }

    // Skip other validations if empty and not required
    if (!val.trim() && !rules.required) {
      return { isValid: true };
    }

    // Length validations
    if (rules.minLength && val.length < rules.minLength) {
      return { 
        isValid: false, 
        error: `${label} must be at least ${rules.minLength} characters` 
      };
    }

    if (rules.maxLength && val.length > rules.maxLength) {
      return { 
        isValid: false, 
        error: `${label} must be no more than ${rules.maxLength} characters` 
      };
    }

    // Email validation
    if (rules.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(val)) {
        return { isValid: false, error: 'Please enter a valid email address' };
      }
    }

    // URL validation
    if (rules.url) {
      try {
        new URL(val);
      } catch {
        return { isValid: false, error: 'Please enter a valid URL' };
      }
    }

    // Pattern validation
    if (rules.pattern && !rules.pattern.test(val)) {
      return { isValid: false, error: `${label} format is invalid` };
    }

    // Custom validation
    if (rules.custom) {
      const customError = rules.custom(val);
      if (customError) {
        return { isValid: false, error: customError };
      }
    }

    // Check for warnings
    let warning: string | undefined;
    if (rules.maxLength && val.length > rules.maxLength * 0.8) {
      warning = `Approaching character limit (${val.length}/${rules.maxLength})`;
    }

    return { isValid: true, warning };
  }, [rules, label]);

  const handleValidation = useCallback((val: string) => {
    const result = validateValue(val);
    setValidation(result);
    onValidation?.(result);
  }, [validateValue, onValidation]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    onChange(newValue);

    if (validateOnChange || touched) {
      handleValidation(newValue);
    }
  };

  const handleBlur = () => {
    setTouched(true);
    setFocused(false);
    
    if (validateOnBlur) {
      handleValidation(value);
    }
  };

  const handleFocus = () => {
    setFocused(true);
  };

  // Validate on mount if value exists
  useEffect(() => {
    if (value && !touched) {
      handleValidation(value);
    }
  }, [value, touched, handleValidation]);

  const showError = showValidation && touched && !focused && validation.error;
  const showWarning = showValidation && validation.warning && !validation.error;
  const showSuccess = showValidation && touched && validation.isValid && value.trim() && !validation.warning;

  const inputClasses = `
    block w-full px-3 py-2 border rounded-md shadow-sm
    placeholder-gray-400 dark:placeholder-gray-500
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    transition-colors duration-200
    ${showError 
      ? 'border-red-300 dark:border-red-600 focus:border-red-500 focus:ring-red-500 bg-red-50 dark:bg-red-900/10' 
      : showWarning
      ? 'border-yellow-300 dark:border-yellow-600 focus:border-yellow-500 focus:ring-yellow-500 bg-yellow-50 dark:bg-yellow-900/10'
      : showSuccess
      ? 'border-green-300 dark:border-green-600 focus:border-green-500 focus:ring-green-500 bg-green-50 dark:bg-green-900/10'
      : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-gray-800'
    }
    text-gray-900 dark:text-gray-100
    ${className}
  `.trim();

  const InputComponent = type === 'textarea' ? 'textarea' : 'input';

  return (
    <div className="space-y-1">
      <label 
        htmlFor={id} 
        className="block text-sm font-medium text-gray-700 dark:text-gray-300"
      >
        {label}
        {rules.required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        <InputComponent
          id={id}
          name={name}
          type={type === 'textarea' ? undefined : type}
          rows={type === 'textarea' ? rows : undefined}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          onFocus={handleFocus}
          disabled={disabled}
          className={inputClasses}
          aria-invalid={showError ? 'true' : 'false'}
          aria-describedby={
            showError ? `${id}-error` : 
            showWarning ? `${id}-warning` : 
            showSuccess ? `${id}-success` : undefined
          }
        />
        
        {/* Validation icon */}
        {showValidation && (showError || showWarning || showSuccess) && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            {showError && (
              <AlertCircle className="h-5 w-5 text-red-500" aria-hidden="true" />
            )}
            {showWarning && (
              <AlertCircle className="h-5 w-5 text-yellow-500" aria-hidden="true" />
            )}
            {showSuccess && (
              <CheckCircle className="h-5 w-5 text-green-500" aria-hidden="true" />
            )}
          </div>
        )}
      </div>

      {/* Validation messages */}
      {showError && (
        <p id={`${id}-error`} className="text-sm text-red-600 dark:text-red-400 flex items-center">
          <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
          {validation.error}
        </p>
      )}
      
      {showWarning && (
        <p id={`${id}-warning`} className="text-sm text-yellow-600 dark:text-yellow-400 flex items-center">
          <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
          {validation.warning}
        </p>
      )}
      
      {showSuccess && (
        <p id={`${id}-success`} className="text-sm text-green-600 dark:text-green-400 flex items-center">
          <CheckCircle className="h-4 w-4 mr-1 flex-shrink-0" />
          Valid
        </p>
      )}

      {/* Character count for inputs with maxLength */}
      {rules.maxLength && value && (
        <p className="text-xs text-gray-500 dark:text-gray-400 text-right">
          {value.length}/{rules.maxLength}
        </p>
      )}
    </div>
  );
}

// Utility function to validate multiple inputs
export function validateForm(
  values: Record<string, string>,
  rules: Record<string, ValidationRule>
): { isValid: boolean; errors: Record<string, string> } {
  const errors: Record<string, string> = {};
  
  for (const [field, fieldRules] of Object.entries(rules)) {
    const value = values[field] || '';
    
    // Required validation
    if (fieldRules.required && !value.trim()) {
      errors[field] = `${field} is required`;
      continue;
    }

    // Skip other validations if empty and not required
    if (!value.trim() && !fieldRules.required) {
      continue;
    }

    // Length validations
    if (fieldRules.minLength && value.length < fieldRules.minLength) {
      errors[field] = `${field} must be at least ${fieldRules.minLength} characters`;
      continue;
    }

    if (fieldRules.maxLength && value.length > fieldRules.maxLength) {
      errors[field] = `${field} must be no more than ${fieldRules.maxLength} characters`;
      continue;
    }

    // Email validation
    if (fieldRules.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        errors[field] = 'Please enter a valid email address';
        continue;
      }
    }

    // URL validation
    if (fieldRules.url) {
      try {
        new URL(value);
      } catch {
        errors[field] = 'Please enter a valid URL';
        continue;
      }
    }

    // Pattern validation
    if (fieldRules.pattern && !fieldRules.pattern.test(value)) {
      errors[field] = `${field} format is invalid`;
      continue;
    }

    // Custom validation
    if (fieldRules.custom) {
      const customError = fieldRules.custom(value);
      if (customError) {
        errors[field] = customError;
        continue;
      }
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}