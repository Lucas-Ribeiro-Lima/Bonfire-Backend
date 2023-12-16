import Footer from "./footer";
import Logo from "./logo";


const LoginForm = () => {
    return (
        <form className="flex flex-col gap-4 items-center">
            <label className="flex flex-row gap-4">
                Username:
                <input type="text" className="w-46 text-black rounded-lg" ></input>
            </label>
            <label className="flex flex-row gap-4">
                Password:
                <input type="password" className="relative left-1 w-46 text-black rounded-lg" ></input>
            </label>
            <label className="flex gap-2 relative right-10 pt-2 text-sm">
                <input type="checkbox"></input>
                Permanecer Conectado
            </label>
            <button type="submit" className="relative left-24 top-4 text-black bg-zinc-400 pl-2 pr-2 pt-1 pb-1 rounded-lg hover:bg-white hover:duration-1000 hover:shadow-2xl hover:shadow-white">Log-in</button>
        </form>
    );
}

const LoginMenu = () => {
    return(
        <div className="flex flex-col items-center gap-12 pt-8 bg-zinc-700 h-2/4 w-1/4 rounded-3xl">
            <Logo></Logo>
            <LoginForm></LoginForm>
        </div>
    );
}

const LoginLayout = () => {
    return(
        <div className="flex flex-col h-screen">            
            <div className="flex flex-1 justify-center items-center">
                <LoginMenu></LoginMenu>
            </div>
            <div>
                <Footer></Footer>
            </div>
        </div>
    );
}

export default LoginLayout

