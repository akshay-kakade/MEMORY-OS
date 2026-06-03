export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Workspace {
  id: number;
  name: string;
  description: string;
}

export interface Chat {
  id: number;
  title: string;
  workspace_id: number;
  is_archived: boolean;
  created_at: string;
}

export interface Message {
  id: number;
  chat_id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Memory {
  id: number;
  content: string;
  workspace_id: number;
  category_id: number;
  importance: number;
  created_at: string;
  is_pinned: boolean;
}
