import { LockIcon } from "lucide-react";
import Footer from "./footer";
import Logo from "./logo";
import Link from "next/link";


const LoginForm = () => {
    return (
        <form className="flex flex-col items-center gap-4">
            <div className="relative right-20 text-xl">
                Sign in to your account
            </div>
            <div className="flex flex-col rounded-md shadow-sm -space-y-px">
                <label>
                    <input type="text" placeholder="Username" 
                     className="w-96 rounded-t-md border border-gray-300 text-black indent-2 focus:outline-none focus:bg-zinc-300" ></input>
                </label>
                <label>
                    <input type="password" placeholder="Password" 
                     className="w-96 rounded-b-md border border-gray-300 text-black indent-2 focus:outline-none focus:bg-zinc-300" ></input>
                </label>
            </div>
            <div className="flex flex-row gap-12 text-sm">
                <label className="flex gap-2">
                    <input type="checkbox"></input>
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

const LoginMenu = () => {
    return(
        <div className="flex flex-col items-center gap-16">
            <div className="pl-5 scale-150">
                <Logo></Logo>
            </div>
            <LoginForm></LoginForm>
        </div>
    );
}

const LoginLayout = () => {
    return(
        <div className="flex flex-col h-screen bg-gradient-to-r from-zinc-900 to-zinc-800">            
            <div className="flex flex-1 justify-center items-center relative bottom-10">
                <LoginMenu></LoginMenu>
            </div>
            <div>
                <Footer></Footer>
            </div>
        </div>
    );
}

export default LoginLayout

