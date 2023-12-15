import { AlignJustify, LucideHome, LucideImport, Settings, Undo } from "lucide-react";
import Link from "next/link";


const MenuBar = () => {
    return (
        <div>
            <nav className="flex flex-row gap-4 p-4 text-zinc-500 rounded-br-lg">
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideHome></LucideHome>Inicio</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><AlignJustify></AlignJustify>Cadastro</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideImport></LucideImport>Importação</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Settings></Settings>Configuração</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Undo></Undo>Sair</Link>
            </nav>
        </div>
    );
}

export default MenuBar;