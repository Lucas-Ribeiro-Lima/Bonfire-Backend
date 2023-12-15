import Link from "next/link"
import { AlignJustify, Flame, LucideHome, LucideImport, LucideSunMoon, Settings, Undo, X, XCircle } from "lucide-react"

export default function Home() {
  return (
      <div className='h-screen flex flex-col'>
        <header className='bg-gradient-to-r from-zinc-900 to-zinc-700 h-20 p-2 align-center border-b border-white/25'>
          <div className="cursor-pointer w-40">
            <h1 className="flex flex-row text-extrabold text-3xl text-red-800 items-center"><Flame></Flame>Bonfire</h1>
            <h2 className="text-bold text-zinc-400">Autos de Infração</h2>
          </div>
          <div className="absolute right-10 top-6 text-zinc-400 hover:text-white hover:duration-1000 cursor-pointer">
            <LucideSunMoon></LucideSunMoon>
          </div>
        </header>
        <div className='flex flex-1'>
          <aside className='w-64'>
            <nav className="flex flex-col gap-4 bg-zinc-700 w-max p-4 text-zinc-500 rounded-br-lg">
              <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideHome></LucideHome>Inicio</Link>
              <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><AlignJustify></AlignJustify>Cadastro</Link>
              <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><LucideImport></LucideImport>Importação</Link>
              <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Settings></Settings>Configuração</Link>
              <Link className="flex gap-2  hover:text-white hover:duration-1000" href="#" ><Undo></Undo>Sair</Link>
            </nav>
          </aside>
          <main className='flex flex-col flex-1 bg-zinc-700 rounded-md m-6 relative right-12 text-white/70 p-6'>
            <div className="flex flex-row justify-center items-center">
              <h1 className="text-bold text-2xl p-4">Importação de Infrações</h1>
              {/* <XCircle className='text-zinc-800 cursor-pointer hover:text-white/80 hover:duration-1000'></XCircle> */}
            </div>
            <div className="flex bg-zinc-500 w-max justify-center rounded p-4">
              <form className="flex flex-col mt-10 gap-4">
                Selecione o arquivo:
                <input type='file' className='rounded-lg'></input>
                <div className="flex flex-row gap-4">
                <label className='flex gap-2'>
                  <input type='checkbox' name='Instancia' value='1Instancia'></input>
                  1° Instância
                </label>
                <label className="flex gap-2">
                  <input type='checkbox' name='Instancia' value='2Instancia'></input>
                  2° Instância
                </label>
                </div>
                <button type='submit' className="bg-zinc-200 w-max rounded-lg text-black p-1 hover:bg-white">Importar</button>
              </form>
            </div>
          </main>
        </div>
        <div>
          <footer className='flex bg-gradient-to-l from-zinc-900 to-zinc-700 h-20 align-center items-center border-t border-white/25 justify-end pr-4 text-white/70'>
            <div className="flex flex-col items-center text-sm">
              <div>
                Desenvolvido por
              </div>
              <div>
              Guilherme Nogueira e Lucas Ribeiro
              </div>
            </div>
          </footer>
        </div>
      </div>
    )
}
