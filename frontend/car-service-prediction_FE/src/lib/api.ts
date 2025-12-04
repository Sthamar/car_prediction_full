import { auth } from './stores/auth';
import { get } from 'svelte/store';

const BASE_URL = 'http://localhost:8000';

async function request(endpoint: string, options: RequestInit = {}) {
    const authState = get(auth);
    const headers = new Headers(options.headers || {});

    if (authState.token) {
        headers.set('Authorization', `Bearer ${authState.token}`);
    }

    if (!headers.has('Content-Type')) {
        headers.set('Content-Type', 'application/json');
    }

    const config = {
        ...options,
        headers
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
        auth.logout();
        // Optional: Redirect to login
    }

    return response;
}

export const api = {
    get: (endpoint: string) => request(endpoint, { method: 'GET' }),
    post: (endpoint: string, body: any) => request(endpoint, { method: 'POST', body: JSON.stringify(body) }),
    put: (endpoint: string, body: any) => request(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (endpoint: string) => request(endpoint, { method: 'DELETE' })
};
