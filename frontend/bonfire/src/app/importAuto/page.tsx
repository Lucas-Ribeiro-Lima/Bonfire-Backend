import Image from 'next/image'
import Sidebar from '../../../components/Sidebar'

export default function Home() {
    return (
        <div className="flex min-h-screen">
          <Sidebar />
          {/* Conteúdo principal da página aqui */}
        </div>
    )
}
