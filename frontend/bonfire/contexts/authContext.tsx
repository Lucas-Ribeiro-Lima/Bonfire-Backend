import { ReactNode, createContext, useState } from "react" 
import { setCookie } from "nookies"
import signInRequest from "@/services/auth";
import Router from "next/router";

interface UserProp {
    name: string;
    email: string;
    avatar_url: string;
}

interface SignInProp {
    username: string;
    password: string;
}

interface AuthContextProps {
    isAuthenticated: boolean;
    user ?: UserProp;
    signIn: ({username, password}: SignInProp) => Promise<void>;
}

interface AuthProviderProps {
    children : ReactNode;
}

export const AuthContext = createContext({} as AuthContextProps)

export function AuthProvider({ children }: AuthProviderProps) {
    const [user, setUser] = useState<UserProp | undefined >(undefined) 
    
    const isAuthenticated = !!user;

    async function signIn({username, password}: SignInProp) {       
        const { token, user } = await signInRequest(
            {
                username,
                password
            }
        )
        
        setCookie(undefined, 'bonfireToken', token, {
            maxAge: 60 * 60 * 1, // 1 hour
        }) 

        setUser(user)
        Router.push('/');

    }

    return(
        <AuthContext.Provider value = {{ user, isAuthenticated, signIn }}>
            {children}
        </AuthContext.Provider>
    );
}