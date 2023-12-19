'use client';

import { importAuto } from '@/services/importAuto';
import { useForm } from 'react-hook-form';

interface ImportFormInput{
    file: File;
    option: string;
}



//Função de handling do import
async function handleImport({file, option}: ImportFormInput) {
    await importAuto({file, option});
}

const ImportForm = () => {

    const { register, handleSubmit } = useForm<ImportFormInput>()    

    return (
        <form 
            onSubmit={handleSubmit(handleImport)} 
            className="flex flex-col gap-4" 
            encType="multipart/form-data">
            <label htmlFor='file' className="flex flex-col gap-4">
                Selecione o arquivo:
                <input {...register('file')} type='file' className='rounded-lg' accept='.docx, .pdf'></input>
            </label>
            <div className="flex flex-row gap-4">
                <label htmlFor='' className='flex gap-2'>
                <input {...register('option')} type='radio' value='1Instancia'></input>
                1° Instância
                </label>
                <label htmlFor='' className="flex gap-2">
                <input {...register('option')} type='radio' value='2Instancia'></input>
                2° Instância
                </label>
            </div>
            <button 
                type='submit' 
                className="bg-zinc-200/50 w-max rounded-lg text-black p-1 hover:bg-white hover:duration-500">
                Importar
            </button>
        </form>
    );
}

export default ImportForm