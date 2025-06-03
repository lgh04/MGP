import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface LoginResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
    user: {
        email: string;
        name: string;
        nickname: string;
    };
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
    const formData = new FormData();
    formData.append('username', email);  // OAuth2 형식에 맞춰 username으로 전송
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/login`, formData);
    const data = response.data;
    
    // 토큰과 사용자 정보를 세션 스토리지에 저장
    sessionStorage.setItem('token', data.access_token);
    sessionStorage.setItem('user', JSON.stringify(data.user));
    
    // 만료 시간 저장 (현재 시간 + expires_in)
    const expiresAt = new Date().getTime() + (data.expires_in * 1000);
    sessionStorage.setItem('expiresAt', expiresAt.toString());
    
    return data;
};

export const logout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('expiresAt');
};

export const getToken = (): string | null => {
    const token = sessionStorage.getItem('token');
    const expiresAt = sessionStorage.getItem('expiresAt');
    
    if (!token || !expiresAt) {
        return null;
    }
    
    // 토큰이 만료되었는지 확인
    if (new Date().getTime() > parseInt(expiresAt)) {
        logout();  // 만료된 토큰 삭제
        return null;
    }
    
    return token;
};

export const isAuthenticated = (): boolean => {
    return getToken() !== null;
};

export const getUser = () => {
    const userStr = sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
};

// axios 인터셉터 설정
axios.interceptors.request.use(
    (config) => {
        const token = getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);
