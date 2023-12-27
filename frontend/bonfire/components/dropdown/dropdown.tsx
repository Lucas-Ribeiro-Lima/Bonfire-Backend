import { ReactNode } from "react";
import Link from "next/link";

interface DropDownFieldData {
    path:string;
    description:string;
    icon?:ReactNode
}


interface DropDownFatherFieldData {
    description:string;
    icon:ReactNode;
    children?:ReactNode;
}

export const DropdownFatherField = ({description, icon, children}: DropDownFatherFieldData) => {

    return(
        <button className="group h-10 w-36 rounded-xl hover:bg-red-950 hover:text-red-600 hover:duration-1000 hover:drop-shadow-2xl">
            <div className="flex justify-center align-middle gap-2"> 
                {icon}{description} 
            </div>
            <div className=' hidden relative top-6 z-10 rounded-xl shadow-2xl c group-hover:block hover:block flex-col bg-zinc-800 text-white'>
                {children}
            </div>
        </button>
    );
}

export const DropDownField = ({path, description, icon}: DropDownFieldData) => {
    return (
        <Link className='flex p-4 justify-center align-middle rounded-xl hover:bg-zinc-600 hover:duration-1000 hover:drop-shadow-2xl cursor-pointer' href={path}> {icon}{description} </Link>
    )
}


