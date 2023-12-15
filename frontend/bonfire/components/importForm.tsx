const ImportForm = () => {
    return (
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
    );
}

export default ImportForm