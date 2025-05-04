import { useState } from 'react';
import type { FormEvent } from 'react';

export function NewsletterSignup() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus('loading');
    
    // Validate email
    if (!email.trim()) {
      setStatus('error');
      setErrorMessage('Email is required');
      return;
    }
    
    if (!validateEmail(email)) {
      setStatus('error');
      setErrorMessage('Please enter a valid email address');
      return;
    }
    
    try {
      const apiBaseUrl = import.meta.env.PUBLIC_API_BASE_URL || '';
      const response = await fetch(`${apiBaseUrl}/newsletter/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to subscribe to newsletter');
      }

      setStatus('success');
      setEmail(''); // Clear the form on success
    } catch (error) {
      setStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'An error occurred');
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-control w-full">
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="email"
              id="newsletter-email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input input-bordered w-full"
              required
            />
            <button
              type="submit"
              disabled={status === 'loading'}
              className="btn btn-primary min-w-[120px]"
            >
              {status === 'loading' ? 
                <span className="loading loading-spinner loading-sm"></span> : 
                'Subscribe'}
            </button>
          </div>
        </div>

        {status === 'error' && (
          <div className="alert alert-error text-sm py-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{errorMessage}</span>
          </div>
        )}

        {status === 'success' && (
          <div className="alert alert-success text-sm py-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Thank you for subscribing to our newsletter!</span>
          </div>
        )}
      </form>
    </div>
  );
}

export default NewsletterSignup; 