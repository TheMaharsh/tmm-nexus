export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  message?: string;
}

export interface Role {
  id: string;
  name: string;
  permissions: string[];
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  organization_id: string;
  organization_name: string;
  role: Role;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthData {
  user: User;
  tokens: TokenPair;
}

export interface DashboardStats {
  total_leads: number;
  new_leads: number;
  qualified_leads: number;
  contacted_leads: number;
  won_leads: number;
  recent_searches: number;
}
