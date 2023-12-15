import Footer from "@/components/footer"
import Header from "@/components/header"
import MainApp from "@/components/mainApp"
import Sidebar from "@/components/sidebar"

export default function Home() {
  return (
      <div className='h-screen flex flex-col'>
          <Header></Header>
        <div className='flex flex-1'>
          <Sidebar></Sidebar>
          <MainApp></MainApp>
        </div>
        <div>
          <Footer></Footer>
        </div>
      </div>
    )
}
