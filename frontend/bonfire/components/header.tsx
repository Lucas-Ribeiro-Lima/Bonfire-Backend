import { Flame, LucideSunMoon } from "lucide-react";

const Header = () => {
    return (
        <header className='bg-gradient-to-r from-zinc-900 to-zinc-700 h-20 p-2 align-center border-b border-white/25'>
          <div className="cursor-pointer w-40">
            <h1 className="flex flex-row text-extrabold text-3xl text-red-800 items-center"><Flame></Flame>Bonfire</h1>
            <h2 className="text-bold text-zinc-400">Autos de Infração</h2>
          </div>
          <div className="absolute right-10 top-6 text-zinc-400 hover:text-white hover:duration-1000 cursor-pointer">
            <LucideSunMoon></LucideSunMoon>
          </div>
        </header>
    );
}

export default Header;