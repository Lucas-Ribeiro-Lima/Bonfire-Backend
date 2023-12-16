import { Flame } from "lucide-react";

const Logo = () => {
    return (
      <div className="w-40">
        <h1 className="flex flex-row text-extrabold text-3xl text-red-700 items-center"><Flame></Flame>Bonfire</h1>
        <h2 className="text-bold text-zinc-300">Autos de Infração</h2>
      </div>
    ); 
}

export default Logo