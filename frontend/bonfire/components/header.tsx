import {LucideSunMoon} from "lucide-react";
import MenuBar from "./menubar";
import Logo from "./logo";

const Header = () => {
    return (
        <header className='flex flex-row bg-gradient-to-r from-zinc-900 to-zinc-700 h-20 p-2 align-center border-b border-white/25'>
          <Logo></Logo>
          <MenuBar></MenuBar>
          <div className="absolute right-10 top-6 text-zinc-400 hover:text-white hover:duration-1000 cursor-pointer">
            <LucideSunMoon></LucideSunMoon>
          </div>
        </header>
    );
}

export default Header;