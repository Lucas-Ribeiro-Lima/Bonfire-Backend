import React, {FC, ReactNode } from "react";

interface MainAppProps {
    children: ReactNode;
    title?: string;
}


const MainApp:FC<MainAppProps> = ({children, title}) => {
    return (
        <main className='flex flex-col flex-1 mt-24 items-center gap-10 text-white/70'>
            <h1 className="text-bold text-4xl p-4">{title}</h1>
            <div className="flex w-max">
                {children}
            </div>
        </main>
    );
}

export default MainApp;