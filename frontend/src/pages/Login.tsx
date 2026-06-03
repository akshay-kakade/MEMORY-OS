import React, { useState } from 'react';
import axios from 'axios';
import { useStore } from '../store/useStore';
import api from '../api/axios';
import { LogIn, UserPlus, Loader2 } from 'lucide-react';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const setUser = useStore((state) => state.setUser);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      if (isLogin) {
        const res = await api.post('/auth/signin', { username_or_email: username || email, password });
        setUser(res.data.user);
      } else {
        const res = await api.post('/auth/signup', { username, email, password });
        setUser(res.data.user);
      }
    } catch (err: unknown) {
      if (axios.isAxiosError<{ detail?: string }>(err)) {
        setError(err.response?.data?.detail ?? 'An error occurred');
      } else {
        setError('An error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center app-aurora-bg p-4">
      <div className="w-full max-w-md bg-panel/80 border border-border/60 rounded-3xl shadow-2xl overflow-hidden backdrop-blur-xl ring-1 ring-white/5">
        <div className="p-8">
          <div className="flex justify-center mb-8">
            <div className="w-16 h-16 bg-linear-to-br from-accent to-[#ff9458] rounded-2xl flex items-center justify-center shadow-lg shadow-accent/25 rotate-3 relative">
              <span className="text-background text-3xl font-bold -rotate-3">M</span>
              <span className="absolute -top-2 -right-2 text-lg">✨</span>
            </div>
          </div>
          
          <h2 className="text-3xl font-bold text-center mb-2">
            {isLogin ? 'Welcome Back 👋' : 'Create Account 🚀'}
          </h2>
          <p className="text-muted text-center mb-8">
            {isLogin ? 'Enter your details to access MemoryOS' : 'Join MemoryOS to start organizing your life'}
          </p>

          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-6 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-muted mb-1">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-background border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all"
                  placeholder="johndoe"
                  required
                />
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-muted mb-1">
                {isLogin ? 'Username or Email' : 'Email'}
              </label>
              <input
                type={isLogin ? "text" : "email"}
                value={isLogin ? (username || email) : email}
                onChange={(e) => isLogin ? setUsername(e.target.value) : setEmail(e.target.value)}
                className="w-full bg-background border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all"
                placeholder={isLogin ? "user@example.com" : "email@example.com"}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-muted mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-background border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-linear-to-r from-accent to-[#ff9458] hover:from-[#ff8f53] hover:to-[#ff7a3d] text-background font-bold py-3 rounded-xl shadow-lg shadow-accent/20 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 mt-4 active:scale-95 hover:-translate-y-0.5"
            >
              {loading ? (
                <Loader2 className="animate-spin" size={20} />
              ) : isLogin ? (
                <>
                  <LogIn size={20} /> Sign In ✨
                </>
              ) : (
                <>
                  <UserPlus size={20} /> Sign Up 🎉
                </>
              )}
            </button>
          </form>

          <div className="mt-8 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-accent hover:underline text-sm font-medium"
            >
              {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
