'use client';

import { importAuto } from '@/lib/importAuto';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

export type ImportFormData = z.infer<typeof ImportFormSchema>

const ImportFormSchema = z.object(
    {
        auto: z.object(
            {
                file: 
                    z.instanceof(FileList)
                    .transform( list => list.item(0)),
                option: 
                    z.coerce.number()
                    .min(1, 'Selecione a opção de instância')
            })
            .superRefine(({file, option}, ctx) => {
            if (option === 1)
            {
                if(!file) {
                    ctx.addIssue({
                        code: z.ZodIssueCode.custom,
                        path: ["file"],
                        message: "Anexe o arquivo PDF das infrações",
                    })
                }
                if(file?.type !== "application/pdf") {
                    ctx.addIssue({
                        code: z.ZodIssueCode.custom,
                        path: ["file"],
                        message: "O arquivo de 1° Instância deve ser um PDF",
                    })
                }
            }
            if (option === 2)
            {
                if(!file) {
                    ctx.addIssue({
                        code: z.ZodIssueCode.custom,
                        path: ["file"],
                        message: "Anexe o arquivo Word das infrações",
                    })
                }
                if (file?.type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document"){
                    ctx.addIssue({
                        code: z.ZodIssueCode.custom,
                        path: ["file"],
                        message: "O arquivo de 2° Instância deve ser um Word",
                    })
                }
            }
            }
        )
    }
 )


//Função de handling do import
async function handleImport(auto: ImportFormData) {
    await importAuto(auto);
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
                {...register('auto.file')} 
                type='file' 
                className='file:rounded-lg file:bg-zinc-400 file:font-semibold file:cursor-pointer' 
                accept='.docx, .pdf'>
                </input>
                {errors.auto?.file && <span className='text-red-500 text-sm'> {errors.auto.file.message} </span>}
            </label>
            <div className='flex flex-col'>
                <div className="flex flex-row justify-center gap-20">
                    <label 
                    htmlFor='' 
                    className='flex gap-2'>
                        <input 

                        {...register('auto.option')} 
                        type='radio' 
                        value='1'>

                        </input>
                        1° Instância
                    </label>
                    <label 
                    htmlFor='' 
                    className="flex gap-2">
                        <input 

                        {...register('auto.option')} 
                        type='radio' 
                        value='2'>
            
                        </input>
                        2° Instância
                    </label>
                </div>
                {errors.auto?.option && <span className='text-red-500 text-sm'>{errors.auto.option.message}</span>}
            </div>
            <button 
                type='submit' 
                className="bg-green-700 w-96 rounded-lg text-black font-semibold p-1 hover:bg-green-500 hover:duration-1000">
                Importar
            </button>
        </form>
    );
}

export default ImportForm;