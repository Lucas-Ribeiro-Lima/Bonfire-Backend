import { AlignJustify, LucideHome, LucideImport, Settings, Undo } from "lucide-react";
import Link from "next/link";


const Sidebar = () => {
    return (
        <aside className='w-64'>
            <nav className="flex flex-col gap-4 bg-zinc-700 w-max p-4 text-zinc-500 rounded-br-lg">
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideHome></LucideHome>Inicio</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><AlignJustify></AlignJustify>Cadastro</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideImport></LucideImport>Importação</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Settings></Settings>Configuração</Link>
            <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Undo></Undo>Sair</Link>
            </nav>
        </aside>
    );
}

export default Sidebar;