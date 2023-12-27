import { ReactNode, useState } from "react";
import Link from "next/link";

interface DropDownFieldData {
    path: string;
    description: string;
    icon?: ReactNode
}
interface DropDownFatherFieldData {
    description: string;
    icon: ReactNode;
    children?: ReactNode;
}

export const DropdownFatherField = ({ description, icon, children }: DropDownFatherFieldData) => {

    const [isDropDown, setIsDropDown] = useState(false);

    return (
        <div>
            <button
                onClick={() => setIsDropDown(!isDropDown)}
                className="
                        peer 
                        w-36
                        h-10
                        rounded-xl 
                        focus:bg-red-950 
                        focus:text-red-600 
                        hover:bg-red-950 
                        hover:text-red-600 
                        hover:duration-1000 
                        hover:drop-shadow-2xl">
                <div className="
                        flex
                        justify-center 
                        align-middle 
                        gap-2">
                    {icon}{description}
                </div>
            </button>
            {isDropDown && (
                <div className='
                        relative
                        top-2 z-10 
                        rounded-xl 
                        shadow-2xl 
                        flex-col 
                        bg-zinc-800 
                        text-white'>
                    {children}
                </div>
            )}
        </div>
    );
}

export const DropDownField = ({ path, description, icon }: DropDownFieldData) => {
    return (
        <Link className='
                flex 
                p-4 
                justify-center
                align-middle 
                rounded-xl 
                hover:bg-zinc-600 
                hover:duration-1000 
                hover:drop-shadow-2xl 
                cursor-pointer'
            href={path}> {icon}{description}
        </Link>
    )
}

export const SimpleField = ({path, description, icon}: DropDownFieldData) => {
    return (
        <Link
            href={path}
            className="
                w-36
                h-10
                rounded-xl 
                focus:bg-red-950 
                focus:text-red-600 
                hover:bg-red-950 
                hover:text-red-600 
                hover:duration-1000 
                hover:drop-shadow-2xl">
            <div className="
                flex
                justify-center
                align-middle
                gap-2">
                {icon}{description}
            </div>
        </Link>
    )
}

