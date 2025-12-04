import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { jwtDecode } from 'jwt-decode';

interface User {
    email: string;
    is_superuser: boolean;
}

interface AuthState {
    isAuthenticated: boolean;
    token: string | null;
    user: User | null;
    loading: boolean;
}

const initialState: AuthState = {
    isAuthenticated: false,
    token: null,
    user: null,
    loading: true
};

function createAuthStore() {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    async function fetchUser(token: string) {
        try {
            const response = await fetch('http://localhost:8000/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const userData = await response.json();
                update(state => ({
                    ...state,
                    isAuthenticated: true,
                    token,
                    user: userData,
                    loading: false
                }));
            } else {
                // Token might be invalid
                set({ ...initialState, loading: false });
                if (browser) localStorage.removeItem('token');
            }
        } catch (e) {
            console.error("Error fetching user", e);
            set({ ...initialState, loading: false });
        }
    }

    return {
        subscribe,
        login: async (token: string) => {
            if (browser) {
                localStorage.setItem('token', token);
            }
            // Set initial state with token but loading true
            update(state => ({ ...state, isAuthenticated: true, token, loading: true }));
            await fetchUser(token);
        },
        logout: () => {
            if (browser) {
                localStorage.removeItem('token');
            }
            set({ ...initialState, loading: false });
        },
        initialize: async () => {
            if (browser) {
                const token = localStorage.getItem('token');
                if (token) {
                    update(state => ({ ...state, isAuthenticated: true, token, loading: true }));
                    await fetchUser(token);
                } else {
                    set({ ...initialState, loading: false });
                }
            } else {
                set({ ...initialState, loading: false });
            }
        },
        setUser: (user: User) => {
            update(state => ({ ...state, user }));
        }
    };
}

export const auth = createAuthStore();
