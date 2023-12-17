'use client';

import { useForm } from "react-hook-form";
import { LockIcon } from "lucide-react";
import { useContext } from "react";
import { AuthContext } from "../../contexts/authContext";
import Link from "next/link";

export interface LoginFormInput {
    username: string;
    password: string;
    rememberMe: boolean;
}

async function handleSignIn({username, password, rememberMe }: LoginFormInput){
    
    const {signIn} = useContext(AuthContext);

    await signIn({username, password});
}

const LoginForm = () => {

    const { register, handleSubmit } = useForm<LoginFormInput>()

    return (
        <form onSubmit={handleSubmit(handleSignIn)} className="flex flex-col items-center gap-4">
            <div className="relative mr-auto text-xl">
                Sign in to your account
            </div>
            <div className="flex flex-col rounded-md shadow-sm -space-y-px">
                <label htmlFor="username">
                    <input {...register('username')} type="text" placeholder="Username" autoComplete="email" required
                     className="w-96 rounded-t-md border border-gray-300 text-black indent-2 focus:outline-none focus:bg-zinc-300" ></input>
                </label>
                <label htmlFor="password">
                    <input {...register('password')} type="password" placeholder="Password" autoComplete="current-password" required
                     className="w-96 rounded-b-md border border-gray-300 text-black indent-2 focus:outline-none focus:bg-zinc-300" ></input>
                </label>
            </div>
            <div className="flex flex-row gap-12 text-sm">
                <label className="flex gap-2">
                    <input {...register('rememberMe')} type="checkbox"></input>
                    Remember me
                </label>
                <Link href="#" className="text-red-800">
                    Forgot password?
                </Link>
            </div>
            <button type="submit" className="flex flex-row gap-2 w-5/6 h-8 justify-center items-center text-black bg-zinc-400 rounded-lg hover:bg-red-800 hover:duration-1000 hover:shadow-2xl hover:shadow-black">
                <LockIcon></LockIcon>
                Sign in
            </button>
        </form>
    );
}

export default LoginForm;