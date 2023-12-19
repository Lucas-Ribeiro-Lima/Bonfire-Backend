'use client';

import { importAuto } from '../../lib/importAuto';
import { useForm } from 'react-hook-form';
import {  number, z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

export type ImportFormData = z.infer<typeof ImportFormSchema>

const ImportFormSchema = z.object(
    {
        file: 
            z.instanceof(FileList)
            .transform( list => list.item(0))
            .superRefine(
                (file, ctx) => {
                    if (file?.name === null){
                        ctx.addIssue({
                            code: z.ZodIssueCode.custom,
                            message: "Anexe o arquivo de infrações",
                        })
                    }
                    else if (file?.type !== "application/pdf"){
                        ctx.addIssue({
                            code: z.ZodIssueCode.custom,
                            message: "Arquivo inválido, anexe um arquivo PDF",
                        })
                    }
                    // else if (file?.type !==  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"){
                    //     ctx.addIssue({
                    //         code: z.ZodIssueCode.custom,
                    //         message: "Arquivo inválido, anexe um arquivo Word (docx)",
                    //     })
                    // }
                }
            ),
        option: 
            z.coerce.number()
            .min(1, 'Selecione a opção de instância')
    }
)

//Função de handling do import
async function handleImport({file, option}: ImportFormData) {
    await importAuto({file, option});
}

const ImportForm = () => {

    const { 
        register, 
        handleSubmit, 
        control, 
        formState: {errors} 
        } = useForm<ImportFormData>(
            {
                resolver: zodResolver(ImportFormSchema)
            }
        )    

    return (
        <form 
        onSubmit={handleSubmit(handleImport)} 
        className="flex flex-col gap-4" 
        encType="multipart/form-data">
            <label 
            htmlFor='file' 
            className="flex flex-col gap-2">
                Selecione o arquivo:
                <input 
                {...register('file')} 
                type='file' 
                className='file:rounded-lg file:bg-zinc-400 file:font-semibold file:cursor-pointer' 
                accept='.docx, .pdf'>
                </input>
                {errors.file && <span className='text-red-500 text-sm'> {errors.file.message} </span>}
            </label>
            <div className='flex flex-col'>
                <div className="flex flex-row justify-center gap-20">
                    <label 
                    htmlFor='' 
                    className='flex gap-2'>
                        <input 

                        {...register('option')} 
                        type='radio' 
                        value='1'>

                        </input>
                        1° Instância
                    </label>
                    <label 
                    htmlFor='' 
                    className="flex gap-2">
                        <input 

                        {...register('option')} 
                        type='radio' 
                        value='2'>
            
                        </input>
                        2° Instância
                    </label>
                </div>
                {errors.option && <span className='text-red-500 text-sm'>{errors.option.message}</span>}
            </div>
            <button 
                type='submit' 
                className="bg-green-700 w-96 rounded-lg text-black font-semibold p-1 hover:bg-green-500 hover:duration-1000">
                Importar
            </button>
        </form>
    );
}

export default ImportForm