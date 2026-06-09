import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Get an environment variable with optional fallback and validation
 * @param key Primary environment variable key to check
 * @param options Configuration options
 * @returns The environment variable value or default
 * @throws Error if required and not found
 */
export function getEnv(
  key: string, 
  options: {
    fallbackKeys?: string[];
    default?: string;
    required?: boolean;
    validateFn?: (value: string) => boolean;
  } = {}
): string | undefined {
  // First check primary key
  let value = process.env[key];
  
  // If not found, try fallback keys
  if (!value && options.fallbackKeys) {
    for (const fallbackKey of options.fallbackKeys) {
      value = process.env[fallbackKey];
      if (value) {
        if (process.env.NODE_ENV === 'development') {
          console.warn(`Warning: ${key} not found, using ${fallbackKey} instead.`);
        }
        break;
      }
    }
  }
  
  // If still not found, use default
  if (!value && options.default !== undefined) {
    if (process.env.NODE_ENV === 'development') {
      console.warn(`Warning: ${key} not found, using default value.`);
    }
    value = options.default;
  }
  
  // Validate if required
  if (options.required && !value) {
    throw new Error(`Required environment variable ${key} is not set.`);
  }
  
  // Validate with custom function
  if (value && options.validateFn && !options.validateFn(value)) {
    throw new Error(`Environment variable ${key} failed validation.`);
  }
  
  return value;
}

/**
 * Get and parse a numeric environment variable
 * @param key Environment variable key
 * @param options Configuration options
 * @returns The parsed numeric value
 */
export function getNumericEnv(
  key: string,
  options: {
    fallbackKeys?: string[];
    default?: number;
    required?: boolean;
    min?: number;
    max?: number;
  } = {}
): number | undefined {
  const strValue = getEnv(key, {
    fallbackKeys: options.fallbackKeys,
    default: options.default?.toString(),
    required: options.required,
  });
  
  if (strValue === undefined) {
    return options.default;
  }
  
  const numValue = Number(strValue);
  
  if (isNaN(numValue)) {
    throw new Error(`Environment variable ${key} is not a valid number.`);
  }
  
  if (options.min !== undefined && numValue < options.min) {
    throw new Error(`Environment variable ${key} must be at least ${options.min}.`);
  }
  
  if (options.max !== undefined && numValue > options.max) {
    throw new Error(`Environment variable ${key} must be at most ${options.max}.`);
  }
  
  return numValue;
}

/**
 * Get a boolean environment variable
 * @param key Environment variable key
 * @param options Configuration options
 * @returns The parsed boolean value
 */
export function getBooleanEnv(
  key: string,
  options: {
    fallbackKeys?: string[];
    default?: boolean;
    required?: boolean;
  } = {}
): boolean | undefined {
  const strValue = getEnv(key, {
    fallbackKeys: options.fallbackKeys,
    default: options.default?.toString(),
    required: options.required,
  });
  
  if (strValue === undefined) {
    return options.default;
  }
  
  return ['true', '1', 'yes'].includes(strValue.toLowerCase());
} 