import Footer from "./footer";
import Header from "./header";
import React, {FC, ReactNode} from "react";

interface Props {
    children?: ReactNode;
}

const Layout:FC<Props> = ({children}) => {
    return(
        <div className='h-screen flex flex-col'>
        <Header></Header>
        <div className='flex flex-1'>
          {children}
        </div>
        <div>
          <Footer></Footer>
        </div>
      </div>
    );
}

export default Layout;