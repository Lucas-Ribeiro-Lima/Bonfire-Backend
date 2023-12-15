import ImportForm from "./importForm";


const MainApp = () => {
    return (
        <main className='flex flex-col flex-1 bg-zinc-700 rounded-md m-6 relative right-12 text-white/70 p-6'>
            <div className="flex flex-row justify-center items-center">
            <h1 className="text-bold text-2xl p-4">Importação de Infrações</h1>
            {/* <XCircle className='text-zinc-800 cursor-pointer hover:text-white/80 hover:duration-1000'></XCircle> */}
            </div>
            <div className="flex bg-zinc-500 w-max justify-center rounded p-4">
                <ImportForm></ImportForm>
            </div>
        </main>
    );
}

export default MainApp;