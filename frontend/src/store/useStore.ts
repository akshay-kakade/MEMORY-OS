import { create } from 'zustand';
import type { User, Workspace, Chat, Message } from '../types';

interface AppState {
  user: User | null;
  workspaces: Workspace[];
  currentWorkspace: Workspace | null;
  chats: Chat[];
  currentChat: Chat | null;
  messages: Message[];
  view: 'chat' | 'knowledge' | 'graph';
  
  setUser: (user: User | null) => void;
  setWorkspaces: (workspaces: Workspace[]) => void;
  setCurrentWorkspace: (workspace: Workspace | null) => void;
  setChats: (chats: Chat[]) => void;
  setCurrentChat: (chat: Chat | null) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  setView: (view: 'chat' | 'knowledge' | 'graph') => void;
  deleteChat: (chatId: number) => void;
  updateChat: (chatId: number, data: Partial<Chat>) => void;
}

const initialUser = typeof window !== 'undefined' && window.localStorage.getItem('memoryos_user')
  ? JSON.parse(window.localStorage.getItem('memoryos_user')!)
  : null;

export const useStore = create<AppState>((set) => ({
  user: initialUser,
  workspaces: [],
  currentWorkspace: null,
  chats: [],
  currentChat: null,
  messages: [],
  view: 'chat',

  setUser: (user) => {
    try {
      if (user) {
        window.localStorage.setItem('memoryos_user', JSON.stringify(user));
      } else {
        window.localStorage.removeItem('memoryos_user');
      }
    } catch (e) {
      // ignore storage errors
    }
    set({ user });
  },
  setWorkspaces: (workspaces) => set({ workspaces }),
  setCurrentWorkspace: (currentWorkspace) => set({ currentWorkspace }),
  setChats: (chats) => set({ chats }),
  setCurrentChat: (currentChat) => set({ currentChat }),
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setView: (view) => set({ view }),
  deleteChat: (chatId) => set((state) => ({ 
    chats: state.chats.filter(c => c.id !== chatId),
    currentChat: state.currentChat?.id === chatId ? null : state.currentChat,
    messages: state.currentChat?.id === chatId ? [] : state.messages
  })),
  updateChat: (chatId, data) => set((state) => ({
    chats: state.chats.map(c => c.id === chatId ? { ...c, ...data } : c),
    currentChat: state.currentChat?.id === chatId ? { ...state.currentChat, ...data } : state.currentChat
  })),
}));
