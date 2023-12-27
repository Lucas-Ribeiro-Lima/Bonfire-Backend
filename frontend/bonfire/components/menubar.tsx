'use client'

import { LucideHome, AlignJustify, FileSpreadsheetIcon, LucideImport, Settings, LogIn } from "lucide-react";
import { DropDownField, DropdownFatherField, SimpleField } from '@/components/dropdown/dropdown'



const MenuBar = () => {
    return (
        <div className="flex flex-row gap-8 p-4 text-zinc-500 rounded-br-lg">

            <DropdownFatherField description="Inicio" icon={<LucideHome />}></DropdownFatherField>

            <DropdownFatherField description="Cadastros" icon={<AlignJustify />}>
                <DropDownField path='/registers/vehicles' description='Veiculos'></DropDownField>
                <DropDownField path='/#' description='Linhas'></DropDownField>
                <DropDownField path='/#' description='Consórcio'></DropDownField>
            </DropdownFatherField>

            <DropdownFatherField description="Relatórios" icon={<FileSpreadsheetIcon />}></DropdownFatherField>

            <DropdownFatherField description="Importação" icon={<LucideImport />}>
                <DropDownField path='/import' description='Primeira Instância'></DropDownField>
                <DropDownField path='/import' description='Segunda Instância'></DropDownField>
            </DropdownFatherField>

            <DropdownFatherField description="Configuração" icon={<Settings />}></DropdownFatherField>

            <SimpleField path='/login' description="Sair" icon={<LogIn />}></SimpleField>
            
        </div>
    );
}

export default MenuBar;