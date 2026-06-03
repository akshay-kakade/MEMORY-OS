import React, { useState, useRef, useEffect } from 'react';
import { useStore } from '../store/useStore';
import api from '../api/axios';
import ReactMarkdown from 'react-markdown';
import { 
  Send, 
  Paperclip, 
  Image as ImageIcon, 
  FileText, 
  Download,
  MoreVertical,
  Loader2,
  Sparkles
} from 'lucide-react';
import { clsx } from 'clsx';
import { motion, AnimatePresence } from 'framer-motion';
const quickPrompts = [
  { emoji: '🧠', text: 'Remember my favorite coding stack' },
  { emoji: '📌', text: 'What did we discuss about the project last week?' },
  { emoji: '🧾', text: 'Extract text from my uploaded receipt' },
  { emoji: '🚀', text: 'Summarize our research on GenAI' }
];

type MessageSquareProps = {
  size?: number;
  className?: string;
};

const MessageSquare = ({ size = 16, className }: MessageSquareProps) => (
  <FileText size={size} className={className} />
);

const ChatWindow = () => {
  const { currentChat, messages, addMessage, user, updateChat } = useStore();
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // file input refs for uploads (must be declared unconditionally to avoid hook order changes)
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const imageInputRef = useRef<HTMLInputElement | null>(null);

  const handleFileClick = () => fileInputRef.current?.click();
  const handleImageClick = () => imageInputRef.current?.click();

  const handleUpload = async (file: File | null) => {
    if (!file || !currentChat) return;
    setLoading(true);
    try {
      const fd = new FormData();
      const workspaceId = (useStore.getState().currentWorkspace?.id) || 1;
      fd.append('workspace_id', String(workspaceId));
      fd.append('file', file, file.name);

      const endpoint = file.type === 'application/pdf' ? '/pdf/' : '/ocr/';
      const res = await api.post(endpoint, fd, { headers: { 'Content-Type': 'multipart/form-data' } });

      const assistantContent = file.type === 'application/pdf'
        ? `Uploaded PDF. Extract: ${res.data.extracted_text || ''}`
        : `Uploaded image: ${res.data.url || ''}\n\nExtracted text:\n${res.data.extracted_text || ''}`;

      addMessage({
        id: Date.now(),
        chat_id: currentChat.id,
        role: 'assistant',
        content: assistantContent,
        created_at: new Date().toISOString()
      });
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || !currentChat || loading) return;

    const userMsg = input;
    const chatId = currentChat.id;
    const isNewChat = messages.length === 0;
    
    setInput('');
    setLoading(true);

    // Optimistic update for user message
    const tempUserMsg = {
      id: Date.now(),
      chat_id: chatId,
      role: 'user' as const,
      content: userMsg,
      created_at: new Date().toISOString()
    };
    addMessage(tempUserMsg);

    try {
      const res = await api.post(`/chats/${chatId}/messages/`, {
        chat_id: chatId,
        role: 'user',
        content: userMsg
      });
      addMessage(res.data);

      // Auto-name chat if it's the first message
      if (isNewChat) {
        try {
          const titleRes = await api.post(`/chats/${chatId}/generate-title`);
          updateChat(chatId, { title: titleRes.data.title });
        } catch (titleErr) {
          console.error("Failed to generate title:", titleErr);
        }
      }
    } catch (err) {
      console.error(err);
      addMessage({
        id: Date.now() + 1,
        chat_id: chatId,
        role: 'assistant' as const,
        content: "Sorry, I encountered an error. Please check your connection or API key.",
        created_at: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  if (!currentChat) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-6 relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_30%_30%,rgba(255,122,61,0.12),transparent_55%),radial-gradient(circle_at_70%_70%,rgba(107,214,255,0.12),transparent_52%)]" />
        <div className="w-24 h-24 bg-panel border border-border rounded-3xl flex items-center justify-center shadow-2xl rotate-6 animate-pulse relative z-10">
           <Sparkles size={48} className="text-accent -rotate-6" />
        </div>
        <div className="max-w-md space-y-2 relative z-10">
          <h2 className="text-3xl font-bold">Welcome to MemoryOS</h2>
          <p className="text-muted">Select a chat from the sidebar or start a new conversation to experience private, intelligent memory. ✨</p>
        </div>
        <div className="grid grid-cols-2 gap-4 w-full max-w-2xl mt-8 relative z-10">
          {quickPrompts.map((suggestion, i) => (
            <motion.button
              key={suggestion.text}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              whileHover={{ y: -3, scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              className="p-4 bg-panel/85 border border-border rounded-2xl text-left text-sm hover:border-accent/50 hover:bg-panel-lighter transition-all group backdrop-blur-sm shadow-lg shadow-black/15"
            >
              <p className="text-muted group-hover:text-text">
                <span className="mr-1">{suggestion.emoji}</span>
                {suggestion.text}
              </p>
            </motion.button>
          ))}
        </div>
      </div>
    );
  }

  

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-background/40 relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_25%_15%,rgba(255,122,61,0.1),transparent_45%),radial-gradient(circle_at_80%_80%,rgba(107,214,255,0.1),transparent_48%)]" />
      {/* Header */}
      <header className="h-16 border-b border-border/70 flex items-center justify-between px-6 bg-background/65 backdrop-blur-xl sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-linear-to-br from-panel-lighter to-panel border border-border rounded-lg flex items-center justify-center shadow-inner">
            <MessageSquare size={16} className="text-accent" />
          </div>
          <h1 className="font-bold truncate max-w-50 md:max-w-md">✨ {currentChat.title}</h1>
        </div>
        <div className="flex items-center gap-2">
          <button title="Download" className="p-2 hover:bg-panel-lighter rounded-lg text-muted transition-all duration-300 hover:-translate-y-0.5">
            <Download size={18} />
          </button>
          <button title="More" className="p-2 hover:bg-panel-lighter rounded-lg text-muted transition-all duration-300 hover:-translate-y-0.5">
            <MoreVertical size={18} />
          </button>
        </div>
      </header>

      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto custom-scrollbar p-4 md:p-8 space-y-8 relative z-10"
      >
        <AnimatePresence initial={false}>
          {messages.map((msg, idx) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ type: 'spring', stiffness: 220, damping: 22 }}
              key={msg.id || idx}
              className={clsx(
                "flex gap-4 md:gap-6 max-w-4xl mx-auto group",
                msg.role === 'user' ? "flex-row-reverse" : "flex-row"
              )}
            >
              <div className={clsx(
                "w-8 h-8 md:w-10 md:h-10 rounded-xl flex items-center justify-center shrink-0 shadow-lg",
                msg.role === 'user' 
                  ? "bg-linear-to-br from-accent to-[#ff9458] text-background font-bold" 
                  : "bg-panel-lighter border border-border text-accent"
              )}>
                {msg.role === 'user' ? user?.username?.[0]?.toUpperCase() ?? 'U' : <Sparkles size={20} />}
              </div>
              <div className={clsx(
                "flex-1 space-y-2 overflow-hidden",
                msg.role === 'user' ? "text-right" : "text-left"
              )}>
                <div className={clsx(
                  "inline-block px-4 py-3 md:px-6 md:py-4 rounded-3xl text-sm md:text-base leading-relaxed shadow-sm transition-all duration-300",
                  msg.role === 'user'
                    ? "bg-linear-to-br from-accent via-[#ff8a4d] to-[#ff6c2f] text-[#1a0f0b] rounded-tr-none font-semibold shadow-[0_12px_30px_rgba(255,122,61,0.22)]"
                    : "bg-linear-to-br from-panel to-panel-lighter border border-border/70 rounded-tl-none text-text prose prose-invert max-w-none shadow-[0_12px_30px_rgba(7,16,31,0.3)]"
                )}>
                  {msg.role === 'assistant' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>
                <p className="text-[10px] text-muted uppercase tracking-widest font-bold px-1">
                  {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {loading && (
          <div className="flex gap-4 md:gap-6 max-w-4xl mx-auto animate-pulse">
            <div className="w-8 h-8 md:w-10 md:h-10 rounded-xl bg-panel-lighter border border-border flex items-center justify-center shrink-0">
              <Loader2 className="animate-spin text-accent" size={20} />
            </div>
            <div className="flex-1 space-y-2">
              <div className="h-10 bg-panel border border-border rounded-3xl rounded-tl-none w-2/3"></div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 md:p-8 bg-linear-to-t from-background via-background/95 to-transparent relative z-10">
        <form 
          onSubmit={handleSend}
          className="max-w-4xl mx-auto relative group"
        >
          <div className="absolute -inset-0.5 bg-linear-to-r from-accent/30 via-blue/20 to-accent/30 rounded-3xl blur opacity-40 group-focus-within:opacity-100 transition duration-700 pointer-events-none" />
          <div className="relative flex items-end gap-2 bg-panel/80 border border-border/70 rounded-3xl p-2 pl-4 focus-within:border-accent/55 transition-all duration-300 shadow-2xl focus-within:shadow-[0_0_0_1px_rgba(255,122,61,0.24),0_18px_38px_rgba(8,15,28,0.6)] backdrop-blur-xl">
            <div className="flex items-center gap-1 mb-1">
              <button type="button" onClick={handleFileClick} title="Attach File" className="p-2 text-muted hover:text-accent hover:bg-panel-lighter rounded-full transition-all duration-300 hover:-translate-y-0.5">
                <Paperclip size={20} />
              </button>
              <button type="button" onClick={handleImageClick} title="Insert Image" className="p-2 text-muted hover:text-blue hover:bg-panel-lighter rounded-full transition-all duration-300 hover:-translate-y-0.5">
                <ImageIcon size={20} />
              </button>
            </div>

            {/* Hidden file inputs triggered by the buttons */}
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(e) => handleUpload(e.target.files?.[0] ?? null)}
            />
            <input
              ref={imageInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => handleUpload(e.target.files?.[0] ?? null)}
            />
            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask anything... MemoryOS is listening ✨"
              className="flex-1 bg-transparent border-none text-text placeholder:text-muted/85 py-3 max-h-48 custom-scrollbar resize-none outline-none focus:outline-none focus-visible:outline-none focus:ring-0"
            />
            <button 
              type="submit"
              disabled={!input.trim() || loading}
              className="mb-1 p-3 bg-linear-to-br from-accent to-[#ff9458] text-background rounded-2xl hover:from-[#ff8f53] hover:to-[#ff7a3d] disabled:opacity-30 disabled:hover:from-accent disabled:hover:to-[#ff9458] transition-all duration-300 shadow-lg shadow-accent/25 active:scale-95 hover:-translate-y-0.5"
            >
              {loading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
            </button>
          </div>
          <p className="text-[10px] text-center mt-3 text-muted">
            MemoryOS can make mistakes. Verify important information. Your data is encrypted and private. 🔐✨
          </p>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;
