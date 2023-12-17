import Footer from "./footer";
import React, {FC, ReactNode} from "react";

interface SecondaryLayoutProp{
    children: ReactNode;
}

const SecondaryLayout:FC<SecondaryLayoutProp> = ({children}) => {
    return(
        <div className="flex flex-col h-screen bg-gradient-to-r from-zinc-900 to-zinc-800">            
            <div className="flex flex-1 justify-center items-center relative bottom-10">
                {children}
            </div>
            <div>
                <Footer></Footer>
            </div>
        </div>
    );
}

export default SecondaryLayout

