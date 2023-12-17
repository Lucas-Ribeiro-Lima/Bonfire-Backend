import { AlignJustify, LogIn, LucideHome, LucideImport, Settings, FileSpreadsheetIcon } from "lucide-react";
import React, {FC, ReactNode} from "react";
import Link from "next/link";


interface Buttons {
    path:string;
    description:string;
    icon?:ReactNode
}

const NavigationButton:FC<Buttons> = ({path, description, icon}: Buttons) => {
    return(
        <Link className="flex gap-2  hover:text-white hover:duration-1000 hover:drop-shadow-2xl" href={path}> {icon}{description} </Link>
    );
}

const NavigationButtons = () => {
    return (
        <nav className="flex flex-row gap-4 p-4 text-zinc-500 rounded-br-lg">
        <NavigationButton path="/" description="Inicio" icon={<LucideHome />} />
        <NavigationButton path="#" description="Cadastro" icon={<AlignJustify />} />
        <NavigationButton path="#" description="Relatórios" icon={<FileSpreadsheetIcon />} />
        <NavigationButton path="/import" description="Importação" icon={<LucideImport />} />
        <NavigationButton path="#" description="Configuração" icon={<Settings />} />
        <NavigationButton path="/login" description="Sair" icon={<LogIn />} />
      </nav>
    );
}

export default NavigationButtons