const MainApp = () => {
    return (
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
    );
}

export default MainApp;