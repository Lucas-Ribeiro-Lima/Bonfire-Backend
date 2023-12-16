import React, {FC, ReactNode } from "react";

interface MainAppProps {
    children?: ReactNode;
    title?: string;
}


const MainApp:FC<MainAppProps> = ({children, title}) => {
    return (
        <main className='flex flex-col flex-1 items-center bg-zinc-700 rounded-md text-white/70 m-6 p-6'>
            <div className="flex flex-row">
            <h1 className="text-bold text-2xl p-4">{title}</h1>
            {/* <XCircle className='text-zinc-800 cursor-pointer hover:text-white/80 hover:duration-1000'></XCircle> */}
            </div>
            <div className="flex w-max bg-zinc-500 rounded p-4">
                {children}
            </div>
        </main>
    );
}

export default MainApp;