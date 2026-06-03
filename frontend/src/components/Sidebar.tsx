import { useStore } from '../store/useStore';
import api from '../api/axios';
import { 
  Plus, 
  MessageSquare, 
  LogOut, 
  ChevronDown,
  BrainCircuit,
  Database,
  Trash2
} from 'lucide-react';
import { clsx } from 'clsx';
import type { Chat } from '../types';

const Sidebar = () => {
  const { 
    user, 
    setUser, 
    currentWorkspace, 
    chats, 
    currentChat, 
    setCurrentChat,
    setChats,
    setMessages,
    view,
    setView,
    deleteChat
  } = useStore();

  const handleNewChat = async () => {
    setView('chat');
    if (!currentWorkspace) return;
    try {
      const res = await api.post('/chats/', {
        title: 'New Chat',
        workspace_id: currentWorkspace.id
      });
      setChats([res.data, ...chats]);
      setCurrentChat(res.data);
      setMessages([]);
    } catch (err) {
      console.error(err);
    }
  };

  const handleChatSelect = async (chat: Chat) => {
    setView('chat');
    setCurrentChat(chat);
    try {
      const res = await api.get(`/chats/${chat.id}/messages/`);
      setMessages(res.data);
    } catch (err) {
      console.error('Failed to load chat messages', err);
      setMessages([]);
    }
  };

  const handleDeleteChat = async (e: React.MouseEvent, chatId: number) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this chat?')) return;
    
    try {
      await api.delete(`/chats/${chatId}`);
      deleteChat(chatId);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="w-72 bg-panel/80 backdrop-blur-xl border-r border-border/70 flex flex-col h-full transition-all duration-300 ease-in-out shadow-[0_0_30px_rgba(6,12,24,0.45)]">
      {/* Workspace Switcher */}
      <div className="p-4 border-b border-border">
        <button className="w-full flex items-center justify-between p-2 rounded-xl bg-linear-to-r from-panel-lighter to-panel hover:from-panel hover:to-panel-lighter transition-all duration-300 group hover:-translate-y-0.5">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center font-bold text-background shadow-md">
              {currentWorkspace?.name?.[0] || 'W'}
            </div>
            <div className="text-left overflow-hidden">
              <p className="text-sm font-semibold truncate">{currentWorkspace?.name || 'Loading...'}</p>
              <p className="text-[10px] text-muted uppercase tracking-wider">Workspace</p>
            </div>
          </div>
          <ChevronDown size={16} className="text-muted group-hover:text-text transition-colors" />
        </button>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 bg-linear-to-r from-accent to-[#ff9458] text-background font-bold py-2.5 rounded-xl hover:from-[#ff8f53] hover:to-[#ff7a3d] transition-all duration-300 shadow-lg shadow-accent/25 active:scale-95 hover:-translate-y-0.5"
        >
          <Plus size={18} />
          New Chat ✨
        </button>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto custom-scrollbar px-2 space-y-1">
        <div className="px-2 py-2 text-[10px] font-bold text-muted uppercase tracking-[0.2em]">History ✨</div>
        {chats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => handleChatSelect(chat)}
            className={clsx(
              "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300 group cursor-pointer relative hover:-translate-y-0.5",
              currentChat?.id === chat.id && view === 'chat'
                ? "bg-linear-to-r from-panel-lighter to-panel text-text ring-1 ring-accent/25 shadow-inner" 
                : "text-muted hover:bg-panel-lighter/50 hover:text-text"
            )}
          >
            <MessageSquare size={16} className={clsx(
              "shrink-0",
              currentChat?.id === chat.id && view === 'chat' ? "text-accent" : "text-muted group-hover:text-text"
            )} />
            <span className="text-sm truncate font-medium flex-1 pr-6">{chat.title}</span>
            <button
              onClick={(e) => handleDeleteChat(e, chat.id)}
              className="absolute right-2 opacity-0 group-hover:opacity-100 p-1 hover:text-red-500 transition-all"
            >
              <Trash2 size={14} />
            </button>
          </div>
        ))}
      </div>

      {/* Bottom Actions */}
      <div className="mt-auto p-4 space-y-2 border-t border-border">
        <button 
          onClick={() => setView('knowledge')}
          className={clsx(
            "w-full flex items-center gap-3 px-3 py-2 rounded-xl transition-all duration-300 group hover:-translate-y-0.5",
            view === 'knowledge' ? "bg-panel-lighter text-text ring-1 ring-blue/30 shadow-inner" : "text-muted hover:bg-panel-lighter hover:text-text"
          )}
        >
          <Database size={18} className={clsx("group-hover:text-blue", view === 'knowledge' && "text-blue")} />
          <span className="text-sm font-medium">Knowledge Base 📚</span>
        </button>
        <button 
          onClick={() => setView('graph')}
          className={clsx(
            "w-full flex items-center gap-3 px-3 py-2 rounded-xl transition-all duration-300 group hover:-translate-y-0.5",
            view === 'graph' ? "bg-panel-lighter text-text ring-1 ring-accent/30 shadow-inner" : "text-muted hover:bg-panel-lighter hover:text-text"
          )}
        >
          <BrainCircuit size={18} className={clsx("group-hover:text-accent", view === 'graph' && "text-accent")} />
          <span className="text-sm font-medium">Knowledge Graph 🧠</span>
        </button>
        
        <div className="pt-2">
          <div className="flex items-center gap-3 px-3 py-3 rounded-2xl bg-panel-lighter/30 border border-border/50 transition-all duration-300 hover:border-accent/30">
            <div className="w-9 h-9 bg-border rounded-full flex items-center justify-center text-xs font-bold ring-2 ring-accent/20">
              {user?.username?.[0]?.toUpperCase() ?? 'U'}
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="text-xs font-bold truncate">{user?.username}</p>
              <p className="text-[10px] text-muted truncate">{user?.email}</p>
            </div>
            <button 
              onClick={() => setUser(null)}
              className="p-1.5 hover:bg-red-500/10 hover:text-red-500 rounded-lg transition-colors"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
